import fs from "node:fs";
import process from "node:process";
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";
import axe from "axe-core";

const WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"];

function redact(value) {
  if (typeof value === "string") {
    return value.replace(/([?&](?:verifier|access_token|token)=)[^&"'\s>]+/gi, "$1REDACTED");
  }
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, redact(item)]));
  }
  return value;
}

async function main() {
  const [inputPath, outputPath] = process.argv.slice(2);
  if (!inputPath || !outputPath) throw new Error("usage: node axe_runner.mjs INPUT OUTPUT");
  const input = JSON.parse(fs.readFileSync(inputPath, "utf8"));
  const launchOptions = { headless: true };
  if (input.chromePath && fs.existsSync(input.chromePath)) launchOptions.executablePath = input.chromePath;
  const browser = await chromium.launch(launchOptions);
  const browserVersion = browser.version();
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const pages = [];
  try {
    for (const item of input.pages) {
      const page = await context.newPage();
      const record = { slug: item.slug, error: null, axe: null };
      try {
        await page.route("**/*", async (route) => {
          const type = route.request().resourceType();
          if (["image", "media", "font", "script"].includes(type)) await route.abort();
          else await route.continue();
        });
        await page.setContent(item.document, { waitUntil: "domcontentloaded", timeout: 30000 });
        record.axe = redact(await new AxeBuilder({ page })
          .include("#canvas-page")
          .withTags(WCAG_TAGS)
          .analyze());
      } catch (error) {
        record.error = `${error.name}: ${error.message}`;
      } finally {
        await page.close();
      }
      pages.push(record);
    }
  } finally {
    await context.close();
    await browser.close();
  }
  const artifact = {
    schemaVersion: 1,
    scope: "Canvas Page body content",
    tags: WCAG_TAGS,
    tool: { name: "@axe-core/playwright", axeCoreVersion: axe.version },
    browser: { name: "chromium", version: browserVersion },
    pages,
  };
  fs.writeFileSync(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.stack ?? error}\n`);
  process.exitCode = 1;
});
