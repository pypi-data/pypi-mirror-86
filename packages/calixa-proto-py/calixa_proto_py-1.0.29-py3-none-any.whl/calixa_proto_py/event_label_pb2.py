# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: event_label.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='event_label.proto',
  package='calixa.domain.entity',
  syntax='proto3',
  serialized_options=b'\n\027io.calixa.domain.entityH\001P\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11\x65vent_label.proto\x12\x14\x63\x61lixa.domain.entity*\xf2\x05\n\nEventLabel\x12\x1b\n\x17\x45VENT_LABEL_UNSPECIFIED\x10\x00\x12\x15\n\x11\x45VENT_LABEL_TRACK\x10\x01\x12$\n EVENT_LABEL_ACCOUNT_USER_CREATED\x10\x64\x12$\n EVENT_LABEL_ACCOUNT_USER_UPDATED\x10\x65\x12&\n\"EVENT_LABEL_ACCOUNT_USER_NEW_LOGIN\x10\x66\x12\x1f\n\x1b\x45VENT_LABEL_ACCOUNT_CREATED\x10g\x12\x1f\n\x1b\x45VENT_LABEL_ACCOUNT_UPDATED\x10h\x12*\n&EVENT_LABEL_ACCOUNT_ADDED_ACCOUNT_USER\x10i\x12,\n(EVENT_LABEL_ACCOUNT_REMOVED_ACCOUNT_USER\x10j\x12!\n\x1c\x45VENT_LABEL_CHARGE_SUCCEEDED\x10\xc8\x01\x12\x1e\n\x19\x45VENT_LABEL_CHARGE_FAILED\x10\xc9\x01\x12 \n\x1b\x45VENT_LABEL_CHARGE_REFUNDED\x10\xca\x01\x12\x1f\n\x1a\x45VENT_LABEL_CHARGE_UPDATED\x10\xcb\x01\x12 \n\x1b\x45VENT_LABEL_INVOICE_CREATED\x10\xac\x02\x12\x1d\n\x18\x45VENT_LABEL_INVOICE_PAID\x10\xad\x02\x12\x1f\n\x1a\x45VENT_LABEL_INVOICE_VOIDED\x10\xae\x02\x12&\n!EVENT_LABEL_INVOICE_UNCOLLECTIBLE\x10\xaf\x02\x12 \n\x1b\x45VENT_LABEL_INVOICE_UPDATED\x10\xb0\x02\x12%\n EVENT_LABEL_SUBSCRIPTION_CREATED\x10\xb1\x02\x12%\n EVENT_LABEL_CONVERSATION_CREATED\x10\xf4\x03\x12 \n\x1b\x45VENT_LABEL_MESSAGE_CREATED\x10\xf5\x03\x42\x1d\n\x17io.calixa.domain.entityH\x01P\x01\x62\x06proto3'
)

_EVENTLABEL = _descriptor.EnumDescriptor(
  name='EventLabel',
  full_name='calixa.domain.entity.EventLabel',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_TRACK', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_ACCOUNT_USER_CREATED', index=2, number=100,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_ACCOUNT_USER_UPDATED', index=3, number=101,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_ACCOUNT_USER_NEW_LOGIN', index=4, number=102,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_ACCOUNT_CREATED', index=5, number=103,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_ACCOUNT_UPDATED', index=6, number=104,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_ACCOUNT_ADDED_ACCOUNT_USER', index=7, number=105,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_ACCOUNT_REMOVED_ACCOUNT_USER', index=8, number=106,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_CHARGE_SUCCEEDED', index=9, number=200,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_CHARGE_FAILED', index=10, number=201,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_CHARGE_REFUNDED', index=11, number=202,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_CHARGE_UPDATED', index=12, number=203,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_INVOICE_CREATED', index=13, number=300,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_INVOICE_PAID', index=14, number=301,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_INVOICE_VOIDED', index=15, number=302,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_INVOICE_UNCOLLECTIBLE', index=16, number=303,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_INVOICE_UPDATED', index=17, number=304,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_SUBSCRIPTION_CREATED', index=18, number=305,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_CONVERSATION_CREATED', index=19, number=500,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EVENT_LABEL_MESSAGE_CREATED', index=20, number=501,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=44,
  serialized_end=798,
)
_sym_db.RegisterEnumDescriptor(_EVENTLABEL)

EventLabel = enum_type_wrapper.EnumTypeWrapper(_EVENTLABEL)
EVENT_LABEL_UNSPECIFIED = 0
EVENT_LABEL_TRACK = 1
EVENT_LABEL_ACCOUNT_USER_CREATED = 100
EVENT_LABEL_ACCOUNT_USER_UPDATED = 101
EVENT_LABEL_ACCOUNT_USER_NEW_LOGIN = 102
EVENT_LABEL_ACCOUNT_CREATED = 103
EVENT_LABEL_ACCOUNT_UPDATED = 104
EVENT_LABEL_ACCOUNT_ADDED_ACCOUNT_USER = 105
EVENT_LABEL_ACCOUNT_REMOVED_ACCOUNT_USER = 106
EVENT_LABEL_CHARGE_SUCCEEDED = 200
EVENT_LABEL_CHARGE_FAILED = 201
EVENT_LABEL_CHARGE_REFUNDED = 202
EVENT_LABEL_CHARGE_UPDATED = 203
EVENT_LABEL_INVOICE_CREATED = 300
EVENT_LABEL_INVOICE_PAID = 301
EVENT_LABEL_INVOICE_VOIDED = 302
EVENT_LABEL_INVOICE_UNCOLLECTIBLE = 303
EVENT_LABEL_INVOICE_UPDATED = 304
EVENT_LABEL_SUBSCRIPTION_CREATED = 305
EVENT_LABEL_CONVERSATION_CREATED = 500
EVENT_LABEL_MESSAGE_CREATED = 501


DESCRIPTOR.enum_types_by_name['EventLabel'] = _EVENTLABEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
