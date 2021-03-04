const puppeteer = require("puppeteer");

(async () => {
    const uiUrl = "https://nscstrdevusw2thucommon.z5.web.core.windows.net/users/1";
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    console.log(`Navigating to ${uiUrl}`);
    await page.goto(uiUrl)

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
    const screenshotPath = `../results/ui-test-results/users-id/ui_users_id_${todate}.png`;

    console.log(`Screenshot Successful!`);
    await page.screenshot({ path: screenshotPath});

    await browser.close();
})().catch(err => console.log(err)); 