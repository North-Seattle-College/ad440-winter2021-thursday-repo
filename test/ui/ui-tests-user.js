const puppeteer = require("puppeteer");

(async () => {
    const uiLocation = "https://nscstrdevusw2thucommon.z5.web.core.windows.net/";
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    console.log(`Page opened, going to ${uiLocation}`);
    await page.goto(uiLocation)

    const [div] = await page.$x("//div[contains(., '/users')]");
    await div.click();
    // const [response] = await Promise.all([
    //     page.waitForNavigation(),
    //     div.click(),
    // ]);

    await page.screenshot({ path: "../results/ui-test-results/ui-test-users-page-screenshot.png"});

    await browser.close();
})(); 