"""Shared schemas for benchmark services."""

# AVRO Schema - shared between requester and responder
# This schema is used by both avro_requester and avro_responder
# to ensure compatibility and eliminate duplication
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
