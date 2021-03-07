import {startBrowser, goToHomePage, fillInputs, goToEndpointPage, getSelectorContent} from './ui-test-tasks.js';
import puppeteer from 'puppeteer';

const baseUrl = 'https://nscstrdevusw2thucommon.z5.web.core.windows.net';
const endPoints = new Map();
//endPoints.set('users', '/users');
endPoints.set('userId', '/users/{userId}');
endPoints.set('tasks', '/users/{userId}/tasks');
endPoints.set('taskId', '/users/{userId}/tasks/{taskId}');



/**
 * The Main UI test runner.
 * @param {url} - The URL to navigate to.
 * @param {Iterable} - An iterable of strings representing endpoints.
 * @param {}
 * @return {PuppetInstance} - The puppeteer intance
 */
const runUiTest = async (url, endpoints, selector) => {
  let {browser, page} = await startBrowser();
  let screenshotDir = `../results/ui-test-results/{}${new Date(Date.now()).toISOString()}.png`
  for (let endpoint of endpoints.values()) {
    await goToHomePage(url, page);
    await fillInputs(page, endpoint);
    await goToEndpointPage(page, endpoint);
    let selectorContent = await getSelectorContent(page, selector);
    console.log(`Text Value of header: ${selectorContent}`);
    let screenshotDir = `../results/ui-test-results/${endpoint.replace(/\//g, '-')}-${new Date(Date.now()).toISOString()}.png`
    await page.screenshot({path: screenshotDir});
  };
  await browser.close();
};

runUiTest(baseUrl, endPoints, 'h1').catch(error => console.error(error));