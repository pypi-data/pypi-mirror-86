# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: streamlit/proto/Block.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='streamlit/proto/Block.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1bstreamlit/proto/Block.proto\"\xc5\x02\n\x05\x42lock\x12#\n\x08vertical\x18\x01 \x01(\x0b\x32\x0f.Block.VerticalH\x00\x12\'\n\nhorizontal\x18\x02 \x01(\x0b\x32\x11.Block.HorizontalH\x00\x12\x1f\n\x06\x63olumn\x18\x03 \x01(\x0b\x32\r.Block.ColumnH\x00\x12\'\n\nexpandable\x18\x04 \x01(\x0b\x32\x11.Block.ExpandableH\x00\x12\x13\n\x0b\x61llow_empty\x18\x05 \x01(\x08\x1a\x1a\n\x08Vertical\x12\x0e\n\x06unused\x18\x01 \x01(\x08\x1a\"\n\nHorizontal\x12\x14\n\x0ctotal_weight\x18\x02 \x01(\x01\x1a\x18\n\x06\x43olumn\x12\x0e\n\x06weight\x18\x01 \x01(\x01\x1a-\n\nExpandable\x12\r\n\x05label\x18\x01 \x01(\t\x12\x10\n\x08\x65xpanded\x18\x02 \x01(\x08\x42\x06\n\x04typeb\x06proto3')
)




_BLOCK_VERTICAL = _descriptor.Descriptor(
  name='Vertical',
  full_name='Block.Vertical',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='unused', full_name='Block.Vertical.unused', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=214,
  serialized_end=240,
)

_BLOCK_HORIZONTAL = _descriptor.Descriptor(
  name='Horizontal',
  full_name='Block.Horizontal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='total_weight', full_name='Block.Horizontal.total_weight', index=0,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=242,
  serialized_end=276,
)

_BLOCK_COLUMN = _descriptor.Descriptor(
  name='Column',
  full_name='Block.Column',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='weight', full_name='Block.Column.weight', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=278,
  serialized_end=302,
)

_BLOCK_EXPANDABLE = _descriptor.Descriptor(
  name='Expandable',
  full_name='Block.Expandable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='label', full_name='Block.Expandable.label', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expanded', full_name='Block.Expandable.expanded', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=304,
  serialized_end=349,
)

_BLOCK = _descriptor.Descriptor(
  name='Block',
  full_name='Block',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='vertical', full_name='Block.vertical', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='horizontal', full_name='Block.horizontal', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='column', full_name='Block.column', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expandable', full_name='Block.expandable', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='allow_empty', full_name='Block.allow_empty', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_BLOCK_VERTICAL, _BLOCK_HORIZONTAL, _BLOCK_COLUMN, _BLOCK_EXPANDABLE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='type', full_name='Block.type',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=32,
  serialized_end=357,
)

_BLOCK_VERTICAL.containing_type = _BLOCK
_BLOCK_HORIZONTAL.containing_type = _BLOCK
_BLOCK_COLUMN.containing_type = _BLOCK
_BLOCK_EXPANDABLE.containing_type = _BLOCK
_BLOCK.fields_by_name['vertical'].message_type = _BLOCK_VERTICAL
_BLOCK.fields_by_name['horizontal'].message_type = _BLOCK_HORIZONTAL
_BLOCK.fields_by_name['column'].message_type = _BLOCK_COLUMN
_BLOCK.fields_by_name['expandable'].message_type = _BLOCK_EXPANDABLE
_BLOCK.oneofs_by_name['type'].fields.append(
  _BLOCK.fields_by_name['vertical'])
_BLOCK.fields_by_name['vertical'].containing_oneof = _BLOCK.oneofs_by_name['type']
_BLOCK.oneofs_by_name['type'].fields.append(
  _BLOCK.fields_by_name['horizontal'])
_BLOCK.fields_by_name['horizontal'].containing_oneof = _BLOCK.oneofs_by_name['type']
_BLOCK.oneofs_by_name['type'].fields.append(
  _BLOCK.fields_by_name['column'])
_BLOCK.fields_by_name['column'].containing_oneof = _BLOCK.oneofs_by_name['type']
_BLOCK.oneofs_by_name['type'].fields.append(
  _BLOCK.fields_by_name['expandable'])
_BLOCK.fields_by_name['expandable'].containing_oneof = _BLOCK.oneofs_by_name['type']
DESCRIPTOR.message_types_by_name['Block'] = _BLOCK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Block = _reflection.GeneratedProtocolMessageType('Block', (_message.Message,), dict(

  Vertical = _reflection.GeneratedProtocolMessageType('Vertical', (_message.Message,), dict(
    DESCRIPTOR = _BLOCK_VERTICAL,
    __module__ = 'streamlit.proto.Block_pb2'
    # @@protoc_insertion_point(class_scope:Block.Vertical)
    ))
  ,

  Horizontal = _reflection.GeneratedProtocolMessageType('Horizontal', (_message.Message,), dict(
    DESCRIPTOR = _BLOCK_HORIZONTAL,
    __module__ = 'streamlit.proto.Block_pb2'
    # @@protoc_insertion_point(class_scope:Block.Horizontal)
    ))
  ,

  Column = _reflection.GeneratedProtocolMessageType('Column', (_message.Message,), dict(
    DESCRIPTOR = _BLOCK_COLUMN,
    __module__ = 'streamlit.proto.Block_pb2'
    # @@protoc_insertion_point(class_scope:Block.Column)
    ))
  ,

  Expandable = _reflection.GeneratedProtocolMessageType('Expandable', (_message.Message,), dict(
    DESCRIPTOR = _BLOCK_EXPANDABLE,
    __module__ = 'streamlit.proto.Block_pb2'
    # @@protoc_insertion_point(class_scope:Block.Expandable)
    ))
  ,
  DESCRIPTOR = _BLOCK,
  __module__ = 'streamlit.proto.Block_pb2'
  # @@protoc_insertion_point(class_scope:Block)
  ))
_sym_db.RegisterMessage(Block)
_sym_db.RegisterMessage(Block.Vertical)
_sym_db.RegisterMessage(Block.Horizontal)
_sym_db.RegisterMessage(Block.Column)
_sym_db.RegisterMessage(Block.Expandable)


# @@protoc_insertion_point(module_scope)
