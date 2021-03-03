const puppeteer = require("puppeteer");

(async () => {
    const uiLocation = "https://nscstrdevusw2thucommon.z5.web.core.windows.net/users";
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    console.log(`Page opened, going to ${uiLocation}`);
    await page.goto(uiLocation)

    const dateOptions = { 
        timeZone: "America/Los_Angeles",
        month: '2-digit',
        day: '2-digit',
        hour12: false,
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit',
        year: 'numeric'
    };
    let [month, date, year]    = new Date().toLocaleDateString("en-US", dateOptions).split(",")[0].split("/");
    let [_, hour, minute, second] = new Date().toLocaleTimeString("en-US", dateOptions).split(/:| /);

    const todate = `${year}_${month}_${date}_${hour}-${minute}-${second}`;
    const screenshotPath = `../results/ui-test-results/users/ui_users_${todate}.png`;

    console.log(`Navigated to ${uiLocation}, taking screenshot and storing in ${screenshotPath}`);
    await page.screenshot({ path: screenshotPath});

    await browser.close();
})().catch(err => console.log(err)); 