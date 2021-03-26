const puppeteer = require('puppeteer')

var NUM_TIMES=40;
let totalSeconds = 0;
let loadtime=0;

(async() =>{
    var startDate = new Date();
    var startTime = startDate.getTime();
    const ENV_PAGE = "https://nscstrdevusw2thucommon.z5.web.core.windows.net/#/users/2/tasks/1";
    const browser = await puppeteer.launch()
    for(var i = 0; i< NUM_TIMES; i++){
        const webpage = await browser.newPage();
        console.log(`Opening Page. Heading for target page...`);
        await webpage.goto(ENV_PAGE)
        await webpage.setCacheEnabled(false)
            var endDate = new Date();
        loadtime = endDate.getTime-startTime;
        console.log(`Time to load page was: ${loadtime}`)
        await webpage.close();    
        }
        console.log(`The average time it took to load the page 40 times: ${totalSeconds/NUM_TIMES}`)
    })().catch(err => console.log(err));
    
    
    


