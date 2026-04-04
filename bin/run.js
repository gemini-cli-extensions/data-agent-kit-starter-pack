#!/usr/bin/env node
const { spawn } = require('child_process');
const path = require('path');

const serverPath = path.resolve(__dirname, '../notebook_mcp/build/server.js');

const child = spawn(process.execPath, [serverPath], {
  stdio: 'inherit'
});

child.on('exit', (code) => {
  process.exit(code ?? 0);
});
