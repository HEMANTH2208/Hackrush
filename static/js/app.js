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

// Load sample data
function loadScamSample() {
    document.getElementById('jobText').value = scamSample.jobText;
    document.getElementById('companyName').value = scamSample.companyName;
    document.getElementById('recruiterEmail').value = scamSample.recruiterEmail;
    document.getElementById('contactMethod').value = scamSample.contactMethod;
    document.getElementById('offeredSalary').value = scamSample.offeredSalary;
    
    // Show advanced options
    const advancedOptions = document.getElementById('advancedOptions');
    if (!advancedOptions.classList.contains('show')) {
        new bootstrap.Collapse(advancedOptions).show();
    }
    
    showToast('success', 'Scam example loaded! Click "Analyze for Fraud" to see results.');
}

function loadLegitSample() {
    document.getElementById('jobText').value = legitSample.jobText;
    document.getElementById('companyName').value = legitSample.companyName;
    document.getElementById('recruiterEmail').value = legitSample.recruiterEmail;
    document.getElementById('contactMethod').value = legitSample.contactMethod;
    document.getElementById('offeredSalary').value = legitSample.offeredSalary;
    
    // Show advanced options
    const advancedOptions = document.getElementById('advancedOptions');
    if (!advancedOptions.classList.contains('show')) {
        new bootstrap.Collapse(advancedOptions).show();
    }
    
    showToast('success', 'Legitimate example loaded! Click "Analyze for Fraud" to compare.');
}

// Enhanced form submission for email input
document.getElementById('emailAnalysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await analyzeJob('email');
});

// Enhanced form submission for text input
document.getElementById('textAnalysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await analyzeJob('text');
});

// Link analysis form
document.getElementById('linkAnalysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await analyzeJob('link');
});

// WhatsApp analysis form
document.getElementById('whatsappAnalysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await analyzeJob('whatsapp');
});

// Main analysis function
async function analyzeJob(inputType) {
    let formData = { input_type: inputType };
    
    // Validate and collect data based on input type
    if (inputType === 'email') {
        const emailText = document.getElementById('emailText').value.trim();
        const emailSender = document.getElementById('emailSender').value.trim();
        const emailSubject = document.getElementById('emailSubject').value.trim();
        
        if (!emailText) {
            showToast('error', 'Please enter email content');
            return;
        }
        if (emailText.length < 20) {
            showToast('error', 'Email content is too short. Provide more details.');
            return;
        }
        
        // Combine email parts
        let fullEmail = '';
        if (emailSubject) fullEmail += `Subject: ${emailSubject}\n\n`;
        if (emailSender) fullEmail += `From: ${emailSender}\n\n`;
        fullEmail += emailText;
        
        formData.job_text = fullEmail;
        formData.recruiter_email = emailSender;
    } else if (inputType === 'text') {
        const jobText = document.getElementById('jobText').value.trim();
        if (!jobText) {
            showToast('error', 'Please enter job description text');
            return;
        }
        if (jobText.length < 20) {
            showToast('error', 'Job description is too short. Provide more details.');
            return;
        }
        
        formData.job_text = jobText;
        formData.company_name = document.getElementById('companyName').value.trim();
        formData.recruiter_email = document.getElementById('recruiterEmail').value.trim();
        formData.contact_method = document.getElementById('contactMethod').value;
        formData.linkedin_url = document.getElementById('linkedinUrl').value.trim();
        formData.offered_salary = document.getElementById('offeredSalary').value ? 
            parseInt(document.getElementById('offeredSalary').value) : null;
    } else if (inputType === 'link') {
        const jobLink = document.getElementById('jobLink').value.trim();
        if (!jobLink) {
            showToast('error', 'Please enter job posting URL');
            return;
        }
        if (!jobLink.startsWith('http')) {
            showToast('error', 'Please enter a valid URL (starting with http:// or https://)');
            return;
        }
        formData.job_link = jobLink;
    } else if (inputType === 'whatsapp') {
        const whatsappText = document.getElementById('whatsappText').value.trim();
        if (!whatsappText) {
            showToast('error', 'Please enter WhatsApp message');
            return;
        }
        if (whatsappText.length < 20) {
            showToast('error', 'WhatsApp message is too short. Provide more details.');
            return;
        }
        formData.whatsapp_text = whatsappText;
        formData.whatsapp_number = document.getElementById('whatsappNumber').value.trim();
    }
    
    // Hide results, show loading
    document.getElementById('resultsCard').style.display = 'none';
    document.getElementById('loadingCard').style.display = 'block';
    
    // Scroll to loading card
    document.getElementById('loadingCard').scrollIntoView({ behavior: 'smooth', block: 'center' });
    
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
        showToast('error', 'Error: ' + error.message + '. Please try again or train models first.');
    }
}

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
        <div class="risk-score ${riskClass}">
            <div style="font-size: 4rem; font-weight: 900;">${data.risk_score}%</div>
            <div style="font-size: 1.3rem; margin-top: 0.5rem;">${formatRiskTier(data.risk_tier)}</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
                <i class="fas fa-shield-alt me-2"></i>Fraud Probability Score
            </div>
        </div>
        
        <!-- Recommendation with Icon -->
        <div class="recommendation-box ${riskClass}">
            <div class="d-flex align-items-center">
                <i class="fas fa-exclamation-triangle fa-2x me-3"></i>
                <div>
                    <strong style="font-size: 1.1rem;">Recommendation</strong>
                    <p class="mb-0 mt-1">${data.recommendation}</p>
                </div>
            </div>
        </div>
        
        <!-- Download Report Button -->
        <div class="text-center mb-4">
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
            <div class="component-score">
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
                        <p class="mb-0 fw-bold">${(data.ml_result.model || 'Default')}</p>
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
                <div class="rule-match">
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
                <div class="evidence-item ${severityClass}">
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
    
    // Company Verification (MCA + OpenCorporates)
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
                        <p class="mb-0 fw-bold">${cv.company_name || 'N/A'}</p>
                    </div>
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Status</small>
                        <p class="mb-0 fw-bold">${(cv.status || 'N/A')}</p>
                    </div>
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Confidence Score</small>
                        <p class="mb-0 fw-bold text-success">${cv.confidence}%</p>
                    </div>
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Verification Source</small>
                        <p class="mb-0">${(cv.verification_source || cv.source || 'Registry')}</p>
                    </div>
                    ${cv.jurisdiction ? `
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Jurisdiction</small>
                        <p class="mb-0">${cv.jurisdiction}</p>
                    </div>
                    ` : ''}
                    ${cv.indicators && cv.indicators.length > 0 ? `
                    <div class="col-12 mb-2">
                        <small class="text-muted">Indicators</small>
                        <p class="mb-0">${cv.indicators.map(i => `<span class="badge bg-secondary me-1">${i}</span>`).join('')}</p>
                    </div>
                    ` : ''}
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
                    ${(cv.message || 'Company could not be verified in corporate registries')}
                </p>
            `;
        }
        html += `
                </div>
            </div>
        `;
    }
    
    // MCA Verification (if separate from company_verification)
    if (data.mca_verification && data.mca_verification.confidence > 0) {
        html += `
            <h5 class="mb-3">
                <i class="fas fa-landmark me-2"></i>
                MCA (India) Verification
            </h5>
            <div class="card bg-light border-0 mb-4">
                <div class="card-body">
        `;
        const mca = data.mca_verification;
        if (mca.found) {
            html += `
                <p class="mb-2">
                    <span class="verification-status verified">
                        <i class="fas fa-check-circle me-1"></i> Registered with MCA
                    </span>
                </p>
                <div class="row mt-3">
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Company Name</small>
                        <p class="mb-0 fw-bold">${mca.company_name || 'N/A'}</p>
                    </div>
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Confidence</small>
                        <p class="mb-0 fw-bold text-success">${mca.confidence}%</p>
                    </div>
                    ${mca.status ? `
                    <div class="col-md-6 mb-2">
                        <small class="text-muted">Status</small>
                        <p class="mb-0">${mca.status}</p>
                    </div>
                    ` : ''}
                    ${mca.indicators && mca.indicators.length > 0 ? `
                    <div class="col-12 mb-2">
                        <small class="text-muted">Indian Company Indicators</small>
                        <p class="mb-0">${mca.indicators.map(i => `<span class="badge bg-secondary me-1">${i}</span>`).join('')}</p>
                    </div>
                    ` : ''}
                    ${mca.message ? `
                    <div class="col-12 mb-2">
                        <small class="text-muted">Details</small>
                        <p class="mb-0">${mca.message}</p>
                    </div>
                    ` : ''}
                </div>
            `;
        } else {
            html += `
                <p class="mb-2">
                    <span class="verification-status not-verified">
                        <i class="fas fa-times-circle me-1"></i> Not Found in MCA
                    </span>
                </p>
                <p class="text-danger mt-3 mb-0">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${(mca.message || 'Company not registered with Ministry of Corporate Affairs')}
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
            <div class="card bg-light border-0 mb-4">
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
                                    ${data.recruiter_score.trust_level.replace('_', ' ').toUpperCase()}
                                </span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Spam Lines Detection
    if (data.spam_lines && data.spam_lines.length > 0) {
        html += `
            <h5 class="mb-3">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Detected Spam/Scam Lines (${data.spam_lines.length})
            </h5>
            <div class="alert alert-danger">
                <i class="fas fa-info-circle me-2"></i>
                <strong>These lines contain multiple scam indicators and should be treated with extreme caution.</strong>
            </div>
        `;
        
        data.spam_lines.slice(0, 10).forEach((spam, index) => {
            const patterns = spam.patterns.slice(0, 5).join(', ');
            html += `
                <div class="card border-danger mb-3">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="text-danger mb-0">
                                <i class="fas fa-flag me-2"></i>
                                Suspicious Line #${index + 1}
                            </h6>
                            <span class="badge bg-danger">Risk Score: ${spam.score}</span>
                        </div>
                        <p class="mb-2 p-2" style="background: #FFE5E5; border-left: 3px solid #E74C3C; font-family: monospace;">
                            "${spam.line}"
                        </p>
                        <small class="text-muted">
                            <i class="fas fa-search me-1"></i>
                            Matched patterns: <strong>${patterns}</strong>
                        </small>
                    </div>
                </div>
            `;
        });
    }
    
    resultsBody.innerHTML = html;
    resultsCard.style.display = 'block';
    resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Helper functions
function getRiskClass(tier) {
    if (tier.includes('CRITICAL')) return 'bg-danger';
    if (tier.includes('HIGH')) return 'bg-warning';
    if (tier.includes('MODERATE')) return 'bg-warning';
    return 'bg-success';
}

function getRiskScoreClass(tier) {
    if (tier.includes('CRITICAL')) return 'risk-critical';
    if (tier.includes('HIGH')) return 'risk-high';
    if (tier.includes('MODERATE')) return 'risk-moderate';
    return 'risk-low';
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
async function trainModels(event) {
    const btn = event.target;
    const originalHTML = btn.innerHTML;
    
    if (!confirm('This will train ML models with 120 samples (60 scam + 60 legitimate). This may take 30-60 seconds. Continue?')) {
        return;
    }
    
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Training...';
    
    // Update nav status
    document.getElementById('navStatusSpinner').style.display = 'inline-block';
    document.getElementById('navStatusText').textContent = 'Training...';
    
    try {
        const response = await fetch('/train', { method: 'POST' });
        const result = await response.json();
        
        if (response.ok) {
            showToast('success', `Models trained successfully! Best Model: ${result.best_model} | Samples: 120`);
            document.getElementById('navStatusText').textContent = 'Ready ✓';
            document.getElementById('navStatusSpinner').style.display = 'none';
            
            // Hide alert after success
            setTimeout(() => {
                const alert = document.querySelector('#setupAlert .alert');
                if (alert) {
                    alert.classList.add('fade');
                    setTimeout(() => document.getElementById('setupAlert').remove(), 500);
                }
            }, 2000);
        } else {
            throw new Error(result.error || 'Training failed');
        }
    } catch (error) {
        showToast('error', 'Error training models: ' + error.message);
        document.getElementById('navStatusText').textContent = 'Error';
        document.getElementById('navStatusSpinner').style.display = 'none';
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
            document.getElementById('navStatusText').textContent = `Ready ✓`;
            // Hide setup alert if models are loaded
            const setupAlert = document.getElementById('setupAlert');
            if (setupAlert) {
                setupAlert.style.display = 'none';
            }
        }
    } catch (error) {
        console.error('Error checking model status:', error);
    }
});
