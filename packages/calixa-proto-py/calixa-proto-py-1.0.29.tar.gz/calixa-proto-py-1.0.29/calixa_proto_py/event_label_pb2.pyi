# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    NewType as typing___NewType,
    cast as typing___cast,
)


builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

EventLabelValue = typing___NewType('EventLabelValue', builtin___int)
type___EventLabelValue = EventLabelValue
EventLabel: _EventLabel
class _EventLabel(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[EventLabelValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    EVENT_LABEL_UNSPECIFIED = typing___cast(EventLabelValue, 0)
    EVENT_LABEL_TRACK = typing___cast(EventLabelValue, 1)
    EVENT_LABEL_ACCOUNT_USER_CREATED = typing___cast(EventLabelValue, 100)
    EVENT_LABEL_ACCOUNT_USER_UPDATED = typing___cast(EventLabelValue, 101)
    EVENT_LABEL_ACCOUNT_USER_NEW_LOGIN = typing___cast(EventLabelValue, 102)
    EVENT_LABEL_ACCOUNT_CREATED = typing___cast(EventLabelValue, 103)
    EVENT_LABEL_ACCOUNT_UPDATED = typing___cast(EventLabelValue, 104)
    EVENT_LABEL_ACCOUNT_ADDED_ACCOUNT_USER = typing___cast(EventLabelValue, 105)
    EVENT_LABEL_ACCOUNT_REMOVED_ACCOUNT_USER = typing___cast(EventLabelValue, 106)
    EVENT_LABEL_CHARGE_SUCCEEDED = typing___cast(EventLabelValue, 200)
    EVENT_LABEL_CHARGE_FAILED = typing___cast(EventLabelValue, 201)
    EVENT_LABEL_CHARGE_REFUNDED = typing___cast(EventLabelValue, 202)
    EVENT_LABEL_CHARGE_UPDATED = typing___cast(EventLabelValue, 203)
    EVENT_LABEL_INVOICE_CREATED = typing___cast(EventLabelValue, 300)
    EVENT_LABEL_INVOICE_PAID = typing___cast(EventLabelValue, 301)
    EVENT_LABEL_INVOICE_VOIDED = typing___cast(EventLabelValue, 302)
    EVENT_LABEL_INVOICE_UNCOLLECTIBLE = typing___cast(EventLabelValue, 303)
    EVENT_LABEL_INVOICE_UPDATED = typing___cast(EventLabelValue, 304)
    EVENT_LABEL_SUBSCRIPTION_CREATED = typing___cast(EventLabelValue, 305)
    EVENT_LABEL_CONVERSATION_CREATED = typing___cast(EventLabelValue, 500)
    EVENT_LABEL_MESSAGE_CREATED = typing___cast(EventLabelValue, 501)
EVENT_LABEL_UNSPECIFIED = typing___cast(EventLabelValue, 0)
EVENT_LABEL_TRACK = typing___cast(EventLabelValue, 1)
EVENT_LABEL_ACCOUNT_USER_CREATED = typing___cast(EventLabelValue, 100)
EVENT_LABEL_ACCOUNT_USER_UPDATED = typing___cast(EventLabelValue, 101)
EVENT_LABEL_ACCOUNT_USER_NEW_LOGIN = typing___cast(EventLabelValue, 102)
EVENT_LABEL_ACCOUNT_CREATED = typing___cast(EventLabelValue, 103)
EVENT_LABEL_ACCOUNT_UPDATED = typing___cast(EventLabelValue, 104)
EVENT_LABEL_ACCOUNT_ADDED_ACCOUNT_USER = typing___cast(EventLabelValue, 105)
EVENT_LABEL_ACCOUNT_REMOVED_ACCOUNT_USER = typing___cast(EventLabelValue, 106)
EVENT_LABEL_CHARGE_SUCCEEDED = typing___cast(EventLabelValue, 200)
EVENT_LABEL_CHARGE_FAILED = typing___cast(EventLabelValue, 201)
EVENT_LABEL_CHARGE_REFUNDED = typing___cast(EventLabelValue, 202)
EVENT_LABEL_CHARGE_UPDATED = typing___cast(EventLabelValue, 203)
EVENT_LABEL_INVOICE_CREATED = typing___cast(EventLabelValue, 300)
EVENT_LABEL_INVOICE_PAID = typing___cast(EventLabelValue, 301)
EVENT_LABEL_INVOICE_VOIDED = typing___cast(EventLabelValue, 302)
EVENT_LABEL_INVOICE_UNCOLLECTIBLE = typing___cast(EventLabelValue, 303)
EVENT_LABEL_INVOICE_UPDATED = typing___cast(EventLabelValue, 304)
EVENT_LABEL_SUBSCRIPTION_CREATED = typing___cast(EventLabelValue, 305)
EVENT_LABEL_CONVERSATION_CREATED = typing___cast(EventLabelValue, 500)
EVENT_LABEL_MESSAGE_CREATED = typing___cast(EventLabelValue, 501)
type___EventLabel = EventLabel
