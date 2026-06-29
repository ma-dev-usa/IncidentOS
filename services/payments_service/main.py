import os

from fastapi import FastAPI, HTTPException

app = FastAPI(title="IncidentOS Payments Service")


@app.get("/health")
def health():
    return {"service": "payments", "status": "ok"}


@app.post("/charge")
def charge_payment():
    scenario = os.getenv("SCENARIO", "normal")

    if scenario == "payment-500":
        raise HTTPException(
            status_code=500,
            detail={
                "service": "payments",
                "error": "payment processor error",
            },
        )

    return {
        "service": "payments",
        "status": "charged",
        "payment_id": "pay_123",
    }
