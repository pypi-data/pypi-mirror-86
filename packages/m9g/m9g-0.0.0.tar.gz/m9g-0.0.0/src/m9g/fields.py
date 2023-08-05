# ~ coding: future_fstrings ~

from __future__ import absolute_import, print_function, unicode_literals

# http://python-future.org/str_object.html <- habilita el tipo de str de py3
from future.builtins import super, zip, isinstance, bytes, object
from future.builtins import str as future_str
from future.utils import iteritems, with_metaclass

import decimal
import base64
import datetime
import abc
import sys
import os
from collections import OrderedDict

from .exceptions import ValidationError


class _Missing(object):
    def __bool__(self):
        return False

    def __repr__(self):
        return "<m9g.missing>"


def _default_validation_hook(value):
    pass


missing = _Missing()


class Field(with_metaclass(abc.ABCMeta)):
    def __init__(
            self,
            default=missing,
            pk=False,
            allow_none=False,
            validation_hook=_default_validation_hook
    ):
        self.__pk = pk
        self.allow_none = allow_none
        self.validation_hook = validation_hook
        if default is not missing:
            default = self.adapt(default)
            self.validate(default)
        self.default = default

    def serialize(self, format, value):
        serialize_fn = getattr(self, f"serialize_{format}", None)
        if not serialize_fn:
            return self.serialize_default(format, value)
        return serialize_fn(value)

    def deserialize(self, format, value):
        deserialize_fn = getattr(self, f"deserialize_{format}", None)
        if not deserialize_fn:
            return self.deserialize_default(format, value)
        return deserialize_fn(value)

    def serialize_default(self, format, value):
        return value

    def deserialize_default(self, format, value):
        return value

    def get_default(self):
        return self.default

    @classmethod
    def is_field_type_of(cls, value):
        return type(value) == cls.FIELD_TYPE

    def validate(self, value):
        if not self.allow_none and value is None:
            raise ValidationError(f"{self.__class__} was marked as not nullable")

        if value is not None and not isinstance(value, self.FIELD_TYPE):
            raise ValidationError(f"{value} is not instance of declared type {self.FIELD_TYPE}")

        try:
            validation_hook = self.validation_hook
            validation_hook(value)
        except Exception as e:
            raise ValidationError(f'Validation hook raised "{e}" for value {value}')

    @property
    def pk(self):
        return self.__pk

    @pk.setter
    def pk(self, pk):
        self.__pk = pk

    def adapt(self, value):
        return value


class StringField(Field):
    FIELD_TYPE = (str, future_str)

    def __init__(self, encoding='utf-8', **kwargs):
        self.encoding = encoding
        super().__init__(**kwargs)

    @classmethod
    def is_field_type_of(cls, value):
        return isinstance(value, cls.FIELD_TYPE)

    def adapt(self, value):
        if sys.version_info[0] < 3 and isinstance(value, str):
            return value.decode(self.encoding)
        return value


class IntField(Field):
    FIELD_TYPE = int

    def serialize_json(self, value):
        return int(value)

    def deserialize_json(self, value):
        return int(value)


class FloatField(Field):
    FIELD_TYPE = float

    def serialize_json(self, value):
        return float(value)

    def deserialize_json(self, value):
        return float(value)


class DecimalField(Field):
    FIELD_TYPE = decimal.Decimal

    def __init__(self, precition_digits=3, **kwargs):
        super().__init__(**kwargs)
        self.precition_digits = precition_digits

    def serialize_json(self, value):
        precision_format = "%%.0%df" % self.precition_digits
        return precision_format % value

    def deserialize_json(self, value):
        return decimal.Decimal(value)


class BytesField(Field):
    FIELD_TYPE = bytes

    def serialize_json(self, value):
        return base64.b64encode(value).decode('utf-8')

    def deserialize_json(self, value):
        return base64.b64decode(value.encode('utf-8'))


class DateField(Field):
    FIELD_TYPE = datetime.date

    def serialize_json(self, value):
        return value.isoformat()

    def deserialize_json(self, date_str):
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date.date()


class DateTimeField(Field):
    FIELD_TYPE = datetime.datetime

    def serialize_json(self, value):
        # No usamos isoformat porque no agrega los milisegundos
        return value.strftime('%Y-%m-%dT%H:%M:%S.%f')

    def deserialize_json(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')


class DictField(Field):
    FIELD_TYPE = dict

    def __init__(self, key_field_type, value_field_type, **kwargs):
        self.key_field_type = key_field_type
        self.value_field_type = value_field_type
        super().__init__(**kwargs)

    def serialize_default(self, format, to_serialize_dict):
        serialized = {}
        for k, v in iteritems(to_serialize_dict):
            serialized_k = self.key_field_type.serialize(format, k)
            serialized_v = self.value_field_type.serialize(format, v)
            serialized[serialized_k] = serialized_v

        return serialized

    def deserialize_default(self, format, str_dict):
        from_serialize = {}
        for k, v in iteritems(str_dict):
            deserialized_k = self.key_field_type.deserialize(format, k)
            deserialized_v = self.value_field_type.deserialize(format, v)
            from_serialize[deserialized_k] = deserialized_v

        return from_serialize

    def validate(self, value):
        for k, v in iteritems(value):
            self.key_field_type.validate(k)
            self.value_field_type.validate(v)


class ListField(Field):
    FIELD_TYPE = list

    def __init__(self, items_field_type, **kwargs):
        self.items_fields_type = items_field_type
        super().__init__(**kwargs)

    def serialize_default(self, format, value):
        return [self.items_fields_type.serialize(format, x) for x in value]

    def deserialize_default(self, format, value):
        return [self.items_fields_type.deserialize(format, x) for x in value]

    def validate(self, value):
        super().validate(value)
        for v in value:
            self.items_fields_type.validate(v)


class TupleField(Field):
    FIELD_TYPE = tuple

    def __init__(self, items_field_types, **kwargs):
        self.items_fields_types = items_field_types
        super().__init__(**kwargs)

    def serialize_default(self, format, values):
        serialized_values = []
        for value, field in zip(values, self.items_fields_types):
            serialized_values.append(field.serialize(format, value))
        return serialized_values

    def deserialize_default(self, format, values):
        serialized_values = []
        for value, field in zip(values, self.items_fields_types):
            serialized_values.append(field.deserialize(format, value))
        return tuple(serialized_values)

    def validate(self, value):
        super().validate(value)
        for value, field in zip(value, self.items_fields_types):
            field.validate(value)


class ReferenceField(Field):

    # TODO: chequar que las refencias tengan definida al menos una clave primaria

    def __init__(self, ref_class, **kwargs):
        self.ref_class = self._resolve_ref_class(ref_class)
        self.USE_THIN_REF = os.environ.get('M9G_SERIALIZE_THIN', False)
        self.FIELD_TYPE = self.ref_class
        super().__init__(**kwargs)

    def _get_module_and_class(self, ref_str):
        tokens = ref_str.split('.')
        class_name = tokens.pop()
        module = '.'.join([x for x in tokens])
        return module, class_name

    def _resolve_ref_class(self, ref_class):
        from m9g import Model

        if isinstance(ref_class, future_str):
            module, class_name = self._get_module_and_class(ref_class)
            model = Model.get_model(module, class_name)
            return model
        return ref_class

    def _is_lazy(self, ref):
        return getattr(ref, '_ref_status', None) == 'lazy'

    def _build_thin_ref(self, value, model, format):
        # es de la forma (<primary_key_value>, <primary_key_value>...)
        if not isinstance(value, list):
            assert len(model.primary_key_fields) == 1
            value = [value]

        pk_values = tuple(v for v in value)
        attrs = {}

        for i, serialized_pk_value in enumerate(pk_values):
            attr_key = model.primary_key_fields[i]
            attr_value = model.field_from_key(attr_key).deserialize(format, serialized_pk_value)
            attrs[attr_key] = attr_value

        return model.thinRef(**attrs)

    def _build_gross_ref(self, value, model, format):
        # es de la forma {'<pk1>': <pk_value>...}
        fields = {}
        for k, v in iteritems(value):
            fields[k] = model.field_from_key(k).deserialize(format, v)
        return model.grossRef(**fields)

    def _build_full_obj(self, value, model, format):
        fields = {}
        for k, v in iteritems(value):
            fields[k] = model.field_from_key(k).deserialize(format, v)
        return model(**fields)

    def validate(self, ref):
        super().validate(ref)
        if not ref.primary_key_fields:
            raise ValidationError("References must have primary keys declared")

    def serialize_default(self, format, ref):
        # TODO: hacer validacion de tipos contra el registry
        data = OrderedDict()
        fields = ref._fields

        if self._is_lazy(ref):
            fields = ref.__dict__

        if self.USE_THIN_REF:
            fields = ref.primary_key_fields

        for k, v in iteritems(ref._fields):
            if k not in fields:
                continue
            data[k] = v.serialize(format, getattr(ref, k))

        if len(data.keys()) == 1:
            return list(data.values()).pop()

        if len(data.keys()) == len(ref.primary_key_fields):
            return tuple(data.values())

        return data

    def deserialize_default(self, format, value):
        model = self.ref_class
        if isinstance(value, dict):
            if len(value) == len(model._fields):
                return self._build_full_obj(value, model, format)
            else:
                return self._build_gross_ref(value, model, format)

        return self._build_thin_ref(value, model, format)


class DynamicField(Field):
    ATOMIC_FIELDS = [
        StringField,
        IntField,
        FloatField,
        DecimalField,
        BytesField,
        DateField,
        DateTimeField
    ]
    COMPLEX_FIELDS = [
        DictField,
        ListField,
        TupleField,
    ]

    def _lookup_for_field_type(self, field_type_str):
        for type_ in self.ATOMIC_FIELDS:
            if type_.__name__ == field_type_str:
                return type_

        for type_ in self.COMPLEX_FIELDS:
            if type_.__name__ == field_type_str:
                return type_
        return None

    def _field_from_field_value(self, field_value):
        for field_class in self.ATOMIC_FIELDS:
            # no usamos isinstance porque no discrimina entre datetime y date
            if field_class.is_field_type_of(field_value):
                return field_class

        for field_class in self.COMPLEX_FIELDS:
            # no usamos isinstance porque no discrimina entre datetime y date
            if field_class.is_field_type_of(field_value):
                return field_class

        return None

    def _build_field_as_dynamic(self, field_type, value):
        if field_type == DictField:
            return DictField(DynamicField(), DynamicField())
        if field_type == ListField:
            return ListField(DynamicField())
        if field_type == TupleField:
            args = tuple([DynamicField()] * len(value))
            return TupleField(args)
        return field_type()

    def validate(self, value):
        pass

    def serialize_default(self, format, value):
        field_type = self._field_from_field_value(value)
        field = self._build_field_as_dynamic(field_type, value)
        return (field.__class__.__name__, field.serialize(format, value))

    def deserialize_default(self, format, value):
        field_type_name, serialized_value = value
        field_type = self._lookup_for_field_type(field_type_name)
        field = self._build_field_as_dynamic(field_type, value)
        return field.deserialize(format, serialized_value)

    def serialize_json(self, value):
        # JSON no soporte tuplas como claves (caso diccionario)
        return str(self.serialize_default("json", value))

    def deserialize_json(self, value):
        value = eval(value)
        return self.deserialize_default("json", value)


class CompositeField(Field):

    def __init__(self, ref, **kwargs):
        self.ref = ref
        super().__init__(**kwargs)

    def serialize_default(self, format, value):
        return value.serialize(format=format)

    def deserialize_default(self, format, value):
        return self.ref.deserialize(value, format=format)

    def validate(self, value):
        pass
