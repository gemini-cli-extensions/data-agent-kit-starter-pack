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

export async function getNotebookInfo(notebookPath: string) {
  try {
    const data = await fs.readFile(notebookPath, 'utf8');
    const notebook = JSON.parse(data);
    
    if (!notebook.cells || !Array.isArray(notebook.cells)) {
      throw new Error("Invalid notebook format: missing cells array");
    }

    const totalCells = notebook.cells.length;
    let codeCells = 0;
    let markdownCells = 0;

    notebook.cells.forEach((cell: any) => {
      if (cell.cell_type === 'code') codeCells++;
      if (cell.cell_type === 'markdown') markdownCells++;
    });

    return {
      totalCells,
      cellTypeSummary: {
        code: codeCells,
        markdown: markdownCells,
      },
      metadata: notebook.metadata || {},
    };
  } catch (error: any) {
    throw new Error(`Failed to get notebook info: ${error.message}`);
  }
}
