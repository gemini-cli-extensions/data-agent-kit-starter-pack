import * as fs from 'fs/promises';

export async function deleteCell(
  notebookPath: string,
  cellIndex: number
) {
  try {
    const data = await fs.readFile(notebookPath, 'utf8');
    const notebook = JSON.parse(data);
    
    if (!notebook.cells || !Array.isArray(notebook.cells)) {
      throw new Error("Invalid notebook format: missing cells array");
    }

    if (cellIndex < 0 || cellIndex >= notebook.cells.length) {
      throw new Error(`Cell index out of bounds: ${cellIndex}. Total cells: ${notebook.cells.length}`);
    }

    notebook.cells.splice(cellIndex, 1);

    await fs.writeFile(notebookPath, JSON.stringify(notebook, null, 2), 'utf8');

    return {
      success: true,
      message: `Cell at index ${cellIndex} deleted`,
    };
  } catch (error: any) {
    throw new Error(`Failed to delete cell: ${error.message}`);
  }
}
