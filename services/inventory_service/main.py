import os
import time

from fastapi import FastAPI, HTTPException

app = FastAPI(title="IncidentOS Inventory Service")


@app.get("/health")
def health():
    return {"service": "inventory", "status": "ok"}


@app.post("/reserve")
def reserve_inventory():
    scenario = os.getenv("SCENARIO", "normal")

    if scenario == "inventory-timeout":
        time.sleep(5)

    if scenario == "inventory-down":
        raise HTTPException(
            status_code=503,
            detail={
                "service": "inventory",
                "error": "inventory unavailable",
            },
        )

    if scenario == "schema-drift":
        return {
            "service": "inventory",
            "reserved": True,
        }

    return {
        "service": "inventory",
        "status": "reserved",
        "reservation_id": "res_123",
    }
