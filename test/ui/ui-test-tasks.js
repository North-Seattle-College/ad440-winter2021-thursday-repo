import puppeteer from 'puppeteer';

/**
 * starts instance of headless chrome
 * and returns the browser and page objects
 * @typedef {Object} PuppetInstance
 * @property {Browser} browser - The puppeteer Browser Object
 * @property {Page} page - The puppeteer Page object
 * @return {PuppetInstance} - The puppeteer intance
 */
const startBrowser = async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  return {browser, page};
};
