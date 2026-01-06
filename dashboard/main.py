"""FastAPI Web Dashboard for Benchmark Metrics."""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from metrics_exporter import MetricsStorage, MetricsExporter
from metrics_exporter.models import BenchmarkResult
from metrics_exporter.utils import import_legacy_results

app = FastAPI(title="Benchmark Metrics Dashboard", version="1.0.0")

# Setup templates and static files
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

# Initialize storage
storage = MetricsStorage()


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page."""
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "title": "Benchmark Dashboard"}
    )


@app.get("/api/stats")
async def get_stats():
    """Get database statistics."""
    return storage.get_stats()


@app.get("/api/runs")
async def get_runs(protocol: Optional[str] = None, limit: int = 100, offset: int = 0):
    """Get all benchmark runs."""
    runs = storage.get_all_runs(protocol=protocol, limit=limit, offset=offset)
    return {"runs": runs, "total": len(runs)}


@app.get("/api/runs/{run_id}")
async def get_run(run_id: str):
    """Get specific benchmark run."""
    result = storage.get_benchmark(run_id)
    if not result:
        raise HTTPException(status_code=404, detail="Run not found")
    return result.dict()


@app.get("/api/latest")
async def get_latest():
    """Get latest benchmark for each protocol."""
    results = storage.get_latest_by_protocol()
    return {protocol: result.dict() for protocol, result in results.items()}


@app.post("/api/import-legacy")
async def import_legacy():
    """Import legacy benchmark results from *_out.txt files."""
    try:
        results = import_legacy_results()

        imported_count = 0
        for result in results:
            storage.save_benchmark(result)
            imported_count += 1

        return {
            "success": True,
            "imported": imported_count,
            "message": f"Successfully imported {imported_count} benchmark results",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/runs/{run_id}")
async def delete_run(run_id: str):
    """Delete a benchmark run."""
    success = storage.delete_run(run_id)
    if not success:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"success": True, "message": "Run deleted successfully"}


@app.get("/api/export/{run_id}/{format}")
async def export_run(run_id: str, format: str):
    """Export benchmark run in specified format."""
    if format not in ["csv", "json", "html"]:
        raise HTTPException(status_code=400, detail="Invalid format")

    result = storage.get_benchmark(run_id)
    if not result:
        raise HTTPException(status_code=404, detail="Run not found")

    output_path = Path("exports") / f"{run_id}.{format}"
    output_path.parent.mkdir(exist_ok=True)

    try:
        if format == "csv":
            MetricsExporter.to_csv(result, str(output_path))
        elif format == "json":
            MetricsExporter.to_json(result, str(output_path))
        elif format == "html":
            MetricsExporter.to_html_report([result], str(output_path))

        return {"success": True, "file": str(output_path), "message": f"Exported to {output_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/compare")
async def compare_protocols():
    """Compare latest results from all protocols."""
    results = storage.get_latest_by_protocol()

    comparison = {
        protocol: {
            "run_id": result.run_id,
            "timestamp": result.timestamp.isoformat(),
            "stats": result.stats.dict() if result.stats else None,
            "sample_count": len(result.metrics),
        }
        for protocol, result in results.items()
    }

    return comparison


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888)
