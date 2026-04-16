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

$ErrorActionPreference = "Stop"

$pluginName = "data-cloud-ai-dev-kit"
$repoUrl = "https://github.com/gemini-cli-extensions/data-cloud-ai-dev-kit"
$pluginsRoot = Join-Path $HOME ".agents\plugins"
$installDir = Join-Path $pluginsRoot $pluginName
$marketplaceFile = Join-Path $pluginsRoot "marketplace.json"

Write-Host "--- $pluginName Installer for Codex ---"

New-Item -ItemType Directory -Force -Path $pluginsRoot | Out-Null

if (Test-Path $installDir) {
    Write-Host "Updating existing plugin at $installDir..."
    git -C $installDir pull
} else {
    Write-Host "Cloning plugin to $installDir..."
    git clone $repoUrl $installDir
}

if (-not (Test-Path $marketplaceFile)) {
    Write-Host "Creating new personal marketplace..."
    '{"name":"personal","plugins":[]}' | Set-Content -LiteralPath $marketplaceFile -Encoding utf8
}

Write-Host "Registering plugin in $marketplaceFile..."
$pluginJson = @"
{
  "name": "$pluginName",
  "interface": {
    "displayName": "Google Data Cloud AI Dev Kit"
  },
  "source": {
    "source": "local",
    "path": "./.agents/plugins/$pluginName"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
"@

$marketplace = Get-Content -LiteralPath $marketplaceFile -Raw | ConvertFrom-Json
$newPlugin = $pluginJson | ConvertFrom-Json

# Ensure plugins is an array and filter out existing entry for this plugin.
if ($null -eq $marketplace.plugins) {
    $marketplace.plugins = @()
} else {
    $marketplace.plugins = @($marketplace.plugins | Where-Object { $_.name -ne $pluginName })
}

# Add the new plugin entry.
$marketplace.plugins += $newPlugin

# Save back to file with sufficient depth to preserve nested objects.
$marketplace | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $marketplaceFile -Encoding utf8

Write-Host "Done! Restart Codex to use the $pluginName plugin."
