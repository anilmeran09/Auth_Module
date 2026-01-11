import uvicorn

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

# 🔹 Your internal imports (FIXED)
from core.config import ENVIRONMENT,DATABASE_URL




# ============================================================
# FastAPI App
# ============================================================
app = FastAPI(
    title="Auth Module",
    version="0.1.0",
    description="Auth Module",
    openapi_url="/openapi.json",
)


# ============================================================
# Custom 422 Validation Handler
# ============================================================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    error_details = exc.errors()
    field_errors = []

    for error in error_details:
        loc = error.get("loc", [])
        msg = error.get("msg", "Invalid value")

        if len(loc) > 1 and loc[0] in ("body", "query", "path"):
            field_name = str(loc[1])
        else:
            field_name = str(loc[-1]) if loc else "unknown"

        field_label = field_name.replace("_", " ").capitalize()

        replacements = ["string", "number", "integer", "boolean", "field", "value"]
        custom_msg = msg.lower()

        for word in replacements:
            if word in custom_msg:
                custom_msg = custom_msg.replace(word, field_label)
                break

        field_errors.append(
            {
                "field": field_name,
                "message": custom_msg,
            }
        )

    return ResponseHandler.unprocessable_entity(
        message="Please fill all the required fields.",
        errors=field_errors,
    )


# ============================================================
# Middleware
# ============================================================
if ENVIRONMENT != "production":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# ============================================================
# Routes
# ============================================================
# app.include_router(api_router)


# ============================================================
# Uvicorn Entry
# ============================================================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=["logs/*", "temp/*"],
        log_config=None,
    )
