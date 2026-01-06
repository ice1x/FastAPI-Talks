# Real Benchmark Results

## Test Environment

- **Date**: 2026-01-06
- **Platform**: Linux 4.4.0
- **Python**: 3.11.14
- **Framework**: FastAPI
- **Network**: Localhost
- **Requests per protocol**: 1,000 sequential

## Results Summary

| Protocol | Mean (ms) | Median (ms) | Std Dev (ms) | Min (ms) | Max (ms) | Samples |
|----------|-----------|-------------|--------------|----------|----------|---------|
| **REST** | 2.36 | 2.29 | 0.76 | 1.74 | 18.15 | 1,000 |
| **AVRO** | 2.66 | 2.57 | 1.20 | 1.93 | 38.98 | 1,000 |
| **CBOR** | 2.85 | 2.79 | 1.13 | 1.82 | 27.18 | 1,000 |
| **Socket.IO** | 99.76 | 99.87 | 57.04 | 1.30 | 199.20 | 1,000 |
| **GraphQL** | 346.41 | 337.91 | 146.66 | 97.22 | 682.09 | 1,000 |
| **gRPC** | ❌ N/A | - | - | - | - | - |

> **Note**: gRPC benchmark could not be completed in this test environment due to dependency issues.

## Key Insights

### 1. REST is Surprisingly Fast
REST showed the best performance (2.36ms average) among successfully tested protocols. The overhead of JSON serialization over HTTP/1.1 was minimal for small payloads.

### 2. Binary Formats Don't Always Win
AVRO (2.66ms) and CBOR (2.85ms) were actually *slower* than REST in this test. This demonstrates that for small payloads, serialization overhead may not be significant.

### 3. Socket.IO Has High Latency
Socket.IO averaged 99.76ms - approximately 42x slower than REST. This is primarily due to:
- WebSocket handshake overhead
- Event-driven architecture overhead
- Implementation details

However, Socket.IO provides bidirectional real-time communication, which REST cannot offer.

### 4. GraphQL is Slowest
GraphQL averaged 346ms - about 150x slower than REST. This is expected due to:
- Query parsing overhead
- Resolver execution
- Type validation
- Batch processing (50 requests per batch in this implementation)

GraphQL's value is in query flexibility, not raw speed.

## Performance Ranking

**Fastest to Slowest:**
1. 🥇 REST (2.36ms)
2. 🥈 AVRO (2.66ms)
3. 🥉 CBOR (2.85ms)
4. Socket.IO (99.76ms)
5. GraphQL (346.41ms)

## Important Caveats

### Test Environment Limitations
- **Localhost only**: No network latency
- **Small payloads**: Only timestamps (minimal data)
- **Sequential requests**: No concurrency testing
- **Development server**: Not production-grade

### Real-World Considerations

**These results may differ significantly in production because:**

1. **Network Latency Dominates** - Over internet, protocol overhead becomes negligible compared to network latency
2. **Payload Size Matters** - Binary formats (AVRO, CBOR) show advantages with larger payloads
3. **Concurrency** - Performance characteristics change under load
4. **Use Case** - GraphQL's 1 request vs 3 REST requests often makes it faster overall

## When These Results Matter

Use these benchmarks when:
- ✅ Localhost/LAN communication
- ✅ Small, frequent requests
- ✅ Low-latency requirements
- ✅ Comparing protocol overhead

These benchmarks are LESS relevant when:
- ❌ Internet-facing APIs (network latency dominates)
- ❌ Large payloads (>1KB)
- ❌ High concurrency workloads
- ❌ Complex query requirements

## Recommendations

Based on these results:

**Choose REST when:**
- Simple CRUD operations
- Small payloads
- Broad compatibility needed
- Team familiarity important

**Choose AVRO when:**
- Schema evolution required
- Kafka/data pipeline integration
- Large datasets

**Choose CBOR when:**
- IoT/embedded systems
- Bandwidth constraints
- Binary efficiency needed without schema

**Choose Socket.IO when:**
- Real-time bidirectional communication required
- Server push needed
- Predictable latency more important than raw speed

**Choose GraphQL when:**
- Multiple related resources needed
- Flexible querying required
- Mobile clients (reduces round trips)

## Reproducing Results

```bash
git clone https://github.com/ice1x/FastAPI-Talks.git
cd FastAPI-Talks
make setup
make run-benchmarks
python compare.py
```

Your results will vary based on:
- CPU speed
- Available RAM
- OS scheduler
- Python version
- Network stack configuration

## Chart

![Benchmark Comparison](benchmark_comparison.png)

## Raw Data

Results are saved in:
- `rest_out.txt`
- `avro_out.txt`
- `cbor_out.txt`
- `sio_out.txt`
- `graphql_out.txt`

Each file contains 1,000 request/response timestamp pairs in JSON format.

---

*Last updated: 2026-01-06*
