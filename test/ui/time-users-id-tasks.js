const puppeteer = require("puppeteer");
var captureTime = 40;
(async () => {
    const uiLocation = "https://nscstrdevusw2thucommon.z5.web.core.windows.net/#/users/6/tasks ";
    const browser = await puppeteer.launch();   
    var startDate = new Date();
    var totalSeconds = 0;     
    var startTime = startDate.getTime();

    for(var i=0; i<captureTime; i++){
        const page = await browser.newPage();
        console.log(`Page opened, going to ${uiLocation}`);

        await page.goto(uiLocation)

        console.log(`Navigated to ${uiLocation}, taking screenshot`);
            await page.screenshot();
            var endDate   = new Date();
        
        var seconds = (endDate.getTime() - startTime) / 1000;
        console.log(`Time it took to load ${seconds}`)
        totalSeconds = totalSeconds + seconds;
        startTime = new Date();
}
    console.log(`Average time to load ${(totalSeconds/captureTime)}`)
    await browser.close();
})().catch(err => console.log(err)); 