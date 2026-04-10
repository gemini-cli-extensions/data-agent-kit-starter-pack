/*
 * Copyright 2026 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import {Server} from '@modelcontextprotocol/sdk/server/index.js';
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import {z} from 'zod';
import {deleteCell} from './tools/delete_cell.js';
import {insertCell} from './tools/insert_cell.js';
import {listCells} from './tools/list_cells.js';
import {readCell} from './tools/read_cell.js';
import {replaceCell} from './tools/replace_cell.js';
import {getNotebookInfo} from './tools/get_notebook_info.js';
import {searchCells} from './tools/search_cells.js';

const server = new Server(
  {
    name: 'notebook',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  },
);

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'list_cells',
        description: 'List all cells in a notebook',
        inputSchema: {
          type: 'object',
          properties: {
            notebookPath: {
              type: 'string',
              description: 'Path to the notebook file',
            },
            maxLength: {
              type: 'number',
              description: 'Maximum length of the preview snippet for each cell (optional, defaults to 100)',
            },
          },
          required: ['notebookPath'],
        },
      },
      {
        name: 'read_cell',
        description: 'Read the content of a specific cell in a notebook',
        inputSchema: {
          type: 'object',
          properties: {
            notebookPath: {
              type: 'string',
              description: 'Path to the notebook file',
            },
            cellIndex: {
              type: 'number',
              description: '0-based index of the cell',
            },
          },
          required: ['notebookPath', 'cellIndex'],
        },
      },
      {
        name: 'insert_cell',
        description: 'Insert a new cell into a notebook',
        inputSchema: {
          type: 'object',
          properties: {
            notebookPath: {
              type: 'string',
              description: 'Path to the notebook file',
            },
            cellIndex: {
              type: 'number',
              description:
                'Index at which to insert the cell (omitted to append)',
            },
            cellType: {
              type: 'string',
              enum: ['code', 'markdown'],
              description: 'Type of cell',
            },
            content: {type: 'string', description: 'Content of the cell'},
          },
          required: ['notebookPath', 'cellType', 'content'],
        },
      },
      {
        name: 'replace_cell',
        description: 'Replace the content of a specific cell in a notebook',
        inputSchema: {
          type: 'object',
          properties: {
            notebookPath: {
              type: 'string',
              description: 'Path to the notebook file',
            },
            cellIndex: {
              type: 'number',
              description: '0-based index of the cell to replace',
            },
            content: {type: 'string', description: 'New content of the cell'},
          },
          required: ['notebookPath', 'cellIndex', 'content'],
        },
      },
      {
        name: 'delete_cell',
        description: 'Delete a specific cell from a notebook',
        inputSchema: {
          type: 'object',
          properties: {
            notebookPath: {
              type: 'string',
              description: 'Path to the notebook file',
            },
            cellIndex: {
              type: 'number',
              description: '0-based index of the cell to delete',
            },
          },
          required: ['notebookPath', 'cellIndex'],
        },
      },
      {
        name: 'get_notebook_info',
        description: 'Get summary information about a notebook',
        inputSchema: {
          type: 'object',
          properties: {
            notebookPath: {
              type: 'string',
              description: 'Path to the notebook file',
            },
          },
          required: ['notebookPath'],
        },
      },
      {
        name: 'search_cells',
        description: 'Search for text within cells of a notebook',
        inputSchema: {
          type: 'object',
          properties: {
            notebookPath: {
              type: 'string',
              description: 'Path to the notebook file',
            },
            query: {
              type: 'string',
              description: 'Text to search for',
            },
            caseSensitive: {
              type: 'boolean',
              description: 'Whether search is case sensitive (optional)',
            },
          },
          required: ['notebookPath', 'query'],
        },
      },
    ],
  };
});

// Zod schemas for validation
const NotebookPathSchema = z.object({
  notebookPath: z.string(),
});

const ListCellsSchema = NotebookPathSchema.extend({
  maxLength: z.number().optional(),
});

const CellIndexSchema = NotebookPathSchema.extend({
  cellIndex: z.number(),
});

const InsertCellSchema = NotebookPathSchema.extend({
  cellIndex: z.number().optional(),
  cellType: z.enum(['code', 'markdown']),
  content: z.string(),
});

const ReplaceCellSchema = CellIndexSchema.extend({
  content: z.string(),
});

const SearchCellsSchema = NotebookPathSchema.extend({
  query: z.string(),
  caseSensitive: z.boolean().optional(),
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const {name, arguments: args} = request.params;

  try {
    switch (name) {
      case 'list_cells': {
        const parsed = ListCellsSchema.parse(args);
        const result = await listCells(parsed.notebookPath, parsed.maxLength);
        return {
          content: [{type: 'text', text: JSON.stringify(result, null, 2)}],
        };
      }
      case 'read_cell': {
        const parsed = CellIndexSchema.parse(args);
        const result = await readCell(parsed.notebookPath, parsed.cellIndex);
        return {
          content: [{type: 'text', text: JSON.stringify(result, null, 2)}],
        };
      }
      case 'insert_cell': {
        const parsed = InsertCellSchema.parse(args);
        const result = await insertCell(
          parsed.notebookPath,
          parsed.cellType,
          parsed.content,
          parsed.cellIndex,
        );
        return {
          content: [{type: 'text', text: JSON.stringify(result, null, 2)}],
        };
      }
      case 'replace_cell': {
        const parsed = ReplaceCellSchema.parse(args);
        const result = await replaceCell(
          parsed.notebookPath,
          parsed.cellIndex,
          parsed.content,
        );
        return {
          content: [{type: 'text', text: JSON.stringify(result, null, 2)}],
        };
      }
      case 'delete_cell': {
        const parsed = CellIndexSchema.parse(args);
        const result = await deleteCell(parsed.notebookPath, parsed.cellIndex);
        return {
          content: [{type: 'text', text: JSON.stringify(result, null, 2)}],
        };
      }
      case 'get_notebook_info': {
        const parsed = NotebookPathSchema.parse(args);
        const result = await getNotebookInfo(parsed.notebookPath);
        return {
          content: [{type: 'text', text: JSON.stringify(result, null, 2)}],
        };
      }
      case 'search_cells': {
        const parsed = SearchCellsSchema.parse(args);
        const result = await searchCells(parsed.notebookPath, parsed.query, parsed.caseSensitive);
        return {
          content: [{type: 'text', text: JSON.stringify(result, null, 2)}],
        };
      }
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new Error(`Invalid arguments for ${name}: ${error.message}`);
    }
    throw error;
  }
});

async function startStandaloneServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Standalone Notebook MCP server running on stdio');
}

async function run() {
  const ideName = process.env.DATA_CLOUD_CURR_IDE_NAME;
  const logPath = '/tmp/mcp_debug.log';

  const log = (msg: string) => {
    fs.appendFileSync(logPath, `[${new Date().toISOString()}] ${msg}\n`);
    console.error(msg);
  };

  log(`Server started. DATA_CLOUD_CURR_IDE_NAME=${ideName}`);

  if (ideName) {
    log(`IDE environment detected via env var (${ideName}). Spawning local proxy...`);

    // Proxy is in ../bin/mcp_proxy_bundle.cjs relative to this file in dist/
    const proxyCmd = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../bin/mcp_proxy_bundle.cjs');
    const proxyArgs = [`notebooks-${ideName.toLowerCase()}`];

    log(`Spawning proxy: ${proxyCmd} ${proxyArgs.join(' ')}`);

    const child = spawn(process.execPath, [proxyCmd, ...proxyArgs], { stdio: ['inherit', 'inherit', 'pipe'] });

    child.stderr.on('data', (data) => {
      log(`[Proxy Stderr] ${data.toString()}`);
    });

    child.on('exit', async (code) => {
      log(`Proxy process exited with code ${code}`);
      if (code !== 0) {
        log('Proxy failed. Falling back to standalone stdio server...');
        await startStandaloneServer();
      } else {
        process.exit(0);
      }
    });
    
    return;
  }

  await startStandaloneServer();
}

run().catch((error) => {
  console.error('Fatal error running server:', error);
  process.exit(1);
});
