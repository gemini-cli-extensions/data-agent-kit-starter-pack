"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const index_js_1 = require("@modelcontextprotocol/sdk/server/index.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const types_js_1 = require("@modelcontextprotocol/sdk/types.js");
const zod_1 = require("zod");
const delete_cell_js_1 = require("./tools/delete_cell.js");
const insert_cell_js_1 = require("./tools/insert_cell.js");
const list_cells_js_1 = require("./tools/list_cells.js");
const read_cell_js_1 = require("./tools/read_cell.js");
const replace_cell_js_1 = require("./tools/replace_cell.js");
const server = new index_js_1.Server({
    name: 'standalone-notebook-mcp',
    version: '0.1.0',
}, {
    capabilities: {
        tools: {},
    },
});
// Define tools
server.setRequestHandler(types_js_1.ListToolsRequestSchema, async () => {
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
                            description: 'Index at which to insert the cell (omitted to append)',
                        },
                        cellType: {
                            type: 'string',
                            enum: ['code', 'markdown'],
                            description: 'Type of cell',
                        },
                        content: { type: 'string', description: 'Content of the cell' },
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
                        content: { type: 'string', description: 'New content of the cell' },
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
const NotebookPathSchema = zod_1.z.object({
    notebookPath: zod_1.z.string(),
});
const CellIndexSchema = NotebookPathSchema.extend({
    cellIndex: zod_1.z.number(),
});
const InsertCellSchema = NotebookPathSchema.extend({
    cellIndex: zod_1.z.number().optional(),
    cellType: zod_1.z.enum(['code', 'markdown']),
    content: zod_1.z.string(),
});
const ReplaceCellSchema = CellIndexSchema.extend({
    content: zod_1.z.string(),
});
server.setRequestHandler(types_js_1.CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    try {
        switch (name) {
            case 'list_cells': {
                const parsed = NotebookPathSchema.parse(args);
                const result = await (0, list_cells_js_1.listCells)(parsed.notebookPath);
                return {
                    content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
                };
            }
            case 'read_cell': {
                const parsed = CellIndexSchema.parse(args);
                const result = await (0, read_cell_js_1.readCell)(parsed.notebookPath, parsed.cellIndex);
                return {
                    content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
                };
            }
            case 'insert_cell': {
                const parsed = InsertCellSchema.parse(args);
                const result = await (0, insert_cell_js_1.insertCell)(parsed.notebookPath, parsed.cellType, parsed.content, parsed.cellIndex);
                return {
                    content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
                };
            }
            case 'replace_cell': {
                const parsed = ReplaceCellSchema.parse(args);
                const result = await (0, replace_cell_js_1.replaceCell)(parsed.notebookPath, parsed.cellIndex, parsed.content);
                return {
                    content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
                };
            }
            case 'delete_cell': {
                const parsed = CellIndexSchema.parse(args);
                const result = await (0, delete_cell_js_1.deleteCell)(parsed.notebookPath, parsed.cellIndex);
                return {
                    content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
                };
            }
            default:
                throw new Error(`Unknown tool: ${name}`);
        }
    }
    catch (error) {
        if (error instanceof zod_1.z.ZodError) {
            throw new Error(`Invalid arguments for ${name}: ${error.message}`);
        }
        throw error;
    }
});
async function run() {
    const transport = new stdio_js_1.StdioServerTransport();
    await server.connect(transport);
    console.error('Standalone Notebook MCP server running on stdio');
}
run().catch((error) => {
    console.error('Fatal error running server:', error);
    process.exit(1);
});
