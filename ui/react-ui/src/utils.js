export const is404 = (response) => {
    if (response && response.status === 404) {
        return true;
    } else {
        return false;
    }
}