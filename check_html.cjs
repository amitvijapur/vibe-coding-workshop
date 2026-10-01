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
      hash: location.hash,
    };
  });
  await page.goto(deckURL);
  await page.evaluate(() => document.fonts.ready);
  assert.equal(await page.locator('.slide').count(), 19);
  assert.equal((await state()).slide, 1);
  assert.equal(await page.locator('.reveal, [data-step], [data-steps]').count(), 0);
  assert.equal(await page.locator('#show-all, #reveal-count').count(), 0);
  assert.equal(await page.locator('.slide.is-active').evaluate(el => getComputedStyle(el).animationDuration), '0.35s');
  assert.equal(await page.locator('.slide.is-active .heading').evaluate(el => getComputedStyle(el).animationName), 'none');
  await page.waitForTimeout(400);
  assert.equal(await page.locator('.slide.is-active').evaluate(el => getComputedStyle(el).opacity), '1');
  await page.keyboard.press('Space');
  assert.equal((await state()).slide, 2);
  // Navigation responds immediately while the whole-slide fade is running.
  await page.keyboard.press('ArrowRight');
  assert.equal((await state()).slide, 3);
  await page.locator('#canvas').click({ position: { x: 1100, y: 650 } });
  assert.equal((await state()).slide, 4);
  await page.keyboard.press('ArrowLeft');
  assert.equal((await state()).slide, 3);
  await page.keyboard.press('Backspace');
  assert.equal((await state()).slide, 2);
  const logos = page.locator('.slide.is-active [aria-label="Durham crest"], .slide.is-active [aria-label="OpenAI logo"], .slide.is-active [aria-label="DragonFly logo"]');
  assert.equal(await logos.count(), 5);
  const heights = await logos.evaluateAll(elements => elements.map(element => element.style.height));
  assert.equal(new Set(heights).size, 1, 'Host logo heights should be consistent');
  assert.equal(await page.locator('.slide.is-active [aria-label="Durham crest"]').count(), 2);
  await page.keyboard.press('PageDown');
  assert.equal((await state()).slide, 3);
  await page.keyboard.press('PageUp');
  assert.equal((await state()).slide, 2);
  await page.reload();
  assert.equal((await state()).slide, 2);
  assert.equal((await state()).hash, '#slide=2');
  await page.keyboard.press('n');
  assert(await page.locator('#notes').isVisible());
  assert.match(await page.locator('#notes').textContent(), /OpenAI Campus Ambassador/);
  await page.keyboard.press('Escape');
  assert(!(await page.locator('#notes').isVisible()));
  await page.keyboard.press('o');
  assert(await page.locator('#overview').isVisible());
  assert.equal(await page.locator('#overview button').count(), 19);
  await page.locator('#overview button').nth(6).click();
  assert.equal((await state()).slide, 7);
  assert(!(await page.locator('#overview').isVisible()));
  await page.locator('#next').click();
  assert.equal((await state()).slide, 8);
  await page.evaluate(() => { location.hash = 'slide=7&step=99'; });
  await page.waitForFunction(() => location.hash === '#slide=7');
  assert.equal((await state()).slide, 7);

  await page.emulateMedia({ reducedMotion: 'reduce' });
  assert.equal(await page.locator('.slide.is-active').evaluate(el => getComputedStyle(el).animationName), 'none');
  await page.keyboard.press('Home');
  assert.equal((await state()).slide, 1);
  await page.keyboard.press('End');
  assert.equal((await state()).slide, 19);
  assert(await page.locator('#next').isDisabled());
  assert.match(await page.locator('.slide.is-active').textContent(), /Thank you/i);
  assert(await page.locator('.slide.is-active a[href="https://github.com/amitvijapur/vibe-coding-workshop"]').count() > 0);
  await page.evaluate(() => { location.hash = 'slide=12'; });
  await page.waitForFunction(() => document.querySelector('.slide.is-active').dataset.title === 'Check the result');
  const checkText = await page.locator('.slide.is-active').textContent();
  assert.match(checkText, /rent|price|budget/i);
  assert.match(checkText, /area/i);
  assert.match(checkText, /shortlist/i);
  assert.match(checkText, /flatmate/i);
  assert.match(checkText, /two|2/i);
  assert.match(checkText, /390\s*×\s*844/);
  await page.evaluate(() => { location.hash = 'slide=9'; });
  await page.waitForFunction(() => document.querySelector('.slide.is-active').dataset.title.includes('How to iterate'));
  const frameworkText = await page.locator('.slide.is-active').textContent();
  assert.match(frameworkText, /Recheck/);
  assert.match(frameworkText, /What happened/);
  await page.keyboard.press('ArrowRight');
  assert.equal((await state()).title, 'Feedback and iteration');
  assert.match(await page.locator('.slide.is-active').textContent(), /weekly budget/);

  const overflow = [];
  for (let number = 1; number <= 19; number++) {
    await page.evaluate(n => { location.hash = `slide=${n}`; }, number);
    await page.waitForFunction(n => document.querySelector('.slide.is-active').getAttribute('aria-label').startsWith(`${n}. `), number);
    assert(await page.locator('.slide.is-active').evaluate(el => !el.inert));
    assert(await page.locator('.slide.is-active').evaluate(slide => [...slide.querySelectorAll('.shape')].every(shape => {
      const style = getComputedStyle(shape);
      return style.visibility !== 'hidden' && style.display !== 'none' && style.opacity === '1';
    })), `Slide ${number} contains initially hidden content`);
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
  const thumbnails = await Promise.all(Array.from({ length: 19 }, async (_, index) => ({
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
  assert.equal(await page.locator('.slide:visible').count(), 19);
  assert(await page.locator('.slide').first().evaluate(el => getComputedStyle(el).opacity === '1'));
  console.log('PASS: 19 slides, one automatic fade per slide, direct keyboard/click navigation, reverse navigation, old/new hash restore, overview, notes, demo checks, GitHub link, reduced motion, offline assets, mobile fit and print visibility.');
  await browser.close();
})().catch(async error => { console.error(error); await browser?.close(); process.exitCode = 1; });
