#!/bin/bash

CATEGORY_ID=1

echo "📌 Creating an expense..."
EXPENSE_ID=$(curl -s -X POST "$API_URL/expenses/" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
    -d "{\"description\": \"Groceries shopping\", \"amount\": 123.45, \"category_id\": $CATEGORY_ID}" | jq -r '.id')

if [ "$EXPENSE_ID" = "null" ]; then
    echo "❌ Failed to create expense"
    exit 1
fi

echo "✅ Created expense with ID: $EXPENSE_ID"

echo "📌 Fetching all expenses..."
curl -s -X GET "$API_URL/expenses/" -H "Authorization: Bearer $TOKEN" | jq .

echo "📌 Fetching single expense..."
curl -s -X GET "$API_URL/expenses/$EXPENSE_ID" -H "Authorization: Bearer $TOKEN" | jq .

echo "📌 Updating expense ID $EXPENSE_ID..."
curl -s -X PUT "$API_URL/expenses/$EXPENSE_ID" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
    -d "{\"description\": \"Supermarket shopping\", \"amount\": 150.00}" | jq .

echo "📌 Verifying updated expense..."
curl -s -X GET "$API_URL/expenses/$EXPENSE_ID" -H "Authorization: Bearer $TOKEN" | jq .

echo "📌 Deleting expense ID $EXPENSE_ID..."
curl -s -X DELETE "$API_URL/expenses/$EXPENSE_ID" -H "Authorization: Bearer $TOKEN" | jq .

echo "📌 Verifying deletion..."
curl -s -X GET "$API_URL/expenses/" -H "Authorization: Bearer $TOKEN" | jq .

echo "✅ Expense tests completed!"
