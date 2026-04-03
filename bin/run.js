#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');

const tsxPath = path.resolve(__dirname, '../node_modules/.bin/tsx');
const serverPath = path.resolve(__dirname, '../notebook_mcp/server.ts');

const child = spawn(tsxPath, [serverPath], {
  stdio: 'inherit'
});

child.on('exit', (code) => {
  process.exit(code ?? 0);
});
