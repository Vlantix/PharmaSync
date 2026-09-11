from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class ReceiveStock(BaseModel):
    """
    Request body for POST /receive.
    Manager records incoming stock with batch and expiry info.
    """
    drug_id: int
    batch_number: Optional[str] = None
    quantity: int
    expiry_date: Optional[date] = None
    notes: Optional[str] = None

class DispenseStock(BaseModel):
    """
    Request body for POST /dispense.
    Pharmacist dispenses a drug — deducts from inventory.
    System should follow FEFO (First Expiry First Out).
    """
    drug_id: int
    quantity: int
    notes: Optional[str] = None

class AdjustStock(BaseModel):
    """
    Request body for POST /adjust.
    Admin or Manager manually adjusts stock level.
    Quantity can be positive (add) or negative (deduct).
    """
    drug_id: int
    quantity: int
    notes: Optional[str] = None

class InventoryResponse(BaseModel):
    """
    Single inventory batch record.
    Returned when viewing stock per batch.
    """
    id: int
    drug_id: int
    batch_number: Optional[str] = None
    quantity: int
    expiry_date: Optional[date] = None
    updated_at: datetime

class TransactionResponse(BaseModel):
    """
    Inventory transaction record.
    Returned by audit log and transaction history endpoints.
    """
    id: int
    drug_id: int
    performed_by: int
    transaction_type: str
    quantity: int
    notes: Optional[str] = None
    created_at: datetime