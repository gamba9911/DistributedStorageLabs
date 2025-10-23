import zmq

from tinyrpc import RPCClient
from tinyrpc.protocols.jsonrpc import JSONRPCProtocol
from tinyrpc.transports.zmq import ZmqClientTransport

ctx = zmq.Context()

rpc_client = RPCClient(
    JSONRPCProtocol(),
    ZmqClientTransport.create(ctx, 'tcp://127.0.0.1:5001')
)

str_server = rpc_client.get_proxy()

# call a method called 'reverse_string' with a single string argument
result = str_server.reverse_string('Hello, World!')

print("Server answered:", result)
