// API configuration for different environments
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5002';

export const apiConfig = {
  baseURL: API_BASE_URL,
  endpoints: {
    smsChat: `${API_BASE_URL}/sms-chat`,
    analyze: `${API_BASE_URL}/analyze`,
    practiceSuggestion: `${API_BASE_URL}/practice-suggestion`,
    simplifyText: `${API_BASE_URL}/simplify-text`,
    uploadAndAnalyze: `${API_BASE_URL}/upload-and-analyze`,
    uploadAndAnalyzeVideo: `${API_BASE_URL}/upload-and-analyze-video`,
    analyzeVideo: `${API_BASE_URL}/analyze-video`,
    analyzeFormality: `${API_BASE_URL}/analyze-formality`,
    health: `${API_BASE_URL}/health`
  }
};

// Helper function to create full API URL
export const createApiUrl = (endpoint) => {
  return `${API_BASE_URL}${endpoint}`;
};

export default apiConfig;
