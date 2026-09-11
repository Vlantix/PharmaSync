from pydantic import ValidationError
import pytest
from datetime import datetime, date
from app.models.inventory import (
    ReceiveStock, DispenseStock, AdjustStock,
    InventoryResponse, TransactionResponse
)


def test_receive_stock_valid():
    data = ReceiveStock(drug_id=1, quantity=100)
    assert data.drug_id == 1
    assert data.quantity == 100
    assert data.batch_number is None
    assert data.expiry_date is None

def test_receive_stock_with_expiry():
    data = ReceiveStock(drug_id=1, quantity=50, expiry_date=date(2026, 12, 31))
    assert data.expiry_date == date(2026, 12, 31)

def test_receive_stock_missing_required():
    with pytest.raises(ValidationError):
        ReceiveStock(quantity=100)  # missing drug_id

def test_dispense_stock_valid():
    data = DispenseStock(drug_id=1, quantity=10)
    assert data.quantity == 10
    assert data.notes is None

def test_dispense_stock_missing_required():
    with pytest.raises(ValidationError):
        DispenseStock(drug_id=1)  # missing quantity

def test_adjust_stock_positive():
    data = AdjustStock(drug_id=1, quantity=20)
    assert data.quantity == 20

def test_adjust_stock_negative():
    data = AdjustStock(drug_id=1, quantity=-10)
    assert data.quantity == -10  # negative is valid for deductions

def test_inventory_response_valid():
    data = InventoryResponse(id=1, drug_id=1, quantity=100, updated_at=datetime.now())
    assert data.id == 1
    assert data.batch_number is None

def test_transaction_response_valid():
    data = TransactionResponse(
        id=1, drug_id=1, performed_by=2,
        transaction_type="dispense", quantity=10,
        created_at=datetime.now()
    )
    assert data.transaction_type == "dispense"