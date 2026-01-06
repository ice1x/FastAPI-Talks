"""Shared schemas for benchmark services."""

# AVRO Schema - shared between requester and responder
TIMESTAMP_SCHEMA_AVRO = """
{
    "type": "record",
    "name": "Timestamp",
    "fields": [
        {"name": "request_timestamp", "type": "string"},
        {"name": "response_timestamp", "type": "string"}
    ]
}
"""

# Common timestamp format
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
