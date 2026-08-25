/**
 * Copyright 2026 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var u=Object.create;var i=Object.defineProperty;var f=Object.getOwnPropertyDescriptor;var l=Object.getOwnPropertyNames;var E=Object.getPrototypeOf,d=Object.prototype.hasOwnProperty;var x=(o,e,r,n)=>{if(e&&typeof e=="object"||typeof e=="function")for(let t of l(e))!d.call(o,t)&&t!==r&&i(o,t,{get:()=>e[t],enumerable:!(n=f(e,t))||n.enumerable});return o};var p=(o,e,r)=>(r=o!=null?u(E(o)):{},x(e||!o||!o.__esModule?i(r,"default",{value:o,enumerable:!0}):r,o));var _=require("url").pathToFileURL(__filename);var a=p(require("net")),m=p(require("os")),s=p(require("path")),g=10,T=2e3;function M(o){return s.isAbsolute(o)||o.startsWith("\\\\?\\pipe\\")?o:process.platform==="win32"?s.join("\\\\?\\pipe\\",`datacloud-mcp-${o}`):s.join(m.tmpdir(),`datacloud-mcp-${o}.sock`)}function S(){let o=process.argv[2];o||(console.error("Usage: node mcp_proxy.js <serverId_or_socketPath>"),process.exit(1));let e=M(o),r=0;function n(){r++;let t=a.createConnection(e);t.on("connect",()=>{process.stdin.pipe(t),t.pipe(process.stdout)}),t.on("error",c=>{if((c.code==="ENOENT"||c.code==="ECONNREFUSED")&&r<g){setTimeout(n,T);return}console.error(`[MCP Proxy] Socket connection error: ${c.message}`),process.exit(1)}),t.on("end",()=>{process.exit(0)})}n()}S();
