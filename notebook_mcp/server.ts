import {Server} from '@modelcontextprotocol/sdk/server/index.js';
import {StdioServerTransport} from '@modelcontextprotocol/sdk/server/stdio.js';
import { spawn } from 'child_process';
import path from 'path';
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

const server = new Server(
  {
    name: 'standalone-notebook-mcp',
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
    ],
  };
});

// Zod schemas for validation
const NotebookPathSchema = z.object({
  notebookPath: z.string(),
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

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const {name, arguments: args} = request.params;

  try {
    switch (name) {
      case 'list_cells': {
        const parsed = NotebookPathSchema.parse(args);
        const result = await listCells(parsed.notebookPath);
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

async function run() {
  // Check for IDE environment variables
  const isIde = Object.keys(process.env).some(key => key.startsWith('GEMINI_CLI_IDE_'));

  if (isIde) {
    console.error('IDE environment detected. Spawning proxy to extension host...');
    
    const extPath = process.env.DATA_CLOUD_CURR_EXT_PATH || '/Users/snehamitshah/.antigravity/extensions/googlecloudtools.datacloud-99.99.99';
    const ideName = process.env.DATA_CLOUD_CURR_IDE_NAME || 'Antigravity';

    const proxyCmd = path.join(extPath, 'mcp_servers/cli/mcp_proxy_bundle.js');
    const proxyArgs = [`notebooks-${ideName.toLowerCase()}`];

    const child = spawn(process.execPath, [proxyCmd, ...proxyArgs], { stdio: 'inherit' });

    child.on('exit', (code) => {
      console.error(`Proxy process exited with code ${code}`);
      process.exit(code ?? 0);
    });
    
    return;
  }

  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Standalone Notebook MCP server running on stdio');
}

run().catch((error) => {
  console.error('Fatal error running server:', error);
  process.exit(1);
});
