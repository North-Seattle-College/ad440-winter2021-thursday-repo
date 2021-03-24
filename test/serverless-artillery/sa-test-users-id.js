const mkdirp = require('mkdirp');
const puppeteer = require('puppeteer');

(async () => {
    const url = "https://nscstrdevusw2thucommon.z5.web.core.windows.net/users/4";
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    console.log(`Navigating to ${url}`);

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
    let [month, date, year] = new Date().toLocaleDateString("en-US", dateOptions).split(",")[0].split("/");
    let [_, hour, minute, second] = new Date().toLocaleTimeString("en-US", dateOptions).split(/:| /);
    
    const todate = `${year}_${month}_${date}_${hour}-${minute}-${second}`;

    const newDirPath = `../results/ui-test-results/users-id/group-${todate}`

    // create folder?
    mkdirp(newDirPath, function(err) { 

        // path exists unless there was an error
        console.log("failed to create folder for snapshots")
    
    });

    // create timer?
    // create array of times
    var i;
    for (i = 0; i < 40; i++) {
        // start timer
        await page.goto(url);
        // end timer
        // save time to array

        // create path to save screenshot
        let [month, date, year] = new Date().toLocaleDateString("en-US", dateOptions).split(",")[0].split("/");
        let [_, hour, minute, second] = new Date().toLocaleTimeString("en-US", dateOptions).split(/:| /);
    
        const todate = `${year}_${month}_${date}_${hour}-${minute}-${second}`;
        const screenshotPath = `${newDirPath}/sa_users_id_${todate}.png`;

        console.log(`Screenshot Successful!`);
        await page.screenshot({ path: screenshotPath});
    }
  await browser.close();
})();