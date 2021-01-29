const fs = require('fs');
const YAML = require('yaml');

const file = fs.readFileSync('./serverless.yml', 'utf8');
const doc = YAML.parseDocument(file);
doc.addIn(['provider'], { key: 'region', value: 'us-west-2' })
let newYAML = doc.toString();
fs.writeFileSync('serverless.yml', newYAML, 'utf8');
