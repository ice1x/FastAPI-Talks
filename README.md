# Compile protobuf
$ python -m grpc_tools.protoc --python_out=./pb --grpc_python_out=./pb -I=./protos hello_grpc.proto

# Run gRPC responder and requester and collect metrics
$ cd ./grpc_responder/

$ python main.py

$ cd ./grpc_requester/

$ uvicorn main:app --host 0.0.0.0

$ cd ../

$ curl http://0.0.0.0:8000/api/run > ./grpc_out.txt

# Run socket.io responder and requester and collect metrics
$ cd ./sio_responder/

$ uvicorn main:sio_app --host 0.0.0.0

$ cd ./sio_requester/

$ uvicorn main:app --host 0.0.0.0 --port 8080

$ cd ../

$ curl http://0.0.0.0:8000/send-timestamp > ./sio_out.txt

# Compare
$ python ./compere.py


