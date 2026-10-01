/* Verify the actual offline presentation player and capture review images. */
const assert = require('node:assert/strict');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const sharp = require('sharp');
let browser;

(async () => {
  browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: 1280, height: 784 } });
  const errors = [];
  const requests = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => requests.push(request.url()));
  const deckURL = pathToFileURL(path.resolve('out/vibe-coding-workshop.html')).href;
  const state = () => page.evaluate(() => {
    const slide = document.querySelector('.slide.is-active');
    return {
      title: slide.dataset.title,
      slide: [...document.querySelectorAll('.slide')].indexOf(slide) + 1,
      steps: Number(slide.dataset.steps),
      step: Number(new URLSearchParams(location.hash.slice(1)).get('step')),
      visible: [...slide.querySelectorAll('.reveal.is-visible')].map(el => Number(el.dataset.step)),
    };
  });
  await page.goto(deckURL);
  await page.evaluate(() => document.fonts.ready);
  assert.equal(await page.locator('.slide').count(), 20);
  assert.equal((await state()).step, 0);
  await page.keyboard.press('Space');
  assert.equal((await state()).step, 1);
  assert.equal(await page.locator('.slide.is-active .reveal').first().evaluate(el => getComputedStyle(el).transitionDuration.split(',')[0].trim()), '0.35s');
  await page.waitForTimeout(400);
  assert.equal(await page.locator('.slide.is-active .reveal').first().evaluate(el => getComputedStyle(el).opacity), '1');
  await page.keyboard.press('ArrowRight');
  assert.equal((await state()).slide, 2);
  for (let step = 1; step <= 3; step++) {
    await page.keyboard.press('ArrowRight');
    const current = await state();
    assert.equal(current.step, step);
    assert(current.visible.every(value => value <= step));
  }
  await page.keyboard.press('ArrowLeft');
  assert.equal((await state()).step, 2);
  await page.reload();
  assert.equal((await state()).slide, 2);
  assert.equal((await state()).step, 2);
  await page.keyboard.press('n');
  assert(await page.locator('#notes').isVisible());
  assert.match(await page.locator('#notes').textContent(), /OpenAI Campus Ambassador/);
  await page.keyboard.press('Escape');
  assert(!(await page.locator('#notes').isVisible()));
  await page.keyboard.press('o');
  assert(await page.locator('#overview').isVisible());
  assert.equal(await page.locator('#overview button').count(), 20);
  await page.locator('#overview button').nth(6).click();
  assert.equal((await state()).slide, 7);
  assert(!(await page.locator('#overview').isVisible()));
  await page.locator('#show-all').click();
  assert.equal((await state()).step, 5);
  await page.locator('#next').click();
  assert.equal((await state()).slide, 8);

  await page.emulateMedia({ reducedMotion: 'reduce' });
  assert.equal(await page.locator('.slide.is-active .reveal').first().evaluate(el => getComputedStyle(el).transitionDuration), '0s');
  await page.keyboard.press('Home');
  assert.equal((await state()).slide, 1);
  await page.keyboard.press('End');
  assert.equal((await state()).slide, 20);
  assert.equal((await state()).step, 1);
  assert(await page.locator('#next').isDisabled());

  const overflow = [];
  for (let number = 1; number <= 20; number++) {
    await page.evaluate(n => { location.hash = `slide=${n}&step=99`; }, number);
    await page.waitForFunction(n => document.querySelector('.slide.is-active').getAttribute('aria-label').startsWith(`${n}. `), number);
    const current = await state();
    assert.equal(current.step, current.steps);
    assert(await page.locator('.slide.is-active').evaluate(el => !el.inert));
    const offslide = await page.locator('.slide.is-active').evaluate(slide => {
      const bounds = slide.getBoundingClientRect();
      return [...slide.querySelectorAll('.text-shape span')].flatMap(span => {
        const range = document.createRange();
        range.selectNodeContents(span);
        return [...range.getClientRects()].filter(rect => rect.right > bounds.right + 2 || rect.bottom > bounds.bottom + 2)
          .map(() => span.textContent);
      });
    });
    if (offslide.length) overflow.push({ slide: number, text: offslide });
    await page.screenshot({ path: `out/html-slide-${String(number).padStart(2, '0')}.png` });
  }
  assert.deepEqual(overflow, [], 'Slide text crosses the visible presentation boundary');
  assert(requests.every(url => !/^https?:/.test(url)), 'Presentation depends on an internet resource');
  assert.deepEqual(errors, []);
  const thumbnails = await Promise.all(Array.from({ length: 20 }, async (_, index) => ({
    input: await sharp(`out/html-slide-${String(index + 1).padStart(2, '0')}.png`).resize(512, 314).png().toBuffer(),
    left: 16 + (index % 3) * 528,
    top: 16 + Math.floor(index / 3) * 330,
  })));
  await sharp({ create: { width: 1600, height: 2330, channels: 3, background: '#dedbd1' } })
    .composite(thumbnails).png().toFile('out/html-overview.png');
  await page.setViewportSize({ width: 375, height: 812 });
  await page.waitForTimeout(100);
  const mobile = await page.evaluate(() => {
    const slide = document.querySelector('.slide.is-active').getBoundingClientRect();
    const controls = document.querySelector('#toolbar').getBoundingClientRect();
    return { left: slide.left, right: slide.right, bottom: slide.bottom, controlsTop: controls.top };
  });
  assert(mobile.left >= -1 && mobile.right <= 376 && mobile.bottom <= mobile.controlsTop + 1);
  await page.emulateMedia({ media: 'print' });
  assert.equal(await page.locator('.slide:visible').count(), 20);
  assert(await page.locator('.reveal').first().evaluate(el => getComputedStyle(el).opacity === '1'));
  console.log('PASS: 20 slides, reveals, reverse navigation, hash restore, overview, notes, reduced motion, offline assets, mobile fit and print visibility.');
  await browser.close();
})().catch(async error => { console.error(error); await browser?.close(); process.exitCode = 1; });
