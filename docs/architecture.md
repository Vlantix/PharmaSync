SYSTEM ARCHITECTURE

Core Components:

1.Barcode Scanning Interface
Web app or mobile-friendly interface
Pharmacist scans barcode → system looks up drug
Quantity input → stock updates instantly
Offline capability (scan locally, sync when network returns)

2.Real-Time Stock Dashboard
Live inventory view (WebSocket updates)
Low-stock alerts highlighted
Role-based views (Pharmacist sees dispense history, Manager sees trends)

3.Alert System
Minimum stock threshold per drug
Auto-trigger email/in-app notification when threshold breached
SMS alert sender when needed if there is no internet
Alert log (who was notified, when, for which drug)

4.Bulk Import Pipeline
Upload Excel (new stock received) or OCR images (manual counts)
Validate barcodes against existing drugs
Manager reviews → approves → commits to stock

5.Audit Trail
Every scan logged: user, drug, barcode, qty, timestamp, reason (dispense/receive/adjustment)
Immutable (can't be edited, only new entries added)


Data Entities:

- Drug (name, barcode, min_stock, supplier, price)
- StockTransaction (drug_id, user_id, qty_change, type, timestamp)
- Alert (drug_id, triggered_at, acknowledged_by)
- User (name, role, email)
- AuditLog (all changes, immutable)

User Roles & Permissions:

Role	Can Scan	Can Adjust	Can Import	Can Approve Import	Can Set Alerts	View Dashboard
Admin	   ✓	        ✓	        ✓	        ✓	                ✓	            ✓
Manager	   ✗	        ✓	        ✓	        ✓	                ✓	            ✓
Pharmacist ✓	        ✓	        ✗	        ✗	                ✗	            ✓

