#!/bin/bash
# publish-test.sh — helper script to test publish to TestPyPI

set -e

PACKAGE_NAME="indaleko_registry_service"
DIST_DIR="dist"
TEST_PYPI_REPO_URL="https://test.pypi.org/legacy/"

read -p "⚠️  Confirm test publish of $PACKAGE_NAME to TestPyPI? (yes/no) " confirm
if [[ "$confirm" != "yes" ]]; then
  echo "Aborted."
  exit 1
fi

# Clean previous builds
echo "🧹 Cleaning old builds..."
rm -rf build $DIST_DIR *.egg-info

# Build using uv
echo "📦 Building package with uv..."
uv build

# Upload to TestPyPI
echo "🧪 Uploading to TestPyPI..."
twine upload --repository-url $TEST_PYPI_REPO_URL $DIST_DIR/*

echo "✅ Done. $PACKAGE_NAME published to TestPyPI."
