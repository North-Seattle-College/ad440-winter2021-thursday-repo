/**
 * Loads users/ page 40 times (with caching on) capturing a screenshot and load time for each.
 */

 const puppeteer = require("puppeteer");
 const testCount = 40;
 const url = "https://nsc-thursday-react-app.azureedge.net/users";

 (async () => {
  const browser = await puppeteer.launch();

  const page = await browser.newPage();
  page.setCacheEnabled([true]);

  for (let i = 0; i < testCount; ++i){
    await page.goto(url);
    const usersMetrics = await page.metrics();
    const testDate = usersMetrics.Timestamp
    const screenshotPath = `../results/ui-test-results/users-load40_cache_on_${testDate}.png`;
    const browserTimer = usersMetrics.TaskDuration
    console.log(
      `${url}-  
      Load time test: #${i}, 
      Time to load page: ${browserTimer}, 
      Screenshot will be stored as: ${screenshotPath}`);
    await page.screenshot({ path: screenshotPath});
  }  

  await browser.close();
})().catch(err => console.log(err)); 