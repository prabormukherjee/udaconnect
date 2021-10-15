# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import apis_pb2 as apis__pb2


class ApiServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create_location = channel.unary_unary(
                '/ApiService/create_location',
                request_serializer=apis__pb2.LocationMessage.SerializeToString,
                response_deserializer=apis__pb2.LocationMessage.FromString,
                )
        self.create_person = channel.unary_unary(
                '/ApiService/create_person',
                request_serializer=apis__pb2.PersonMessage.SerializeToString,
                response_deserializer=apis__pb2.PersonMessage.FromString,
                )


class ApiServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create_location(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def create_person(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ApiServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create_location': grpc.unary_unary_rpc_method_handler(
                    servicer.create_location,
                    request_deserializer=apis__pb2.LocationMessage.FromString,
                    response_serializer=apis__pb2.LocationMessage.SerializeToString,
            ),
            'create_person': grpc.unary_unary_rpc_method_handler(
                    servicer.create_person,
                    request_deserializer=apis__pb2.PersonMessage.FromString,
                    response_serializer=apis__pb2.PersonMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ApiService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ApiService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create_location(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ApiService/create_location',
            apis__pb2.LocationMessage.SerializeToString,
            apis__pb2.LocationMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def create_person(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ApiService/create_person',
            apis__pb2.PersonMessage.SerializeToString,
            apis__pb2.PersonMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
