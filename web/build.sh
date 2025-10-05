#!/usr/bin/env bash

set -euxo pipefail

# Run the build
observable build

# Copy static assets
if [ -d "./dist/_file/assets" ]; then
    echo "Copy static assets to dist"
    cp ./src/assets/*.svg ./dist/_file/assets
fi
