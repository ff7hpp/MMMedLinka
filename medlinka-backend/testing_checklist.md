# Testing Checklist

| # | Test                                        | Endpoint              | Expected          | Output Verification |
|---|---------------------------------------------|-----------------------|-------------------|---------------------|
| 1 | Register a new user                         | POST /api/auth/register | JWT token returned| Ensure DB 'users' has hashed pwd |
| 2 | Login with registered user                  | POST /api/auth/login    | JWT + user data   | Ensure JSON token matches |
| 3 | Send AI chat message                        | POST /api/chat/send     | AI reply returned | Chat History row inserted |
| 4 | List all doctors                            | GET /api/doctors        | Array of doctors  | See 10 seeded doctors |
| 5 | Book an appointment                         | POST /api/appointments/book| Confirmation      | New row in 'appointments' table |
| 6 | Search for "aspirin" in pharmacy            | GET /api/medicines/search | OpenFDA results   | JSON list populated with OpenFDA |
| 7 | Place a medicine order                      | POST /api/orders/place  | Order ID returned | DB 'orders' shows "Pending" |
| 8 | Create a medicine reminder                  | POST /api/reminders     | Reminder saved    | 'reminders' table updated |
| 9 | Receive reminder email at scheduled time    | (background scheduler)  | Email in inbox    | Check Brevo test inbox |
|10 | Open MedLinka.html — all data loads live    | (frontend test)         | No mock data shown| Watch network tab on browser |
