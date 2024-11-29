# Mock Payment Server
This is a simple mock payment server that simulates processing payments with basic authentication. It is intended for use as a demo or prototype for testing payment processing systems.

## Features:
- Basic authentication for users.
- Mock payment processing logic.
- Accepts POST requests to simulate payment transactions.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/WM-SahilShah/mock-payment.git
cd mock-payment-server
```

2. Install the dependencies by running the following command:
```bash
pip install -r requirements.txt
```

3. Run the application locally:
```bash
uvicorn main:app --reload
```
The application will be available at `http://127.0.0.1:8000` (or the port you specify in the code).

## API Endpoints:

### POST `/payment`

This endpoint accepts a POST request to process a payment. It requires basic authentication and the following parameters in the request body.

#### **Request Body (JSON)**:
```json
{
  "product_price": 20.00,
  "account_balance": 100.00
}
```

#### **Response (JSON)**:
- On successful payment:
  ```json
  {
    "message": "Payment of 20.00 processed successfully for <username>.",
    "updated_account_balance": 80.00
  }
  ```
- If the account balance is insufficient:
  ```json
  {
    "detail": "Insufficient account balance."
  }
  ```
- If there are validation errors (e.g., negative values):
  ```json
  {
    "detail": [
      {
        "loc": ["body", "product_price"],
        "msg": "Value must be non-negative.",
        "type": "value_error"
      }
    ]
  }
  ```

### Authentication:

The server uses HTTP Basic Authentication. You need to provide a valid username and password with each request. You can use the following credentials for testing:

- **Username**: `test_username`
- **Password**: `test_password`

You can pass the credentials as part of the request using `curl`, or any HTTP client.

### Example `curl` Command:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/payment' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -u test_username:test_password \
  -d '{
  "product_price": 20.00,
  "account_balance": 100.00
}'
```
or
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/payment' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Basic dGVzdF91c2VybmFtZTp0ZXN0X3Bhc3N3b3Jk' \
  -d '{
  "product_price": 20.00,
  "account_balance": 100.00
}'
```