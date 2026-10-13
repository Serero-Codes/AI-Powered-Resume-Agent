<script setup>
import { onMounted, ref } from "vue";

import {
    checkBackendHealth,
    getCareerProfile,
} from "./services/api";

// Store the backend connection status
const backendStatus = ref("Connecting to backend...");

// Store the career profile retrieved from Flask
const profile = ref(null);

// Store any errors
const errorMessage = ref("");

// Retrieve the data when the component loads
onMounted(async () => {
    try {
        // Check the backend connection
        const health = await checkBackendHealth();

        backendStatus.value = health.message;

        // Retrieve the career profile
        const result = await getCareerProfile();

        profile.value = result.profile;
    } catch (error) {
        backendStatus.value = "Connection failed";

        errorMessage.value = error.message;

        console.error("API connection error:", error);
    }
});
</script>

<template>
    <main class="app-container">
        <header class="app-header">
            <h1>AI-Powered Resume Agent</h1>

            <p>
                Your personal career profile and intelligent CV assistant.
            </p>
        </header>

        <!-- Backend connection status -->
        <section class="status-card">
            <h2>Backend Connection</h2>

            <p>{{ backendStatus }}</p>

            <p v-if="errorMessage" class="error-message">
                {{ errorMessage }}
            </p>
        </section>

        <!-- Career profile -->
        <section v-if="profile" class="profile-card">
            <h2>Career Profile</h2>

            <div class="profile-section">
                <h3>Personal Information</h3>

                <p>
                    <strong>Name:</strong>
                    {{ profile.personal.full_name || "Not provided" }}
                </p>

                <p>
                    <strong>Email:</strong>
                    {{ profile.personal.email || "Not provided" }}
                </p>

                <p>
                    <strong>Location:</strong>
                    {{ profile.personal.location || "Not provided" }}
                </p>

                <p>
                    <strong>LinkedIn:</strong>
                    {{ profile.personal.linkedin || "Not provided" }}
                </p>

                <p>
                    <strong>GitHub:</strong>
                    {{ profile.personal.github || "Not provided" }}
                </p>
            </div>

            <div class="profile-section">
                <h3>Professional Summary</h3>

                <p>
                    {{ profile.professional_summary || "No summary available." }}
                </p>
            </div>

            <div class="profile-section">
                <h3>Education</h3>

                <ul>
                    <li
                        v-for="(education, index) in profile.education"
                        :key="index"
                    >
                        {{ education.name }}
                    </li>
                </ul>
            </div>

            <div class="profile-section">
                <h3>Work Experience</h3>

                <article
                    v-for="(job, index) in profile.experience"
                    :key="index"
                    class="experience-item"
                >
                    <h4>{{ job.role }}</h4>

                    <p>
                        <strong>{{ job.company }}</strong>
                        — {{ job.period }}
                    </p>

                    <ul>
                        <li
                            v-for="(highlight, highlightIndex) in job.highlights"
                            :key="highlightIndex"
                        >
                            {{ highlight }}
                        </li>
                    </ul>
                </article>
            </div>

            <div class="profile-section">
                <h3>Projects</h3>

                <article
                    v-for="(project, index) in profile.projects"
                    :key="index"
                    class="project-item"
                >
                    <h4>{{ project.name }}</h4>

                    <p>{{ project.description }}</p>

                    <p>
                        <strong>Technologies:</strong>
                        {{ project.technologies.join(", ") }}
                    </p>
                </article>
            </div>

            <div class="profile-section">
                <h3>Skills</h3>

                <div
                    v-for="(skills, category) in profile.skills"
                    :key="category"
                    class="skill-category"
                >
                    <h4>
                        {{ category.replaceAll("_", " ") }}
                    </h4>

                    <p v-if="skills.length">
                        {{ skills.join(", ") }}
                    </p>

                    <p v-else>No skills listed.</p>
                </div>
            </div>

            <div class="profile-section">
                <h3>Certifications</h3>

                <ul>
                    <li
                        v-for="(certification, index) in profile.certifications"
                        :key="index"
                    >
                        {{ certification.name }}
                    </li>
                </ul>
            </div>
        </section>

        <!-- Loading indicator -->
        <p v-else-if="!errorMessage">
            Loading your career profile...
        </p>
    </main>
</template>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: #f3f5f9;
    color: #1f2937;
}

.app-container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 32px 20px;
}

.app-header {
    margin-bottom: 28px;
}

.app-header h1 {
    margin-bottom: 8px;
    color: #172554;
}

.app-header p {
    color: #64748b;
}

.status-card,
.profile-card {
    background: #ffffff;
    padding: 24px;
    margin-bottom: 24px;
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
}

.status-card h2,
.profile-card > h2 {
    margin-top: 0;
    color: #1d4ed8;
}

.profile-section {
    padding: 20px 0;
    border-bottom: 1px solid #e5e7eb;
    overflow-wrap: anywhere;
}

.profile-section:last-child {
    border-bottom: none;
}

.profile-section h3 {
    color: #1e40af;
}

.experience-item,
.project-item {
    margin: 20px 0;
    padding: 16px;
    background: #f8fafc;
    border-radius: 8px;
}

.experience-item h4,
.project-item h4 {
    margin-top: 0;
}

.skill-category {
    margin: 16px 0;
}

.skill-category h4 {
    text-transform: capitalize;
    margin-bottom: 6px;
}

.error-message {
    color: #b91c1c;
}
</style>