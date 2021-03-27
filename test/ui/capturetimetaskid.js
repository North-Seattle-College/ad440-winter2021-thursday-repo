const puppeteer = require('puppeteer')

var NUM_TIMES=40;

(async() =>{
    let startDate = new Date();
    let startTime = startDate.getTime();
    let totalSeconds = 0;
    //var totalSeconds = 0;
    const ENV_PAGE = "https://nscstrdevusw2thucommon.z5.web.core.windows.net/#/users/2/tasks/1";
    const browser = await puppeteer.launch({headless:false})
    for(var i = 0; i< NUM_TIMES; i++){
        const webpage = await browser.newPage();
        console.log(`Opening Page. Heading for target page...`);
        await webpage.goto(ENV_PAGE)
        await webpage.setCacheEnabled(false)
            var endDate = new Date();
        var loadtime = endDate.getTime()-startTime;
        console.log(`Time to load page was: ${loadtime}ms`)
        totalSeconds = totalSeconds + loadtime
        //Resets the startTime for next page loading
        startTime = new Date()
        await webpage.close();    
        }
        console.log(`The average time it took to load the page 40 times: ${(totalSeconds/NUM_TIMES)}`)
    })().catch(err => console.log(err));
    
    
    


