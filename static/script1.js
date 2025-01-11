
const API_BASE_URL = 'http://127.0.0.1:5000/api/';
// Function to handle all opportunities
document.getElementById('findAllOpportunities').addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/programs`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch opportunities');
        }
        displayOpportunities(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to fetch opportunities');
    }
});

// Search by category
async function searchByCategory() {
    const category = document.getElementById('categoryInput').value;
    if (!category) {
        showError('Please enter a category');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/programs/category/${encodeURIComponent(category)}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch opportunities by category');
        }
        displayOpportunities(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to fetch opportunities by category');
    }
}

// Search by location
async function searchByLocation() {
    const location = document.getElementById('countryInput').value;
    if (!location) {
        showError('Please enter a country');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/programs/location/${encodeURIComponent(location)}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch opportunities by location');
        }
        displayOpportunities(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to fetch opportunities by location');
    }
}


function displayOpportunities(opportunities) {
    const container = document.getElementById('opportunities-list');
    container.innerHTML = '';
    
    if (!Array.isArray(opportunities) || opportunities.length === 0) {
        container.innerHTML = '<p class="no-results">No opportunities found</p>';
        return;
    }
    
    opportunities.forEach(opportunity => {
        const card = document.createElement('div');
        card.className = 'opportunity-card';
        
        // Create safe values object with default values
        const safeValues = {
            name: opportunity.name || 'Untitled',
            category: opportunity.category || 'N/A',
            description: opportunity.description || 'No description available',
            location: opportunity.location || 'Location not specified',
            application_deadline: opportunity.application_deadline || 'Deadline not specified',
            duration: opportunity.duration || 'Duration not specified',
            eligibility_criteria: opportunity.eligibility_criteria || 'Not specified',
            funding_details: opportunity.funding_details || null,
            application_link: opportunity.application_link || '#'
        };
        
        card.innerHTML = `
            <h3>${escapeHtml(safeValues.name)}</h3>
            <p><strong>Category:</strong> ${escapeHtml(safeValues.category)}</p>
            <p><strong>Description:</strong> ${escapeHtml(safeValues.description)}</p>
            <p><strong>Location:</strong> ${escapeHtml(safeValues.location)}</p>
            <p><strong>Deadline:</strong> ${escapeHtml(safeValues.application_deadline)}</p>
            <p><strong>Duration:</strong> ${escapeHtml(safeValues.duration)}</p>
            <p><strong>Eligibility:</strong> ${escapeHtml(safeValues.eligibility_criteria)}</p>
            ${safeValues.funding_details ? `<p><strong>Funding:</strong> ${escapeHtml(safeValues.funding_details)}</p>` : ''}
            <a href="${escapeHtml(safeValues.application_link)}" target="_blank" class="btn btn-primary">Apply Now</a>
        `;
        
        container.appendChild(card);
    });
}

// Updated fetch function with better error handling
document.getElementById('findAllOpportunities').addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/programs`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Fetched data:', data); // Debug log to see the structure
        displayOpportunities(data);
    } catch (error) {
        console.error('Error:', error);
        const container = document.getElementById('opportunities-list');
        container.innerHTML = '<p class="error-message">Failed to fetch opportunities. Please try again later.</p>';
    }
});

// Modal functions
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.body.style.overflow = ''; // Restore scrolling
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Handle mentor form submission
async function submitMentorForm(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch(`${API_BASE_URL}/mentor`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showSuccess('Mentor registration successful!');
            closeModal('mentor-modal');
            event.target.reset();
        } else {
            throw new Error(result.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to submit mentor registration: ' + error.message);
    }
}

// Handle applicant form submission
async function submitApplicantForm(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch(`${API_BASE_URL}/applicant`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showSuccess('Applicant registration successful!');
            closeModal('applicant-modal');
            event.target.reset();
        } else {
            throw new Error(result.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to submit applicant registration: ' + error.message);
    }
}

// Utility functions
function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') {
        unsafe = String(unsafe || ''); // Convert non-string values to strings, default to empty string
    }
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success';
    successDiv.textContent = message;
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 5000);
}

// Add event listeners when document loads
document.addEventListener('DOMContentLoaded', () => {
    // Close modals with Escape key
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            document.querySelectorAll('.modal').forEach(modal => {
                modal.style.display = 'none';
            });
            document.body.style.overflow = '';
        }
    });

    // Add form submission listeners
    document.getElementById('mentor-form').addEventListener('submit', submitMentorForm);
    document.getElementById('applicant-form').addEventListener('submit', submitApplicantForm);
});