#!/bin/bash
# publish.sh — helper script to build and publish a Python package

set -e

PACKAGE_NAME="indaleko_registry_service"
DIST_DIR="dist"

# Sanity check: confirm we are not accidentally uploading to prod PyPI without intent
read -p "🚨 Are you sure you want to upload $PACKAGE_NAME to PyPI? (yes/no) " confirm
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

# Upload to PyPI
echo "🚀 Uploading to PyPI..."
twine upload $DIST_DIR/*

echo "✅ Done. $PACKAGE_NAME published."
