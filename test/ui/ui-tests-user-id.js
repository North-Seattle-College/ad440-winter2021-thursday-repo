const puppeteer = require('puppeteer');
const screenshotPath = `../results/ui-test-results/users-id/ui-user-user-id.png`;

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://nscstrdevusw2thucommon.z5.web.core.windows.net/users');
  await page.screenshot({ path: screenshotPath});
  console.log(`Screenshot was successful.`);
  await browser.close();
})().catch(err => console.log(err)); 

