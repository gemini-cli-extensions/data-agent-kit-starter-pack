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

import * as fs from 'fs/promises';

export async function listCells(notebookPath: string, maxLength: number = 100) {
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
      const needsTruncation = fullPreview.length > maxLength;
      const previewText = needsTruncation 
        ? fullPreview.substring(0, maxLength) + '... [truncated]' 
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
