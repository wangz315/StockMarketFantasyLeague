// conf.js
exports.config = {
  framework: 'jasmine',
  baseUrl: 'http://localhost:5000/',
  seleniumAddress: 'http://localhost:4444/wd/hub',
  specs: ['stockSpec.js']
}