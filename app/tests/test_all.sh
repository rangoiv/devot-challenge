#!/bin/bash

export DIR="$(cd "$(dirname "$0")" && pwd)"
export API_URL="http://127.0.0.1:8000"

source "$DIR/test_login.sh"

echo $TOKEN

bash "$DIR/test_categories.sh"
bash "$DIR/test_expenses.sh"
bash "$DIR/test_expenses_filtering.sh"


echo "✅ All tests completed!"