import { chromium } from "playwright";
import { existsSync } from "node:fs";
import { pathToFileURL } from "node:url";

const [inputPath, outputPath, chromePath] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  throw new Error("Usage: render_lesson.mjs INPUT_HTML OUTPUT_PNG [CHROME_PATH]");
}

const launchOptions = { headless: true };
if (chromePath && existsSync(chromePath)) {
  launchOptions.executablePath = chromePath;
}

const browser = await chromium.launch(launchOptions);
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto(pathToFileURL(inputPath).href, { waitUntil: "networkidle" });
  await page.screenshot({ path: outputPath, fullPage: true });
} finally {
  await browser.close();
}
