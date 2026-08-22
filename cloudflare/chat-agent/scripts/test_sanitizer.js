import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { JSDOM } from 'jsdom';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Initialize JSDOM environment
const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
global.window = dom.window;
global.document = dom.window.document;
global.DOMParser = dom.window.DOMParser;

// Extract sanitizeHTML function directly from src/index.ts to ensure 100% fidelity with production JS code
const indexPath = path.join(__dirname, '..', 'src', 'index.ts');
const indexSource = fs.readFileSync(indexPath, 'utf8');
const sanitizeMatch = indexSource.match(/function sanitizeHTML\(dirty\)\s*\{[\s\S]*?\n  \}/);

if (!sanitizeMatch) {
  console.error("❌ ERROR: Could not locate sanitizeHTML function in src/index.ts");
  process.exit(1);
}

// Evaluate the actual production sanitizeHTML function
const sanitizeHTML = new Function('dirty', `
  const DOMParser = global.DOMParser;
  const document = global.document;
  ${sanitizeMatch[0]}
  return sanitizeHTML(dirty);
`);

const FUZZ_PAYLOADS = [
  { id: "SZ-001", name: "Mixed-case javascript: URI scheme", input: '<a href="JaVaScRiPt:alert(1)">Click Me</a>', forbidden: ["javascript", "alert(1)"] },
  { id: "SZ-002", name: "HTML Entity encoded javascript: URI scheme", input: '<a href="java&#x73;cript:alert(1)">Click Me</a>', forbidden: ["java&#x73;cript", "alert(1)"] },
  { id: "SZ-003", name: "URL encoded javascript: URI scheme", input: '<a href="javascript%3Aalert(1)">Click Me</a>', forbidden: ["javascript%3a", "alert(1)"] },
  { id: "SZ-004", name: "Null byte padded URI scheme", input: '<a href="\x00javascript:alert(1)">Click Me</a>', forbidden: ["javascript", "alert(1)"] },
  { id: "SZ-005", name: "Data URI HTML payload", input: '<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">Click Me</a>', forbidden: ["data:text/html"] },
  { id: "SZ-006", name: "VBScript URI scheme", input: '<a href="vbscript:msgbox(1)">Click Me</a>', forbidden: ["vbscript:"] },
  { id: "SZ-007", name: "SVG vector injection with onload event handler", input: '<svg/onload=alert(1)>', forbidden: ["<svg", "onload="] },
  { id: "SZ-008", name: "MathML maction link vector injection", input: '<math><maction actiontype="statusline" xlink:href="javascript:alert(1)">Click</maction></math>', forbidden: ["<math", "javascript:"] },
  { id: "SZ-009", name: "Arbitrary inline style attribute stripping", input: '<span style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:999999;background:red;">Overlaid Text</span>', forbidden: ["style="] },
  { id: "SZ-010", name: "DOM clobbering name/id attribute injection", input: '<img id="config" name="config" src="x" onerror="alert(1)">', forbidden: ["onerror=", "<img"] }
];

function runSanitizerTests() {
  console.log("==========================================================");
  console.log("🧪 RUNNING PRODUCTION JS DOM ALLOW-LIST SANITIZER SUITE");
  console.log("==========================================================");

  let passed = 0;
  let failed = 0;
  const total = FUZZ_PAYLOADS.length;

  FUZZ_PAYLOADS.forEach(test => {
    const tid = test.id;
    const name = test.name;
    const sanitized = sanitizeHTML(test.input);

    const failedReasons = [];
    test.forbidden.forEach(f => {
      if (sanitized.toLowerCase().includes(f.toLowerCase())) {
        failedReasons.push(`Forbidden fragment '${f}' remained after sanitization.`);
      }
    });

    if (failedReasons.length > 0) {
      failed++;
      console.log(`❌ FAIL [${tid}]: ${name} -> ${failedReasons.join(', ')}`);
    } else {
      passed++;
      console.log(`✅ PASS [${tid}]: ${name}`);
    }
  });

  console.log("==========================================================");
  console.log(`📊 SUMMARY: Total: ${total} | Passed: ${passed} (${(passed/total*100).toFixed(1)}%) | Failed: ${failed}`);
  console.log("==========================================================");

  if (failed > 0) {
    process.exit(1);
  }
}

runSanitizerTests();
