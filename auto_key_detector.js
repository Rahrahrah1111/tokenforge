/**
 * Browser-based API Key Auto-Detector
 * 
 * This script runs in the browser and automatically detects API keys
 * from clipboard, page content, or user input, then saves them to localStorage.
 * 
 * Usage:
 * 1. Open browser console (F12)
 * 2. Paste this entire script
 * 3. It will monitor for API keys and auto-save them
 */

(function() {
    'use strict';

    console.log('🔑 A.V.A. API Key Auto-Detector initialized');

    const keyPatterns = {
        google: /AIza[0-9A-Za-z_-]{35}/,
        tavily: /tvly-[0-9A-Za-z_-]{20,}/,
        discord: /[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}/
    };

    const keyNames = {
        google: 'GOOGLE_API_KEY',
        tavily: 'TAVILY_API_KEY',
        discord: 'DISCORD_TOKEN'
    };

    function detectKey(text, type) {
        const pattern = keyPatterns[type];
        if (!pattern) return null;
        
        const match = text.match(pattern);
        return match ? match[0] : null;
    }

    function saveKey(key, type) {
        const storageKey = keyNames[type];
        localStorage.setItem(storageKey, key);
        console.log(`✅ ${type.toUpperCase()} key saved:`, key.substring(0, 20) + '...');
        
        // Show notification
        showNotification(`${type.toUpperCase()} key detected and saved!`);
        
        // Update status if on setup page
        updateStatus(type, true);
    }

    function showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(45deg, #00ffff, #20b2aa);
            color: #0a0a0a;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0, 255, 255, 0.5);
            z-index: 10000;
            font-family: 'Orbitron', monospace;
            font-weight: 600;
            animation: slideIn 0.3s ease-out;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    function updateStatus(type, isSet) {
        const statusEl = document.getElementById(`${type}-status`);
        if (statusEl) {
            statusEl.textContent = isSet ? '✅ Set' : 'Not Set';
            statusEl.className = isSet ? 'status set' : 'status not-set';
        }
    }

    // Monitor clipboard
    document.addEventListener('paste', (e) => {
        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
        
        Object.keys(keyPatterns).forEach(type => {
            const key = detectKey(pastedText, type);
            if (key) {
                e.preventDefault();
                saveKey(key, type);
            }
        });
    });

    // Monitor page content for keys
    function scanPage() {
        const pageText = document.body.textContent;
        
        Object.keys(keyPatterns).forEach(type => {
            const key = detectKey(pageText, type);
            if (key && !localStorage.getItem(keyNames[type])) {
                saveKey(key, type);
            }
        });
    }

    // Scan page on load and periodically
    scanPage();
    setInterval(scanPage, 5000);

    // Monitor input fields
    document.addEventListener('input', (e) => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            const text = e.target.value;
            Object.keys(keyPatterns).forEach(type => {
                const key = detectKey(text, type);
                if (key) {
                    saveKey(key, type);
                }
            });
        }
    });

    // Add manual detection function
    window.detectAPIKeys = function(text) {
        const found = {};
        Object.keys(keyPatterns).forEach(type => {
            const key = detectKey(text, type);
            if (key) {
                found[type] = key;
                saveKey(key, type);
            }
        });
        return found;
    };

    // Add manual save function
    window.saveAPIKey = function(type, key) {
        if (keyNames[type]) {
            saveKey(key, type);
        } else {
            console.error('Unknown key type:', type);
        }
    };

    // Check existing keys
    console.log('📋 Current keys:');
    Object.keys(keyNames).forEach(type => {
        const key = localStorage.getItem(keyNames[type]);
        console.log(`   ${type}:`, key ? '✅ ' + key.substring(0, 20) + '...' : '❌ Not set');
    });

    console.log('\n💡 Usage:');
    console.log('   - Just copy/paste API keys anywhere on the page');
    console.log('   - Or use: detectAPIKeys("your text here")');
    console.log('   - Or use: saveAPIKey("google", "your-key-here")');
    console.log('\n✨ Auto-detector is running!');
})();

