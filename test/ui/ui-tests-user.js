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
    let [month, date, year]    = new Date().toLocaleDateString("en-US").split("/")
    let [hour, minute, second, period] = new Date().toLocaleTimeString("en-US").split(/:| /)

    if (String(month).length == 1) month = "0" + month;
    if (String(date).length == 1) date = "0" + date;
    
    if (period === "PM") hour = Number(hour) + 12;

    if (String(hour) == 1) hour = "0" + hour;
    if (String(minute).length == 1) minute = "0" + minute;
    if (String(second).length == 1) minute = "0" + second;

    todate = `${year}_${month}_${date}_${hour}-${minute}-${second}`;
    await page.screenshot({ path: `../results/ui-test-results/users/ui_users_${todate}.png`});

    await browser.close();
})(); 