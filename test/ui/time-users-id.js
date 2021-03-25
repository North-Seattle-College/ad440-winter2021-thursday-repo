const mkdirp = require('mkdirp');
const puppeteer = require('puppeteer');

(async () => {
    const url = "https://nscstrdevusw2thucommon.z5.web.core.windows.net/users/2";
    //const url = "https://nsc-thursday-react-app.azureedge.net/users/2";
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setCacheEnabled(false)
    await page.goto(url);
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

    // create folder
    mkdirp(newDirPath).then(made =>
        console.log(`Made a directory for screenshots: ${made}`))
        .catch(err => console.log(`Unable to make directory: ${err}`))

    // create array of times
    const timeArray = [];
    let totalSeconds = 0.0;

    var i;
    for (i = 0; i < 40; i++) {
        // start timer
        let startTime = new Date().getTime();

        await page.goto(url);

        // end timer
        let endDate = new Date();
        let endTime = endDate.getTime();

        // save time to array
        let seconds = (endTime - startTime)/1000;
        totalSeconds += seconds;
        timeArray[i] = seconds;

        // create path to save screenshot
        let [month, date, year] = endDate.toLocaleDateString("en-US", dateOptions).split(",")[0].split("/");
        let [_, hour, minute, second] = new Date().toLocaleTimeString("en-US", dateOptions).split(/:| /);
    
        const todate = `${year}_${month}_${date}_${hour}-${minute}-${second}`;
        const screenshotPath = `${newDirPath}/time_users_id_${todate}.png`;

        console.log(`Screenshot # ${i} Successful! Time: ${seconds}`);
        await page.screenshot({ path: screenshotPath});
    }

    console.log(`Total time: ${totalSeconds} seconds`);
    avgSeconds = totalSeconds/40;
    console.log(`Average time: ${avgSeconds} seconds`);

  await browser.close();
  
})().catch(err => console.log(err));