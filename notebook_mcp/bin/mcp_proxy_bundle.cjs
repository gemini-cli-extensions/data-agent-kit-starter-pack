var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// third_party/golang/esbuild/import_meta_url.js
var importMetaUrl = require("url").pathToFileURL(__filename);

// cloud/developer_experience/datacloud_vscode/mcp_servers/cli/mcp_proxy.ts
var net = __toESM(require("net"));
var os = __toESM(require("os"));
var path = __toESM(require("path"));
var MAX_ATTEMPTS = 5;
var RETRY_DELAY_MS = 1000;
function getSocketPath(idOrPath) {
  if (path.isAbsolute(idOrPath)) {
    return idOrPath;
  }
  if (idOrPath.startsWith("\\\\?\\pipe\\")) {
    return idOrPath;
  }
  if (process.platform === "win32") {
    return path.join("\\\\?\\pipe\\", `datacloud-mcp-${idOrPath}`);
  }
  return path.join(os.tmpdir(), `datacloud-mcp-${idOrPath}.sock`);
}
function main() {
  const arg = process.argv[2];
  if (!arg) {
    console.error("Usage: node mcp_proxy.js <serverId_or_socketPath>");
    process.exit(1);
  }
  const socketPath = getSocketPath(arg);
  let attempts = 0;
  function connect() {
    attempts++;
    const client = net.createConnection(socketPath);
    client.on("connect", () => {
      process.stdin.pipe(client);
      client.pipe(process.stdout);
    });
    client.on("error", (err) => {
      if (err.code === "ENOENT" || err.code === "ECONNREFUSED") {
        if (attempts < MAX_ATTEMPTS) {
          setTimeout(connect, RETRY_DELAY_MS);
          return;
        }
      }
      console.error(`[MCP Proxy] Socket connection error: ${err.message}`);
      process.exit(1);
    });
    client.on("end", () => {
      process.exit(0);
    });
  }
  connect();
}
main();
