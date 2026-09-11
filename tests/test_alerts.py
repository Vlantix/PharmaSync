from pydantic import ValidationError
import pytest
from datetime import datetime
from app.models.alerts import AlertAcknowledge, AlertResponse, AuditLogResponse


def test_alert_acknowledge_no_notes():
    data = AlertAcknowledge()
    assert data.notes is None

def test_alert_acknowledge_with_notes():
    data = AlertAcknowledge(notes="Restocked already")
    assert data.notes == "Restocked already"

def test_alert_response_valid():
    data = AlertResponse(
        id=1, drug_id=1,
        alert_type="low_stock",
        message="Stock below threshold",
        is_resolved=False,
        created_at=datetime.now()
    )
    assert data.alert_type == "low_stock"
    assert data.resolved_at is None

def test_alert_response_resolved():
    now = datetime.now()
    data = AlertResponse(
        id=1, drug_id=1,
        alert_type="expiry",
        message="Batch expiring soon",
        is_resolved=True,
        created_at=now,
        resolved_at=now
    )
    assert data.is_resolved is True
    assert data.resolved_at is not None

def test_audit_log_response_valid():
    data = AuditLogResponse(
        id=1, action="UPDATE",
        target_table="drugs",
        created_at=datetime.now()
    )
    assert data.performed_by is None
    assert data.old_data is None
    assert data.new_data is None

def test_audit_log_response_with_data():
    data = AuditLogResponse(
        id=1, performed_by=1,
        action="UPDATE", target_table="drugs", target_id=5,
        old_data={"price": 9.50}, new_data={"price": 12.00},
        ip_address="192.168.1.1",
        created_at=datetime.now()
    )
    assert data.old_data == {"price": 9.50}
    assert data.new_data == {"price": 12.00}