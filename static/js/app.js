// Enhanced Sample data for testing
const scamSample = {
    jobText: "🎉 CONGRATULATIONS! You are SELECTED for Google India! 💼\n\nPosition: Software Engineer\nSalary: 25 LPA for FRESHERS! 🤑\n\n⚠️ URGENT: Pay Rs 5000 registration fee within 24 HOURS to confirm your joining!\n\n📱 Contact ONLY via WhatsApp: +91-9876543210\n\nDon't miss this GOLDEN opportunity! Limited seats available! ⏰",
    companyName: "Google India",
    recruiterEmail: "hr.google.recruitment@gmail.com",
    contactMethod: "whatsapp",
    offeredSalary: 2500
};

const legitSample = {
    jobText: "Dear Candidate,\n\nWe are pleased to inform you that your application for the Software Engineer position at Infosys Limited has been shortlisted.\n\nWe would like to invite you for an interview at our Bangalore office:\n\nDate: 25th January 2024\nTime: 10:00 AM\nVenue: Infosys Campus, Electronics City, Bangalore\n\nPlease bring the following documents:\n- Updated resume\n- Educational certificates\n- Valid photo ID proof\n- Passport size photographs\n\nOur HR team will contact you via email with further details and interview schedule.\n\nBest regards,\nHR Team\nInfosys Limited",
    companyName: "Infosys Limited",
    recruiterEmail: "recruitment@infosys.com",
    contactMethod: "email",
    offeredSalary: 600
};

// Toast notification helper
function showToast(type, message) {
    const toastId = type === 'success' ? 'successToast' : 'errorToast';
    const messageId = type === 'success' ? 'successMessage' : 'errorMessage';
    
    document.getElementById(messageId).textContent = message;
    const toast = new bootstrap.Toast(document.getElementById(toastId));
    toast.show();
}

// Load sample data with animation
function loadScamSample() {
    const form = document.getElementById('analysisForm');
    form.classList.add('animate__animated', 'animate__pulse');
    
    document.getElementById('jobText').value = scamSample.jobText;
    document.getElementById('companyName').value = scamSample.companyName;
    document.getElementById('recruiterEmail').value = scamSample.recruiterEmail;
    document.getElementById('contactMethod').value = scamSample.contactMethod;
    document.getElementById('offeredSalary').value = scamSample.offeredSalary;
    
    setTimeout(() => {
        form.classList.remove('animate__animated', 'animate__pulse');
    }, 1000);
    
    showToast('success', 'Scam example loaded! Click "Analyze for Fraud" to see results.');
}

function loadLegitSample() {
    const form = document.getElementById('analysisForm');
    form.classList.add('animate__animated', 'animate__pulse');
    
    document.getElementById('jobText').value = legitSample.jobText;
    document.getElementById('companyName').value = legitSample.companyName;
    document.getElementById('recruiterEmail').value = legitSample.recruiterEmail;
    document.getElementById('contactMethod').value = legitSample.contactMethod;
    document.getElementById('offeredSalary').value = legitSample.offeredSalary;
    
    setTimeout(() => {
        form.classList.remove('animate__animated', 'animate__pulse');
    }, 1000);
    
    showToast('success', 'Legitimate example loaded! Click "Analyze for Fraud" to compare.');
}

// Enhanced form submission with better error handling
document.getElementById('analysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Validate job text
    const jobText = document.getElementById('jobText').value.trim();
    if (!jobText) {
        showToast('error', 'Please enter job description text');
        return;
    }
    
    if (jobText.length < 20) {
        showToast('error', 'Job description is too short. Please provide more details.');
        return;
    }
    
    // Hide placeholder and results, show loading
    document.getElementById('placeholderCard').style.display = 'none';
    document.getElementById('resultsCard').style.display = 'none';
    document.getElementById('loadingCard').style.display = 'block';
    
    // Scroll to results
    document.getElementById('loadingCard').scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Collect form data
    const formData = {
        job_text: jobText,
        company_name: document.getElementById('companyName').value.trim(),
        recruiter_email: document.getElementById('recruiterEmail').value.trim(),
        contact_method: document.getElementById('contactMethod').value,
        linkedin_url: document.getElementById('linkedinUrl').value.trim(),
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
            showToast('success', 'Analysis complete! Check the results below.');
        } else {
            throw new Error(result.error || 'Analysis failed');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loadingCard').style.display = 'none';
        document.getElementById('placeholderCard').style.display = 'block';
        showToast('error', 'Error: ' + error.message + '. Please try again or train models first.');
    }
});

// Enhanced results display with animations
function displayResults(data) {
    document.getElementById('loadingCard').style.display = 'none';
    
    const resultsCard = document.getElementById('resultsCard');
    const resultsHeader = document.getElementById('resultsHeader');
    const resultsBody = document.getElementById('resultsBody');
    
    // Set header color based on risk
    const riskClass = getRiskClass(data.risk_tier);
    resultsHeader.className = `card-header text-white ${riskClass}`;
    
    // Build enhanced results HTML
    let html = `
        <!-- Risk Score with Animation -->
        <div class="risk-score ${riskClass} animate__animated animate__zoomIn">
            <div style="font-size: 4rem; font-weight: 900;">${data.risk_score}%</div>
            <div style="font-size: 1.3rem; margin-top: 0.5rem;">${formatRiskTier(data.risk_tier)}</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
                <i class="fas fa-shield-alt me-2"></i>Fraud Probability Score
            </div>
        </div>
        
        <!-- Recommendation with Icon -->
        <div class="recommendation-box ${riskClass} animate__animated animate__fadeIn">
            <div class="d-flex align-items-center">
                <i class="fas fa-exclamation-triangle fa-2x me-3"></i>
                <div>
                    <strong style="font-size: 1.1rem;">Recommendation</strong>
                    <p class="mb-0 mt-1">${data.recommendation}</p>
                </div>
            </div>
        </div>
        
        <!-- Download Report Button -->
        <div class="text-center mb-4 animate__animated animate__fadeIn animate__delay-1s">
            <a href="/download/${data.pdf_report}" class="btn btn-lg btn-dark">
                <i class="fas fa-file-pdf me-2"></i> Download Forensic Report
            </a>
        </div>
        
        <div class="section-divider"></div>
        
        <!-- Component Scores -->
        <h5 class="mb-3">
            <i class="fas fa-chart-pie me-2"></i>
            Risk Component Breakdown
        </h5>
        <div class="mb-4">
    `;
    
    // Component scores with progress bars
    const components = [
        { key: 'ml_probability', icon: 'robot', label: 'ML Model Detection' },
        { key: 'rule_score', icon: 'flag', label: 'Fraud Pattern Match' },
        { key: 'company_risk', icon: 'building', label: 'Company Risk' },
        { key: 'salary_anomaly', icon: 'money-bill-wave', label: 'Salary Anomaly' },
        { key: 'recruiter_risk', icon: 'user-tie', label: 'Recruiter Risk' }
    ];
    
    components.forEach(comp => {
        const score = data.component_scores[comp.key] || 0;
        const percentage = score;
        const barClass = percentage > 70 ? 'bg-danger' : percentage > 40 ? 'bg-warning' : 'bg-success';
        
        html += `
            <div class="component-score animate__animated animate__fadeInLeft">
                <span>
                    <i class="fas fa-${comp.icon} me-2"></i>
                    ${comp.label}
                </span>
                <span><strong>${score.toFixed(1)}%</strong></span>
            </div>
            <div class="progress mb-3">
                <div class="progress-bar ${barClass}" 
                     role="progressbar" 
                     style="width: ${percentage}%"
                     aria-valuenow="${percentage}" 
                     aria-valuemin="0" 
                     aria-valuemax="100">
                    ${percentage.toFixed(0)}%
                </div>
            </div>
        `;
    });
    
    html += `</div><div class="section-divider"></div>`;
    
    // ML Model Result
    html += `
        <h5 class="mb-3">
            <i class="fas fa-robot me-2"></i>
            AI Model Detection
        </h5>
        <div class="card bg-light border-0 mb-4">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4 mb-2">
                        <small class="text-muted">Model Used</small>
                        <p class="mb-0 fw-bold">${data.ml_result.model || 'Default'}</p>
                    </div>
                    <div class="col-md-4 mb-2">
                        <small class="text-muted">Scam Probability</small>
                        <p class="mb-0 fw-bold text-danger">${data.ml_result.probability}%</p>
                    </div>
                    <div class="col-md-4 mb-2">
                        <small class="text-muted">Confidence Level</small>
                        <p class="mb-0">
                            <span class="badge ${getConfidenceBadge(data.ml_result.confidence)}">
                                ${data.ml_result.confidence.toUpperCase()}
                            </span>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Triggered Rules
    if (data.triggered_rules && data.triggered_rules.length > 0) {
        html += `
            <h5 class="mb-3">
                <i class="fas fa-flag me-2"></i>
                Fraud Pattern Matches (${data.triggered_rules.length})
            </h5>
        `;
        data.triggered_rules.forEach((rule, index) => {
            html += `
                <div class="rule-match animate__animated animate__fadeInUp" style="animation-delay: ${index * 0.1}s">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${formatComponentName(rule.category)}</strong>
                            <p class="mb-0 mt-1 small">"${rule.pattern}"</p>
                        </div>
                        <span class="badge bg-danger">Severity: ${rule.severity}</span>
                    </div>
                </div>
            `;
        });
        html += `<div class="section-divider"></div>`;
    }
    
    // Explanations
    if (data.explanations && data.explanations.length > 0) {
        html += `
            <h5 class="mb-3">
                <i class="fas fa-lightbulb me-2"></i>
                Risk Factors Explained (${data.explanations.length})
            </h5>
        `;
        data.explanations.forEach((exp, index) => {
            const severityClass = exp.severity === 'high' ? 'evidence-high' : 
                                 exp.severity === 'medium' ? 'evidence-medium' : 'evidence-low';
            const severityIcon = exp.severity === 'high' ? 'exclamation-circle' : 
                                exp.severity === 'medium' ? 'exclamation-triangle' : 'info-circle';
            
            html += `
                <div class="evidence-item ${severityClass} animate__animated animate__fadeInRight" style="animation-delay: ${index * 0.1}s">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <strong>
                                <i class="fas fa-${severityIcon} me-2"></i>
                                ${exp.factor}
                            </strong>
                            <p class="mb-0 mt-2">${exp.detail}</p>
                        </div>
                        <span class="badge bg-secondary ms-2">${exp.severity.toUpperCase()}</span>
                    </div>
                </div>
            `;
        });
        html += `<div class="section-divider"></div>`;
    }
    
    // Company Verification
    if (data.company_verification) {
        html += `
            <h5 class="mb-3">
                <i class="fas fa-building me-2"></i>
                Company Verification
            </h5>
            <div class="card bg-light border-0 mb-4">
                <div class="card-body">
        `;
        const cv = data.company_verification;
        if (cv.found) {
            html += `
                <p class="mb-2">
                    <span class="verification-status verified">
                        <i class="fas fa-check-circle me-1"></i> Company Found in Registry
                    </span>
                </p>
                <div class="row mt-3">
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Company Name</small>
                        <p class="mb-0 fw-bold">${cv.company_name}</p>
                    </div>
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Status</small>
                        <p class="mb-0 fw-bold">${cv.status || 'N/A'}</p>
                    </div>
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Confidence Score</small>
                        <p class="mb-0 fw-bold text-success">${cv.confidence}%</p>
                    </div>
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Jurisdiction</small>
                        <p class="mb-0">${cv.jurisdiction || 'N/A'}</p>
                    </div>
                </div>
            `;
        } else {
            html += `
                <p class="mb-2">
                    <span class="verification-status not-verified">
                        <i class="fas fa-times-circle me-1"></i> Company Not Found
                    </span>
                </p>
                <p class="text-danger mt-3 mb-0">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${cv.message || 'Company could not be verified in corporate registries'}
                </p>
            `;
        }
        html += `
                </div>
            </div>
        `;
    }
    
    // Salary Analysis
    if (data.salary_analysis && data.salary_analysis.offered_salary) {
        html += `
            <h5 class="mb-3">
                <i class="fas fa-money-bill-wave me-2"></i>
                Salary Analysis
            </h5>
            <div class="card bg-light border-0 mb-4">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-3 mb-2">
                            <small class="text-muted">Offered Salary</small>
                            <p class="mb-0 fw-bold">₹${data.salary_analysis.offered_salary}k/year</p>
                        </div>
                        <div class="col-md-3 mb-2">
                            <small class="text-muted">Job Level</small>
                            <p class="mb-0 fw-bold">${data.salary_analysis.job_level.toUpperCase()}</p>
                        </div>
                        <div class="col-md-3 mb-2">
                            <small class="text-muted">Market Range</small>
                            <p class="mb-0 fw-bold">₹${data.salary_analysis.benchmark_range}</p>
                        </div>
                        <div class="col-md-3 mb-2">
                            <small class="text-muted">Anomaly Score</small>
                            <p class="mb-0 fw-bold ${data.salary_analysis.anomaly_score > 50 ? 'text-danger' : 'text-success'}">
                                ${data.salary_analysis.anomaly_score}%
                            </p>
                        </div>
                    </div>
                    ${data.salary_analysis.message ? `
                        <div class="alert alert-warning mt-3 mb-0">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            ${data.salary_analysis.message}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    // Recruiter Score
    if (data.recruiter_score) {
        html += `
            <h5 class="mb-3">
                <i class="fas fa-user-tie me-2"></i>
                Recruiter Trust Assessment
            </h5>
            <div class="card bg-light border-0">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-2">
                            <small class="text-muted">Trust Score</small>
                            <p class="mb-0 fw-bold">${data.recruiter_score.trust_score}%</p>
                        </div>
                        <div class="col-md-6 mb-2">
                            <small class="text-muted">Trust Level</small>
                            <p class="mb-0">
                                <span class="badge ${getTrustBadge(data.recruiter_score.trust_level)}">
                                    ${data.recruiter_score.trust_level.replace('_', ' ')}
                                </span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    resultsBody.innerHTML = html;
    resultsCard.style.display = 'block';
    resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

function getConfidenceBadge(confidence) {
    if (confidence === 'high') return 'bg-success';
    if (confidence === 'medium') return 'bg-warning';
    return 'bg-secondary';
}

function getTrustBadge(level) {
    if (level.includes('HIGH')) return 'bg-success';
    if (level.includes('MODERATE')) return 'bg-info';
    if (level.includes('LOW')) return 'bg-warning';
    return 'bg-danger';
}

// Enhanced train models function
async function trainModels() {
    const btn = event.target;
    const originalHTML = btn.innerHTML;
    
    if (!confirm('This will train ML models with sample data. This may take 10-30 seconds. Continue?')) {
        return;
    }
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Training Models...';
    
    // Update status
    document.getElementById('statusSpinner').style.display = 'inline-block';
    document.getElementById('statusText').textContent = 'Training...';
    
    try {
        const response = await fetch('/train', { method: 'POST' });
        const result = await response.json();
        
        if (response.ok) {
            showToast('success', `Models trained successfully! Best Model: ${result.best_model}`);
            document.getElementById('statusText').textContent = 'Trained ✓';
            document.getElementById('statusSpinner').style.display = 'none';
            document.getElementById('modelStatus').classList.remove('bg-secondary');
            document.getElementById('modelStatus').classList.add('bg-success');
            
            // Hide alert after success
            setTimeout(() => {
                const alert = document.querySelector('.alert-info');
                if (alert) {
                    alert.classList.add('animate__animated', 'animate__fadeOut');
                    setTimeout(() => alert.remove(), 1000);
                }
            }, 2000);
        } else {
            throw new Error(result.error || 'Training failed');
        }
    } catch (error) {
        showToast('error', 'Error training models: ' + error.message);
        document.getElementById('statusText').textContent = 'Failed ✗';
        document.getElementById('statusSpinner').style.display = 'none';
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalHTML;
    }
}

// Check model status on page load
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/health');
        const result = await response.json();
        
        if (result.ml_model_loaded) {
            document.getElementById('statusText').textContent = `Trained ✓ (${result.model_name})`;
            document.getElementById('modelStatus').classList.remove('bg-secondary');
            document.getElementById('modelStatus').classList.add('bg-success');
        }
    } catch (error) {
        console.error('Error checking model status:', error);
    }
});
