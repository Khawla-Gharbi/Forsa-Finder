const API_BASE_URL = 'http://127.0.0.1:5000/api/';
// Function to handle all mentors
document.getElementById('findAllMentors').addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/mentors`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch mentors');
        }
        displayMentors(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to fetch mentors');
    }
});


async function searchByExpertise() {
    const expertise = document.getElementById('expertiseInput').value;
    if (!expertise) {
        showError('Please enter an expertise');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/mentors/field/${encodeURIComponent(expertise)}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch mentors by field of expertise');
        }
        displayMentors(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to fetch mentors by field of expertise');
    }
}


async function searchByTypeofMentorship() {
    const mentorship = document.getElementById('mentorshipInput').value;
    if (!mentorship) {
        showError('Please enter a mentorship type');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/mentors/type/${encodeURIComponent(mentorship)}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Failed to fetch mentors by type of mentorship');
        }
        displayMentors(data);
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to fetch mentors by type of mentorship');
    }
}

function displayMentors(mentors) {
    const container = document.getElementById('mentors-list');
    container.innerHTML = '';
    
    if (!Array.isArray(mentors) || mentors.length === 0) {
        container.innerHTML = '<p class="no-results">No mentors found</p>';
        return;
    }
    
    mentors.forEach(mentor => {
        const card = document.createElement('div');
        card.className = 'mentor-card';
        const safeValues = {
            full_name: mentor.full_name || 'Name not provided',
            email: mentor.email || 'Email not provided',
            contact_link: mentor.contact_link || '#',
            field_of_expertise: mentor.field_of_expertise || 'Field not specified',
            previous_attended_program: mentor.previous_attended_program || 'None',
            type_of_mentorship: mentor.type_of_mentorship || 'Type not specified',
            organization: mentor.organization || 'Organization not specified',
            availability: mentor.availability || 'Availability not specified'
        };
        
        card.innerHTML = `
        <h3>${escapeHtml(safeValues.full_name)}</h3>
        <p><strong>Email:</strong> ${escapeHtml(safeValues.email)}</p>
        ${safeValues.contact_link !== '#' ? `<p><strong>Contact:</strong> <a href="${escapeHtml(safeValues.contact_link)}" target="_blank">${escapeHtml(safeValues.contact_link)}</a></p>` : ''}
        <p><strong>Field of Expertise:</strong> ${escapeHtml(safeValues.field_of_expertise)}</p>
        <p><strong>Previously Attended Program:</strong> ${escapeHtml(safeValues.previous_attended_program)}</p>
        <p><strong>Type of Mentorship:</strong> ${escapeHtml(safeValues.type_of_mentorship)}</p>
        <p><strong>Organization:</strong> ${escapeHtml(safeValues.organization)}</p>
        <p><strong>Availability:</strong> ${escapeHtml(safeValues.availability)}</p>
        `;

        
        container.appendChild(card);
    });
}


document.getElementById('findAllmentors').addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/mentors`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Fetched data:', data); 
        displayMentors(data);
    } catch (error) {
        console.error('Error:', error);
        const container = document.getElementById('mentors-list');
        container.innerHTML = '<p class="error-message">Failed to fetch mentors. Please try again later.</p>';
    }
});

function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') {
        unsafe = String(unsafe || ''); 
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

