const AWS = require("aws-sdk");
const fs = require("fs");
const config = {
  s3BucketName: process.env.BUCKET_NAME,
  filePath: '../results/serverless-artillery-test-users-api.json'
};
const s3Config = {
    signatureVersion: 'v4',
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
}
const s3 = new AWS.S3(s3Config);
s3.putObject({
  Bucket: 'usersapitest',
  Key: 'serverless-artillery-test-users-api.json',
  Body: fs.readFileSync(config.filePath)
}, (err, res) => {
  if (err) {
      return console.log("Error uploading file ", err)
  }
  console.log('Successfully uploaded!', {res});
});