/**
 * StudyForge Frontend JavaScript
 * Handles UI interactions and API communication
 */

// Configuration
const API_BASE_URL = 'http://localhost:5001';

// Global State
let selectedTemplate = null;
let currentAnalysisId = null;
let templates = [];

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 StudyForge initialized');
    loadTemplates();
    setupEventListeners();
});

/**
 * Load templates from API
 */
async function loadTemplates() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/templates`);
        const data = await response.json();

        if (data.status === 'success') {
            templates = data.templates;
            renderTemplates(templates);
        } else {
            showToast('Failed to load templates', 'error');
        }
    } catch (error) {
        console.error('Error loading templates:', error);
        showToast('Unable to connect to server. Make sure Flask is running on port 5000.', 'error');
        // Show fallback templates
        renderFallbackTemplates();
    }
}

/**
 * Render templates in the grid
 */
function renderTemplates(templatesData) {
    const grid = document.getElementById('templates-grid');
    grid.innerHTML = '';

    templatesData.forEach(template => {
        const card = createTemplateCard(template);
        grid.appendChild(card);
    });
}

/**
 * Create a template card element
 */
function createTemplateCard(template) {
    const card = document.createElement('div');
    card.className = 'template-card bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition cursor-pointer card-shine fade-in';
    card.onclick = () => selectTemplate(template.id);

    card.innerHTML = `
        <div class="text-5xl mb-4">${template.icon_emoji}</div>
        <h4 class="text-xl font-bold text-gray-900 mb-2">${template.name}</h4>
        <p class="text-gray-600 mb-4 text-sm">${template.description}</p>
        <div class="mb-4">
            <span class="template-badge bg-indigo-100 text-indigo-700">
                ${template.sections ? template.sections.length : 0} Sections
            </span>
        </div>
        <div class="bg-gray-50 rounded-lg p-3 mb-4">
            <p class="text-xs text-gray-500 mb-1">Example Use Case:</p>
            <p class="text-sm text-gray-700">${template.example_use_case}</p>
        </div>
        <button class="w-full py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg transition btn-ripple">
            Use This Template
        </button>
    `;

    return card;
}

/**
 * Render fallback templates if API fails
 */
function renderFallbackTemplates() {
    const fallbackTemplates = [
        {
            id: 'lecture-digest',
            name: 'Lecture Digest',
            icon_emoji: '📚',
            description: 'Transform lengthy university lectures into concise summaries',
            example_use_case: 'Converting 2-hour economics lecture notes',
            sections: ['Key Concepts', 'Definitions', 'Summary']
        },
        {
            id: 'case-study-analyzer',
            name: 'Case Study Analyzer',
            icon_emoji: '💼',
            description: 'Break down business cases into actionable insights',
            example_use_case: 'Analyzing Harvard Business School cases',
            sections: ['Problem', 'Analysis', 'Solutions']
        },
        {
            id: 'concept-mapper',
            name: 'Concept Mapper',
            icon_emoji: '🧠',
            description: 'Extract and organize technical concepts',
            example_use_case: 'Technical documentation study guides',
            sections: ['Concepts', 'Examples', 'Best Practices']
        },
        {
            id: 'exam-prep-sprint',
            name: 'Exam Prep Sprint',
            icon_emoji: '🎯',
            description: 'Focused exam preparation materials',
            example_use_case: 'Last-minute final exam review',
            sections: ['Topics', 'Formulas', 'Practice Questions']
        }
    ];
    renderTemplates(fallbackTemplates);
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

function setupEventListeners() {
    // Character counter for textarea
    const contentInput = document.getElementById('content-input');
    if (contentInput) {
        contentInput.addEventListener('input', function() {
            const charCount = this.value.length;
            document.getElementById('char-count').textContent = `${charCount} characters`;
        });
    }

    // Close modals on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeModal();
            closePreview();
        }
    });

    // Close modals when clicking outside
    const uploadModal = document.getElementById('upload-modal');
    const previewModal = document.getElementById('preview-modal');

    if (uploadModal) {
        uploadModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
    }

    if (previewModal) {
        previewModal.addEventListener('click', function(e) {
            if (e.target === this) {
                closePreview();
            }
        });
    }
}

// ============================================================================
// TEMPLATE SELECTION
// ============================================================================

/**
 * Select a template and open upload modal
 */
function selectTemplate(templateId) {
    const template = templates.find(t => t.id === templateId);
    if (!template) {
        console.error('Template not found:', templateId);
        return;
    }

    selectedTemplate = template;
    console.log('📋 Selected template:', template.name);

    // Update modal with template info
    document.getElementById('modal-template-emoji').textContent = template.icon_emoji;
    document.getElementById('modal-template-name').textContent = template.name;
    document.getElementById('modal-template-description').textContent = template.description;

    // Open the modal
    openModal();
}

/**
 * Show custom template modal (no template pre-selected)
 */
function showCustomModal() {
    selectedTemplate = null;
    document.getElementById('modal-template-emoji').textContent = '✨';
    document.getElementById('modal-template-name').textContent = 'Custom Study Guide';
    document.getElementById('modal-template-description').textContent = 'Our AI will analyze your content and choose the best structure';

    openModal();
}

// ============================================================================
// MODAL CONTROLS
// ============================================================================

function openModal() {
    const modal = document.getElementById('upload-modal');
    modal.classList.remove('hidden');
    modal.classList.add('flex', 'modal-show');
    document.body.style.overflow = 'hidden';

    // Clear previous content
    document.getElementById('content-input').value = '';
    document.getElementById('char-count').textContent = '0 characters';
    hideProgress();
}

function closeModal() {
    const modal = document.getElementById('upload-modal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
    document.body.style.overflow = 'auto';
    hideProgress();
}

function openPreview() {
    const modal = document.getElementById('preview-modal');
    modal.classList.remove('hidden');
    modal.classList.add('flex', 'modal-show');
}

function closePreview() {
    const modal = document.getElementById('preview-modal');
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

// ============================================================================
// CONTENT ANALYSIS
// ============================================================================

/**
 * Analyze user content using the API
 */
async function analyzeContent() {
    const content = document.getElementById('content-input').value.trim();

    // Validation
    if (!content) {
        showToast('Please paste some content to analyze', 'error');
        return;
    }

    if (content.length < 50) {
        showToast('Please provide at least 50 characters of content', 'error');
        return;
    }

    // Get customization options
    const options = {
        length: document.getElementById('length-option').value,
        include_examples: document.getElementById('include-examples').checked,
        include_questions: document.getElementById('include-questions').checked
    };

    console.log('🔍 Analyzing content...', {
        contentLength: content.length,
        template: selectedTemplate?.name || 'Custom',
        options
    });

    // Show loading state
    setLoadingState(true);
    showProgress('Analyzing your content...', 0);

    try {
        // Step 1: Analyze content
        updateProgress('Analyzing content structure...', 25);
        const analysisResponse = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: content,
                content_type: 'text'
            })
        });

        const analysisData = await analysisResponse.json();
        console.log('📊 Analysis result:', analysisData);

        if (analysisData.status !== 'success') {
            throw new Error(analysisData.message || 'Analysis failed');
        }

        currentAnalysisId = 'temp_' + Date.now(); // Placeholder ID

        // Step 2: Match template (if not already selected)
        updateProgress('Matching to best template...', 50);
        let finalTemplate = selectedTemplate;

        if (!selectedTemplate) {
            const matchResponse = await fetch(`${API_BASE_URL}/api/match-template`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    analysis_id: currentAnalysisId
                })
            });

            const matchData = await matchResponse.json();
            console.log('🎯 Matched template:', matchData);

            if (matchData.status === 'success' && matchData.matched_template) {
                finalTemplate = matchData.matched_template;
            }
        }

        // Step 3: Generate study guide
        updateProgress('Generating your study guide...', 75);
        const generateResponse = await fetch(`${API_BASE_URL}/api/generate-guide`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                analysis_id: currentAnalysisId,
                template_id: finalTemplate?.id || 'lecture-digest',
                customization_options: options
            })
        });

        const generateData = await generateResponse.json();
        console.log('📚 Generated guide:', generateData);

        if (generateData.status !== 'success') {
            throw new Error(generateData.message || 'Guide generation failed');
        }

        // Complete!
        updateProgress('Complete!', 100);
        setTimeout(() => {
            setLoadingState(false);
            closeModal();
            showPreview(generateData.study_guide, finalTemplate);
            showToast('Study guide generated successfully!', 'success');
        }, 500);

    } catch (error) {
        console.error('❌ Error:', error);
        setLoadingState(false);
        hideProgress();
        showToast(error.message || 'Failed to generate study guide. Please try again.', 'error');
    }
}

// ============================================================================
// PREVIEW & RESULTS
// ============================================================================

/**
 * Show the generated study guide preview
 */
function showPreview(studyGuide, template) {
    const previewContent = document.getElementById('preview-content');

    // TODO: Replace with actual formatted study guide
    previewContent.innerHTML = `
        <div class="space-y-4">
            <div class="border-b pb-4">
                <h3 class="text-2xl font-bold text-gray-900 mb-2">
                    ${template?.icon_emoji || '📚'} ${template?.name || 'Study Guide'}
                </h3>
                <p class="text-gray-600">Your personalized study guide is ready!</p>
            </div>

            <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                <div class="flex">
                    <div class="text-2xl mr-3">⚠️</div>
                    <div>
                        <h4 class="font-semibold text-yellow-800">Preview Mode</h4>
                        <p class="text-sm text-yellow-700 mt-1">
                            This is a placeholder preview. The actual study guide will be generated
                            once you implement the Mistral AI integration in the backend.
                        </p>
                    </div>
                </div>
            </div>

            <div class="prose max-w-none">
                <h4 class="font-semibold text-gray-900">Template Information:</h4>
                <ul class="text-gray-700 text-sm">
                    <li><strong>Template:</strong> ${template?.name || 'N/A'}</li>
                    <li><strong>Sections:</strong> ${template?.sections?.join(', ') || 'N/A'}</li>
                    <li><strong>Generated:</strong> ${new Date().toLocaleString()}</li>
                </ul>

                <div class="mt-6 p-4 bg-gray-100 rounded-lg">
                    <p class="text-sm text-gray-600 italic">
                        Your formatted study guide content will appear here once the AI processing is implemented.
                        It will include all the sections defined in your chosen template with beautifully
                        formatted content based on your input.
                    </p>
                </div>
            </div>
        </div>
    `;

    openPreview();
}

// ============================================================================
// UI HELPERS
// ============================================================================

function setLoadingState(isLoading) {
    const btn = document.getElementById('analyze-btn');
    const btnText = document.getElementById('analyze-btn-text');
    const btnSpinner = document.getElementById('analyze-btn-spinner');

    btn.disabled = isLoading;

    if (isLoading) {
        btnText.classList.add('hidden');
        btnSpinner.classList.remove('hidden');
    } else {
        btnText.classList.remove('hidden');
        btnSpinner.classList.add('hidden');
    }
}

function showProgress(text, percent) {
    const section = document.getElementById('progress-section');
    const progressText = document.getElementById('progress-text');
    const progressPercent = document.getElementById('progress-percent');
    const progressBar = document.getElementById('progress-bar');

    section.classList.remove('hidden');
    progressText.textContent = text;
    progressPercent.textContent = `${percent}%`;
    progressBar.style.width = `${percent}%`;
}

function updateProgress(text, percent) {
    showProgress(text, percent);
}

function hideProgress() {
    const section = document.getElementById('progress-section');
    section.classList.add('hidden');
}

function showToast(message, type = 'info') {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(toast => toast.remove());

    // Create new toast
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️'
    };

    toast.innerHTML = `
        <span class="text-2xl">${icons[type] || icons.info}</span>
        <span class="text-gray-800">${message}</span>
    `;

    document.body.appendChild(toast);

    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

function scrollToTemplates() {
    document.getElementById('templates').scrollIntoView({ behavior: 'smooth' });
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Download study guide as PDF
 * TODO: Implement PDF generation
 */
function downloadPDF() {
    showToast('PDF download feature coming soon!', 'info');
}

/**
 * Copy study guide to clipboard
 * TODO: Implement clipboard copy
 */
function copyToClipboard() {
    showToast('Clipboard copy feature coming soon!', 'info');
}

// Fade out animation CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(20px); }
    }
`;
document.head.appendChild(style);
