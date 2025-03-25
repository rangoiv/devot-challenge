#!/bin/bash

BASE_URL="http://127.0.0.1:8000/categories"

echo "📌 Creating a category..."
CATEGORY_ID=$(curl -s -X POST "$BASE_URL/" -H "Content-Type: application/json" -d '{"name": "goods"}' | jq -r '.id')

if [ "$CATEGORY_ID" = "null" ]; then
    echo "❌ Failed to create category"
    exit 1
fi

echo "✅ Created category with ID: $CATEGORY_ID"

echo "📌 Getting all categories..."
curl -s -X GET "$BASE_URL/" | jq .

echo "📌 Updating category ID $CATEGORY_ID..."
curl -s -X PUT "$BASE_URL/$CATEGORY_ID" -H "Content-Type: application/json" -d '{"name": "groceries"}' | jq .

echo "📌 Getting category ID $CATEGORY_ID..."
curl -s -X GET "$BASE_URL/$CATEGORY_ID" | jq .

echo "📌 Deleting category ID $CATEGORY_ID..."
curl -s -X DELETE "$BASE_URL/$CATEGORY_ID" | jq .

echo "📌 Verifying deletion..."
curl -s -X GET "$BASE_URL/$CATEGORY_ID" | jq .

echo "✅ All tests completed!"
