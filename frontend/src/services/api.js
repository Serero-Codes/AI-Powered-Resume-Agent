// frontend/src/services/api.js

// Base URL of the Flask backend
const API_BASE_URL = "http://127.0.0.1:5000/api";

// Reusable function for making API requests
async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        },
    });

    // Convert the response into JSON
    const data = await response.json();

    // Handle unsuccessful HTTP responses
    if (!response.ok) {
        throw new Error(
            data.message || `Request failed with status ${response.status}`
        );
    }

    return data;
}

// Check whether the backend is running
export async function checkBackendHealth() {
    return apiRequest("/health");
}

// Retrieve the permanent career profile
export async function getCareerProfile() {
    return apiRequest("/profile");
}

// Save an updated career profile
export async function updateCareerProfile(profile) {
    return apiRequest("/profile", {
        method: "PUT",
        body: JSON.stringify(profile),
    });
}
