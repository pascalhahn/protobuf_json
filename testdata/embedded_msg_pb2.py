# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='embedded_msg.proto',
  package='',
  serialized_pb='\n\x12\x65mbedded_msg.proto\"%\n\x0f\x45mbeddedMessage\x12\x12\n\x04test\x18\x01 \x02(\t:\x04test\"4\n\x0bTestMessage\x12%\n\x0btestmessage\x18\x01 \x02(\x0b\x32\x10.EmbeddedMessage')




_EMBEDDEDMESSAGE = descriptor.Descriptor(
  name='EmbeddedMessage',
  full_name='EmbeddedMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='test', full_name='EmbeddedMessage.test', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=True, default_value=unicode("test", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=22,
  serialized_end=59,
)


_TESTMESSAGE = descriptor.Descriptor(
  name='TestMessage',
  full_name='TestMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='testmessage', full_name='TestMessage.testmessage', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=61,
  serialized_end=113,
)

_TESTMESSAGE.fields_by_name['testmessage'].message_type = _EMBEDDEDMESSAGE
DESCRIPTOR.message_types_by_name['EmbeddedMessage'] = _EMBEDDEDMESSAGE
DESCRIPTOR.message_types_by_name['TestMessage'] = _TESTMESSAGE

class EmbeddedMessage(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EMBEDDEDMESSAGE
  
  # @@protoc_insertion_point(class_scope:EmbeddedMessage)

class TestMessage(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TESTMESSAGE
  
  # @@protoc_insertion_point(class_scope:TestMessage)

# @@protoc_insertion_point(module_scope)