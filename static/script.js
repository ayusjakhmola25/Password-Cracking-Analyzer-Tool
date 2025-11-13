// JavaScript to handle tab switching
function showTab(tabId) {
    document.querySelectorAll('.main-nav .nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = 'none';
    });

    const linkElement = document.getElementById(tabId + '-link');
    const contentElement = document.getElementById(tabId + '-content');

    if (linkElement) {
        linkElement.classList.add('active');
    }
    if (contentElement) {
        contentElement.style.display = 'block';
    }
}

// Live password strength calculation
function calculateStrength(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[!@#$%^&*()_+=\-{}[\]:;"\'<,>.?/`~]/.test(password)) score++;

    let strength = 'Weak';
    let color = '#ff5f75'; // Red
    let width = '20%';

    if (score >= 5) {
        strength = 'Strong';
        color = '#25d996'; // Green
        width = '100%';
    } else if (score >= 3) {
        strength = 'Moderate';
        color = '#ffc241'; // Orange
        width = '60%';
    }

    return { strength, color, width };
}

// Update progress bar and text
function updateStrength() {
    const password = document.getElementById('analyze_password').value;
    const progressFill = document.getElementById('progress-fill');
    const strengthText = document.getElementById('strength-text');

    if (password.length === 0) {
        // Hide progress bar and text when no password is entered--
        progressFill.style.width = '0%';
        strengthText.textContent = '';
        return;
    }

    const { strength, color, width } = calculateStrength(password);

    progressFill.style.width = width;
    progressFill.style.backgroundColor = color;
    strengthText.textContent = `Strength: ${strength}`;
}

// Render chart for search attempts
function renderChart() {
    const chartCanvas = document.getElementById('attemptsChart');
    if (!chartCanvas) return;

    const ctx = chartCanvas.getContext('2d');
    const linearAttempts = parseInt(chartCanvas.dataset.linear || 0);
    const binaryAttempts = parseInt(chartCanvas.dataset.binary || 0);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Linear Search', 'Binary Search'],
            datasets: [{
                label: 'Attempts',
                data: [linearAttempts, binaryAttempts],
                backgroundColor: ['#ff5f75', '#00c0e7'],
                borderColor: ['#ff5f75', '#00c0e7'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Get initial tab from data attribute
    const initialTab = document.body.dataset.initialTab || 'search';
    showTab(initialTab);

    // Add event listener for live strength
    const passwordInput = document.getElementById('analyze_password');
    if (passwordInput) {
        passwordInput.addEventListener('input', updateStrength);
    }

    // Render chart if on search tab and canvas exists
    if (initialTab === 'search' && document.getElementById('attemptsChart')) {
        renderChart();
    }
});
