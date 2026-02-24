import { test } from '@playwright/test';

// Example smoke test
test.describe('Application Smoke Tests', () => {
  test('should load dashboard', async ({ page }) => {
    await page.goto('/');
    await page.waitForSelector('h1.welcome-title');
    const title = await page.textContent('h1.welcome-title');
    expect(title).toContain('Welcome');
  });
});