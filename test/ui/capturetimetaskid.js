const puppeteer = require('puppeteer')

var NUM_TIMES=40;
const ENV_PAGE = `https://nscstrdevusw2thucommon.z5.web.core.windows.net/#/users/2/tasks/1`;
let totalSeconds = 0;
let loadtime=0;

const  pageMetrics = async() =>{
    const browser = await puppeteer.launch({headless: false})
    const webpage = await browser.newPage()
    await webpage.setCacheEnabled([False])
    ENV_PAGE = os.environ['target_website']
    await webpage.goto(ENV_PAGE)
    const pagePerf = await page.evaluate(_=>{
            loadtime =PerformanceNavigationTiming.loadEventEnd - PerformanceNavigationTiming.loadEventStart
            return loadtime
       
    })
    totalSeconds+=pagePerf.loadtime
    console.log(`Page Load took: ${pagePerf.loadtime}ms`)
    await webpage.close()
}

for(var i = 0; i <NUM_TIMES; i++){
    pageMetrics();

}
console.log(`The average time it took to load the page 40 times: ${totalSeconds/NUM_TIMES}`)