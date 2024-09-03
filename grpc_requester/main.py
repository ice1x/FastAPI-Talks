from typing import Callable

from fastapi import FastAPI

from api.router import router
from core.config import settings

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    root_path=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)


def customize_openapi(func: Callable[..., dict]) -> Callable[..., dict]:
    """Customize OpenAPI schema."""

    def wrapper(*args, **kwargs) -> dict:
        """Wrapper."""
        res = func(*args, **kwargs)
        for _, method_item in res.get("paths", {}).items():
            for _, param in method_item.items():
                responses = param.get("responses")
                # remove default 422 - the default 422 schema is HTTPValidationError
                if "422" in responses and responses["422"]["content"][
                    "application/json"
                ]["schema"]["$ref"].endswith("HTTPValidationError"):
                    del responses["422"]
        return res

    return wrapper


app.openapi = customize_openapi(app.openapi)
app.include_router(router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {"Say": "Hello!"}
