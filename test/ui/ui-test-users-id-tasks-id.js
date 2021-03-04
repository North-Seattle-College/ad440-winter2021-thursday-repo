const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch(); //promise to launch puppeteer
  const page = await browser.newPage(); //promise to open a browser
  await page.goto("https://nscstrdevusw2thucommon.z5.web.core.windows.net/users/1/tasks/1"); //promise to go to the specified page
  

  let unversaldate = new Date(); //   capture current local date and time in universal time
  let stringDate = universalldate.getFullYear() + "-" + (universaldate.getMonth() + 1) + "-" + universalldate.getDate() + "-" + universalldate.getHours() + ":" + universalldate.getMinutes() + ':' + universalldate.getSeconds();

  await page.screenshot({ path: `../results/ui-test-results/users-id-tasks-id/ui_taskid_${stringDate}.png` });

  await browser.close();

})().catch(err => console.log(err));