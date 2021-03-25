const puppeteer = require('puppeteer')

NUM_TIMES=40
totalSeconds = 0
loadtime=0

const  pageMetrics = async() =>{
    const browser = await puppeteer.launch({headless: false})
    const webpage = await browser.newPage()
    ENV_PAGE = os.environ['target_website']
    await webpage.goto(ENV_PAGE)
    const pagePerf = await page.evaluate(_=>{
        const{loadEventEnd, navigationStart}=PerformanceTiming
        return({loadtime=loadEventEnd-navigationStart
        })
        
    })
    totalSeconds+=pagePerf.loadtime
    console.log(`Page Load took: ${pagePerf.loadtime}ms`)
    await webpage.close()
}

for(var i = 0; i <NUM_TIMES; i++){
    pageMetrics()

}
console.log(`The average time it took to load the page 40 times: ${totalSeconds/40}`)