import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const moduleRoot = decodeURIComponent(new URL("..", import.meta.url).pathname);
const payloadPath = "/tmp/neuroscience_questions_payload_final.json";
const outputPath = `${moduleRoot}/NEUROSCIENCE SYSTEM_Questions.xlsx`;
const previewPath = "/tmp/neuroscience_questions_preview.png";

const payload = JSON.parse(await fs.readFile(payloadPath, "utf8"));
if (payload.errors?.length) {
  throw new Error(`Payload is not clean: ${payload.errors.join("; ")}`);
}
if (payload.hardConflictCount) {
  throw new Error(`Payload has ${payload.hardConflictCount} hard duplicate conflicts`);
}

const headers = payload.headers;
const rows = payload.questions.map((question) => headers.map((header) => question[header] ?? null));
const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Questions");
sheet.showGridLines = false;
sheet.tabColor = "#17365D";

const lastRow = rows.length + 1;
const lastColumn = "AE";
sheet.getRange(`A1:${lastColumn}${lastRow}`).values = [headers, ...rows];
sheet.getRange(`A1:${lastColumn}1`).format = {
  fill: "#17365D",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
  wrapText: true,
  verticalAlignment: "center",
};
sheet.getRange(`A2:${lastColumn}${lastRow}`).format = {
  font: { name: "Arial", size: 10, color: "#111827" },
  wrapText: true,
  verticalAlignment: "top",
};
sheet.getRange(`A1:${lastColumn}${lastRow}`).format.borders = {
  preset: "inside",
  style: "hair",
  color: "#D9E2F3",
};
sheet.getRange(`A1:${lastColumn}1`).format.rowHeight = 34;
sheet.getRange(`A2:${lastColumn}${lastRow}`).format.rowHeight = 42;

const widths = {
  A: 6, B: 14, C: 58, D: 18, E: 18,
  F: 30, G: 30, H: 30, I: 30, J: 30, K: 30,
  L: 18, M: 18, N: 18, O: 18, P: 18,
  Q: 8, R: 22, S: 72, T: 26, U: 38, V: 9,
  W: 28, X: 24, Y: 18, Z: 18, AA: 20, AB: 10, AC: 34, AD: 18, AE: 22,
};
for (const [column, width] of Object.entries(widths)) {
  sheet.getRange(`${column}1:${column}${lastRow}`).format.columnWidth = width;
}
sheet.freezePanes.freezeRows(1);

workbook.recalculate();
const inspection = await workbook.inspect({
  kind: "sheet",
  include: "id,name",
  sheetId: sheet.id,
  range: "A1:AE5",
});
console.log(inspection.ndjson ?? inspection);

const preview = await workbook.render({
  sheetName: "Questions",
  range: "A1:AE8",
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
console.log(JSON.stringify({ outputPath, previewPath, rowCount: rows.length, columnCount: headers.length }));
