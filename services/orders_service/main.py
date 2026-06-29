import os

import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="IncidentOS Orders Service")

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://localhost:8002")
PAYMENTS_URL = os.getenv("PAYMENTS_URL", "http://localhost:8003")


@app.get("/health")
def health():
    return {"service": "orders", "status": "ok"}


@app.post("/orders")
async def create_order():
    scenario = os.getenv("SCENARIO", "normal")

    if scenario == "bad-config":
        raise HTTPException(
            status_code=500,
            detail={
                "service": "orders",
                "error": "missing required configuration value",
                "missing_config": "PAYMENTS_URL",
            },
        )

    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            inventory = await client.post(f"{INVENTORY_URL}/reserve")
            payment = await client.post(f"{PAYMENTS_URL}/charge")

        if inventory.status_code >= 400:
            raise HTTPException(
                status_code=502,
                detail={
                    "service": "orders",
                    "failed_dependency": "inventory",
                    "dependency_status": inventory.status_code,
                    "dependency_response": inventory.json(),
                },
            )

        if payment.status_code >= 400:
            raise HTTPException(
                status_code=502,
                detail={
                    "service": "orders",
                    "failed_dependency": "payments",
                    "dependency_status": payment.status_code,
                    "dependency_response": payment.json(),
                },
            )

        inventory_body = inventory.json()

        if "reservation_id" not in inventory_body:
            raise HTTPException(
                status_code=502,
                detail={
                    "service": "orders",
                    "failed_dependency": "inventory",
                    "error": "schema drift detected",
                    "missing_field": "reservation_id",
                    "dependency_response": inventory_body,
                },
            )

        return {
            "service": "orders",
            "status": "created",
            "order_id": "ord_123",
            "inventory": inventory_body,
            "payment": payment.json(),
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=504,
            detail={
                "service": "orders",
                "error": "orders failed while calling dependencies",
                "exception": str(exc),
            },
        )
