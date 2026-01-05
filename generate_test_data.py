#!/usr/bin/env python3
"""Generate test benchmark data for demonstration."""

import json
from datetime import datetime, timedelta
import random

# Generate test data for each protocol
protocols = {
    'grpc_out.txt': {
        'format': 'list',
        'req_field': 'grpc_requester_timestamp',
        'resp_field': 'grpc_responder_timestamp'
    },
    'rest_out.txt': {
        'format': 'list',
        'req_field': 'request_timestamp',
        'resp_field': 'response_timestamp'
    },
    'graphql_out.txt': {
        'format': 'list',
        'req_field': 'requestTimestamp',
        'resp_field': 'responseTimestamp'
    },
    'avro_out.txt': {
        'format': 'list',
        'req_field': 'request_timestamp',
        'resp_field': 'response_timestamp'
    },
    'cbor_out.txt': {
        'format': 'list',
        'req_field': 'request_timestamp',
        'resp_field': 'response_timestamp'
    },
}

base_latencies = {
    'grpc_out.txt': 0.001,      # gRPC is fast
    'rest_out.txt': 0.002,      # REST is slower
    'graphql_out.txt': 0.0025,  # GraphQL is similar to REST
    'avro_out.txt': 0.0015,     # AVRO is efficient
    'cbor_out.txt': 0.0018,     # CBOR is efficient
}

for filename, config in protocols.items():
    data = []
    base_latency = base_latencies[filename]

    for i in range(1000):
        # Add some randomness to latency
        latency = base_latency + random.gauss(0, base_latency * 0.2)
        latency = max(0.0001, latency)  # Ensure positive

        req_time = datetime.utcnow() - timedelta(seconds=random.uniform(0, 10))
        resp_time = req_time + timedelta(seconds=latency)

        item = {
            config['req_field']: req_time.isoformat() + 'Z',
            config['resp_field']: resp_time.isoformat() + 'Z'
        }

        data.append(item)

    # Save to file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Generated {filename} with {len(data)} metrics")

# Generate Socket.IO format (different structure)
sio_data = {
    'request_ts': datetime.utcnow().isoformat() + 'Z',
    'respond_ts': []
}

for i in range(1000):
    latency = 0.0022 + random.gauss(0, 0.0004)
    latency = max(0.0001, latency)
    resp_time = datetime.utcnow() + timedelta(seconds=latency)
    sio_data['respond_ts'].append(resp_time.isoformat() + 'Z')

with open('sio_out.txt', 'w') as f:
    json.dump(sio_data, f, indent=2)

print(f"✓ Generated sio_out.txt with {len(sio_data['respond_ts'])} metrics")

print("\n=== Test Data Generated ===")
print("\nNow run:")
print("  python metrics_cli.py import")
print("  python metrics_cli.py dashboard")
