# Compile protobuf
$ python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto

