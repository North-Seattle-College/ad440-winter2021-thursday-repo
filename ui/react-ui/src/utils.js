export const is404 = (response) => {
    if (response && response.status === 404) {
        return true;
    } else {
        return false;
    }
}

/**
 * @author - Sean Gilliland <gillilands19@gmail.com>
 * 
 *  Returns string stripped of plural S
 * @param {string} str - The string to strip the plural S from
 * @return {string} - The Depluralized string
 */
export const dePluralize = (str) => {
    let depluralStr = str
    const strLen = depluralStr.length
    if(depluralStr.toLowerCase().charAt(strLen - 1) === 's') {
       depluralStr = str.substring(0, strLen - 1)
    }
    return depluralStr;
}

/**
 * @author - Sean Gilliland <gillilands19@gmail.com>
 * 
 *  Returns page title from endpoint
 * @param {string} str - url endpoint to extract title from
 * @return {string} - the title
 */
export const getTitleFromUrl = (str) => {
    let splitStr = str.split('/');
    let len = splitStr.length;
    return splitStr[len - 1];
}

/**
 * @author - Sean Gilliland <gillilands19@gmail.com>
 * 
 * Fetches and sets state for tables displaying API data
 * @param {string} endPoint - The API endpoint before parameters e.g api/[users]
 * @param {function} setStateFunc - The function setState function passed to React useState Hook
 * @param {string} urlParam - the parameter passed to url string e.g api/users/[1]
 * @return {Response} - Fetch API Response Object
 */
export const fetchSetTblState = async (endPoint, setStateFunc, urlParam = '') => {
    let title = getTitleFromUrl(endPoint);
    let depluralTitle = dePluralize(title);
    let subtitleStr = `All ${title}`;
    let apiURL;

    if(!urlParam) {
      apiURL = `https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/${endPoint}/`
    } else {
      apiURL = `https://nsc-fun-dev-usw2-thursday.azurewebsites.net/api/${endPoint}/${urlParam}`
    }

    const response = await fetch(apiURL);
    if(urlParam !== null) {
        subtitleStr = `Single ${depluralTitle}`;
    };
    if(response.ok) {
      const resJson = await response.clone().json();
      setStateFunc([
        {
        title: `${depluralTitle.toUpperCase()} ${urlParam}`,
        subtitle: `${subtitleStr}`
        },
        response,
        resJson
      ])
    } else {
      setStateFunc([
        {
        title: response.status,
        subtitle: response.statusText
        },
        response
      ])
    };
    return response;
  };