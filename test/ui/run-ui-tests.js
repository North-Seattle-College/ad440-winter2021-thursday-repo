import {startBrowser, goToHomePage, fillInputs, goToEndpointPage, getSelectorContent} from './ui-test-tasks.js';
import puppeteer from 'puppeteer';
import * as fs from 'fs';

/**
 * Main UI test runner and logger.
 * @module ui/run-ui-tests
 * 
 */


const baseUrl = 'https://nscstrdevusw2thucommon.z5.web.core.windows.net';
const endPoints = new Map();
endPoints.set('users', '/users');
endPoints.set('userId', '/users/{userId}');
endPoints.set('tasks', '/users/{userId}/tasks');
endPoints.set('taskId', '/users/{userId}/tasks/{taskId}');

const selectors = ['h1', '.App']



/**
 * The Main UI test runner.
 * @param {String} url - The URL to navigate to.
 * @param {Iterable<String>} endpoints - An iterable of strings representing endpoints.
 * @param {Array<String>} selectors - an array of selectors.
 * @param {Number} numRuns - Number of times to run the test. One run equal to one iteration through all endpoints.
 * @returns {PuppetInstance} - The puppeteer intance.
 */
const runUiTest = async (url, endpoints, selectors, resultDir, numRuns=10) => {
  const errorArr = ['404', '400', '500', '401', 'Failed To Render'];
  // convert Map to Object
  const epObj = Array.from(endpoints).reduce((obj, [key,val]) => {
    obj[key] = val;
    return obj;
  },{});
  const resultsObj = {}
  // copy keys into resultsObj for perfLog['results']
  Object.keys(epObj).forEach((key) => {
    resultsObj[key] = [];
  });
  //create key for home page metrics
  resultsObj['home'] = [];
  // the main log object to be recorded.
  const perfLog = {
    'summary': {
      url,
      'endpoints': Object.values(epObj),
      'totalTime': null,
      'avgRenderTime': null,
      'timeUnit': 'ms',
      'runsPerPage': numRuns,
      'totalTests': numRuns * endpoints.size + numRuns,
      'errorRatio': null,
      'errors': [],
    },
    'results': resultsObj,
  };
  // start tests
  let {browser, page} = await startBrowser();
  // run n amount of times equal to numRuns param
  let counter = 0;
  let epResult = {};
  let homeDetails = {};
  let runDetails = {};
  let times = [];
  while (counter <= numRuns) {
    let [homeTime, homeContent] = await timeRenderPerf(goToHomePage, [url, page]);
    let homeScrShot = dateifyFileName(resultDir, 'home', 'png');
    for (let [epKey, endpoint] of endpoints) {
      await page.screenshot({path: homeScrShot});
      await fillInputs(page, endpoint);
      await goToEndpointPage(page, endpoint);
      console.log(`Running UI Performance Test for: ${endpoint}`)
      let [timeElapsed, selectorContent] = await timeRenderPerf(getSelectorContent, [page, ...selectors]);
      console.log(`${endpoint} test complete`)
      let screenshotDir = dateifyFileName(resultDir, endpoint, 'png');
      await page.screenshot({path: screenshotDir});
      await goToHomePage(url, page);
      // record endpoint metrics
      runDetails = {
        endpoint,
        'text': selectorContent ? selectorContent.elemContent : 'Failed To Render',
        timeElapsed,
        'unit': 'ms',
        'scrShotPath': screenshotDir,
      };
      // record error details if http error or failure
      if (errorArr.includes(runDetails.text)) {
        epResult = {
          endpoint,
          'httpError': runDetails.text,
          'runNumber': counter,
          timeElapsed,
        };
        perfLog.summary.errors.push(epResult);
      };
      perfLog.results[epKey].push(runDetails)
      times.push(homeTime);
      times.push(timeElapsed);
    };
    // record home page metrics
    homeDetails = {
      'endpoint': '/',
      'text': homeContent,
      'timeElapsed': homeTime,
      'unit': 'ms',
      'scrShotPath': homeScrShot,  
    };
    counter += 1
  };
  // set total time, avg time, and error ratio
  const totalTime = times.reduce((acc, currVal) => acc + currVal, 0);
  const avgTime = totalTime / perfLog.summary.totalTests;
  perfLog.summary.totalTime = totalTime;
  perfLog.summary.avgRenderTime = avgTime;
  perfLog.summary.errorRatio = perfLog.summary.errors.length / perfLog.summary.totalTests
  await browser.close();
  const logPath = logRenderPerf(perfLog, resultDir, 'ui-performance', 'json');
};

/**
 * Times and returns performance of an operation measured in milliseconds. In our case,
 * the amount of time it takes to get a response from the API
 * server and for the UI to render. Can be used to time
 * the performance of any function.
 * @param {Function} callback - the operation to test performance of.
 * @param {Array} params - array of params to pass to the callback function.
 * @returns {Promise<object>} - {timeElapsed, cbReturn} Object containing the time elapsed and the return value of callback function.
 */
const timeRenderPerf = async (callback, params=[]) => {
  let cbReturn;
  let timeElapsed;
  let startTime;
  let endTime;
  if (params.length) {
    startTime = Date.now();
    cbReturn = await callback(...params).catch(error => console.error(error));
    endTime = Date.now()
  } else {
    startTime = Date.now()
    cbReturn = await callback(error => console.error(error));
    endTime = Date.now()
}
  timeElapsed = (endTime - startTime)
  return [timeElapsed, cbReturn]
};

/**
 * stringifys the logEntry object and creates a new UI test results file
 * in the specified directory
 * @param {object} logEntry - Object Containing the performance log details
 * @param {String} directory - The directory path to save the results file to.
 * @param {String} name - The main body of the file name.
 * @param {String} ext - the file extension without the leading '.'
 * @returns - the relative file path where the log file is saved.
 */
const logRenderPerf = (logEntry, directory, name, ext) => {
  const logToJson = JSON.stringify(logEntry, null, '\t');
  const newFileStr = dateifyFileName(directory, name, ext);
  fs.writeFileSync(newFileStr, logToJson);
  return newFileStr
};

/**
 * Takes a directory path, filename, and extension
 * and adds the current datetime as a prefix to the file name.
 * @param {String} directory - The Directory path. 
 * @param {String} namePrefix - Body of filename.
 * @returns {String} - A new string with the current datetime appended to the file name.
 */
const dateifyFileName = (directory, name, extension) => {
  return `${directory}${name
    .replace(/\//g, '-')}-${new Date(Date.now()).toISOString()}.${extension}`
}

runUiTest(baseUrl, endPoints, selectors, `../results/ui-test-results/`, 40)
  .catch(error => console.error(error));