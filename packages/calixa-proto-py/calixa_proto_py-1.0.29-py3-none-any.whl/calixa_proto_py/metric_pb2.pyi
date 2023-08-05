# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from common_pb2 import (
    RequestContext as common_pb2___RequestContext,
)

from event_label_pb2 import (
    EventLabelValue as event_label_pb2___EventLabelValue,
)

from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.field_mask_pb2 import (
    FieldMask as google___protobuf___field_mask_pb2___FieldMask,
)

from google.protobuf.internal.containers import (
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from google.protobuf.struct_pb2 import (
    Struct as google___protobuf___struct_pb2___Struct,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp as google___protobuf___timestamp_pb2___Timestamp,
)

from integration_source_pb2 import (
    IntegrationSourceValue as integration_source_pb2___IntegrationSourceValue,
)

from typing import (
    Iterable as typing___Iterable,
    NewType as typing___NewType,
    Optional as typing___Optional,
    Text as typing___Text,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

MetricStatusValue = typing___NewType('MetricStatusValue', builtin___int)
type___MetricStatusValue = MetricStatusValue
MetricStatus: _MetricStatus
class _MetricStatus(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[MetricStatusValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    METRIC_STATUS_UNSPECIFIED = typing___cast(MetricStatusValue, 0)
    ACTIVE = typing___cast(MetricStatusValue, 1)
    DELETED = typing___cast(MetricStatusValue, 2)
METRIC_STATUS_UNSPECIFIED = typing___cast(MetricStatusValue, 0)
ACTIVE = typing___cast(MetricStatusValue, 1)
DELETED = typing___cast(MetricStatusValue, 2)
type___MetricStatus = MetricStatus

MetricTypeValue = typing___NewType('MetricTypeValue', builtin___int)
type___MetricTypeValue = MetricTypeValue
MetricType: _MetricType
class _MetricType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[MetricTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    METRIC_TYPE_UNSPECIFIED = typing___cast(MetricTypeValue, 0)
    CUMULATIVE = typing___cast(MetricTypeValue, 1)
    GAUGE = typing___cast(MetricTypeValue, 2)
METRIC_TYPE_UNSPECIFIED = typing___cast(MetricTypeValue, 0)
CUMULATIVE = typing___cast(MetricTypeValue, 1)
GAUGE = typing___cast(MetricTypeValue, 2)
type___MetricType = MetricType

MetricValueTypeValue = typing___NewType('MetricValueTypeValue', builtin___int)
type___MetricValueTypeValue = MetricValueTypeValue
MetricValueType: _MetricValueType
class _MetricValueType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[MetricValueTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    METRIC_VALUE_TYPE_UNSPECIFIED = typing___cast(MetricValueTypeValue, 0)
    INT64 = typing___cast(MetricValueTypeValue, 1)
    DOUBLE = typing___cast(MetricValueTypeValue, 2)
    MONEY = typing___cast(MetricValueTypeValue, 3)
METRIC_VALUE_TYPE_UNSPECIFIED = typing___cast(MetricValueTypeValue, 0)
INT64 = typing___cast(MetricValueTypeValue, 1)
DOUBLE = typing___cast(MetricValueTypeValue, 2)
MONEY = typing___cast(MetricValueTypeValue, 3)
type___MetricValueType = MetricValueType

MetricExternalEntityTypeValue = typing___NewType('MetricExternalEntityTypeValue', builtin___int)
type___MetricExternalEntityTypeValue = MetricExternalEntityTypeValue
MetricExternalEntityType: _MetricExternalEntityType
class _MetricExternalEntityType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[MetricExternalEntityTypeValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    METRIC_EXTERNAL_ENTITY_UNSPECIFIED = typing___cast(MetricExternalEntityTypeValue, 0)
    ORGANIZATION = typing___cast(MetricExternalEntityTypeValue, 1)
    ACCOUNT = typing___cast(MetricExternalEntityTypeValue, 2)
METRIC_EXTERNAL_ENTITY_UNSPECIFIED = typing___cast(MetricExternalEntityTypeValue, 0)
ORGANIZATION = typing___cast(MetricExternalEntityTypeValue, 1)
ACCOUNT = typing___cast(MetricExternalEntityTypeValue, 2)
type___MetricExternalEntityType = MetricExternalEntityType

MetricOriginValue = typing___NewType('MetricOriginValue', builtin___int)
type___MetricOriginValue = MetricOriginValue
MetricOrigin: _MetricOrigin
class _MetricOrigin(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[MetricOriginValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    METRIC_ORIGIN_UNSPECIFIED = typing___cast(MetricOriginValue, 0)
    METRIC_ORIGIN_API = typing___cast(MetricOriginValue, 1)
    METRIC_ORIGIN_AUTOMATIC = typing___cast(MetricOriginValue, 2)
METRIC_ORIGIN_UNSPECIFIED = typing___cast(MetricOriginValue, 0)
METRIC_ORIGIN_API = typing___cast(MetricOriginValue, 1)
METRIC_ORIGIN_AUTOMATIC = typing___cast(MetricOriginValue, 2)
type___MetricOrigin = MetricOrigin

MetricGroupingValue = typing___NewType('MetricGroupingValue', builtin___int)
type___MetricGroupingValue = MetricGroupingValue
MetricGrouping: _MetricGrouping
class _MetricGrouping(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[MetricGroupingValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    METRIC_GROUPING_UNSPECIFIED = typing___cast(MetricGroupingValue, 0)
    HOUR = typing___cast(MetricGroupingValue, 1)
    DAY = typing___cast(MetricGroupingValue, 2)
    WEEK = typing___cast(MetricGroupingValue, 3)
    MONTH = typing___cast(MetricGroupingValue, 4)
    YEAR = typing___cast(MetricGroupingValue, 5)
METRIC_GROUPING_UNSPECIFIED = typing___cast(MetricGroupingValue, 0)
HOUR = typing___cast(MetricGroupingValue, 1)
DAY = typing___cast(MetricGroupingValue, 2)
WEEK = typing___cast(MetricGroupingValue, 3)
MONTH = typing___cast(MetricGroupingValue, 4)
YEAR = typing___cast(MetricGroupingValue, 5)
type___MetricGrouping = MetricGrouping

AggregateOperationValue = typing___NewType('AggregateOperationValue', builtin___int)
type___AggregateOperationValue = AggregateOperationValue
AggregateOperation: _AggregateOperation
class _AggregateOperation(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[AggregateOperationValue]):
    DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
    AGGREGATE_OPERATION_UNSPECIFIED = typing___cast(AggregateOperationValue, 0)
    SUM = typing___cast(AggregateOperationValue, 1)
    AVG = typing___cast(AggregateOperationValue, 2)
    COUNT = typing___cast(AggregateOperationValue, 3)
AGGREGATE_OPERATION_UNSPECIFIED = typing___cast(AggregateOperationValue, 0)
SUM = typing___cast(AggregateOperationValue, 1)
AVG = typing___cast(AggregateOperationValue, 2)
COUNT = typing___cast(AggregateOperationValue, 3)
type___AggregateOperation = AggregateOperation

class MetricDescriptor(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    metric_descriptor_id: typing___Text = ...
    organization_id: typing___Text = ...
    status: type___MetricStatusValue = ...
    metric_type: type___MetricTypeValue = ...
    value_type: type___MetricValueTypeValue = ...
    metric_origin: type___MetricOriginValue = ...
    name: typing___Text = ...
    description: typing___Text = ...

    @property
    def created_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def updated_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def properties(self) -> google___protobuf___struct_pb2___Struct: ...

    def __init__(self,
        *,
        metric_descriptor_id : typing___Optional[typing___Text] = None,
        organization_id : typing___Optional[typing___Text] = None,
        status : typing___Optional[type___MetricStatusValue] = None,
        metric_type : typing___Optional[type___MetricTypeValue] = None,
        value_type : typing___Optional[type___MetricValueTypeValue] = None,
        metric_origin : typing___Optional[type___MetricOriginValue] = None,
        created_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        updated_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        name : typing___Optional[typing___Text] = None,
        description : typing___Optional[typing___Text] = None,
        properties : typing___Optional[google___protobuf___struct_pb2___Struct] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"properties",b"properties",u"updated_at",b"updated_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"created_at",b"created_at",u"description",b"description",u"metric_descriptor_id",b"metric_descriptor_id",u"metric_origin",b"metric_origin",u"metric_type",b"metric_type",u"name",b"name",u"organization_id",b"organization_id",u"properties",b"properties",u"status",b"status",u"updated_at",b"updated_at",u"value_type",b"value_type"]) -> None: ...
type___MetricDescriptor = MetricDescriptor

class MetricSummaryRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    time_zone: typing___Text = ...
    external_entity_type: type___MetricExternalEntityTypeValue = ...
    canonical_entity_id: google___protobuf___internal___containers___RepeatedScalarFieldContainer[typing___Text] = ...

    @property
    def starting_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        time_zone : typing___Optional[typing___Text] = None,
        starting_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        external_entity_type : typing___Optional[type___MetricExternalEntityTypeValue] = None,
        canonical_entity_id : typing___Optional[typing___Iterable[typing___Text]] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"starting_at",b"starting_at"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"canonical_entity_id",b"canonical_entity_id",u"external_entity_type",b"external_entity_type",u"organization_id",b"organization_id",u"starting_at",b"starting_at",u"time_zone",b"time_zone"]) -> None: ...
type___MetricSummaryRequest = MetricSummaryRequest

class MetricSummary(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    canonical_entity_id: typing___Text = ...
    external_entity_type: type___MetricExternalEntityTypeValue = ...
    metric_descriptor_id: typing___Text = ...
    time_zone: typing___Text = ...

    @property
    def today(self) -> type___MetricObservationAtTime: ...

    @property
    def yesterday(self) -> type___MetricObservationAtTime: ...

    @property
    def last_7_days(self) -> type___MetricObservationAtTime: ...

    @property
    def last_30_days(self) -> type___MetricObservationAtTime: ...

    @property
    def last_365_days(self) -> type___MetricObservationAtTime: ...

    def __init__(self,
        *,
        canonical_entity_id : typing___Optional[typing___Text] = None,
        external_entity_type : typing___Optional[type___MetricExternalEntityTypeValue] = None,
        metric_descriptor_id : typing___Optional[typing___Text] = None,
        time_zone : typing___Optional[typing___Text] = None,
        today : typing___Optional[type___MetricObservationAtTime] = None,
        yesterday : typing___Optional[type___MetricObservationAtTime] = None,
        last_7_days : typing___Optional[type___MetricObservationAtTime] = None,
        last_30_days : typing___Optional[type___MetricObservationAtTime] = None,
        last_365_days : typing___Optional[type___MetricObservationAtTime] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"last_30_days",b"last_30_days",u"last_365_days",b"last_365_days",u"last_7_days",b"last_7_days",u"today",b"today",u"yesterday",b"yesterday"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"canonical_entity_id",b"canonical_entity_id",u"external_entity_type",b"external_entity_type",u"last_30_days",b"last_30_days",u"last_365_days",b"last_365_days",u"last_7_days",b"last_7_days",u"metric_descriptor_id",b"metric_descriptor_id",u"time_zone",b"time_zone",u"today",b"today",u"yesterday",b"yesterday"]) -> None: ...
type___MetricSummary = MetricSummary

class CreateMetricDescriptorRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def metric_descriptor(self) -> type___MetricDescriptor: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        metric_descriptor : typing___Optional[type___MetricDescriptor] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"metric_descriptor",b"metric_descriptor",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"metric_descriptor",b"metric_descriptor",u"request_context",b"request_context"]) -> None: ...
type___CreateMetricDescriptorRequest = CreateMetricDescriptorRequest

class GetMetricDescriptorRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    metric_descriptor_id: typing___Text = ...
    metric_origin: type___MetricOriginValue = ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        metric_descriptor_id : typing___Optional[typing___Text] = None,
        metric_origin : typing___Optional[type___MetricOriginValue] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"metric_descriptor_id",b"metric_descriptor_id",u"metric_origin",b"metric_origin",u"organization_id",b"organization_id"]) -> None: ...
type___GetMetricDescriptorRequest = GetMetricDescriptorRequest

class FindOrCreateAutoMetricDescriptorRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    organization_id: typing___Text = ...
    source: integration_source_pb2___IntegrationSourceValue = ...
    event_label: event_label_pb2___EventLabelValue = ...
    metric_type: type___MetricTypeValue = ...
    value_type: type___MetricValueTypeValue = ...
    name: typing___Text = ...

    @property
    def properties(self) -> google___protobuf___struct_pb2___Struct: ...

    def __init__(self,
        *,
        organization_id : typing___Optional[typing___Text] = None,
        source : typing___Optional[integration_source_pb2___IntegrationSourceValue] = None,
        event_label : typing___Optional[event_label_pb2___EventLabelValue] = None,
        metric_type : typing___Optional[type___MetricTypeValue] = None,
        value_type : typing___Optional[type___MetricValueTypeValue] = None,
        properties : typing___Optional[google___protobuf___struct_pb2___Struct] = None,
        name : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"properties",b"properties"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"event_label",b"event_label",u"metric_type",b"metric_type",u"name",b"name",u"organization_id",b"organization_id",u"properties",b"properties",u"source",b"source",u"value_type",b"value_type"]) -> None: ...
type___FindOrCreateAutoMetricDescriptorRequest = FindOrCreateAutoMetricDescriptorRequest

class UpdateMetricDescriptorRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def metric_descriptor(self) -> type___MetricDescriptor: ...

    @property
    def update_mask(self) -> google___protobuf___field_mask_pb2___FieldMask: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        metric_descriptor : typing___Optional[type___MetricDescriptor] = None,
        update_mask : typing___Optional[google___protobuf___field_mask_pb2___FieldMask] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"metric_descriptor",b"metric_descriptor",u"request_context",b"request_context",u"update_mask",b"update_mask"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"metric_descriptor",b"metric_descriptor",u"request_context",b"request_context",u"update_mask",b"update_mask"]) -> None: ...
type___UpdateMetricDescriptorRequest = UpdateMetricDescriptorRequest

class RecordObservationResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    def __init__(self,
        ) -> None: ...
type___RecordObservationResponse = RecordObservationResponse

class MetricObservation(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    metric_descriptor_id: typing___Text = ...
    organization_id: typing___Text = ...
    external_entity_type: type___MetricExternalEntityTypeValue = ...
    external_entity_id: typing___Text = ...
    canonical_entity_id: typing___Text = ...

    @property
    def measured_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def received_at(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    @property
    def metric_value(self) -> type___MetricValue: ...

    @property
    def request_context(self) -> common_pb2___RequestContext: ...

    def __init__(self,
        *,
        metric_descriptor_id : typing___Optional[typing___Text] = None,
        organization_id : typing___Optional[typing___Text] = None,
        external_entity_type : typing___Optional[type___MetricExternalEntityTypeValue] = None,
        external_entity_id : typing___Optional[typing___Text] = None,
        canonical_entity_id : typing___Optional[typing___Text] = None,
        measured_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        received_at : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        metric_value : typing___Optional[type___MetricValue] = None,
        request_context : typing___Optional[common_pb2___RequestContext] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"measured_at",b"measured_at",u"metric_value",b"metric_value",u"received_at",b"received_at",u"request_context",b"request_context"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"canonical_entity_id",b"canonical_entity_id",u"external_entity_id",b"external_entity_id",u"external_entity_type",b"external_entity_type",u"measured_at",b"measured_at",u"metric_descriptor_id",b"metric_descriptor_id",u"metric_value",b"metric_value",u"organization_id",b"organization_id",u"received_at",b"received_at",u"request_context",b"request_context"]) -> None: ...
type___MetricObservation = MetricObservation

class MetricValue(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    value_type: type___MetricValueTypeValue = ...
    value_as_int64: builtin___int = ...
    value_as_double: builtin___float = ...
    value_as_money: builtin___float = ...

    def __init__(self,
        *,
        value_type : typing___Optional[type___MetricValueTypeValue] = None,
        value_as_int64 : typing___Optional[builtin___int] = None,
        value_as_double : typing___Optional[builtin___float] = None,
        value_as_money : typing___Optional[builtin___float] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"value_as_double",b"value_as_double",u"value_as_int64",b"value_as_int64",u"value_as_money",b"value_as_money",u"values",b"values"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"value_as_double",b"value_as_double",u"value_as_int64",b"value_as_int64",u"value_as_money",b"value_as_money",u"value_type",b"value_type",u"values",b"values"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions___Literal[u"values",b"values"]) -> typing_extensions___Literal["value_as_int64","value_as_double","value_as_money"]: ...
type___MetricValue = MetricValue

class MetricObservationAtTime(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    valuePresent: builtin___bool = ...

    @property
    def metric_value(self) -> type___MetricValue: ...

    @property
    def time(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        valuePresent : typing___Optional[builtin___bool] = None,
        metric_value : typing___Optional[type___MetricValue] = None,
        time : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"metric_value",b"metric_value",u"time",b"time"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"metric_value",b"metric_value",u"time",b"time",u"valuePresent",b"valuePresent"]) -> None: ...
type___MetricObservationAtTime = MetricObservationAtTime

class MetricTimeSeriesRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    metric_descriptor_id: typing___Text = ...
    organization_id: typing___Text = ...
    external_entity_type: type___MetricExternalEntityTypeValue = ...
    canonical_entity_id: typing___Text = ...
    metric_grouping: type___MetricGroupingValue = ...
    time_zone: typing___Text = ...
    aggregate_operation: type___AggregateOperationValue = ...

    @property
    def to(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        metric_descriptor_id : typing___Optional[typing___Text] = None,
        organization_id : typing___Optional[typing___Text] = None,
        external_entity_type : typing___Optional[type___MetricExternalEntityTypeValue] = None,
        canonical_entity_id : typing___Optional[typing___Text] = None,
        metric_grouping : typing___Optional[type___MetricGroupingValue] = None,
        time_zone : typing___Optional[typing___Text] = None,
        to : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        aggregate_operation : typing___Optional[type___AggregateOperationValue] = None,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"from",b"from",u"to",b"to"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"aggregate_operation",b"aggregate_operation",u"canonical_entity_id",b"canonical_entity_id",u"external_entity_type",b"external_entity_type",u"from",b"from",u"metric_descriptor_id",b"metric_descriptor_id",u"metric_grouping",b"metric_grouping",u"organization_id",b"organization_id",u"time_zone",b"time_zone",u"to",b"to"]) -> None: ...
type___MetricTimeSeriesRequest = MetricTimeSeriesRequest
