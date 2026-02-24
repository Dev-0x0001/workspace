const { defineConfig } = require('playwright-config');

module.exports = defineConfig(({ mode }) => ({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!mode.production,
  retries: mode.production ? 2 : 0,
  workers: mode.production ? '50%' : undefined,

  reporter: mode.production ? [['html', { outputFolder: 'report' }]] : [['list']],

  projects: [
    {
      name: 'chromium',
      use: { browser: 'chromium' }
    },
    {
      name: 'firefox',
      use: { browser: 'firefox' }
    },
    {
      name: 'webkit',
      use: { browser: 'webkit' }
    },
  ],
}));