#!/bin/bash

echo "📌 Creating an expense for filtering..."
EXPENSE_ID=$(curl -s -X POST "$API_URL/expenses/" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
    -d '{"description": "Electricity bill", "amount": 75.50, "category_id": 1}' | jq -r '.id')

if [ "$EXPENSE_ID" = "null" ]; then
    echo "❌ Failed to create expense"
    exit 1
fi

echo "✅ Created expense with ID: $EXPENSE_ID"

echo "📌 Filtering expenses with amount >= 50..."
curl -s -X GET "$API_URL/expenses_stats/filter?min_amount=50" -H "Authorization: Bearer $TOKEN" | jq .

echo "📌 Filtering expenses with description containing 'bill'..."
curl -s -X GET "$API_URL/expenses_stats/filter?description=bill" -H "Authorization: Bearer $TOKEN" | jq .

echo "📌 Checking monthly expense stats..."
curl -s -X GET "$API_URL/expenses_stats/stats?period=month" -H "Authorization: Bearer $TOKEN" | jq .

echo "📌 Checking yearly expense stats..."
curl -s -X GET "$API_URL/expenses_stats/stats?period=year" -H "Authorization: Bearer $TOKEN" | jq .

echo "📌 Deleting expense ID $EXPENSE_ID..."
curl -s -X DELETE "$API_URL/expenses/$EXPENSE_ID" -H "Authorization: Bearer $TOKEN" | jq .

echo "✅ Expense filtering and stats tests completed!"
