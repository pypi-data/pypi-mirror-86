# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import account_pb2 as account__pb2
import account_service_pb2 as account__service__pb2
import entity_pb2 as entity__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class AccountServiceStub(object):
    """---------------------- gRPCs

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAccounts = channel.unary_stream(
                '/calixa.domain.account.AccountService/GetAccounts',
                request_serializer=account__service__pb2.GetAccountsRequest.SerializeToString,
                response_deserializer=account__pb2.Account.FromString,
                )
        self.GetAccountUsers = channel.unary_stream(
                '/calixa.domain.account.AccountService/GetAccountUsers',
                request_serializer=account__service__pb2.GetAccountUsersRequest.SerializeToString,
                response_deserializer=account__pb2.AccountUser.FromString,
                )
        self.GetAccountUser = channel.unary_unary(
                '/calixa.domain.account.AccountService/GetAccountUser',
                request_serializer=account__service__pb2.GetAccountUserRequest.SerializeToString,
                response_deserializer=account__pb2.AccountUser.FromString,
                )
        self.GetAccount = channel.unary_unary(
                '/calixa.domain.account.AccountService/GetAccount',
                request_serializer=account__service__pb2.GetAccountRequest.SerializeToString,
                response_deserializer=account__pb2.Account.FromString,
                )
        self.GetAccountByProperty = channel.unary_unary(
                '/calixa.domain.account.AccountService/GetAccountByProperty',
                request_serializer=account__service__pb2.GetAccountByPropertyRequest.SerializeToString,
                response_deserializer=account__pb2.Account.FromString,
                )
        self.CreateAccount = channel.unary_unary(
                '/calixa.domain.account.AccountService/CreateAccount',
                request_serializer=account__service__pb2.CreateAccountRequest.SerializeToString,
                response_deserializer=account__pb2.Account.FromString,
                )
        self.SaveAccount = channel.unary_unary(
                '/calixa.domain.account.AccountService/SaveAccount',
                request_serializer=account__service__pb2.CreateAccountRequest.SerializeToString,
                response_deserializer=account__pb2.Account.FromString,
                )
        self.CreateAccountUser = channel.unary_unary(
                '/calixa.domain.account.AccountService/CreateAccountUser',
                request_serializer=account__service__pb2.CreateAccountUserRequest.SerializeToString,
                response_deserializer=account__pb2.AccountUser.FromString,
                )
        self.SaveAccountUser = channel.unary_unary(
                '/calixa.domain.account.AccountService/SaveAccountUser',
                request_serializer=account__service__pb2.CreateAccountUserRequest.SerializeToString,
                response_deserializer=account__pb2.AccountUser.FromString,
                )
        self.UpdateAccount = channel.unary_unary(
                '/calixa.domain.account.AccountService/UpdateAccount',
                request_serializer=account__service__pb2.UpdateAccountRequest.SerializeToString,
                response_deserializer=account__pb2.Account.FromString,
                )
        self.UpdateAccountUser = channel.unary_unary(
                '/calixa.domain.account.AccountService/UpdateAccountUser',
                request_serializer=account__service__pb2.UpdateAccountUserRequest.SerializeToString,
                response_deserializer=account__pb2.AccountUser.FromString,
                )
        self.GetAccountAssociations = channel.unary_stream(
                '/calixa.domain.account.AccountService/GetAccountAssociations',
                request_serializer=account__service__pb2.GetAccountAssociationsRequest.SerializeToString,
                response_deserializer=account__pb2.AccountAssociationWithOrg.FromString,
                )
        self.AddUserToAccount = channel.unary_unary(
                '/calixa.domain.account.AccountService/AddUserToAccount',
                request_serializer=account__service__pb2.UpdateAccountUserAssociationRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.RemoveUserFromAccount = channel.unary_unary(
                '/calixa.domain.account.AccountService/RemoveUserFromAccount',
                request_serializer=account__service__pb2.RemoveAccountUserAssociationRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.SetUsersOnAccount = channel.unary_unary(
                '/calixa.domain.account.AccountService/SetUsersOnAccount',
                request_serializer=account__service__pb2.UpdateAccountUserAssociationRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.CreateAccountUserRole = channel.unary_unary(
                '/calixa.domain.account.AccountService/CreateAccountUserRole',
                request_serializer=account__service__pb2.CreateAccountUserRoleRequest.SerializeToString,
                response_deserializer=account__pb2.AccountUserRole.FromString,
                )
        self.GetAccountUserRole = channel.unary_unary(
                '/calixa.domain.account.AccountService/GetAccountUserRole',
                request_serializer=account__service__pb2.GetAccountUserRoleRequest.SerializeToString,
                response_deserializer=account__pb2.AccountUserRole.FromString,
                )
        self.GetAccountUserRoles = channel.unary_stream(
                '/calixa.domain.account.AccountService/GetAccountUserRoles',
                request_serializer=account__service__pb2.GetAccountUsersRoleRequest.SerializeToString,
                response_deserializer=account__pb2.AccountUserRole.FromString,
                )
        self.UpdateAccountUserRole = channel.unary_unary(
                '/calixa.domain.account.AccountService/UpdateAccountUserRole',
                request_serializer=account__service__pb2.UpdateAccountUserRoleRequest.SerializeToString,
                response_deserializer=account__pb2.AccountUserRole.FromString,
                )
        self.SaveOpportunityEntity = channel.unary_unary(
                '/calixa.domain.account.AccountService/SaveOpportunityEntity',
                request_serializer=account__service__pb2.SaveOpportunityEntityRequest.SerializeToString,
                response_deserializer=entity__pb2.Entity.FromString,
                )
        self.GetOpportunityEntities = channel.unary_stream(
                '/calixa.domain.account.AccountService/GetOpportunityEntities',
                request_serializer=account__service__pb2.GetOpportunityEntitiesRequest.SerializeToString,
                response_deserializer=entity__pb2.Entity.FromString,
                )
        self.SaveExternalAccountEntity = channel.unary_unary(
                '/calixa.domain.account.AccountService/SaveExternalAccountEntity',
                request_serializer=account__service__pb2.SaveExternalAccountEntityRequest.SerializeToString,
                response_deserializer=entity__pb2.Entity.FromString,
                )
        self.SaveExternalAccountUserEntity = channel.unary_unary(
                '/calixa.domain.account.AccountService/SaveExternalAccountUserEntity',
                request_serializer=account__service__pb2.SaveExternalAccountUserEntityRequest.SerializeToString,
                response_deserializer=entity__pb2.Entity.FromString,
                )


class AccountServiceServicer(object):
    """---------------------- gRPCs

    """

    def GetAccounts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountByProperty(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAccountUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveAccountUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateAccountUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountAssociations(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddUserToAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveUserFromAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetUsersOnAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAccountUserRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountUserRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAccountUserRoles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateAccountUserRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveOpportunityEntity(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOpportunityEntities(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveExternalAccountEntity(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SaveExternalAccountUserEntity(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AccountServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAccounts': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAccounts,
                    request_deserializer=account__service__pb2.GetAccountsRequest.FromString,
                    response_serializer=account__pb2.Account.SerializeToString,
            ),
            'GetAccountUsers': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAccountUsers,
                    request_deserializer=account__service__pb2.GetAccountUsersRequest.FromString,
                    response_serializer=account__pb2.AccountUser.SerializeToString,
            ),
            'GetAccountUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAccountUser,
                    request_deserializer=account__service__pb2.GetAccountUserRequest.FromString,
                    response_serializer=account__pb2.AccountUser.SerializeToString,
            ),
            'GetAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAccount,
                    request_deserializer=account__service__pb2.GetAccountRequest.FromString,
                    response_serializer=account__pb2.Account.SerializeToString,
            ),
            'GetAccountByProperty': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAccountByProperty,
                    request_deserializer=account__service__pb2.GetAccountByPropertyRequest.FromString,
                    response_serializer=account__pb2.Account.SerializeToString,
            ),
            'CreateAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAccount,
                    request_deserializer=account__service__pb2.CreateAccountRequest.FromString,
                    response_serializer=account__pb2.Account.SerializeToString,
            ),
            'SaveAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveAccount,
                    request_deserializer=account__service__pb2.CreateAccountRequest.FromString,
                    response_serializer=account__pb2.Account.SerializeToString,
            ),
            'CreateAccountUser': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAccountUser,
                    request_deserializer=account__service__pb2.CreateAccountUserRequest.FromString,
                    response_serializer=account__pb2.AccountUser.SerializeToString,
            ),
            'SaveAccountUser': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveAccountUser,
                    request_deserializer=account__service__pb2.CreateAccountUserRequest.FromString,
                    response_serializer=account__pb2.AccountUser.SerializeToString,
            ),
            'UpdateAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateAccount,
                    request_deserializer=account__service__pb2.UpdateAccountRequest.FromString,
                    response_serializer=account__pb2.Account.SerializeToString,
            ),
            'UpdateAccountUser': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateAccountUser,
                    request_deserializer=account__service__pb2.UpdateAccountUserRequest.FromString,
                    response_serializer=account__pb2.AccountUser.SerializeToString,
            ),
            'GetAccountAssociations': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAccountAssociations,
                    request_deserializer=account__service__pb2.GetAccountAssociationsRequest.FromString,
                    response_serializer=account__pb2.AccountAssociationWithOrg.SerializeToString,
            ),
            'AddUserToAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.AddUserToAccount,
                    request_deserializer=account__service__pb2.UpdateAccountUserAssociationRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'RemoveUserFromAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveUserFromAccount,
                    request_deserializer=account__service__pb2.RemoveAccountUserAssociationRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SetUsersOnAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.SetUsersOnAccount,
                    request_deserializer=account__service__pb2.UpdateAccountUserAssociationRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'CreateAccountUserRole': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAccountUserRole,
                    request_deserializer=account__service__pb2.CreateAccountUserRoleRequest.FromString,
                    response_serializer=account__pb2.AccountUserRole.SerializeToString,
            ),
            'GetAccountUserRole': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAccountUserRole,
                    request_deserializer=account__service__pb2.GetAccountUserRoleRequest.FromString,
                    response_serializer=account__pb2.AccountUserRole.SerializeToString,
            ),
            'GetAccountUserRoles': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAccountUserRoles,
                    request_deserializer=account__service__pb2.GetAccountUsersRoleRequest.FromString,
                    response_serializer=account__pb2.AccountUserRole.SerializeToString,
            ),
            'UpdateAccountUserRole': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateAccountUserRole,
                    request_deserializer=account__service__pb2.UpdateAccountUserRoleRequest.FromString,
                    response_serializer=account__pb2.AccountUserRole.SerializeToString,
            ),
            'SaveOpportunityEntity': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveOpportunityEntity,
                    request_deserializer=account__service__pb2.SaveOpportunityEntityRequest.FromString,
                    response_serializer=entity__pb2.Entity.SerializeToString,
            ),
            'GetOpportunityEntities': grpc.unary_stream_rpc_method_handler(
                    servicer.GetOpportunityEntities,
                    request_deserializer=account__service__pb2.GetOpportunityEntitiesRequest.FromString,
                    response_serializer=entity__pb2.Entity.SerializeToString,
            ),
            'SaveExternalAccountEntity': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveExternalAccountEntity,
                    request_deserializer=account__service__pb2.SaveExternalAccountEntityRequest.FromString,
                    response_serializer=entity__pb2.Entity.SerializeToString,
            ),
            'SaveExternalAccountUserEntity': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveExternalAccountUserEntity,
                    request_deserializer=account__service__pb2.SaveExternalAccountUserEntityRequest.FromString,
                    response_serializer=entity__pb2.Entity.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'calixa.domain.account.AccountService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AccountService(object):
    """---------------------- gRPCs

    """

    @staticmethod
    def GetAccounts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.account.AccountService/GetAccounts',
            account__service__pb2.GetAccountsRequest.SerializeToString,
            account__pb2.Account.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccountUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.account.AccountService/GetAccountUsers',
            account__service__pb2.GetAccountUsersRequest.SerializeToString,
            account__pb2.AccountUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccountUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/GetAccountUser',
            account__service__pb2.GetAccountUserRequest.SerializeToString,
            account__pb2.AccountUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/GetAccount',
            account__service__pb2.GetAccountRequest.SerializeToString,
            account__pb2.Account.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccountByProperty(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/GetAccountByProperty',
            account__service__pb2.GetAccountByPropertyRequest.SerializeToString,
            account__pb2.Account.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/CreateAccount',
            account__service__pb2.CreateAccountRequest.SerializeToString,
            account__pb2.Account.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/SaveAccount',
            account__service__pb2.CreateAccountRequest.SerializeToString,
            account__pb2.Account.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAccountUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/CreateAccountUser',
            account__service__pb2.CreateAccountUserRequest.SerializeToString,
            account__pb2.AccountUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveAccountUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/SaveAccountUser',
            account__service__pb2.CreateAccountUserRequest.SerializeToString,
            account__pb2.AccountUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/UpdateAccount',
            account__service__pb2.UpdateAccountRequest.SerializeToString,
            account__pb2.Account.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateAccountUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/UpdateAccountUser',
            account__service__pb2.UpdateAccountUserRequest.SerializeToString,
            account__pb2.AccountUser.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccountAssociations(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.account.AccountService/GetAccountAssociations',
            account__service__pb2.GetAccountAssociationsRequest.SerializeToString,
            account__pb2.AccountAssociationWithOrg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddUserToAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/AddUserToAccount',
            account__service__pb2.UpdateAccountUserAssociationRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RemoveUserFromAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/RemoveUserFromAccount',
            account__service__pb2.RemoveAccountUserAssociationRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetUsersOnAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/SetUsersOnAccount',
            account__service__pb2.UpdateAccountUserAssociationRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAccountUserRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/CreateAccountUserRole',
            account__service__pb2.CreateAccountUserRoleRequest.SerializeToString,
            account__pb2.AccountUserRole.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccountUserRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/GetAccountUserRole',
            account__service__pb2.GetAccountUserRoleRequest.SerializeToString,
            account__pb2.AccountUserRole.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAccountUserRoles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.account.AccountService/GetAccountUserRoles',
            account__service__pb2.GetAccountUsersRoleRequest.SerializeToString,
            account__pb2.AccountUserRole.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateAccountUserRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/UpdateAccountUserRole',
            account__service__pb2.UpdateAccountUserRoleRequest.SerializeToString,
            account__pb2.AccountUserRole.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveOpportunityEntity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/SaveOpportunityEntity',
            account__service__pb2.SaveOpportunityEntityRequest.SerializeToString,
            entity__pb2.Entity.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOpportunityEntities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/calixa.domain.account.AccountService/GetOpportunityEntities',
            account__service__pb2.GetOpportunityEntitiesRequest.SerializeToString,
            entity__pb2.Entity.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveExternalAccountEntity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/SaveExternalAccountEntity',
            account__service__pb2.SaveExternalAccountEntityRequest.SerializeToString,
            entity__pb2.Entity.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SaveExternalAccountUserEntity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/calixa.domain.account.AccountService/SaveExternalAccountUserEntity',
            account__service__pb2.SaveExternalAccountUserEntityRequest.SerializeToString,
            entity__pb2.Entity.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
