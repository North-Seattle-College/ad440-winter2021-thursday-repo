import {startBrowser, getSelectorContent} from './ui-test-tasks.js';

const baseUrl = 'https://nscstrdevusw2thucommon.z5.web.core.windows.net';
const endPoints = {
    'users': '/users',
    'userId': '/users/{userId}',
    'tasks': '/users/{userId}/tasks',
    'taskId': '/users/{userId}/tasks/{taskId}', 
};

(async () => {
    let url = baseUrl;
    let selector = 'h1';
    let pupInstance = await startBrowser();
    const page = pupInstance.page;
    let selectorContent = await getSelectorContent(url, page, endPoints.tasks, selector);
})();