#!/bin/bash
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

PLUGIN_NAME="data-cloud-ai-dev-kit"
REPO_URL="https://github.com/gemini-cli-extensions/data-cloud-ai-dev-kit"
INSTALL_DIR="$HOME/.agents/plugins/$PLUGIN_NAME"
MARKETPLACE_FILE="$HOME/.agents/plugins/marketplace.json"

echo "--- $PLUGIN_NAME Installer for Codex ---"

# 1. Download/Update Plugin Content
mkdir -p "$HOME/.agents/plugins"
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing plugin at $INSTALL_DIR..."
    cd "$INSTALL_DIR" && git pull
else
    echo "Cloning plugin to $INSTALL_DIR..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 2. Register with Codex Marketplace
if [ ! -f "$MARKETPLACE_FILE" ]; then
    echo "Creating new personal marketplace..."
    echo '{"name": "personal", "plugins": []}' > "$MARKETPLACE_FILE"
fi

echo "Registering plugin in $MARKETPLACE_FILE..."
node -e "
const fs = require('fs');
const path = require('path');
const file = path.resolve(process.env.HOME, '.agents/plugins/marketplace.json');
let data;
try {
    data = JSON.parse(fs.readFileSync(file, 'utf8'));
} catch (e) {
    data = { name: 'personal', plugins: [] };
}
data.plugins = data.plugins || [];
data.plugins = data.plugins.filter(p => p.name !== '${PLUGIN_NAME}');
data.plugins.push({
    name: '${PLUGIN_NAME}',
    source: { source: 'local', path: './${PLUGIN_NAME}' },
    policy: { installation: 'AVAILABLE', authentication: 'ON_INSTALL' },
    category: 'Productivity'
});
fs.writeFileSync(file, JSON.stringify(data, null, 2));
"

echo "Done! Restart Codex to use the $PLUGIN_NAME plugin."
