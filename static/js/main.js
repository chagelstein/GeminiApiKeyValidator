// Main JavaScript for Gemini API Key Tester

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initPasswordToggle();
    initFormSubmission();
    initTooltips();
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

/**
 * Initialize password toggle functionality
 */
function initPasswordToggle() {
    const toggleButton = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('api_key');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (toggleButton && passwordInput && toggleIcon) {
        toggleButton.addEventListener('click', function() {
            // Toggle password visibility
            const isPassword = passwordInput.type === 'password';
            passwordInput.type = isPassword ? 'text' : 'password';
            
            // Update icon
            toggleIcon.className = isPassword ? 'fas fa-eye-slash' : 'fas fa-eye';
            
            // Update button title
            toggleButton.title = isPassword ? 'Hide API key' : 'Show API key';
        });
    }
}

/**
 * Initialize form submission with loading states
 */
function initFormSubmission() {
    const form = document.getElementById('testForm');
    const button = document.getElementById('testButton');
    const buttonText = document.getElementById('buttonText');
    const buttonSpinner = document.getElementById('buttonSpinner');
    
    if (form && button && buttonText && buttonSpinner) {
        form.addEventListener('submit', function(e) {
            // Show loading state
            button.disabled = true;
            button.classList.add('loading');
            buttonText.textContent = 'Testing...';
            buttonSpinner.classList.remove('d-none');
            
            // Validate API key format
            const apiKey = document.getElementById('api_key').value.trim();
            if (!validateApiKey(apiKey)) {
                e.preventDefault();
                showError('Please enter a valid API key.');
                resetButton();
                return;
            }
        });
    }
}

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Validate API key format
 * @param {string} apiKey - The API key to validate
 * @returns {boolean} - Whether the API key appears valid
 */
function validateApiKey(apiKey) {
    // Basic validation: not empty, minimum length, no spaces
    if (!apiKey || apiKey.length < 30 || apiKey.includes(' ')) {
        return false;
    }
    
    // Check if it starts with expected prefix (Google API keys often start with specific patterns)
    // This is a basic check and may need adjustment based on actual Gemini API key format
    return true;
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    // Remove existing error alerts
    const existingAlerts = document.querySelectorAll('.alert-danger');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new error alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert before the form
    const form = document.getElementById('testForm');
    if (form && form.parentNode) {
        form.parentNode.insertBefore(alertDiv, form.parentNode.firstChild);
    }
}

/**
 * Reset button to original state
 */
function resetButton() {
    const button = document.getElementById('testButton');
    const buttonText = document.getElementById('buttonText');
    const buttonSpinner = document.getElementById('buttonSpinner');
    
    if (button && buttonText && buttonSpinner) {
        button.disabled = false;
        button.classList.remove('loading');
        buttonText.textContent = 'Test API Key';
        buttonSpinner.classList.add('d-none');
    }
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        // Show success message
        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-success border-0 position-fixed top-0 end-0 m-3';
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-check me-2"></i>
                    Copied to clipboard!
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        document.body.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }).catch(function(err) {
        console.error('Failed to copy text: ', err);
    });
}

/**
 * Format API key for display (mask sensitive parts)
 * @param {string} apiKey - The API key to format
 * @returns {string} - Formatted API key
 */
function formatApiKey(apiKey) {
    if (!apiKey || apiKey.length <= 12) {
        return '*'.repeat(apiKey ? apiKey.length : 0);
    }
    
    return apiKey.substring(0, 8) + '*'.repeat(apiKey.length - 12) + apiKey.substring(apiKey.length - 4);
}

/**
 * Auto-resize textarea based on content
 * @param {HTMLTextAreaElement} textarea - The textarea element
 */
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Add click handlers for any copy buttons that might be added dynamically
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('copy-btn')) {
        const textToCopy = e.target.getAttribute('data-copy');
        if (textToCopy) {
            copyToClipboard(textToCopy);
        }
    }
});

// Handle form validation on input
document.addEventListener('input', function(e) {
    if (e.target.id === 'api_key') {
        const apiKey = e.target.value.trim();
        const feedback = document.querySelector('.invalid-feedback');
        
        if (apiKey && !validateApiKey(apiKey)) {
            e.target.classList.add('is-invalid');
            if (!feedback) {
                const feedbackDiv = document.createElement('div');
                feedbackDiv.className = 'invalid-feedback';
                feedbackDiv.textContent = 'Please enter a valid API key (minimum 30 characters, no spaces).';
                e.target.parentNode.appendChild(feedbackDiv);
            }
        } else {
            e.target.classList.remove('is-invalid');
            if (feedback) {
                feedback.remove();
            }
        }
    }
});
