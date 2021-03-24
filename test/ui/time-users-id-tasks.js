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

        let universaldate = new Date(); //   capture current local date and time in universal time
        let stringDate = universaldate.getFullYear() + "_" + (universaldate.getMonth() + 1) + "_" + universaldate.getDate() + "-" + universaldate.getHours() + "-" + universaldate.getMinutes() + '-' + universaldate.getSeconds() + '-' + universaldate.getMilliseconds();

        await page.screenshot({ path: `../results/ui-test-results/users-id-tasks-id/ui_taskid_${stringDate}.png` });
        const screenshotPath = `../results/ui-test-results/capture-time/test-users-userid-task/ui_users_task_task_id_${stringDate}.png`;

        console.log(`Navigated to ${uiLocation}, taking screenshot and storing in ${screenshotPath}`);
            await page.screenshot({ path: screenshotPath});
            var endDate   = new Date();
        
        var seconds = (endDate.getTime() - startTime) / 1000;
        console.log(`Time it took to load ${seconds}`)
        totalSeconds = totalSeconds + seconds;
        startTime = new Date();
}
    console.log(`Average time to load ${(totalSeconds/40)}`)
    await browser.close();
})().catch(err => console.log(err)); 