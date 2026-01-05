"""
Tests for benchmark comparison script.
"""

import pytest
import json
import pandas as pd
from pathlib import Path
from compare import (
    process_grpc_data,
    process_socketio_data,
    process_graphql_data,
    process_avro_data,
    process_cbor_data,
    process_rest_data
)


class TestCompareScript:
    """Test benchmark comparison functionality."""

    def test_process_grpc_data(self):
        """Test processing gRPC benchmark data."""
        sample_data = [
            {
                "request_id": 0,
                "grpc_requester_timestamp": "2024-01-01T00:00:00",
                "grpc_responder_timestamp": "2024-01-01T00:00:01"
            },
            {
                "request_id": 1,
                "grpc_requester_timestamp": "2024-01-01T00:00:02",
                "grpc_responder_timestamp": "2024-01-01T00:00:03"
            }
        ]
        df = process_grpc_data(sample_data)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "request_id" in df.columns
        assert "response_time" in df.columns
        assert df["response_time"].iloc[0] == 1.0

    def test_process_socketio_data(self):
        """Test processing Socket.IO benchmark data."""
        sample_data = {
            "request_ts": "2024-01-01T00:00:00",
            "respond_ts": [
                "2024-01-01T00:00:01",
                "2024-01-01T00:00:02"
            ]
        }
        df = process_socketio_data(sample_data)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "request_id" in df.columns
        assert "response_time" in df.columns

    def test_process_graphql_data(self):
        """Test processing GraphQL benchmark data."""
        sample_data = [
            {
                "requestTimestamp": "2024-01-01T00:00:00",
                "responseTimestamp": "2024-01-01T00:00:01"
            },
            {
                "requestTimestamp": "2024-01-01T00:00:02",
                "responseTimestamp": "2024-01-01T00:00:03"
            }
        ]
        df = process_graphql_data(sample_data)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "response_time" in df.columns

    def test_process_avro_data(self):
        """Test processing AVRO benchmark data."""
        sample_data = [
            {
                "request_timestamp": "2024-01-01T00:00:00",
                "response_timestamp": "2024-01-01T00:00:01"
            }
        ]
        df = process_avro_data(sample_data)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "response_time" in df.columns

    def test_process_cbor_data(self):
        """Test processing CBOR benchmark data."""
        sample_data = [
            {
                "request_timestamp": "2024-01-01T00:00:00",
                "response_timestamp": "2024-01-01T00:00:01"
            }
        ]
        df = process_cbor_data(sample_data)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "response_time" in df.columns

    def test_process_rest_data(self):
        """Test processing REST API benchmark data."""
        sample_data = [
            {
                "request_timestamp": "2024-01-01T00:00:00",
                "response_timestamp": "2024-01-01T00:00:01"
            },
            {
                "request_timestamp": "2024-01-01T00:00:02",
                "response_timestamp": "2024-01-01T00:00:03"
            }
        ]
        df = process_rest_data(sample_data)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "response_time" in df.columns
        assert df["response_time"].iloc[0] == 1.0
