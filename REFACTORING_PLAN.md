# Refactoring Plan: Reducing Code Duplication

## Overview

This document outlines the refactoring plan to reduce ~3,100 lines of duplicate code across the benchmark services by introducing base classes and shared utilities.

## Current State

### Code Duplication Analysis

- **6 requester services**: ~1,500 LOC duplicated (95% identical code)
- **6 responder services**: ~1,080 LOC duplicated (90% identical code)
- **6 metrics parsers**: ~150 LOC duplicated (identical logic)
- **3 protobuf files**: ~36 LOC duplicated
- **2 AVRO schemas**: ~20 LOC duplicated
- **CLI overlap**: ~70 LOC duplicated

**Total duplicate code: ~3,100 LOC (~65% of service code)**

## Refactoring Strategy

### Phase 1: Base Classes (Week 1) ✅ COMPLETED

#### 1.1 Create Common Module

```
common/
├── __init__.py              # Module exports
├── base_requester.py        # Base class for all requesters
├── base_responder.py        # Base class for all responders
├── config.py                # Shared configuration
└── schemas.py               # Shared schemas (AVRO, etc.)
```

**Status**: ✅ Files created

**Estimated reduction**: ~430 lines

#### 1.2 Share AVRO Schema

Move AVRO schema definition from:
- `avro_requester/main.py` (lines 20-31)
- `avro_responder/main.py` (lines 17-28)

To: `common/schemas.py`

**Estimated reduction**: ~20 lines

#### 1.3 Consolidate Protobuf Definitions

Create single shared protobuf:
```
protos/
└── timestamp.proto          # Shared between grpc_requester and grpc_responder
```

Remove duplicates from:
- `grpc_requester/protos/hello_grpc.proto`
- `grpc_responder/protos/hello_grpc.proto`
- `grpc_responder_fastapi/protos/hello_grpc.proto`

**Estimated reduction**: ~36 lines

### Phase 2: Refactor Services (Week 2)

#### 2.1 Refactor REST Services

**Before** (`rest_requester/main.py` - 81 lines):
```python
from fastapi import FastAPI
import httpx

app = FastAPI(...)

REQUEST_COUNT = 1000
TIMEOUT = 30

@app.get("/run-benchmark")
async def run_benchmark():
    results = []
    async with httpx.AsyncClient() as client:
        for i in range(REQUEST_COUNT):
            # ... 20+ lines of benchmark logic
    return results

@app.get("/")
async def root():
    return {"service": "REST Requester", ...}
```

**After** (`rest_requester/main.py` - ~30 lines):
```python
from common import BaseBenchmarkRequester, BenchmarkConfig
import httpx
import json

class RestRequester(BaseBenchmarkRequester):
    def __init__(self):
        config = BenchmarkConfig(protocol_name="REST")
        super().__init__(config)

    async def _send_request(self, client, request_timestamp):
        url = f"{self.config.responder_url}/timestamp"
        response = await client.post(url, json={"request_timestamp": request_timestamp})
        response.raise_for_status()
        return response.json()

requester = RestRequester()
app = requester.app
```

**Reduction**: 81 → 30 lines (-51 lines, -63%)

#### 2.2 Refactor AVRO Services

**Before** (`avro_requester/main.py` - 116 lines):
- Lines 1-19: Imports and setup
- Lines 20-31: AVRO schema definition (DUPLICATE)
- Lines 34-48: Serialize/deserialize functions
- Lines 51-80: Benchmark endpoint
- Lines 83-116: Health check, startup

**After** (`avro_requester/main.py` - ~45 lines):
```python
from common import BaseBenchmarkRequester, BenchmarkConfig, TIMESTAMP_SCHEMA_AVRO
import avro.io
import httpx

class AvroRequester(BaseBenchmarkRequester):
    def __init__(self):
        config = BenchmarkConfig(protocol_name="AVRO")
        self.schema = avro.schema.parse(TIMESTAMP_SCHEMA_AVRO)
        super().__init__(config)

    async def _send_request(self, client, request_timestamp):
        # Serialize with AVRO
        data = {"request_timestamp": request_timestamp, "response_timestamp": ""}
        serialized = self._serialize_avro(data)

        # Send request
        response = await client.post(
            f"{self.config.responder_url}/timestamp",
            content=serialized,
            headers={"Content-Type": "application/avro"}
        )

        # Deserialize response
        return self._deserialize_avro(response.content)

    def _serialize_avro(self, data):
        # AVRO serialization logic
        ...

    def _deserialize_avro(self, data):
        # AVRO deserialization logic
        ...

requester = AvroRequester()
app = requester.app
```

**Reduction**: 116 → 45 lines (-71 lines, -61%)

#### 2.3 Refactor CBOR Services

Similar pattern to AVRO:

**Reduction**: 92 → 35 lines (-57 lines, -62%)

#### 2.4 Refactor All Responder Services

Apply same pattern to responders:

**REST Responder**: 62 → 25 lines (-37 lines, -60%)
**AVRO Responder**: 80 → 35 lines (-45 lines, -56%)
**CBOR Responder**: 54 → 25 lines (-29 lines, -54%)

### Phase 3: Unified Metrics Parser (Week 3)

#### 3.1 Generic Parser Function

**Before** (`metrics_exporter/utils.py` - 233 lines):
- 6 nearly identical functions
- Each with same timestamp parsing logic
- Only difference: field names

**After** (~80 lines):
```python
from typing import Dict, Callable

def parse_legacy_benchmark(
    data: Union[List, Dict],
    protocol: str,
    request_field: str,
    response_field: str,
    multi_response: bool = False
) -> BenchmarkResult:
    """
    Generic parser for all benchmark formats.

    Args:
        data: Raw benchmark data
        protocol: Protocol name (gRPC, REST, etc.)
        request_field: Field name for request timestamp
        response_field: Field name for response timestamp
        multi_response: Whether protocol has multiple responses
    """
    metrics = []

    # Handle single vs multi-response protocols
    items = data if isinstance(data, list) else [data]

    for idx, item in enumerate(items):
        req_ts = item.get(request_field)
        resp_ts = item.get(response_field)

        if req_ts and resp_ts:
            # Parse timestamps
            req_dt = datetime.fromisoformat(req_ts.replace("Z", "+00:00"))
            resp_dt = datetime.fromisoformat(resp_ts.replace("Z", "+00:00"))

            # Calculate latency
            latency = (resp_dt - req_dt).total_seconds()

            metrics.append(MetricData(
                request_id=idx,
                request_timestamp=req_ts,
                response_timestamp=resp_ts,
                latency_seconds=latency
            ))

    # Calculate statistics
    latencies = [m.latency_seconds for m in metrics]
    stats = calculate_statistics(latencies)

    return BenchmarkResult(
        run_id=f"{protocol}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        protocol=protocol,
        timestamp=datetime.utcnow(),
        metrics=metrics,
        stats=stats
    )

# Configuration-based parsers
PARSER_CONFIGS = {
    "grpc_out.txt": {
        "protocol": "gRPC",
        "request_field": "grpc_requester_timestamp",
        "response_field": "grpc_responder_timestamp",
    },
    "rest_out.txt": {
        "protocol": "REST",
        "request_field": "request_timestamp",
        "response_field": "response_timestamp",
    },
    "socketio_out.txt": {
        "protocol": "Socket.IO",
        "request_field": "requester_timestamp",
        "response_field": "responder_timestamp",
        "multi_response": True,
    },
    # ... etc for all protocols
}

def import_legacy_results(directory: str = ".") -> List[BenchmarkResult]:
    """Import legacy results using configuration."""
    results = []

    for filename, config in PARSER_CONFIGS.items():
        path = Path(directory) / filename
        if path.exists():
            with open(path) as f:
                data = json.load(f)

            result = parse_legacy_benchmark(data, **config)
            results.append(result)

    return results
```

**Reduction**: 233 → 80 lines (-153 lines, -66%)

### Phase 4: Consolidate CLI Tools (Week 3)

#### 4.1 Remove update_benchmarks.py

Delete `update_benchmarks.py` completely.

**Reasoning**: Functionality is 100% duplicated in:
- `metrics_cli.py import` - imports legacy results
- `metrics_cli.py export-all` - exports results
- `metrics_cli.py stats` - shows statistics
- Dashboard UI - has import button

**Reduction**: -70 lines

#### 4.2 Update Documentation

Remove references to `update_benchmarks.py` from:
- `README.md`
- `METRICS_DASHBOARD.md`
- `DASHBOARD_INSTALL.md`

Update to show only:
```bash
# Import results
python metrics_cli.py import

# Start dashboard
python metrics_cli.py dashboard
```

### Phase 5: Benchmark Runner Refactoring (Optional - Week 4)

#### 5.1 Configuration-Driven Runner

**Before** (`run_benchmarks.py` - 6 nearly identical methods, ~225 lines):

**After** (~100 lines):
```python
BENCHMARK_CONFIGS = {
    "REST": {
        "responder_dir": "rest_responder",
        "responder_cmd": ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
        "responder_port": 8000,
        "requester_dir": "rest_requester",
        "requester_cmd": ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"],
        "requester_port": 8080,
        "endpoint": "http://127.0.0.1:8080/run-benchmark",
        "output_file": "rest_out.txt",
    },
    # ... configs for all protocols
}

async def run_protocol_benchmark(self, protocol: str, config: dict) -> bool:
    """Generic benchmark runner using configuration."""
    print(f"\n{'=' * 60}")
    print(f"{protocol} BENCHMARK")
    print(f"{'=' * 60}")

    # Start responder
    responder = self.start_service(
        f"{protocol} Responder",
        config["responder_dir"],
        config["responder_cmd"],
        config["responder_port"]
    )
    if not responder:
        return False

    # Start requester
    requester = self.start_service(
        f"{protocol} Requester",
        config["requester_dir"],
        config["requester_cmd"],
        config["requester_port"]
    )
    if not requester:
        return False

    # Execute benchmark
    success = await self.execute_benchmark(
        protocol,
        config["endpoint"],
        config["output_file"]
    )

    # Cleanup
    requester.terminate()
    responder.terminate()
    time.sleep(2)

    return success

async def run_all_benchmarks(self):
    """Run all configured benchmarks."""
    results = {}

    for protocol, config in BENCHMARK_CONFIGS.items():
        results[protocol] = await self.run_protocol_benchmark(protocol, config)

    # ... rest of logic
```

**Reduction**: 225 → 100 lines (-125 lines, -56%)

## Migration Guide

### For Contributors

When adding a new protocol benchmark:

**Old way** (requires duplicating 200+ lines):
1. Copy existing requester/responder
2. Modify protocol-specific parts
3. Update multiple files

**New way** (requires ~40 lines):
1. Create requester subclass:
```python
from common import BaseBenchmarkRequester, BenchmarkConfig

class MyProtocolRequester(BaseBenchmarkRequester):
    async def _send_request(self, client, request_timestamp):
        # Only implement protocol-specific logic
        pass
```

2. Create responder subclass:
```python
from common import BaseBenchmarkResponder, BenchmarkConfig

class MyProtocolResponder(BaseBenchmarkResponder):
    # Provide serializer/deserializer in __init__
    pass
```

3. Add parser config to `PARSER_CONFIGS`
4. Add benchmark config to `BENCHMARK_CONFIGS`

### Testing Strategy

1. **Unit tests** for base classes
2. **Integration tests** to verify refactored services match original behavior
3. **Benchmark results comparison** before/after refactoring

### Rollout Plan

1. Create base classes (non-breaking)
2. Refactor one service (REST) as proof of concept
3. Compare benchmark results (must be identical)
4. Refactor remaining services one by one
5. Update documentation
6. Remove old duplicate code

## Expected Impact

### Code Reduction

| Component | Before | After | Reduction | % |
|-----------|--------|-------|-----------|---|
| Requesters (6) | 1,500 | 450 | -1,050 | -70% |
| Responders (6) | 1,080 | 350 | -730 | -68% |
| Parsers | 233 | 80 | -153 | -66% |
| Schemas | 56 | 20 | -36 | -64% |
| CLI tools | 250 | 180 | -70 | -28% |
| **Total** | **3,119** | **1,080** | **-2,039** | **-65%** |

### Maintainability Improvements

- **Adding new protocol**: 200+ lines → 40 lines (~80% reduction)
- **Bug fixes**: Fix once in base class vs 6 times in services
- **Feature additions**: Extend base class instead of updating 6 files
- **Code review**: Review 40 lines instead of 200 lines
- **Testing**: Test base class once vs each service separately

### Performance Impact

**Zero performance impact** - refactoring is purely organizational:
- Same HTTP requests
- Same serialization
- Same benchmark logic
- Only code organization changes

## Timeline

| Week | Tasks | LOC Reduction |
|------|-------|---------------|
| 1 | Create base classes, schemas, config | -56 |
| 2 | Refactor REST, AVRO, CBOR services | -400 |
| 3 | Refactor parsers, remove update_benchmarks.py | -223 |
| 4 | Refactor gRPC, Socket.IO, GraphQL | -400 |
| 5 | Refactor benchmark runner (optional) | -125 |
| 6 | Testing, documentation, cleanup | - |
| **Total** | | **-2,039 lines** |

## Success Criteria

- ✅ All existing tests pass
- ✅ Benchmark results identical before/after
- ✅ Code coverage maintained or improved
- ✅ Documentation updated
- ✅ At least 60% code reduction achieved
- ✅ No performance regression

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking changes | High | Gradual rollout, extensive testing |
| Performance regression | Medium | Benchmark before/after comparison |
| Increased complexity | Low | Good documentation, examples |
| Learning curve | Low | Migration guide, code examples |

## Questions?

For questions about this refactoring plan:
1. Review the example code in `common/base_requester.py` and `common/base_responder.py`
2. Check existing tests
3. Open a GitHub issue with label "refactoring"
