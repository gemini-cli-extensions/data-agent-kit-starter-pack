"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.insertCell = insertCell;
const fs = __importStar(require("fs/promises"));
async function insertCell(notebookPath, cellType, content, cellIndex) {
    try {
        const data = await fs.readFile(notebookPath, 'utf8');
        const notebook = JSON.parse(data);
        if (!notebook.cells || !Array.isArray(notebook.cells)) {
            throw new Error("Invalid notebook format: missing cells array");
        }
        const newCell = {
            cell_type: cellType,
            metadata: {},
            source: [content], // Valid nbformat: array containing a single string
        };
        if (cellType === "code") {
            newCell.outputs = [];
            newCell.execution_count = null;
        }
        if (cellIndex === undefined || cellIndex >= notebook.cells.length) {
            notebook.cells.push(newCell);
        }
        else if (cellIndex < 0) {
            notebook.cells.unshift(newCell);
        }
        else {
            notebook.cells.splice(cellIndex, 0, newCell);
        }
        await fs.writeFile(notebookPath, JSON.stringify(notebook, null, 2), 'utf8');
        return {
            success: true,
            message: `Cell inserted at index ${cellIndex !== undefined ? cellIndex : notebook.cells.length - 1}`,
        };
    }
    catch (error) {
        throw new Error(`Failed to insert cell: ${error.message}`);
    }
}
