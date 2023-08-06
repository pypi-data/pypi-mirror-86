import dataclasses
import functools
import inspect
import typing
import yaml

from horkos import _casters
from horkos import _checkeromatic
from horkos import _definitions
from horkos import errors

Schemaable = typing.Union[str, dict, 'Schema', typing.TextIO]


@dataclasses.dataclass(frozen=True)
class Schema:
    """
    The schema of a data set.

    :vartype name: str
    :ivar name:
        The name of the data set the schema describes.
    :vartype description: str
    :ivar description:
        A detailed description of the data set.
    :vartype labels: dict
    :ivar labels:
        An unstructured area of the schema for storing organization
        specific information relating to the data set.
    :vartype fields: typing.Dict[str, horkos.Field]
    :ivar fields:
        A dictionary mapping field names to field objects
    """

    name: str
    description: str
    labels: dict
    fields: typing.Dict[str, 'horkos.Field']

    def cast(self, record: dict) -> dict:
        """
        Cast all the values contained within the record to the types declared
        within the schema. All undeclared fields will be removed from the
        record.

        :param record:
            The record to cast using the schema. This is expected to be
            a dictionary mapping field names to field values.
        :return:
            The record with values cast to the correct types.
        """
        return _casters.cast(record, self.fields)

    def find_errors(self, record: dict) -> list:
        """
        Run all field checks against the record, identifying all failed
        checks. Returns a list of errors if any of the checks have failed
        or an empty list if all passed.

        :param record:
            The record to inspect for errors.
        :return:
            A list of errors associated with the record.
        """
        error_list = []
        for field in self.fields.values():
            if field.required and field.name not in record:
                error_list.append(f'{field.name} is a required field')
                continue
            value = record.get(field.name)
            if value is None:
                if not field.nullable:
                    error_list.append(f'{field.name} cannot be null')
                continue
            for check in field.checks:
                if not check.handler(value):
                    error_list.append(
                        f'value of "{value}" in {field.name} did not '
                        f'pass {check.name} check'
                    )
        return error_list


    def process(self, record: dict) -> dict:
        """
        Process a record against the schema, casting each field of the
        record to its specified type and validating the the given value
        passes all of the checks declared in the schema. If the fields
        cannot be successfully cast or any of the checks failed a
        RecordValidationError exception will be raised.

        :param record:
            The record to process against the schema. This should be
            a dictionary mapping field names to field values.
        :return:
            The processed record with values cast and validated.
        """
        casted = self.cast(record)
        error_list = self.find_errors(casted)
        if error_list:
            raise errors.RecordValidationError(
                f'Check errors - {", ".join(error_list)}'
            )
        return casted


def _schema_from_dict(
        raw_schema: dict,
        strict: bool = True,
        custom_checkers: typing.Dict[str, typing.Callable] = None
) -> Schema:
    """
    Create a schema from a raw schema dictionary.

    :param raw_schema:
        A raw schema matching the expected json/yaml schema format.
    :param strict:
        Whether to operate in strict mode. If True descriptions will be
        required.
    :param custom_checkers:
        A dictionary of custom checkers. This dictionary should map the name
        of the check to a function that generates the check function
    :return:
        The resulting schema.
    """
    standardized = _standardize_schema(raw_schema, strict=strict)
    checkers = _checkeromatic.CHECKER_MAP.copy()
    checkers.update(custom_checkers or {})
    fields = {}
    raw_fields = standardized['fields']
    for field_name, field_body in raw_fields.items():
        checks = []
        for i, raw_check in enumerate(field_body['checks']):
            position = f'fields.{field_name}.checks[{i}]'
            check_name = raw_check['name']
            if check_name not in checkers:
                raise errors.SchemaValidationError(
                    f'In "{position}" check name "{check_name}" is unknown.'
                )
            check = _create_check_func(
                checkers[check_name],
                raw_check['args'],
                position
            )
            checks.append(
                _definitions.Check(check_name, check, raw_check['args'])
            )
        fields[field_name] = _definitions.Field(
            field_name,
            field_body['type'],
            field_body['description'],
            field_body['required'],
            field_body['nullable'],
            checks,
            field_body['labels'],
        )
    return Schema(
        standardized['name'],
        standardized['description'],
        standardized['labels'],
        fields,
    )

def _load_yaml(
        filepath_or_handle: typing.Union[str, typing.TextIO]
) -> dict:
    """
    Read the given yaml file.

    :param filepath_or_handle:
        The path to the yaml file to convert into a schema.
    :return:
        The resulting schema.
    """
    if not isinstance(filepath_or_handle, str):
        return yaml.safe_load(filepath_or_handle)
    with open(filepath_or_handle) as f:
        return yaml.safe_load(f)


def _create_check_func(
        check: typing.Callable, args: dict, position: str
) -> typing.Callable:
    """
    Create the actual check function, baking the args into it. The returned
    function should only expect a single positional argument to check.

    :param check:
        The base check. This is either a class that will be initialized
        with the given arguments, or a function that will be partially filled
        with the given args.
    :param args:
        The arguments to initialize the check with.
    :param position:
        The position of the check within the schema. This is used to provide
        more clear error messages.
    :return:
        A callable that expects a single positional argument that it will
        check.
    """
    try:
        if inspect.isclass(check):
            return check(**args)
        signature = inspect.signature(check)
        signature.bind('value', **args)
    except TypeError:
        raise errors.SchemaValidationError(
            f'Invalid arguments in "{position}"'
        )
    return functools.partial(check, **args)


def _standardize_schema(raw_schema: dict, strict: bool = True) -> dict:
    """
    Standardize the given raw_schema with all optional fields filled out
    with defaults. If the raw schema is not valid a SchemaValidationError will
    be raised.

    :param raw_schema:
        The schema to standardize.
    :param strict:
        Whether to operate in strict mode. If True descriptions will be
        required.
    :return:
        The standardized schema.
    """
    standardized = {}
    top = [
        ('name', str, True),
        ('description', str, strict),
        ('labels', dict, False),
        ('fields', dict, True),
    ]
    for key, type_, required in top:
        if key not in raw_schema and required:
            raise errors.SchemaValidationError(f'"{key}" is required')
        value = raw_schema[key] if key in raw_schema else type_()
        if not isinstance(value, type_):
            raise errors.SchemaValidationError(
                f'"{key}" must be of type {type_.__name__}'
            )
        standardized[key] = value
    standardized['fields'] = {
        field_id: _standardize_field(raw_field, field_id, strict=strict)
        for field_id, raw_field in raw_schema['fields'].items()
    }
    return standardized


def _standardize_field(
        raw_field: dict, field_id: str, strict: bool = True
) -> dict:
    """
    Standardize a given raw field with all the optional parts filled out
    with defaults. If the raw field can't be validated a SchemaValidationError
    will be raised.

    :param raw_field:
        The raw field to standardize.
    :param field_id:
        The id of the field being standardized.
    :param strict:
        Whether to operate in strict mode. If True descriptions will be
        required.
    :return:
        The standardized field.
    """
    standardized = {}
    top = [
        ('type', str, True, None),
        ('description', str, strict, str),
        ('labels', dict, False, dict),
        ('checks', list, False, list),
        ('required', bool, False, lambda: True),
        ('nullable', bool, False, bool),
    ]
    for key, type_, required, default in top:
        working = f'fields.{field_id}.{key}'
        if key not in raw_field and required:
            raise errors.SchemaValidationError(f'"{working}" is required')
        value = raw_field[key] if key in raw_field else default()
        if not isinstance(value, type_):
            raise errors.SchemaValidationError(
                f'"{working}" must be of type {type_.__name__}'
            )
        standardized[key] = value
    standardized['checks'] = [
        _standardize_check(raw_check, f'fields.{field_id}.check[{i}]')
        for i, raw_check in enumerate(raw_field.get('checks') or [])
    ]
    return standardized


def _standardize_check(
        raw_check: typing.Union[str, dict], prefix: str
) -> dict:
    """
    Convert a check into the standard format. If the check cannot be
    standardize a schema validation error is raised.

    :param raw_check:
        The raw_check to standardize.
    :param prefix:
        The document position prefix to integrate into error messages.
    :return:
        A standard check dictionary.
    """
    if isinstance(raw_check, str):
        return {'name': raw_check, 'args': {}}
    if isinstance(raw_check, dict):
        if 'name' not in raw_check:
            raise errors.SchemaValidationError(
                f'"{prefix}.name" is required'
            )
        if not isinstance(raw_check['name'], str):
            raise errors.SchemaValidationError(
                f'"{prefix}.name" must be a string'
            )
        if 'args' in raw_check and not isinstance(raw_check['args'], dict):
            raise errors.SchemaValidationError(
                f'"{prefix}.args" must be a dictionary'
            )
        return {'name': raw_check['name'], 'args': raw_check.get('args', {})}
    raise errors.SchemaValidationError(
        f'"{prefix}" must be a string or dictionary'
    )


def load_schema(
        schema: Schemaable,
        strict: bool = False,
        custom_checkers: typing.Dict[str, typing.Callable] = None
) -> Schema:
    """
    Load a schema from a file or existing schema object.

    :param schema:
        The schema to load. If a string is given, it is assumed to be a path
        to a `.json` or `.yaml` file defining the schema, alternatively a file
        handle can be passed directly. If a dictionary is given it will be
        assumed to be equivalent to the contents of a schema file.
    :param strict:
        Whether to operate in strict mode. If True descriptions will be
        required.
    :param custom_checkers:
        A dictionary of custom checkers. This dictionary should map the name
        of the check to a function that generates the check function. This
        can be used to extend checks beyond those defined within `horkos`.
    :return:
        A Schema object.
    """
    working = schema
    custom_checkers = custom_checkers or {}
    if isinstance(working, Schema):
        return working
    if not isinstance(working, dict):
        working = _load_yaml(working)
    return _schema_from_dict(
        working, strict=strict, custom_checkers=custom_checkers
    )
