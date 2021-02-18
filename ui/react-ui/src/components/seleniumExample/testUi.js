const {Builder, By, Key, Util} = require("selenium-webdriver");
async function example() {
    let driver = await new Builder().forBrowser("chrome").build();
    await driver.get("https://nate-temp-bucket.s3-us-west-2.amazonaws.com/report_users_user_id_tasks_task_id.json")     
}
example();
