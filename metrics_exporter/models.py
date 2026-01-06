"""Data models for metrics storage and export."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MetricData(BaseModel):
    """Single metric measurement."""

    request_id: int
    request_timestamp: str
    response_timestamp: str
    latency_seconds: float


class BenchmarkStats(BaseModel):
    """Statistical summary of benchmark results."""

    mean: float
    median: float
    std_dev: float
    min: float
    max: float
    count: int
    p50: Optional[float] = None  # 50th percentile
    p95: Optional[float] = None  # 95th percentile
    p99: Optional[float] = None  # 99th percentile


class BenchmarkResult(BaseModel):
    """Complete benchmark run result."""

    id: Optional[int] = None
    run_id: str = Field(description="Unique identifier for this benchmark run")
    protocol: str = Field(description="Protocol name: REST, gRPC, Socket.IO, etc.")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metrics: List[MetricData] = Field(default_factory=list)
    stats: Optional[BenchmarkStats] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}


class BenchmarkComparison(BaseModel):
    """Comparison of multiple benchmark results."""

    run_id: str
    timestamp: datetime
    results: Dict[str, BenchmarkResult]
    summary: Optional[Dict[str, Any]] = None
