import * as fs from 'fs/promises';

export async function readCell(notebookPath: string, cellIndex: number) {
  try {
    const data = await fs.readFile(notebookPath, 'utf8');
    const notebook = JSON.parse(data);
    
    if (!notebook.cells || !Array.isArray(notebook.cells)) {
      throw new Error("Invalid notebook format: missing cells array");
    }

    if (cellIndex < 0 || cellIndex >= notebook.cells.length) {
      throw new Error(`Cell index out of bounds: ${cellIndex}. Total cells: ${notebook.cells.length}`);
    }

    const cell = notebook.cells[cellIndex];
    const source = Array.isArray(cell.source) ? cell.source.join('') : cell.source || '';
    const outputs = cell.outputs || [];

    return {
      cellType: cell.cell_type,
      content: source,
      outputs: outputs,
    };
  } catch (error: any) {
    throw new Error(`Failed to read cell: ${error.message}`);
  }
}
