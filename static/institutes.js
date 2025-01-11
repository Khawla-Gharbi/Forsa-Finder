const API_BASE_URL = 'http://127.0.0.1:5000/api/';
// Function to handle all institutes
document.getElementById('findAllInstitutes').addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/institutes`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch institutes');
        }
        displayInstitutes(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to fetch institutes');
    }
});

// Search by Location
async function searchByLocation() {
    const location = document.getElementById('locationInput').value;
    if (!location) {
        showError('Please enter a location');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/institutes/location/${encodeURIComponent(location)}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch institutes by location');
        }
        displayInstitutes(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to fetch institutes by location');
    }
}

// Search by service type
async function searchByService() {
    const service = document.getElementById('serviceInput').value;
    if (!service) {
        showError('Please enter a service type');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/institutes/service/${encodeURIComponent(service)}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch institutes by type of service');
        }
        displayInstitutes(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to fetch institutes by type of service');
    }
}

function displayInstitutes(institutes) {
    const container = document.getElementById('institutes-list');
    container.innerHTML = '';
    
    if (!Array.isArray(institutes) || institutes.length === 0) {
        container.innerHTML = '<p class="no-results">No institutes found</p>';
        return;
    }
    
    institutes.forEach(institute => {
        const card = document.createElement('div');
        card.className = 'institute-card';
    
        const safeValues = {
            name: institute.name || 'Name not provided',
            type: institute.type || 'Type not provided',
            service_offered: institute.service_offered || 'Service not specified',
            location: institute.location || 'Location not provided',
            contact_email: institute.contact_email || 'Email not provided',
            phone_number: institute.phone_number || 'Phone number not provided',
            website: institute.website || '#',
            target_audience: institute.target_audience || 'Target audience not specified',
            cost: institute.cost || 'Cost not specified'
        };
    
        // Render the institute card
        card.innerHTML = `
            <h3>${escapeHtml(safeValues.name)}</h3>
            <p><strong>Type:</strong> ${escapeHtml(safeValues.type)}</p>
            <p><strong>Service Offered:</strong> ${escapeHtml(safeValues.service_offered)}</p>
            <p><strong>Location:</strong> ${escapeHtml(safeValues.location)}</p>
            <p><strong>Contact Email:</strong> ${escapeHtml(safeValues.contact_email)}</p>
            <p><strong>Phone Number:</strong> ${escapeHtml(safeValues.phone_number)}</p>
            ${safeValues.website !== '#' ? `<p><strong>Website:</strong> <a href="${escapeHtml(safeValues.website)}" target="_blank">${escapeHtml(safeValues.website)}</a></p>` : ''}
            <p><strong>Target Audience:</strong> ${escapeHtml(safeValues.target_audience)}</p>
            <p><strong>Cost:</strong> ${escapeHtml(safeValues.cost)}</p>
        `;
        container.appendChild(card);
    });
}

// Updated fetch function with better error handling
document.getElementById('findAllInstitutes').addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/institutes`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Fetched data:', data); // Debug log to see the structure
        displayInstitutes(data);
    } catch (error) {
        console.error('Error:', error);
        const container = document.getElementById('institutes-list');
        container.innerHTML = '<p class="error-message">Failed to fetch institutes. Please try again later.</p>';
    }
});
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

