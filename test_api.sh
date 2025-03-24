#!/bin/bash

API_URL="http://127.0.0.1:8000"

# Test user registration
echo "Registering user..."
curl -X POST "$API_URL/users/register/" -H "Content-Type: application/json" -d '{"email": "test@example.com", "password": "pass123"}'
echo ""

# Test login and get token
TOKEN=$(curl -s -X POST "$API_URL/users/login/" -H "Content-Type: application/x-www-form-urlencoded" -d "username=test@example.com&password=pass123" | jq -r .access_token)
echo "Token: $TOKEN"

# Test protected balance route
echo "Checking balance..."
curl -X GET "$API_URL/transactions/balance/" -H "Authorization: Bearer $TOKEN"
echo ""

# Test deposit money
echo "Depositing money..."
curl -X POST "$API_URL/transactions/deposit/" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"amount": 100}'
echo ""
