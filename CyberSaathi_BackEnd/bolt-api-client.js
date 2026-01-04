/**
 * CyberSaathi API Client for Bolt.new
 * 
 * Copy this entire file to your Bolt.new project at: src/config/api.js
 * 
 * Make sure you have added to your .env file:
 * VITE_API_URL=https://unesoteric-autumn-nonintermittently.ngrok-free.dev
 */

// Get API URL from environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://unesoteric-autumn-nonintermittently.ngrok-free.dev';

// API Configuration
export const apiConfig = {
    baseUrl: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        'ngrok-skip-browser-warning': 'true' // Required for ngrok
    }
};

/**
 * CyberSaathi API Client
 */
export const cyberSaathiAPI = {
    /**
     * Ask a question to CyberSaathi
     * @param {string} query - The question to ask
     * @returns {Promise<Object>} Response with answer, sources, etc.
     */
    async chat(query) {
        try {
            const response = await fetch(`${apiConfig.baseUrl}/chat`, {
                method: 'POST',
                headers: apiConfig.headers,
                body: JSON.stringify({ query })
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('✅ CyberSaathi response:', data);
            return data;
        } catch (error) {
            console.error('❌ Chat API error:', error);
            throw error;
        }
    },

    /**
     * Check if the backend is healthy
     * @returns {Promise<Object>} Health status
     */
    async healthCheck() {
        try {
            const response = await fetch(`${apiConfig.baseUrl}/health`, {
                headers: apiConfig.headers
            });

            if (!response.ok) {
                throw new Error(`Health check failed: ${response.status}`);
            }

            const data = await response.json();
            console.log('✅ Backend health:', data);
            return data;
        } catch (error) {
            console.error('❌ Health check failed:', error);
            throw error;
        }
    },

    /**
     * Get API information
     * @returns {Promise<Object>} API info (version, models, etc.)
     */
    async getInfo() {
        try {
            const response = await fetch(`${apiConfig.baseUrl}/info`, {
                headers: apiConfig.headers
            });

            if (!response.ok) {
                throw new Error(`Info request failed: ${response.status}`);
            }

            const data = await response.json();
            console.log('ℹ️ API info:', data);
            return data;
        } catch (error) {
            console.error('❌ Info request failed:', error);
            throw error;
        }
    },

    /**
     * Test the connection to the backend
     * @returns {Promise<boolean>} True if connected, false otherwise
     */
    async testConnection() {
        try {
            await this.healthCheck();
            return true;
        } catch (error) {
            return false;
        }
    }
};

// Log the API URL on import (for debugging)
console.log('🔗 CyberSaathi API URL:', API_BASE_URL);

// Export default for convenience
export default cyberSaathiAPI;
