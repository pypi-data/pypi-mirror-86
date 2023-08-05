# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: log.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
import integration_source_pb2 as integration__source__pb2
import common_pb2 as common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='log.proto',
  package='calixa.domain.log',
  syntax='proto3',
  serialized_options=b'\n\024io.calixa.domain.logH\001P\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\tlog.proto\x12\x11\x63\x61lixa.domain.log\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x18integration_source.proto\x1a\x0c\x63ommon.proto\"\x83\x02\n\x12ThirdPartyLogEntry\x12\x43\n\x07headers\x18\x01 \x03(\x0b\x32\x32.calixa.domain.log.ThirdPartyLogEntry.HeadersEntry\x12=\n\x04meta\x18\x02 \x03(\x0b\x32/.calixa.domain.log.ThirdPartyLogEntry.MetaEntry\x12\x0c\n\x04\x62ody\x18\x03 \x01(\t\x1a.\n\x0cHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a+\n\tMetaEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xd6\x01\n\x12\x46irstPartyLogEntry\x12\x43\n\x07headers\x18\x01 \x03(\x0b\x32\x32.calixa.domain.log.FirstPartyLogEntry.HeadersEntry\x12\x0c\n\x04\x62ody\x18\x02 \x01(\t\x12=\n\x0frequest_context\x18\x03 \x01(\x0b\x32$.calixa.domain.common.RequestContext\x1a.\n\x0cHeadersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x8a\x03\n\x12WriteAheadLogEntry\x12\n\n\x02id\x18\x01 \x01(\t\x12\x17\n\x0forganization_id\x18\x02 \x01(\t\x12<\n\x06source\x18\x03 \x01(\x0e\x32,.calixa.domain.integration.IntegrationSource\x12\x13\n\x0binstance_id\x18\x04 \x01(\t\x12/\n\x0breceived_at\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0elog_written_at\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x46\n\x15third_party_log_entry\x18\x64 \x01(\x0b\x32%.calixa.domain.log.ThirdPartyLogEntryH\x00\x12\x46\n\x15\x66irst_party_log_entry\x18\x65 \x01(\x0b\x32%.calixa.domain.log.FirstPartyLogEntryH\x00\x42\x07\n\x05\x65ntry\"u\n\x1aWriteAheadLongEntryRequest\x12\x38\n\tlog_entry\x18\x01 \x01(\x0b\x32%.calixa.domain.log.WriteAheadLogEntry\x12\x1d\n\x15process_synchronously\x18\x02 \x01(\x08\"\x1d\n\x1bWriteAheadLongEntryResponse*X\n\tLogStatus\x12\x1a\n\x16LOG_STATUS_UNSPECIFIED\x10\x00\x12\x18\n\x14LOG_STATUS_PROCESSED\x10\x01\x12\x15\n\x11LOG_STATUS_FAILED\x10\x02\x32~\n\x14WriteAheadLogService\x12\x66\n\x05Write\x12-.calixa.domain.log.WriteAheadLongEntryRequest\x1a..calixa.domain.log.WriteAheadLongEntryResponseB\x1a\n\x14io.calixa.domain.logH\x01P\x01\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,integration__source__pb2.DESCRIPTOR,common__pb2.DESCRIPTOR,])

_LOGSTATUS = _descriptor.EnumDescriptor(
  name='LogStatus',
  full_name='calixa.domain.log.LogStatus',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LOG_STATUS_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LOG_STATUS_PROCESSED', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LOG_STATUS_FAILED', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1160,
  serialized_end=1248,
)
_sym_db.RegisterEnumDescriptor(_LOGSTATUS)

LogStatus = enum_type_wrapper.EnumTypeWrapper(_LOGSTATUS)
LOG_STATUS_UNSPECIFIED = 0
LOG_STATUS_PROCESSED = 1
LOG_STATUS_FAILED = 2



_THIRDPARTYLOGENTRY_HEADERSENTRY = _descriptor.Descriptor(
  name='HeadersEntry',
  full_name='calixa.domain.log.ThirdPartyLogEntry.HeadersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='calixa.domain.log.ThirdPartyLogEntry.HeadersEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='calixa.domain.log.ThirdPartyLogEntry.HeadersEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=303,
  serialized_end=349,
)

_THIRDPARTYLOGENTRY_METAENTRY = _descriptor.Descriptor(
  name='MetaEntry',
  full_name='calixa.domain.log.ThirdPartyLogEntry.MetaEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='calixa.domain.log.ThirdPartyLogEntry.MetaEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='calixa.domain.log.ThirdPartyLogEntry.MetaEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=351,
  serialized_end=394,
)

_THIRDPARTYLOGENTRY = _descriptor.Descriptor(
  name='ThirdPartyLogEntry',
  full_name='calixa.domain.log.ThirdPartyLogEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='headers', full_name='calixa.domain.log.ThirdPartyLogEntry.headers', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='meta', full_name='calixa.domain.log.ThirdPartyLogEntry.meta', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='body', full_name='calixa.domain.log.ThirdPartyLogEntry.body', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_THIRDPARTYLOGENTRY_HEADERSENTRY, _THIRDPARTYLOGENTRY_METAENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=135,
  serialized_end=394,
)


_FIRSTPARTYLOGENTRY_HEADERSENTRY = _descriptor.Descriptor(
  name='HeadersEntry',
  full_name='calixa.domain.log.FirstPartyLogEntry.HeadersEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='calixa.domain.log.FirstPartyLogEntry.HeadersEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='calixa.domain.log.FirstPartyLogEntry.HeadersEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=303,
  serialized_end=349,
)

_FIRSTPARTYLOGENTRY = _descriptor.Descriptor(
  name='FirstPartyLogEntry',
  full_name='calixa.domain.log.FirstPartyLogEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='headers', full_name='calixa.domain.log.FirstPartyLogEntry.headers', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='body', full_name='calixa.domain.log.FirstPartyLogEntry.body', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='request_context', full_name='calixa.domain.log.FirstPartyLogEntry.request_context', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_FIRSTPARTYLOGENTRY_HEADERSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=397,
  serialized_end=611,
)


_WRITEAHEADLOGENTRY = _descriptor.Descriptor(
  name='WriteAheadLogEntry',
  full_name='calixa.domain.log.WriteAheadLogEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='calixa.domain.log.WriteAheadLogEntry.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='organization_id', full_name='calixa.domain.log.WriteAheadLogEntry.organization_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source', full_name='calixa.domain.log.WriteAheadLogEntry.source', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='instance_id', full_name='calixa.domain.log.WriteAheadLogEntry.instance_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='received_at', full_name='calixa.domain.log.WriteAheadLogEntry.received_at', index=4,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='log_written_at', full_name='calixa.domain.log.WriteAheadLogEntry.log_written_at', index=5,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='third_party_log_entry', full_name='calixa.domain.log.WriteAheadLogEntry.third_party_log_entry', index=6,
      number=100, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='first_party_log_entry', full_name='calixa.domain.log.WriteAheadLogEntry.first_party_log_entry', index=7,
      number=101, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
    _descriptor.OneofDescriptor(
      name='entry', full_name='calixa.domain.log.WriteAheadLogEntry.entry',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=614,
  serialized_end=1008,
)


_WRITEAHEADLONGENTRYREQUEST = _descriptor.Descriptor(
  name='WriteAheadLongEntryRequest',
  full_name='calixa.domain.log.WriteAheadLongEntryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='log_entry', full_name='calixa.domain.log.WriteAheadLongEntryRequest.log_entry', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='process_synchronously', full_name='calixa.domain.log.WriteAheadLongEntryRequest.process_synchronously', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1010,
  serialized_end=1127,
)


_WRITEAHEADLONGENTRYRESPONSE = _descriptor.Descriptor(
  name='WriteAheadLongEntryResponse',
  full_name='calixa.domain.log.WriteAheadLongEntryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=1129,
  serialized_end=1158,
)

_THIRDPARTYLOGENTRY_HEADERSENTRY.containing_type = _THIRDPARTYLOGENTRY
_THIRDPARTYLOGENTRY_METAENTRY.containing_type = _THIRDPARTYLOGENTRY
_THIRDPARTYLOGENTRY.fields_by_name['headers'].message_type = _THIRDPARTYLOGENTRY_HEADERSENTRY
_THIRDPARTYLOGENTRY.fields_by_name['meta'].message_type = _THIRDPARTYLOGENTRY_METAENTRY
_FIRSTPARTYLOGENTRY_HEADERSENTRY.containing_type = _FIRSTPARTYLOGENTRY
_FIRSTPARTYLOGENTRY.fields_by_name['headers'].message_type = _FIRSTPARTYLOGENTRY_HEADERSENTRY
_FIRSTPARTYLOGENTRY.fields_by_name['request_context'].message_type = common__pb2._REQUESTCONTEXT
_WRITEAHEADLOGENTRY.fields_by_name['source'].enum_type = integration__source__pb2._INTEGRATIONSOURCE
_WRITEAHEADLOGENTRY.fields_by_name['received_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_WRITEAHEADLOGENTRY.fields_by_name['log_written_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_WRITEAHEADLOGENTRY.fields_by_name['third_party_log_entry'].message_type = _THIRDPARTYLOGENTRY
_WRITEAHEADLOGENTRY.fields_by_name['first_party_log_entry'].message_type = _FIRSTPARTYLOGENTRY
_WRITEAHEADLOGENTRY.oneofs_by_name['entry'].fields.append(
  _WRITEAHEADLOGENTRY.fields_by_name['third_party_log_entry'])
_WRITEAHEADLOGENTRY.fields_by_name['third_party_log_entry'].containing_oneof = _WRITEAHEADLOGENTRY.oneofs_by_name['entry']
_WRITEAHEADLOGENTRY.oneofs_by_name['entry'].fields.append(
  _WRITEAHEADLOGENTRY.fields_by_name['first_party_log_entry'])
_WRITEAHEADLOGENTRY.fields_by_name['first_party_log_entry'].containing_oneof = _WRITEAHEADLOGENTRY.oneofs_by_name['entry']
_WRITEAHEADLONGENTRYREQUEST.fields_by_name['log_entry'].message_type = _WRITEAHEADLOGENTRY
DESCRIPTOR.message_types_by_name['ThirdPartyLogEntry'] = _THIRDPARTYLOGENTRY
DESCRIPTOR.message_types_by_name['FirstPartyLogEntry'] = _FIRSTPARTYLOGENTRY
DESCRIPTOR.message_types_by_name['WriteAheadLogEntry'] = _WRITEAHEADLOGENTRY
DESCRIPTOR.message_types_by_name['WriteAheadLongEntryRequest'] = _WRITEAHEADLONGENTRYREQUEST
DESCRIPTOR.message_types_by_name['WriteAheadLongEntryResponse'] = _WRITEAHEADLONGENTRYRESPONSE
DESCRIPTOR.enum_types_by_name['LogStatus'] = _LOGSTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ThirdPartyLogEntry = _reflection.GeneratedProtocolMessageType('ThirdPartyLogEntry', (_message.Message,), {

  'HeadersEntry' : _reflection.GeneratedProtocolMessageType('HeadersEntry', (_message.Message,), {
    'DESCRIPTOR' : _THIRDPARTYLOGENTRY_HEADERSENTRY,
    '__module__' : 'log_pb2'
    # @@protoc_insertion_point(class_scope:calixa.domain.log.ThirdPartyLogEntry.HeadersEntry)
    })
  ,

  'MetaEntry' : _reflection.GeneratedProtocolMessageType('MetaEntry', (_message.Message,), {
    'DESCRIPTOR' : _THIRDPARTYLOGENTRY_METAENTRY,
    '__module__' : 'log_pb2'
    # @@protoc_insertion_point(class_scope:calixa.domain.log.ThirdPartyLogEntry.MetaEntry)
    })
  ,
  'DESCRIPTOR' : _THIRDPARTYLOGENTRY,
  '__module__' : 'log_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.log.ThirdPartyLogEntry)
  })
_sym_db.RegisterMessage(ThirdPartyLogEntry)
_sym_db.RegisterMessage(ThirdPartyLogEntry.HeadersEntry)
_sym_db.RegisterMessage(ThirdPartyLogEntry.MetaEntry)

FirstPartyLogEntry = _reflection.GeneratedProtocolMessageType('FirstPartyLogEntry', (_message.Message,), {

  'HeadersEntry' : _reflection.GeneratedProtocolMessageType('HeadersEntry', (_message.Message,), {
    'DESCRIPTOR' : _FIRSTPARTYLOGENTRY_HEADERSENTRY,
    '__module__' : 'log_pb2'
    # @@protoc_insertion_point(class_scope:calixa.domain.log.FirstPartyLogEntry.HeadersEntry)
    })
  ,
  'DESCRIPTOR' : _FIRSTPARTYLOGENTRY,
  '__module__' : 'log_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.log.FirstPartyLogEntry)
  })
_sym_db.RegisterMessage(FirstPartyLogEntry)
_sym_db.RegisterMessage(FirstPartyLogEntry.HeadersEntry)

WriteAheadLogEntry = _reflection.GeneratedProtocolMessageType('WriteAheadLogEntry', (_message.Message,), {
  'DESCRIPTOR' : _WRITEAHEADLOGENTRY,
  '__module__' : 'log_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.log.WriteAheadLogEntry)
  })
_sym_db.RegisterMessage(WriteAheadLogEntry)

WriteAheadLongEntryRequest = _reflection.GeneratedProtocolMessageType('WriteAheadLongEntryRequest', (_message.Message,), {
  'DESCRIPTOR' : _WRITEAHEADLONGENTRYREQUEST,
  '__module__' : 'log_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.log.WriteAheadLongEntryRequest)
  })
_sym_db.RegisterMessage(WriteAheadLongEntryRequest)

WriteAheadLongEntryResponse = _reflection.GeneratedProtocolMessageType('WriteAheadLongEntryResponse', (_message.Message,), {
  'DESCRIPTOR' : _WRITEAHEADLONGENTRYRESPONSE,
  '__module__' : 'log_pb2'
  # @@protoc_insertion_point(class_scope:calixa.domain.log.WriteAheadLongEntryResponse)
  })
_sym_db.RegisterMessage(WriteAheadLongEntryResponse)


DESCRIPTOR._options = None
_THIRDPARTYLOGENTRY_HEADERSENTRY._options = None
_THIRDPARTYLOGENTRY_METAENTRY._options = None
_FIRSTPARTYLOGENTRY_HEADERSENTRY._options = None

_WRITEAHEADLOGSERVICE = _descriptor.ServiceDescriptor(
  name='WriteAheadLogService',
  full_name='calixa.domain.log.WriteAheadLogService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1250,
  serialized_end=1376,
  methods=[
  _descriptor.MethodDescriptor(
    name='Write',
    full_name='calixa.domain.log.WriteAheadLogService.Write',
    index=0,
    containing_service=None,
    input_type=_WRITEAHEADLONGENTRYREQUEST,
    output_type=_WRITEAHEADLONGENTRYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_WRITEAHEADLOGSERVICE)

DESCRIPTOR.services_by_name['WriteAheadLogService'] = _WRITEAHEADLOGSERVICE

# @@protoc_insertion_point(module_scope)
