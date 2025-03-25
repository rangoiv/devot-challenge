#!/bin/bash

API_URL="http://127.0.0.1:8000"

echo "📌 Registering user..."
curl -s -X POST "$API_URL/users/register/" -H "Content-Type: application/json" -d '{"email": "test@example.com", "password": "pass123"}' | jq .

echo "📌 Logging in user..."
TOKEN=$(curl -s -X POST "$API_URL/users/login/" -H "Content-Type: application/x-www-form-urlencoded" -d "username=test@example.com&password=pass123" | jq -r '.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ Login failed, cannot retrieve token."
    exit 1
fi

echo "✅ Login successful, Token: $TOKEN"

echo "📌 Checking balance..."
curl -s -X GET "$API_URL/expenses/balance/" -H "Authorization: Bearer $TOKEN" | jq .

echo "✅ User tests completed!"
