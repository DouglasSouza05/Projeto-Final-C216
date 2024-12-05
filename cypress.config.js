const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
    },
    baseUrl: 'http://localhost:3000', 
  },
  reporter: 'mochawesome', 
  reporterOptions: {
    reportDir: 'cypress/reports', 
    overwrite: false,
    html: true,
    json: true,
  },
})
