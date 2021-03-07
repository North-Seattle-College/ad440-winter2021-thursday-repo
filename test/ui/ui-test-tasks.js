import puppeteer from 'puppeteer';
import browser from 'puppeteer';
import page from 'puppeteer';
//const puppeteer = require('puppeteer');

/**
 * starts instance of headless chrome
 * and returns the browser and page objects
 * @typedef {Object} PuppetInstance
 * @property {browser} browser - The puppeteer Browser Object
 * @property {Page} page - The puppeteer Page object
 * @return {PuppetInstance} - The puppeteer intance
 */
export const startBrowser = async () => {
  const browser = await puppeteer.launch({
    headless: false,
  });
  const page = await browser.newPage();
  return {browser, page};
};

/**
 * Navigates to passed in URL, Fills in form for endpoint 
 * and Gets contents of selector passed as arg
 * 
 * @param {string} url
 *         The Url to make request to
 * @param {Page} pg
 *        The puppeteer page object
 * @param {string} endpoint
 *        The endpoint to test     
 * @param {string} selector
 *        the document selector to retreive contents of
 * @return {}
 */
export const getSelectorContent = async (url, page, endpoint, selector) => {
  console.log(`Starting Headless Chrome`)
  console.log(`Making request to ${url}`)
  await page.goto(url)
  await page.setViewport({
    width: 1920,
    height: 1080,
  });
  await page.waitForSelector('.container');
  const idArr = getIdParams(endpoint);
  console.log(`Inserting Value into form`);

  /* 
  *  evaluates the callback function in the context of the browser window. 
  *  gets the input elements associated with the endpoint which is
  *  being tested. 
  */
  await page.evaluate(async ({endpoint, idArr}) => {
    setTimeout(() => {
    elemArr = [];
    idArr.forEach((id) => {
      let inputElem = document.getElementById(endpoint + '-' + id);
      elemArr.push(inputElem);
    });
    elemArr.forEach((element) => {
      let event = new Event('change');
      element.addEventListener('change', (e) => e.target.value = Math.floor(Math.random() * Math.floor(1000)))
      triggerEvent = element.dispatchEvent(event);
      //element.value = Math.floor(Math.random() * Math.floor(1000));
    });
  
    let titles = document.querySelectorAll('.endpoint-title');

    titles.forEach((title) => {
      if(endpoint.trim() === title.textContent.trim()) {
        title.click();
      }
    });

  }, 10000);

  }, {endpoint, idArr});

  console.log(`Getting Contents of ${selector}`);
  await page.waitForSelector(selector);
  const element = await page.$(selector);
  const elemContent = await element.evaluate(elem => elem.innerText);
  console.log(elemContent);
  return elemContent;
};

/**
 * splits and filters the endpoint string. Returns the
 * endpoints that need integers as a parameter.
 * 
 * @param {string} endpoint
 *         the endpoint string
 * @return {Array}
 *         An array with endpoints that need an integer value
 */
const getIdParams = (endpoint) => {
  let epArr = endpoint.split(/[{}]/);
  epArr.pop()
  const idArr = epArr.filter((str) => {
    return !str.includes('/');
  });
  return idArr;
};