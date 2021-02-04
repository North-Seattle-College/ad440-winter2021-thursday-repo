function logResponse(requestParams, response, context, ee, next){
      console.log(`${response.request.uri.path}: ${response.statusCode}`);
      return next();
  }

module.exports = {
    logResponse: logResponse
}

