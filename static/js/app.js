// Sample data for testing
const scamSample = {
    jobText: "Congratulations! You are selected for Google. Salary 25 LPA for freshers. Pay Rs 5000 registration fee to confirm your joining within 24 hours. Contact via WhatsApp only: +91-9876543210. Urgent joining required!",
    companyName: "Google",
    recruiterEmail: "hr.google@gmail.com",
    contactMethod: "whatsapp",
    offeredSalary: 2500
};

const legitSample = {
    jobText: "We are pleased to inform you that your application for Software Engineer position has been shortlisted. We would like to invite you for an interview at our Bangalore office on 25th January at 10:00 AM. Please bring your resume, certificates, and a valid ID proof. Our HR team will contact you via email with further details.",
    companyName: "Infosys",
    recruiterEmail: "recruitment@infosys.com",
    contactMethod: "email",
    offeredSalary: 600
};

// Load sample data
function loadScamSample() {
    document.getElementById('jobText').value = scamSample.jobText;
    document.getElementById('companyName').value = scamSample.companyName;
    document.getElementById('recruiterEmail').value = scamSample.recruiterEmail;
    document.getElementById('contactMethod').value = scamSample.contactMethod;
    document.getElementById('offeredSalary').value = scamSample.offeredSalary;
}

function loadLegitSample() {
    document.getElementById('jobText').value = legitSample.jobText;
    document.getElementById('companyName').value = legitSample.companyName;
    document.getElementById('recruiterEmail').value = legitSample.recruiterEmail;
    document.getElementById('contactMethod').value = legitSample.contactMethod;
    document.getElementById('offeredSalary').value = legitSample.offeredSalary;
}

// Form submission
document.getElementById('analysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading
    document.getElementById('resultsCard').style.display = 'none';
    document.getElementById('loadingCard').style.display = 'block';
    
    // Collect form data
    const formData = {
        job_text: document.getElementById('jobText').value,
        company_name: document.getElementById('companyName').value,
        recruiter_email: document.getElementById('recruiterEmail').value,
        contact_method: document.getElementById('contactMethod').value,
        linkedin_url: document.getElementById('linkedinUrl').value,
        offered_salary: document.getElementById('offeredSalary').value ? 
            parseInt(document.getElementById('offeredSalary').value) : null
    };
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResults(result);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error analyzing job posting: ' + error.message);
    } finally {
        document.getElementById('loadingCard').style.display = 'none';
    }
});

// Display results
function displayResults(data) {
    const resultsCard = document.getElementById('resultsCard');
    const resultsHeader = document.getElementById('resultsHeader');
    const resultsBody = document.getElementById('resultsBody');
    
    // Set header color based on risk
    const riskClass = getRiskClass(data.risk_tier);
    resultsHeader.className = `card-header text-white ${riskClass}`;
    
    // Build results HTML
    let html = `
        <!-- Risk Score -->
        <div class="risk-score ${riskClass}">
            <div>${data.risk_score}%</div>
            <div style="font-size: 1.2rem;">${formatRiskTier(data.risk_tier)}</div>
        </div>
        
        <!-- Recommendation -->
        <div class="recommendation-box ${riskClass}">
            <i class="fas fa-exclamation-triangle"></i>
            <strong>Recommendation:</strong> ${data.recommendation}
        </div>
        
        <!-- Download Report -->
        <div class="text-center mb-3">
            <a href="/download/${data.pdf_report}" class="btn btn-download">
                <i class="fas fa-file-pdf"></i> Download Forensic Report
            </a>
        </div>
        
        <div class="section-divider"></div>
        
        <!-- Component Scores -->
        <h6><i class="fas fa-chart-pie"></i> Risk Component Breakdown</h6>
        <div class="mb-3">
    `;
    
    for (const [component, score] of Object.entries(data.component_scores)) {
        const percentage = score;
        const barClass = percentage > 70 ? 'bg-danger' : percentage > 40 ? 'bg-warning' : 'bg-success';
        html += `
            <div class="component-score">
                <span>${formatComponentName(component)}</span>
                <span><strong>${score.toFixed(1)}%</strong></span>
            </div>
            <div class="progress mb-2">
                <div class="progress-bar ${barClass}" style="width: ${percentage}%"></div>
            </div>
        `;
    }
    
    html += `</div><div class="section-divider"></div>`;
    
    // ML Model Result
    html += `
        <h6><i class="fas fa-robot"></i> ML Model Detection</h6>
        <p>Model: <strong>${data.ml_result.model || 'Default'}</strong></p>
        <p>Scam Probability: <strong>${data.ml_result.probability}%</strong></p>
        <p>Confidence: <span class="badge bg-info">${data.ml_result.confidence}</span></p>
        <div class="section-divider"></div>
    `;
    
    // Triggered Rules
    if (data.triggered_rules && data.triggered_rules.length > 0) {
        html += `<h6><i class="fas fa-flag"></i> Fraud Pattern Matches</h6>`;
        data.triggered_rules.forEach(rule => {
            html += `
                <div class="rule-match">
                    <strong>${formatComponentName(rule.category)}</strong>: "${rule.pattern}"
                    <span class="badge bg-danger float-end">Severity: ${rule.severity}</span>
                </div>
            `;
        });
        html += `<div class="section-divider"></div>`;
    }
    
    // Explanations
    if (data.explanations && data.explanations.length > 0) {
        html += `<h6><i class="fas fa-lightbulb"></i> Risk Factors Explained</h6>`;
        data.explanations.forEach(exp => {
            const severityClass = exp.severity === 'high' ? 'evidence-high' : 
                                 exp.severity === 'medium' ? 'evidence-medium' : 'evidence-low';
            html += `
                <div class="evidence-item ${severityClass}">
                    <strong>${exp.factor}</strong>
                    <span class="badge bg-secondary float-end">${exp.severity}</span>
                    <p class="mb-0 mt-1">${exp.detail}</p>
                </div>
            `;
        });
        html += `<div class="section-divider"></div>`;
    }
    
    // Company Verification
    if (data.company_verification) {
        html += `<h6><i class="fas fa-building"></i> Company Verification</h6>`;
        const cv = data.company_verification;
        if (cv.found) {
            html += `
                <p><span class="verification-status verified">✓ Company Found</span></p>
                <p>Name: <strong>${cv.company_name}</strong></p>
                <p>Status: <strong>${cv.status || 'N/A'}</strong></p>
                <p>Confidence: <strong>${cv.confidence}%</strong></p>
            `;
        } else {
            html += `
                <p><span class="verification-status not-verified">✗ Company Not Found</span></p>
                <p>${cv.message}</p>
            `;
        }
        html += `<div class="section-divider"></div>`;
    }
    
    // Salary Analysis
    if (data.salary_analysis && data.salary_analysis.offered_salary) {
        html += `<h6><i class="fas fa-money-bill-wave"></i> Salary Analysis</h6>`;
        const sa = data.salary_analysis;
        html += `
            <p>Offered: <strong>₹${sa.offered_salary}k/year</strong></p>
            <p>Job Level: <strong>${sa.job_level}</strong></p>
            <p>Market Range: <strong>₹${sa.benchmark_range}</strong></p>
            <p>Anomaly Score: <strong>${sa.anomaly_score}%</strong></p>
            ${sa.message ? `<p class="text-warning">${sa.message}</p>` : ''}
            <div class="section-divider"></div>
        `;
    }
    
    // Recruiter Score
    if (data.recruiter_score) {
        html += `<h6><i class="fas fa-user-tie"></i> Recruiter Trust Score</h6>`;
        const rs = data.recruiter_score;
        html += `
            <p>Trust Score: <strong>${rs.trust_score}%</strong></p>
            <p>Trust Level: <span class="badge bg-info">${rs.trust_level.replace('_', ' ')}</span></p>
        `;
    }
    
    resultsBody.innerHTML = html;
    resultsCard.style.display = 'block';
}

// Helper functions
function getRiskClass(tier) {
    if (tier.includes('CRITICAL')) return 'risk-critical bg-danger';
    if (tier.includes('HIGH')) return 'risk-high bg-warning';
    if (tier.includes('MODERATE')) return 'risk-moderate bg-warning';
    return 'risk-low bg-success';
}

function formatRiskTier(tier) {
    return tier.replace(/_/g, ' ');
}

function formatComponentName(name) {
    return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Train models
async function trainModels() {
    if (!confirm('This will train ML models with sample data. Continue?')) return;
    
    const btn = event.target;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Training...';
    
    try {
        const response = await fetch('/train', { method: 'POST' });
        const result = await response.json();
        
        if (response.ok) {
            alert('Models trained successfully!\nBest Model: ' + result.best_model);
            location.reload();
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error training models: ' + error.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-brain"></i> Train Models';
    }
}
