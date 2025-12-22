#!/usr/bin/env node
/**
 * A.V.A. API Keys Automation Script
 * Automates the signup process for Google AI, Tavily, and Discord
 * 
 * Usage: node automate_api_setup.js
 * 
 * Requirements:
 * - Node.js installed
 * - npm install puppeteer
 */

const puppeteer = require('puppeteer');
const readline = require('readline');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
    headless: false, // Set to true to run in background
    timeout: 30000,
    waitForNavigation: { waitUntil: 'networkidle2' }
};

// Create readline interface for user input
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function question(prompt) {
    return new Promise((resolve) => {
        rl.question(prompt, resolve);
    });
}

class APIAutomation {
    constructor() {
        this.browser = null;
        this.page = null;
        this.keys = {
            google: null,
            tavily: null,
            discord: null
        };
        this.userEmail = null;
        this.userPassword = null;
    }

    async init() {
        console.log('🚀 Starting browser automation...');
        this.browser = await puppeteer.launch({
            headless: CONFIG.headless,
            defaultViewport: { width: 1280, height: 720 },
            args: ['--start-maximized']
        });
        this.page = await this.browser.newPage();
        await this.page.setViewport({ width: 1280, height: 720 });
    }

    async getCredentials() {
        console.log('\n📧 We need your credentials to automate signups:');
        this.userEmail = await question('Enter your email: ');
        this.userPassword = await question('Enter a password (or press Enter to skip auto-login): ');
        
        if (!this.userPassword) {
            console.log('⚠️  Auto-login disabled. You\'ll need to sign in manually.');
        }
    }

    async setupGoogleAI() {
        console.log('\n🔵 Setting up Google AI (Gemini)...');
        
        try {
            await this.page.goto('https://makersuite.google.com/app/apikey', {
                waitUntil: 'networkidle2',
                timeout: CONFIG.timeout
            });

            // Wait for page to load
            await this.page.waitForTimeout(2000);

            // Check if already logged in
            const isLoggedIn = await this.page.evaluate(() => {
                return document.body.textContent.includes('Create API key') || 
                       document.body.textContent.includes('API key');
            });

            if (!isLoggedIn) {
                console.log('   → Signing in to Google...');
                await this.handleGoogleSignIn();
            }

            // Look for "Create API Key" button or existing key
            await this.page.waitForTimeout(2000);

            // Try to find and click "Create API Key" button
            const createButton = await this.page.evaluate(() => {
                const buttons = Array.from(document.querySelectorAll('button, a'));
                return buttons.find(btn => 
                    btn.textContent.includes('Create') || 
                    btn.textContent.includes('Get API key') ||
                    btn.textContent.includes('API key')
                );
            });

            if (createButton) {
                await this.page.evaluate((btn) => btn.click(), createButton);
                await this.page.waitForTimeout(3000);
            }

            // Wait for API key to appear
            await this.page.waitForTimeout(2000);

            // Extract API key
            const apiKey = await this.page.evaluate(() => {
                // Look for API key in various formats
                const text = document.body.textContent;
                const keyMatch = text.match(/AIza[0-9A-Za-z_-]{35}/);
                if (keyMatch) return keyMatch[0];

                // Check input fields
                const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');
                for (const input of inputs) {
                    if (input.value && input.value.startsWith('AIza')) {
                        return input.value;
                    }
                }

                // Check code blocks
                const codeBlocks = document.querySelectorAll('code, pre');
                for (const block of codeBlocks) {
                    const match = block.textContent.match(/AIza[0-9A-Za-z_-]{35}/);
                    if (match) return match[0];
                }

                return null;
            });

            if (apiKey) {
                this.keys.google = apiKey;
                console.log('   ✅ Google AI key found:', apiKey.substring(0, 20) + '...');
                return true;
            } else {
                console.log('   ⚠️  Could not auto-detect key. Please copy it manually.');
                const manualKey = await question('   Paste your Google AI key here (or press Enter to skip): ');
                if (manualKey.trim()) {
                    this.keys.google = manualKey.trim();
                    return true;
                }
            }
        } catch (error) {
            console.log('   ❌ Error:', error.message);
            const manualKey = await question('   Paste your Google AI key here (or press Enter to skip): ');
            if (manualKey.trim()) {
                this.keys.google = manualKey.trim();
                return true;
            }
        }

        return false;
    }

    async setupTavily() {
        console.log('\n🟢 Setting up Tavily Search...');
        
        try {
            await this.page.goto('https://tavily.com', {
                waitUntil: 'networkidle2',
                timeout: CONFIG.timeout
            });

            await this.page.waitForTimeout(2000);

            // Look for sign up button
            const signUpButton = await this.page.evaluate(() => {
                const buttons = Array.from(document.querySelectorAll('a, button'));
                return buttons.find(btn => 
                    btn.textContent.toLowerCase().includes('sign up') ||
                    btn.textContent.toLowerCase().includes('get started') ||
                    btn.textContent.toLowerCase().includes('register')
                );
            });

            if (signUpButton) {
                console.log('   → Clicking sign up...');
                await this.page.evaluate((btn) => btn.click(), signUpButton);
                await this.page.waitForTimeout(3000);
            }

            // Fill signup form if visible
            const emailInput = await this.page.$('input[type="email"]');
            if (emailInput && this.userEmail) {
                await emailInput.type(this.userEmail, { delay: 100 });
                await this.page.waitForTimeout(1000);

                const passwordInput = await this.page.$('input[type="password"]');
                if (passwordInput && this.userPassword) {
                    await passwordInput.type(this.userPassword, { delay: 100 });
                    await this.page.waitForTimeout(1000);
                }

                // Submit form
                const submitButton = await this.page.$('button[type="submit"], input[type="submit"]');
                if (submitButton) {
                    await submitButton.click();
                    await this.page.waitForTimeout(5000);
                }
            }

            // Navigate to API keys page
            await this.page.goto('https://app.tavily.com/api-keys', {
                waitUntil: 'networkidle2',
                timeout: CONFIG.timeout
            });

            await this.page.waitForTimeout(3000);

            // Extract API key
            const apiKey = await this.page.evaluate(() => {
                const text = document.body.textContent;
                const keyMatch = text.match(/tvly-[0-9A-Za-z_-]{20,}/);
                if (keyMatch) return keyMatch[0];

                const inputs = document.querySelectorAll('input[type="text"], input[type="password"], code');
                for (const input of inputs) {
                    const value = input.value || input.textContent;
                    if (value && value.startsWith('tvly-')) {
                        return value.trim();
                    }
                }

                return null;
            });

            if (apiKey) {
                this.keys.tavily = apiKey;
                console.log('   ✅ Tavily key found:', apiKey.substring(0, 20) + '...');
                return true;
            } else {
                console.log('   ⚠️  Could not auto-detect key. Please copy it manually.');
                const manualKey = await question('   Paste your Tavily key here (or press Enter to skip): ');
                if (manualKey.trim()) {
                    this.keys.tavily = manualKey.trim();
                    return true;
                }
            }
        } catch (error) {
            console.log('   ❌ Error:', error.message);
            const manualKey = await question('   Paste your Tavily key here (or press Enter to skip): ');
            if (manualKey.trim()) {
                this.keys.tavily = manualKey.trim();
                return true;
            }
        }

        return false;
    }

    async setupDiscord() {
        console.log('\n🟣 Setting up Discord Bot...');
        
        try {
            await this.page.goto('https://discord.com/developers/applications', {
                waitUntil: 'networkidle2',
                timeout: CONFIG.timeout
            });

            await this.page.waitForTimeout(3000);

            // Check if logged in
            const isLoggedIn = await this.page.evaluate(() => {
                return !document.body.textContent.includes('Login') &&
                       !document.body.textContent.includes('Sign In');
            });

            if (!isLoggedIn) {
                console.log('   → Please sign in to Discord manually...');
                await question('   Press Enter after you\'ve signed in...');
            }

            // Look for "New Application" button
            await this.page.waitForTimeout(2000);
            const newAppButton = await this.page.evaluate(() => {
                const buttons = Array.from(document.querySelectorAll('button, a'));
                return buttons.find(btn => 
                    btn.textContent.includes('New Application') ||
                    btn.textContent.includes('Create Application')
                );
            });

            if (newAppButton) {
                console.log('   → Creating new application...');
                await this.page.evaluate((btn) => btn.click(), newAppButton);
                await this.page.waitForTimeout(2000);

                // Fill application name
                const nameInput = await this.page.$('input[type="text"]');
                if (nameInput) {
                    await nameInput.type('A.V.A. Bot', { delay: 100 });
                    await this.page.waitForTimeout(1000);
                }

                // Submit
                const submitButton = await this.page.$('button[type="submit"]');
                if (submitButton) {
                    await submitButton.click();
                    await this.page.waitForTimeout(3000);
                }
            }

            // Navigate to Bot section
            const botLink = await this.page.evaluate(() => {
                const links = Array.from(document.querySelectorAll('a'));
                return links.find(link => 
                    link.textContent.includes('Bot') ||
                    link.href.includes('/bot')
                );
            });

            if (botLink) {
                await this.page.evaluate((link) => link.click(), botLink);
                await this.page.waitForTimeout(2000);
            }

            // Look for "Add Bot" or "Reset Token"
            const addBotButton = await this.page.evaluate(() => {
                const buttons = Array.from(document.querySelectorAll('button'));
                return buttons.find(btn => 
                    btn.textContent.includes('Add Bot') ||
                    btn.textContent.includes('Reset Token')
                );
            });

            if (addBotButton) {
                await this.page.evaluate((btn) => btn.click(), addBotButton);
                await this.page.waitForTimeout(2000);
            }

            // Extract token
            const token = await this.page.evaluate(() => {
                const text = document.body.textContent;
                // Discord tokens are long alphanumeric strings
                const tokenMatch = text.match(/[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}/);
                if (tokenMatch) return tokenMatch[0];

                const inputs = document.querySelectorAll('input[type="text"], input[type="password"], code');
                for (const input of inputs) {
                    const value = input.value || input.textContent;
                    if (value && value.length > 50 && /^[MN]/.test(value)) {
                        return value.trim();
                    }
                }

                return null;
            });

            if (token) {
                this.keys.discord = token;
                console.log('   ✅ Discord token found:', token.substring(0, 20) + '...');
                return true;
            } else {
                console.log('   ⚠️  Could not auto-detect token. Please copy it manually.');
                const manualToken = await question('   Paste your Discord token here (or press Enter to skip): ');
                if (manualToken.trim()) {
                    this.keys.discord = manualToken.trim();
                    return true;
                }
            }
        } catch (error) {
            console.log('   ❌ Error:', error.message);
            const manualToken = await question('   Paste your Discord token here (or press Enter to skip): ');
            if (manualToken.trim()) {
                this.keys.discord = manualToken.trim();
                return true;
            }
        }

        return false;
    }

    async handleGoogleSignIn() {
        // Wait for user to sign in manually
        console.log('   → Please sign in to Google in the browser window...');
        await question('   Press Enter after you\'ve signed in...');
    }

    async saveKeys() {
        console.log('\n💾 Saving API keys...');

        // Save to localStorage file (for browser)
        const localStorageFile = path.join(__dirname, 'api_keys_localStorage.js');
        const localStorageContent = `// A.V.A. API Keys - Auto-generated
// Copy and paste these into browser console (F12)

localStorage.setItem('GOOGLE_API_KEY', '${this.keys.google || ''}');
localStorage.setItem('TAVILY_API_KEY', '${this.keys.tavily || ''}');
localStorage.setItem('DISCORD_TOKEN', '${this.keys.discord || ''}');

console.log('✅ API keys saved to localStorage!');
console.log('Google:', localStorage.getItem('GOOGLE_API_KEY') ? '✅' : '❌');
console.log('Tavily:', localStorage.getItem('TAVILY_API_KEY') ? '✅' : '❌');
console.log('Discord:', localStorage.getItem('DISCORD_TOKEN') ? '✅' : '❌');
`;

        fs.writeFileSync(localStorageFile, localStorageContent);
        console.log('   ✅ Saved to:', localStorageFile);

        // Save to .env file (for Node.js)
        const envFile = path.join(__dirname, '.env');
        const envContent = `# A.V.A. API Keys - Auto-generated
GOOGLE_API_KEY=${this.keys.google || ''}
TAVILY_API_KEY=${this.keys.tavily || ''}
DISCORD_TOKEN=${this.keys.discord || ''}
`;

        fs.writeFileSync(envFile, envContent);
        console.log('   ✅ Saved to:', envFile);

        // Save to JSON
        const jsonFile = path.join(__dirname, 'api_keys.json');
        fs.writeFileSync(jsonFile, JSON.stringify(this.keys, null, 2));
        console.log('   ✅ Saved to:', jsonFile);

        console.log('\n📋 Summary:');
        console.log('   Google AI:', this.keys.google ? '✅ ' + this.keys.google.substring(0, 20) + '...' : '❌ Not set');
        console.log('   Tavily:', this.keys.tavily ? '✅ ' + this.keys.tavily.substring(0, 20) + '...' : '❌ Not set');
        console.log('   Discord:', this.keys.discord ? '✅ ' + this.keys.discord.substring(0, 20) + '...' : '❌ Not set');
    }

    async run() {
        try {
            await this.init();
            await this.getCredentials();

            console.log('\n🎯 Starting automated setup...');
            console.log('   The browser will open and guide you through each service.');
            console.log('   You may need to complete some steps manually (email verification, CAPTCHA, etc.)\n');

            // Setup each service
            await this.setupGoogleAI();
            await this.setupTavily();
            await this.setupDiscord();

            // Save all keys
            await this.saveKeys();

            console.log('\n✨ Setup complete!');
            console.log('   Next steps:');
            console.log('   1. Open index.html in your browser');
            console.log('   2. Open browser console (F12)');
            console.log('   3. Copy and paste the contents of api_keys_localStorage.js');
            console.log('   4. Refresh the page');

        } catch (error) {
            console.error('❌ Error:', error);
        } finally {
            if (this.browser) {
                await this.browser.close();
            }
            rl.close();
        }
    }
}

// Run automation
if (require.main === module) {
    const automation = new APIAutomation();
    automation.run().catch(console.error);
}

module.exports = APIAutomation;

