#!/usr/bin/env node
/**
 * html_to_png.js — 把一张「解释型配图」HTML 渲染成高清 PNG。
 *
 * 用 Playwright/Chromium 打开本地 HTML，等字体与网络空闲后，
 * 只截取 `.illustration` 元素（外层卡片），得到中文清晰、数字精确、
 * 像素级排版的 PNG。这是 illustrate 配图框架的「渲染层主力」。
 *
 * 用法:
 *   node html_to_png.js <in.html> <out.png> [--width 1100] [--scale 2] [--selector .illustration]
 *
 * 退出码:
 *   0 — 成功，PNG 已写入
 *   2 — 浏览器不可用（未装 Playwright / Chromium）→ 调用方可降级
 *   1 — 其它硬失败
 *
 * 依赖: Node + playwright + Chromium
 *   首次在 CI: `npx playwright install --with-deps chromium`
 *   中文需系统装有 CJK 字体（如 fonts-wqy-zenhei / fonts-noto-cjk）
 */
"use strict";

const path = require("path");
const { pathToFileURL } = require("url");

function parseArgs(argv) {
  const pos = [];
  const opt = { width: 1100, scale: 2, selector: ".illustration" };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--width") opt.width = parseInt(argv[++i], 10);
    else if (a === "--scale") opt.scale = parseFloat(argv[++i]);
    else if (a === "--selector") opt.selector = argv[++i];
    else pos.push(a);
  }
  return { pos, opt };
}

async function main() {
  const { pos, opt } = parseArgs(process.argv.slice(2));
  if (pos.length < 2) {
    console.error("用法: node html_to_png.js <in.html> <out.png> [--width N] [--scale N] [--selector SEL]");
    process.exit(1);
  }
  const inHtml = path.resolve(pos[0]);
  const outPng = path.resolve(pos[1]);

  let chromium;
  try {
    ({ chromium } = require("playwright"));
  } catch (e) {
    console.error("Playwright 未安装，无法 HTML→PNG（可降级）: " + e.message);
    process.exit(2);
  }

  let browser;
  try {
    browser = await chromium.launch({ args: ["--no-sandbox", "--disable-dev-shm-usage"] });
  } catch (e) {
    console.error("Chromium 启动失败（可能未 `playwright install chromium`，可降级）: " + e.message);
    process.exit(2);
  }

  try {
    const page = await browser.newPage({
      deviceScaleFactor: opt.scale,
      viewport: { width: opt.width + 120, height: 800 },
    });
    await page.goto(pathToFileURL(inHtml).href, { waitUntil: "networkidle", timeout: 30000 });
    // 等字体就绪，避免截到 fallback 字体或方块（ECharts 也在 fonts.ready 后才绘制）
    await page.evaluate(() => (document.fonts ? document.fonts.ready : Promise.resolve()));
    await page.waitForTimeout(400);

    const el = await page.$(opt.selector);
    const target = el || page;
    await target.screenshot({ path: outPng, omitBackground: false });
    console.error(`OK [html→png]: ${outPng}`);
    await browser.close();
    process.exit(0);
  } catch (e) {
    console.error("渲染失败: " + e.message);
    try { await browser.close(); } catch (_) {}
    process.exit(1);
  }
}

main();
