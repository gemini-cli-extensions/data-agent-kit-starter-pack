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

export async function insertCell(
  notebookPath: string,
  cellType: "code" | "markdown",
  content: string,
  cellIndex?: number
) {
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
      (newCell as any).outputs = [];
      (newCell as any).execution_count = null;
    }

    if (cellIndex === undefined || cellIndex >= notebook.cells.length) {
      notebook.cells.push(newCell);
    } else if (cellIndex < 0) {
      notebook.cells.unshift(newCell);
    } else {
      notebook.cells.splice(cellIndex, 0, newCell);
    }

    await fs.writeFile(notebookPath, JSON.stringify(notebook, null, 2), 'utf8');

    return {
      success: true,
      message: `Cell inserted at index ${cellIndex !== undefined ? cellIndex : notebook.cells.length - 1}`,
    };
  } catch (error: any) {
    throw new Error(`Failed to insert cell: ${error.message}`);
  }
}
