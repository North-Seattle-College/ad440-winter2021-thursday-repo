const puppeteer = require("puppeteer");

(async () => {
    const uiLocation = "http://localhost:3000/users/6/tasks";
    const browser = await puppeteer.launch();   
    var startDate = new Date();
    var totalSeconds = 0;     
    var startTime = startDate.getTime();

    for(var i=0; i<40; i++){
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
    console.log(`Average time to load ${(totalSeconds/40)}`)
    await browser.close();
})().catch(err => console.log(err)); 