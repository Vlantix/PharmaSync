from pydantic import ValidationError
import pytest
from datetime import datetime
from app.models.drugs import DrugCreate, DrugUpdate, DrugResponse


def test_drug_create_valid():
    drug = DrugCreate(generic_name="Paracetamol", unit="tablet")
    assert drug.generic_name == "Paracetamol"
    assert drug.price == 0.00
    assert drug.brand_name is None

def test_drug_create_with_all_fields():
    drug = DrugCreate(
        generic_name="Paracetamol",
        brand_name="Biogesic",
        category_id=1,
        unit="tablet",
        price=9.50,
        barcode="123456789"
    )
    assert drug.brand_name == "Biogesic"
    assert drug.price == 9.50

def test_drug_create_missing_required():
    with pytest.raises(ValidationError):
        DrugCreate(brand_name="Biogesic")  # missing generic_name and unit

def test_drug_update_all_optional():
    update = DrugUpdate()
    assert update.generic_name is None
    assert update.price is None
    assert update.is_active is None

def test_drug_update_partial():
    update = DrugUpdate(price=12.00, is_active=False)
    assert update.price == 12.00
    assert update.is_active is False

def test_drug_response_valid():
    now = datetime.now()
    drug = DrugResponse(
        id=1,
        generic_name="Paracetamol",
        brand_name=None,
        category_id=None,
        description=None,
        unit="tablet",
        price=9.50,
        barcode=None,
        is_active=True,
        created_at=now,
        updated_at=now
    )
    assert drug.id == 1
    assert drug.total_stock is None