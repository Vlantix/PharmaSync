API Routes (skeleton):

POST   /auth/login
POST   /auth/register            (Create new account - Admin only)
POST   /auth/logout
GET    /users/{user_id}          (Fetch single user by ID)
PATCH  /users/{user_id}          (partial update on user)
GET    /users
DELETE /users/{user_id}          (Deactivate user - SOFT DELETE)


GET    /drugs                    (list all drugs with current stock)
GET    /drugs/{drug_id}          (lookup by ID)
PATCH  /drugs/{drug_id}          (Partial update on drug)
POST   /drugs                    (create new drug - admin only)
GET    /drugs/barcode/{barcode}  (lookup by barcode)
PUT    /thresholds/{drug_id}     (update threshold)
DELETE /drugs/{drug_id}          (Deactivate drug availability - SOFT DELETE)


POST   /dispense                 (pharmacist scans & dispenses)
POST   /receive                  (stock arrival)
POST   /adjust                   (manual adjustment)


POST   /imports                  (upload Excel/OCR)
GET    /imports/{id}             (review import before approval)
POST   /imports/{id}/approve     (manager approves)


GET    /alerts                   (view all active alerts)
POST   /alerts/{drug_id}/acknowledge


GET    /audit-log                (view all transactions - immutable)


WebSocket /ws                    (real-time stock updates)