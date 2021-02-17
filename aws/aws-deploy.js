const AWS = require("aws-sdk");
const fs = require("fs");
// configuration
const config = {
  s3BucketName: process.env.BUCKET_NAME,
  filePath: `../test/results/serverless-artillery-test-users-api.json`
};
// serverless-artillery-test-users-api.json
// initialize S3 client
const s3Config = {
    signatureVersion: 'v4',
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
}
const s3 = new AWS.S3(s3Config);
console.log('sdasdasdasdasdasdasdasdasdsad', s3)
s3.putObject({
  Bucket: 'usersapitest',
  Key: 'serverless-artillery-test-users-api.json',
  Body: fs.readFileSync(config.filePath)
}, (err, res) => {
  if (err) {
      return console.log("Error uploading file ", err)
  }
  console.log(`Successfully uploaded!`, {res});
});