import puppeteer from 'puppeteer';
import browser from 'puppeteer';
import page from 'puppeteer';

/**
 * Starts instance of headless chrome.
 * Returns the browser and page objects.
 * @typedef {object} PuppetInstance
 * @property {browser} browser - The puppeteer Browser Object
 * @property {page} page - The puppeteer Page object
 * @param {String} url - The URL to navigate to.
 * @returns {PuppetInstance} - The puppeteer intance
 */
export const startBrowser = async () => {
  console.log(`Launching Headless Chrome`);
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  return {browser, page};
};

/**
 * Navigates to the url and waits for initial selector.
 * @param {String} url - The URL to navigate to.
 * @param {page} page - The Puppeteer Page Object.
 * @returns - Void
 */
export const goToHomePage = async (url, page) => {
  console.log(`Making request to ${url}`);
  await page.goto(url);
  await page.setViewport({
    width: 1920,
    height: 1080,
  });
  await page.waitForSelector('.param-input');
};

/**
 * Fills in forms for endpoint that is being tested
 * @typedef {object} Page
 * @param {Page} page - The puppeteer page object
 * @param {String} endpoint - The endpoint to test     
 * @param {String} selector - the document selector to retreive contents of
 * @returns - Void
 */
export const fillInputs = async (page, endpoint) => {
  const idArr = getIdParams(endpoint);
  console.log(`Inserting Value into input field`);
  /* 
  *  evaluates the callback function in the context of the browser window. 
  *  gets the input elements associated with the endpoint which is
  *  being tested. 
  */
  await page.evaluate(async ({endpoint, idArr}) => {
    elemArr = [];
    idArr.forEach((id) => {
      let inputElem = document.getElementById(`${endpoint}-{${id}}`);
      elemArr.push(inputElem);
    });
    /**
     * sets input to random id.
     * simulates actual user input to trigger both
     * a React onChange event and allows the onChange event
     * handler to pick up a programatically set value
     * to validate and set state.
     * simply using element.value = 'new Value' does
     * not trigger an event nor expose the new value
     * to the event handler.
     */
    elemArr.forEach((element) => {
      let randId = Math.floor(Math.random() * Math.floor(1000) + 1);
      const inputValSetter = Object
        .getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      inputValSetter.call(element, randId);
      let event = new Event('change', {bubbles: true});
      triggerEvent = element.dispatchEvent(event);
    });
  }, {endpoint, idArr});
};

/**
 * Finds and clicks on the trigger
 * element to go the the endpoint page.
 * @param {Page} page - The puppeteer page object
 * @param {string} endpoint - The endpoint to test     
 * @returns {void} void
 */
export const goToEndpointPage = async (page, endpoint) => {
  await page.evaluate((endpoint) => {
    /**
     * split endpoint to create lookup array of different formats.
     * Used to determine which div contains the 
     * button to create click event on.
     */
    let endPointArr = endpoint.split(/[{}]/);
    let lookUpText;
    let lookUpArr;
    if (endPointArr[endPointArr.length - 1] === '') {
      endPointArr.pop();
    }
    // set values of lookup array
    if (endPointArr.length < 3){
      lookUpText = endPointArr[0];
      lookUpArr = [lookUpText]; 
    } else {
      lookUpText = endPointArr[0]+endPointArr[2];
      lookUpArr = [
      lookUpText.trim(),
      lookUpText.trim().substring(0, lookUpText.length - 1),
      lookUpText.trim() + '/'
      ];
    }
    let titles = document.querySelectorAll('.endpoint-title');
    titles.forEach((title) => {
      if (lookUpArr.includes(title.textContent.trim())) {
        title.parentElement.children[1].click();
      };
    });
  }, endpoint);
};

/**
 * Gets the innerText of the specified selector.
 * @param {Page} page - The puppeteer page object   
 * @param {String} contentSelector - the document selector to retreive contents of
 * @param {String} targetSelector - the document selector to detect re-render on
 * @returns {String} - the text content of HTML element
 */
export const getSelectorContent = async (page, contentSelector, targetSelector) => {
  console.log(`Getting Contents of ${contentSelector}`);
  await page.waitForSelector(targetSelector);
  //get the selector
  const targetElement = await page.$(targetSelector);
  const contentElement = await page.$(contentSelector);
   // evaluates callback function in browser window.
   // passes the retreived element from above as first arg.
  const elemContent = await targetElement.evaluate(async (targetElem, contentElem) => {
    console.log(targetElem);
    console.log(contentElem);
     // Returns Promise to await for the first page's re-render
     // then retreives the innerText of the element. This avoids
     // returning and undefined elemContent.
    return new Promise((resolve, reject) => {
      const body = document.body;
      /**
       * observes a DOM element for mutations from
       * Reacts first re-render after API call return.
       * This ensures we aren't getting loading screen
       * or initial state values.
       * @param {HTMLElement} mutationEl - The element to observe. 
       * @param {HTMLElement} targetEl - The element to get innerText from.
       */
      const waitForMutatedValue = (mutationEl, targetEl) => {
        let elInnerText;
        const observer = new MutationObserver((mutationsList, observer) => {
          if(targetEl) {
            elInnerText = targetEl.innerText;
          }
          resolve(elInnerText);
        });
        observer.observe(mutationEl, {subtree: true, childList: true});
      };
      waitForMutatedValue(targetElem, contentElem);
      setTimeout(() => {
        reject('Timeout');
      }, 30000);
    });
  }, contentElement);
  return {elemContent};
};

/**
 * splits and filters the endpoint string. Returns an array 
 * of the endpoints that need integers as a parameter.
 * @param {string} endpoint - the endpoint string
 * @returns {Array<String>} - An array with endpoint params that need an integer value
 */
const getIdParams = (endpoint) => {
  let epArr = endpoint.split(/[{}]/);
  epArr.pop();
  const idArr = epArr.filter((str) => {
    return !str.includes('/');
  });
  return idArr;
};