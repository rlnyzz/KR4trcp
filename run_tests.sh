#!/bin/bash
echo "🚀 Installing dev dependencies..."
pip install -r requirements-dev.txt

echo "🧪 Running async tests with pytest..."
pytest -v

echo "✅ Done!"