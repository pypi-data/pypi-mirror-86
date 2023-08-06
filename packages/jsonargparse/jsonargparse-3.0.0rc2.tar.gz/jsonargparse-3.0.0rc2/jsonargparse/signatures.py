"""Metods to add arguments based on class/method/function signatures."""

import inspect
from enum import Enum
from typing import Union, Optional, List, Set, Type, Callable

from .util import _issubclass
from .actions import ActionEnum
from .jsonschema import ActionJsonSchema
from .optionals import docstring_parser_support, import_docstring_parse, dataclasses_support, import_dataclasses


__all__ = ['SignatureArguments']


class SignatureArguments:
    """Methods to add arguments based on signatures to an ArgumentParser instance."""

    def add_class_arguments(
        self,
        theclass: Type,
        nested_key: Optional[str] = None,
        as_group: bool = True,
        skip: Optional[Set[str]] = None,
    ) -> int:
        """Adds arguments from a class based on its type hints and docstrings.

        Note: Keyword arguments without at least one valid type are ignored.

        Args:
            theclass: Class from which to add arguments.
            nested_key: Key for nested namespace.
            as_group: Whether arguments should be added to a new argument group.
            skip: Names of arguments that should be skipped.

        Returns:
            Number of arguments added.

        Raises:
            ValueError: When not given a class.
            ValueError: When there are positional arguments without at least one valid type.
        """
        if not inspect.isclass(theclass):
            raise ValueError('Expected a class object.')

        def docs_func(base):
            return [base.__init__.__doc__, base.__doc__]

        return self._add_signature_arguments(inspect.getmro(theclass), nested_key, as_group, docs_func, skip)


    def add_method_arguments(
        self,
        theclass: Type,
        themethod: str,
        nested_key: Optional[str] = None,
        as_group: bool = True,
        skip: Optional[Set[str]] = None,
    ) -> int:
        """Adds arguments from a class based on its type hints and docstrings.

        Note: Keyword arguments without at least one valid type are ignored.

        Args:
            theclass: Class which includes the method.
            themethod: Name of the method for which to add arguments.
            nested_key: Key for nested namespace.
            as_group: Whether arguments should be added to a new argument group.
            skip: Names of arguments that should be skipped.

        Returns:
            Number of arguments added.

        Raises:
            ValueError: When not given a class or the name of a method of the class.
            ValueError: When there are positional arguments without at least one valid type.
        """
        if not inspect.isclass(theclass):
            raise ValueError('Expected a class object.')
        if not hasattr(theclass, themethod) or not callable(getattr(theclass, themethod)):
            raise ValueError('Expected the method to a callable member of the class.')

        def docs_func(base):
            return [base.__doc__]

        skip_first = False if isinstance(theclass.__dict__[themethod], staticmethod) else True
        themethod = getattr(theclass, themethod)

        return self._add_signature_arguments([themethod], nested_key, as_group, docs_func, skip, skip_first=skip_first)


    def add_function_arguments(
        self,
        function: Callable,
        nested_key: Optional[str] = None,
        as_group: bool = True,
        skip: Optional[Set[str]] = None,
    ) -> int:
        """Adds arguments from a function based on its type hints and docstrings.

        Note: Keyword arguments without at least one valid type are ignored.

        Args:
            function: Function from which to add arguments.
            nested_key: Key for nested namespace.
            as_group: Whether arguments should be added to a new argument group.
            skip: Names of arguments that should be skipped.

        Returns:
            Number of arguments added.

        Raises:
            ValueError: When not given a callable.
            ValueError: When there are positional arguments without at least one valid type.
        """
        if not callable(function):
            raise ValueError('Expected a callable object.')

        def docs_func(base):
            return [base.__doc__]

        return self._add_signature_arguments([function], nested_key, as_group, docs_func, skip)


    def _add_signature_arguments(
        self,
        objects,
        nested_key: Optional[str],
        as_group: bool,
        docs_func: Callable,
        skip: Optional[Set[str]] = None,
        skip_first: bool = False,
    ) -> int:
        """Adds arguments from arguments of objects based on signatures and docstrings.

        Args:
            objects: Objects from which to add signatures.
            nested_key: Key for nested namespace.
            as_group: Whether arguments should be added to a new argument group.
            docs_func: Function that returns docstrings for a given object.
            skip: Names of arguments that should be skipped.
            skip_first: Whether to skip first argument, i.e., skip self of class methods.

        Returns:
            Number of arguments added.

        Raises:
            ValueError: When there are positional arguments without at least one valid type.
        """
        kinds = inspect._ParameterKind

        def update_has_args_kwargs(base, has_args=True, has_kwargs=True):
            params = list(inspect.signature(base).parameters.values())
            has_args &= any(p._kind == kinds.VAR_POSITIONAL for p in params)
            has_kwargs &= any(p._kind == kinds.VAR_KEYWORD for p in params)
            return has_args, has_kwargs

        ## Determine propagation of arguments ##
        add_types = [(True, True)]
        has_args, has_kwargs = update_has_args_kwargs(objects[0])
        for num in range(1, len(objects)):
            if not (has_args or has_kwargs):
                objects = objects[:num]
                break
            add_types.append((has_args, has_kwargs))
            has_args, has_kwargs = update_has_args_kwargs(objects[num], has_args, has_kwargs)

        ## Gather docstrings ##
        doc_group = None
        doc_params = {}
        if docstring_parser_support:
            docstring_parse = import_docstring_parse('_add_signature_arguments')
            for base in objects:
                for doc in docs_func(base):
                    docstring = docstring_parse(doc)
                    if docstring.short_description and not doc_group:
                        doc_group = docstring.short_description
                    for param in docstring.params:
                        if param.arg_name not in doc_params:
                            doc_params[param.arg_name] = param.description

        ## Create group if requested ##
        group = self
        if as_group:
            if doc_group is None:
                doc_group = str(objects[0])
            name = objects[0].__name__ if nested_key is None else nested_key
            group = self.add_argument_group(doc_group, name=name)  # type: ignore

        ## Add objects arguments ##
        added_args = set()
        if skip is None:
            skip = set()
        if dataclasses_support:
            dataclasses = import_dataclasses('_add_signature_arguments')
        for obj, (add_args, add_kwargs) in zip(objects, add_types):
            for num, param in enumerate(inspect.signature(obj).parameters.values()):
                name = param.name
                annotation = param.annotation
                default = param.default
                is_positional = default == inspect._empty  # type: ignore
                skip_message = 'Skipping argument "'+name+'" from "'+obj.__name__+'" because of: '
                if param._kind in {kinds.VAR_POSITIONAL, kinds.VAR_KEYWORD} or \
                   (is_positional and skip_first and num == 0) or \
                   (annotation == inspect._empty and not is_positional and default is None):  # type: ignore
                    continue
                elif is_positional and not add_args:
                    self.logger.debug(skip_message+'Positional argument but *args not propagated.')  # type: ignore
                    continue
                elif not is_positional and not add_kwargs:
                    self.logger.debug(skip_message+'Keyword argument but **kwargs not propagated.')  # type: ignore
                    continue
                elif name in skip:
                    self.logger.debug(skip_message+'Argument requested to be skipped.')  # type: ignore
                    continue
                if dataclasses_support and default.__class__ == dataclasses._HAS_DEFAULT_FACTORY_CLASS:
                    default = obj.__dataclass_fields__[name].default_factory()
                if annotation == inspect._empty and not is_positional:  # type: ignore
                    annotation = type(default)
                kwargs = {'help': doc_params.get(name)}
                if is_positional:
                    kwargs['required'] = True
                else:
                    kwargs['default'] = default
                if annotation in {str, int, float, bool} or \
                   _issubclass(annotation, (str, int, float)):
                    kwargs['type'] = annotation
                elif _issubclass(annotation, Enum):
                    kwargs['action'] = ActionEnum(enum=annotation)
                else:
                    try:
                        kwargs['action'] = ActionJsonSchema(annotation=annotation, enable_path=False)
                    except ValueError as ex:
                        self.logger.debug(skip_message+str(ex))  # type: ignore
                if 'type' in kwargs or 'action' in kwargs:
                    arg = '--' + (nested_key+'.' if nested_key else '') + name
                    if arg in added_args:
                        self.logger.debug(skip_message+'Argument already added.')  # type: ignore
                    else:
                        group.add_argument(arg, **kwargs)  # type: ignore
                        added_args.add(arg)
                elif is_positional:
                    raise ValueError('Positional argument without a type for '+obj.__name__+' argument '+name+'.')

        return len(added_args)
