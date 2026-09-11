from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlertAcknowledge(BaseModel):
    """
    Request body for POST /alerts/{drug_id}/acknowledge.
    Admin or Manager acknowledges and resolves an active alert.
    """
    notes: Optional[str] = None

class AlertResponse(BaseModel):
    """
    Alert representation returned by GET /alerts.
    Covers both low_stock and expiry alert types.
    """
    id: int
    drug_id: int
    alert_type: str
    message: str
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None

class AuditLogResponse(BaseModel):
    """
    Immutable audit log entry returned by GET /audit-log.
    Records every write operation — who did what, when, and on what.
    Never editable, only appendable.
    """
    id: int
    performed_by: Optional[int] = None
    action: str
    target_table: str
    target_id: Optional[int] = None
    old_data: Optional[dict] = None
    new_data: Optional[dict] = None
    ip_address: Optional[str] = None
    created_at: datetime