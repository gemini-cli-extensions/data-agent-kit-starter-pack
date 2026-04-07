import * as fs from 'fs/promises';

export async function listCells(notebookPath: string) {
  try {
    const data = await fs.readFile(notebookPath, 'utf8');
    const notebook = JSON.parse(data);
    
    if (!notebook.cells || !Array.isArray(notebook.cells)) {
      throw new Error("Invalid notebook format: missing cells array");
    }

    const cells = notebook.cells.map((cell: any, index: number) => {
      const source = Array.isArray(cell.source) ? cell.source.join('') : cell.source || '';
      const preview = source.split('\n')[0] || '';
      const fullPreview = preview;
      const needsTruncation = fullPreview.length > 100;
      const previewText = needsTruncation 
        ? fullPreview.substring(0, 100) + '... [truncated]' 
        : fullPreview;

      return {
        index,
        type: cell.cell_type,
        preview: previewText,
      };
    });

    return {
      cells,
    };
  } catch (error: any) {
    throw new Error(`Failed to list cells: ${error.message}`);
  }
}
