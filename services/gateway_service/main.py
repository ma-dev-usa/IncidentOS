import os
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="IncidentOS Gateway Service")

ORDERS_URL = os.getenv("ORDERS_URL", "http://localhost:8001")


@app.get("/health")
def health():
    return {"service": "gateway", "status": "ok"}


@app.post("/checkout")
async def checkout():
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(f"{ORDERS_URL}/orders")

        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail={
                    "service": "gateway",
                    "upstream_service": "orders",
                    "upstream_status": response.status_code,
                    "upstream_response": response.json(),
                },
            )

        return {
            "service": "gateway",
            "status": "created",
            "result": response.json(),
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=504,
            detail={
                "service": "gateway",
                "error": "gateway failed while calling orders",
                "exception": str(exc),
            },
        )
