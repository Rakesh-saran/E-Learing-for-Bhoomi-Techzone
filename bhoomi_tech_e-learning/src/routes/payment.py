from fastapi import APIRouter, HTTPException
from database.schemas.payment import PaymentSchema
from database.repositories.payment_repository import PaymentRepository

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/")
def add_payment(payment: PaymentSchema):
    result = PaymentRepository.create(payment.dict())
    payment_dict = payment.dict()
    payment_dict["id"] = str(result.inserted_id)
    return payment_dict

@router.get("/")
def list_payments():
    payments = PaymentRepository.find_all()
    for p in payments:
        p["id"] = str(p["_id"])
        p.pop("_id")
    return payments

@router.get("/{payment_id}")
def get_payment(payment_id: str):
    payment = PaymentRepository.find_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment["id"] = str(payment["_id"])
    payment.pop("_id")
    return payment

@router.delete("/{payment_id}")
def remove_payment(payment_id: str):
    result = PaymentRepository.delete(payment_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted"}
