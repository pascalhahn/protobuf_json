#!/usr/bin/python
#
# Parse json to protobuf messages and vice versa.
#
# TODO: add embedded message support from json to proto


__author__ = 'Pascal Hahn <ph@lxd.bz>'


import simplejson

from google.protobuf.descriptor import FieldDescriptor as protofd


class Error(Exception):
  pass


class JsonDataMissingError(Error):
  pass


class ProcessingError(Error):
  pass


class UnsupportedFieldTypeError(Error):
  pass


class ProtoEnumValueNotFoundError(Error):
  pass


TYPE_MAP = {
    protofd.TYPE_BOOL: bool,
    protofd.TYPE_FLOAT: float,
    protofd.TYPE_INT32: int,
    protofd.TYPE_INT64: int,
    protofd.TYPE_UINT32: int,
    protofd.TYPE_UINT64: int,
    protofd.TYPE_STRING: unicode,
    protofd.TYPE_ENUM: int,
    }


def _convert_json_value(field, value, message_class):
  """Convert the fields value, using the TYPE_MAP.

  Args:
    field: field instance - proto field we work with
    value: one of TYPE_MAP.keys() - value to convert
    message_class: Proto message class

  Returns:
    value: converted value

  Raises:
    ProtoEnumValueNotFoundError: if the enum does not have the value
    UnsupportedFieldTypeError: If the proto field type is not supported
  """
  # convert ENUM fields to cleartext for readability of json
  if field.type == protofd.TYPE_ENUM:
    if not hasattr(message_class, value):
      raise ProtoEnumValueNotFoundError(
        'Enum does not have a value %s' % value)
    return getattr(message_class, value)
  # cast fields to their appropriate datatypes according
  # to TYPE_MAP
  elif field.type in TYPE_MAP:
    return TYPE_MAP[field.type](value)
  else:
    raise UnsupportedFieldTypeError(
      'ProtoType %i not supported yet' % field.type)


def json2proto(json_str, message_class):
  """Parse json input to a proto.

  Take a hash in json and parse it to a proto. The resulting protos will
  always be valid because all the fields of the message are ensured to be
  valid.

  IsInitialized() is intentionally not called due to the overhead and because
  it is made sure that protos are valid via code.

  Args:
    json_str: str - json input
    message_class: proto Message class - the message that the proto should be
                   parsed to

  Returns:
    proto_obj: instance of the message_class: message instance filled with data

  Raises:
    ProtoEnumValueNotFoundError: if the enum does not have the requested value
                                 (from _convert_json_value)
    UnsupportedFieldTypeError: if the proto field type is not supported
                               (from _convert_json_value)
    JsonDataMissingError: if the json does not have all the required data
  """
  json_data = simplejson.loads(json_str)
  proto_obj = message_class()

  for field in message_class.DESCRIPTOR.fields:
    if field.name in json_data:
      value = json_data[field.name]
        
      # treat repeated fields properly, 
      if field.label == protofd.LABEL_REPEATED:
        label_obj = getattr(proto_obj, field.name)
        label_obj.extend([
            _convert_json_value(field, val, message_class)
            for val in value])
      else:
        setattr(
          proto_obj, field.name,
          _convert_json_value(field, value, message_class))
    # we always want to set a default value explicitly due to weird handling of
    # required fields with a default
    # (http://code.google.com/p/protobuf/issues/detail?id=312)
    elif field.has_default_value:
      setattr(proto_obj, field.name, field.default_value)
    elif field.label == field.LABEL_REQUIRED:
      raise JsonDataMissingError(
          'Field %s is not set in json data' % field.name)

  return proto_obj


def _convert_proto_value(field, value, message_obj):
  """Convert the fields value, using the TYPE_MAP.

  Args:
    field: proto field instance - the field we work with
    value: one of TYPE_MAP.keys() - value to convert
    message_obj: Proto message instance

  Returns:
    value: converted value

  Raises:
    ProtoEnumValueNotFoundError: if the enum does not have the value
    UnsupportedFieldTypeError: If the proto field type is not supported
  """
  # convert ENUM fields to cleartext for readability of json
  if field.type == protofd.TYPE_ENUM:
    tmp_field = field.enum_type.values_by_number.get(value, None)
    if tmp_field == None:
      raise ProtoEnumValueNotFoundError(
        'Enum does not have a value %d' % value)
    return tmp_field.name
  # no need to cast values from proto, pass them directly if they are supported
  elif field.type in TYPE_MAP:
    return value
  elif field.type == protofd.TYPE_MESSAGE:
    return proto2json_dict(value)
  else:
    raise UnsupportedFieldTypeError(
      'ProtoType %i not supported yet' % field.type)


def proto2json(message_instance):
  """Parse a proto message instance to json.

  During conversion, also default values are converted. This is so that we can rely on
  the data to be consistent even across versions of the proto. Otherwise we'd not know
  if the json data is not a valid dataset if we just had changed in the defaults and
  if we only added in values with a default.

  Args:
    message_instance: instance of protobuf message - message to parse

  Returns:
    json_str: str - message as json string

  Raises:
    ProtoEnumValueNotFoundError: if the enum does not have the value
    UnsupportedFieldTypeError: If the proto field type is not supported
  """
  return simplejson.dumps(proto2json_dict(message_instance))


def proto2json_dict(message_instance):
  """Parse a proto message instance to a dict.

  During conversion, also default values are converted. This is so that we can rely on
  the data to be consistent even across versions of the proto. Otherwise we'd not know
  if the json data is not a valid dataset if we just had changed in the defaults and
  if we only added in values with a default.

  Args:
    message_instance: instance of protobuf message - message to parse

  Returns:
    json_data: dict - message as dict

  Raises:
    ProtoEnumValueNotFoundError: if the enum does not have the value
    UnsupportedFieldTypeError: If the proto field type is not supported
  """
  json_data = {}
  for field in message_instance.DESCRIPTOR.fields:
    value = getattr(message_instance, field.name)
    if field.label == protofd.LABEL_REPEATED:
      json_data[field.name] = [_convert_proto_value(field, val, message_instance) for val in value]
    else:
      json_data[field.name] = _convert_proto_value(field, value, message_instance)
  return json_data

# vim: set tabstop=2 softtabstop=2 shiftwidth=2 textwidth=80 syntax=python smarttab expandtab:
