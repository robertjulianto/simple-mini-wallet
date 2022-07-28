from marshmallow import Schema, EXCLUDE, validates_schema, fields, ValidationError, post_dump
from marshmallow_enum import EnumField

from mini_wallet.core.common.enums import ResponseStatus

ISO_FORMAT = '%Y-%m-%dT%H:%M:%S%z'


class MiniWalletSchema(Schema):
    class Meta:
        datetimeformat = ISO_FORMAT
        unknown = EXCLUDE

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = field_obj.data_key or field_name

    @validates_schema(skip_on_field_errors=False)
    def __validate_empty_string(self, data, **kwargs):
        error_messages = {
            obj.data_key: ['Field cannot be empty']
            for fld, obj in self.fields.items()
            if isinstance(obj, fields.String) and obj.required and not obj.validate and not data.get(fld)
        }
        if error_messages:
            raise ValidationError(message=error_messages)

    @post_dump
    def __convert_timestamp_to_iso_format(self, data, **kwargs):
        for _, obj in self.fields.items():
            key = obj.data_key
            if isinstance(obj, fields.DateTime) and data[key]:
                data[key] = f"{data[key][:-2]}:{data[key][-2:]}"
        return data


class BaseResponse(MiniWalletSchema):
    status = EnumField(ResponseStatus, by_value=True)
