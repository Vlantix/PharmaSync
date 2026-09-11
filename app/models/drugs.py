from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DrugCreate(BaseModel):
    """
    Request body for POST /drugs.
    Admin only — adds a new drug to the catalog.
    """
    generic_name: str
    brand_name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    unit: str
    price: float = 0.00
    barcode: Optional[str] = None

class DrugUpdate(BaseModel):
    """
    Request body for PATCH /drugs/{drug_id}.
    All fields optional — only provided fields will be updated.
    """
    generic_name: Optional[str] = None
    brand_name: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class DrugResponse(BaseModel):
    """
    Drug representation returned by GET /drugs and GET /drugs/{drug_id}.
    Includes total_stock aggregated across all batches.
    """
    id: int
    generic_name: str
    brand_name: Optional[str]
    category_id: Optional[int]
    description: Optional[str]
    unit: str
    price: float
    barcode: Optional[str]
    is_active: bool
    total_stock: Optional[int] = None
    created_at: datetime
    updated_at: datetime
