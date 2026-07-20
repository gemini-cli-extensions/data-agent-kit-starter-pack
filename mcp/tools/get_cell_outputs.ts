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

export type McpContentPayload = Array<
  {type: 'text'; text: string} | {type: 'image'; data: string; mimeType: string}
>;

export async function getCellOutputs(notebookPath: string, cellIndex: number) {
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
    
    if (cell.cell_type !== 'code') {
      throw new Error(`Cell at index ${cellIndex} is not a code cell; it has no execution outputs.`);
    }

    const prefixText = `Outputs for cell ${cellIndex} in ${notebookPath}:`;
    const contentPayload = parseCellOutputs(cell, cellIndex, notebookPath, prefixText);

    return contentPayload;
  } catch (error: any) {
    throw new Error(`Failed to get cell outputs: ${error.message}`);
  }
}

function parseCellOutputs(
  cell: any,
  index: number,
  path: string,
  prefixText: string,
): McpContentPayload {
  const contentPayload: McpContentPayload = [];
  let textBuffer = `${prefixText}\n`;
  
  const executionCount = cell.execution_count ?? null;
  textBuffer += `Execution Count: ${executionCount ?? 'N/A'}\n`;

  if (cell.outputs && cell.outputs.length > 0) {
    textBuffer += `\nOutputs:\n`;
    for (const o of cell.outputs) {
      const outputType = o.output_type;
      
      if (outputType === 'stream') {
        const text = Array.isArray(o.text) ? o.text.join('') : o.text || '';
        const textPreview = text.length > 3000 ? `${text.slice(0, 3000)}\n...[Truncated]` : text;
        textBuffer += `\n[stream:${o.name}]\n${textPreview}\n`;
      } else if (outputType === 'execute_result' || outputType === 'display_data') {
        for (const mime in o.data) {
          const data = o.data[mime];
          const textData = Array.isArray(data) ? data.join('') : data || '';
          
          if (mime.startsWith('text/') || mime.includes('json')) {
            const textPreview = textData.length > 3000 ? `${textData.slice(0, 3000)}\n...[Truncated]` : textData;
            textBuffer += `\n[${mime}]\n${textPreview}\n`;
          } else if (mime === 'image/png' || mime === 'image/jpeg') {
            if (textBuffer.trim().length > 0) {
              contentPayload.push({type: 'text', text: textBuffer});
              textBuffer = '';
            }
            
            if (typeof textData !== 'string') {
              textBuffer += `\n[${mime}]\n(Warning: Image data is not a string. Type: ${typeof textData})\n`;
            } else {
              contentPayload.push({
                type: 'image',
                data: textData,
                mimeType: mime,
              });
            }
          }
        }
      } else if (outputType === 'error') {
        const traceback = Array.isArray(o.traceback) ? o.traceback.join('\n') : o.traceback || '';
        textBuffer += `\n[error]\n${traceback}\n`;
      }
    }
  } else {
    textBuffer += `\n(No output generated)\n`;
  }

  if (textBuffer.length > 0) {
    contentPayload.push({type: 'text', text: textBuffer});
  }

  return contentPayload;
}
