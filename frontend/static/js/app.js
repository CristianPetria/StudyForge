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
let uploadedFiles = [];

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

    // Character counter for study description
    const studyDescription = document.getElementById('study-description');
    if (studyDescription) {
        studyDescription.addEventListener('input', function() {
            const charCount = this.value.length;
            document.getElementById('desc-char-count').textContent = `${charCount} characters`;
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
 * Show modal with a specific template pre-selected
 */
function showModalWithTemplate(templateType) {
    selectedTemplate = { id: templateType };

    if (templateType === 'marketing') {
        document.getElementById('modal-template-emoji').textContent = '📊';
        document.getElementById('modal-template-name').textContent = 'Marketing & Business Concepts';
        document.getElementById('modal-template-description').textContent = 'Perfect for marketing frameworks, business strategies, and case studies';
    } else if (templateType === 'technical') {
        document.getElementById('modal-template-emoji').textContent = '⚙️';
        document.getElementById('modal-template-name').textContent = 'Technical & Engineering Docs';
        document.getElementById('modal-template-description').textContent = 'Ideal for API documentation, technical specifications, and engineering concepts';
    }

    openModal();
}

/**
 * Show custom template modal (no template pre-selected)
 */
function showCustomModal() {
    selectedTemplate = null;
    document.getElementById('modal-template-emoji').textContent = '✨';
    document.getElementById('modal-template-name').textContent = 'Create Your Custom Study Guide';
    document.getElementById('modal-template-description').textContent = 'Tell us about your learning needs and we\'ll suggest the perfect template for you';

    openModal();
}

/**
 * Suggest templates and generate study guide in one flow
 */
async function suggestTemplatesAndGenerate() {
    const ageGroup = document.getElementById('age-group').value;
    const learningStyle = document.getElementById('learning-style').value;
    const courseType = document.getElementById('course-type').value;
    const description = document.getElementById('study-description').value.trim();

    // Validation
    if (!ageGroup || !learningStyle || !courseType || !description) {
        showToast('Please fill in all fields to create your study guide', 'error');
        return;
    }

    if (description.length < 20) {
        showToast('Please provide more details about what you need (at least 20 characters)', 'error');
        return;
    }

    console.log('🎯 Creating custom study guide...');
    setLoadingState(true);
    showProgress('Finding the perfect template for you...', 20);

    try {
        // Step 1: Get template suggestions
        updateProgress('Analyzing your preferences...', 40);
        
        const suggestResponse = await fetch(`${API_BASE_URL}/api/templates/suggest`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                age_group: ageGroup,
                learning_style: learningStyle,
                course_type: courseType,
                description: description
            })
        });

        const suggestData = await suggestResponse.json();
        console.log('📚 Suggestions:', suggestData);

        if (suggestData.status !== 'success' || !suggestData.suggested_templates.length) {
            throw new Error('Could not find suitable templates');
        }

        // Use the best matching template
        const bestTemplate = suggestData.suggested_templates[0];
        selectedTemplate = { id: bestTemplate.id };

        updateProgress('Generating your customized study guide...', 70);

        // Step 2: Generate the study guide with the selected template
        const options = {
            length: document.getElementById('length-option').value,
            include_examples: document.getElementById('include-examples').checked,
            include_questions: document.getElementById('include-questions').checked
        };

        const generateResponse = await fetch(`${API_BASE_URL}/api/complete-workflow`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: description,
                content_type: 'custom_guide',
                template_id: bestTemplate.id,
                customization_options: options
            })
        });

        const generateData = await generateResponse.json();
        console.log('✅ Generation result:', generateData);

        if (generateData.status !== 'success') {
            throw new Error(generateData.message || 'Guide generation failed');
        }

        updateProgress('Complete! Opening your study guide...', 100);

        setTimeout(() => {
            setLoadingState(false);
            hideProgress();
            closeModal();

            // Redirect to the generated guide
            if (generateData.guide_id) {
                window.location.href = `${API_BASE_URL}/api/guide/${generateData.guide_id}`;
            } else {
                showToast('Study guide created but URL not available', 'info');
            }
        }, 500);

    } catch (error) {
        console.error('❌ Error:', error);
        setLoadingState(false);
        hideProgress();
        showToast(error.message || 'Failed to create study guide. Please try again.', 'error');
    }
}

/**
 * Switch between content upload and custom form modes
 */
function switchModalMode(mode) {
    const contentColumn = document.querySelector('[id*="content-input"]')?.closest('div');
    const customForm = document.getElementById('custom-form-section');
    const tabContent = document.getElementById('tab-content');
    const tabCustom = document.getElementById('tab-custom');
    const gridContainer = document.querySelector('.grid.grid-cols-1.md\\:grid-cols-2');

    if (mode === 'content') {
        // Show content, hide custom form
        if (customForm) customForm.style.display = 'none';
        if (gridContainer) gridContainer.style.gridTemplateColumns = '1fr';
        
        // Update tabs
        tabContent.classList.add('text-indigo-600', 'border-indigo-600');
        tabContent.classList.remove('text-gray-600', 'border-transparent');
        tabCustom.classList.remove('text-indigo-600', 'border-indigo-600');
        tabCustom.classList.add('text-gray-600', 'border-transparent');
    } else {
        // Show custom form, show content as well
        if (customForm) customForm.style.display = 'block';
        if (gridContainer) gridContainer.style.gridTemplateColumns = 'repeat(2, minmax(0, 1fr))';
        
        // Update tabs
        tabCustom.classList.add('text-indigo-600', 'border-indigo-600');
        tabCustom.classList.remove('text-gray-600', 'border-transparent');
        tabContent.classList.remove('text-indigo-600', 'border-indigo-600');
        tabContent.classList.add('text-gray-600', 'border-transparent');
    }
}

/**
 * Suggest templates based on user's study description and preferences
 */
async function suggestTemplates() {
    const ageGroup = document.getElementById('age-group').value;
    const learningStyle = document.getElementById('learning-style').value;
    const courseType = document.getElementById('course-type').value;
    const description = document.getElementById('study-description').value.trim();

    // Validation
    if (!ageGroup || !learningStyle || !courseType || !description) {
        showToast('Please fill in all fields to get template suggestions', 'error');
        return;
    }

    console.log('🔍 Suggesting templates based on user input...');
    showProgress('Analyzing your preferences and finding the best template...', 30);

    try {
        const response = await fetch(`${API_BASE_URL}/api/templates/suggest`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                age_group: ageGroup,
                learning_style: learningStyle,
                course_type: courseType,
                description: description
            })
        });

        const data = await response.json();
        console.log('📚 Template suggestions:', data);

        updateProgress('Displaying recommendations...', 100);

        if (data.status === 'success' && data.suggested_templates) {
            displaySuggestedTemplates(data.suggested_templates);
            showToast('✅ Found perfect templates for you!', 'success');
        } else {
            showToast('Could not find template suggestions. Try uploading content instead.', 'error');
        }

        hideProgress();

    } catch (error) {
        console.error('❌ Error:', error);
        hideProgress();
        showToast(error.message || 'Failed to suggest templates. Please try again.', 'error');
    }
}

/**
 * Display suggested templates
 */
function displaySuggestedTemplates(suggestedTemplates) {
    const container = document.getElementById('suggested-templates');
    const templatesDiv = document.getElementById('templates-suggestions');

    templatesDiv.innerHTML = '';

    suggestedTemplates.forEach(template => {
        const templateEl = document.createElement('div');
        templateEl.className = 'p-3 bg-white rounded-lg border-l-4 border-indigo-500 hover:shadow-md transition cursor-pointer';
        templateEl.innerHTML = `
            <div class="flex items-start justify-between">
                <div class="flex-1">
                    <h5 class="font-semibold text-gray-900">${template.name}</h5>
                    <p class="text-xs text-gray-600 mt-1">${template.description}</p>
                    ${template.match_score ? `<p class="text-xs text-indigo-600 mt-1">Match Score: ${Math.round(template.match_score * 100)}%</p>` : ''}
                </div>
                <button onclick="selectSuggestedTemplate('${template.id}')" class="px-3 py-1 bg-indigo-600 text-white text-xs rounded hover:bg-indigo-700 transition">
                    Use
                </button>
            </div>
        `;
        templatesDiv.appendChild(templateEl);
    });

    container.classList.remove('hidden');
}

/**
 * Select a suggested template and set it for analysis
 */
function selectSuggestedTemplate(templateId) {
    const template = templates.find(t => t.id === templateId);
    if (template) {
        selectedTemplate = template;
        console.log('📋 Selected suggested template:', template.name);
        showToast(`✅ Template selected: ${template.name}`, 'success');
        
        // Switch back to content mode and focus on content input
        switchModalMode('content');
        document.getElementById('content-input').focus();
    }
}

/**
 * Handle file selection from input or drag-drop
 */
function handleFileSelect(event) {
    const files = event.target.files;
    addFilesToUpload(files);
}

/**
 * Handle drag and drop
 */
function handleDrop(event) {
    event.preventDefault();
    event.stopPropagation();
    
    const files = event.dataTransfer.files;
    addFilesToUpload(files);
}

/**
 * Add files to the upload list
 */
function addFilesToUpload(files) {
    const fileList = document.getElementById('file-list');
    const maxSize = 10 * 1024 * 1024; // 10MB
    const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'];
    
    for (let file of files) {
        // Validate file size
        if (file.size > maxSize) {
            showToast(`File ${file.name} is too large (max 10MB)`, 'error');
            continue;
        }
        
        // Validate file type
        if (!allowedTypes.includes(file.type)) {
            showToast(`File type ${file.type} not supported`, 'error');
            continue;
        }
        
        // Check if file already added
        if (uploadedFiles.some(f => f.name === file.name && f.size === file.size)) {
            showToast(`File ${file.name} already added`, 'info');
            continue;
        }
        
        uploadedFiles.push(file);
        console.log(`✅ Added file: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`);
    }
    
    // Display files
    displayUploadedFiles();
    showToast(`✅ ${uploadedFiles.length} file(s) ready to upload`, 'success');
}

/**
 * Display uploaded files in the list
 */
function displayUploadedFiles() {
    const fileList = document.getElementById('file-list');
    fileList.innerHTML = '';
    
    if (uploadedFiles.length === 0) {
        return;
    }
    
    uploadedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'flex items-center justify-between p-3 bg-white border-2 border-gray-200 rounded-lg hover:border-indigo-300 transition';
        fileItem.innerHTML = `
            <div class="flex items-center space-x-3 flex-1">
                <div class="text-2xl">
                    ${file.type.includes('pdf') ? '📄' : file.type.includes('word') ? '📝' : file.type.includes('powerpoint') ? '📊' : '📎'}
                </div>
                <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900 truncate">${file.name}</p>
                    <p class="text-xs text-gray-500">${(file.size / 1024).toFixed(2)} KB</p>
                </div>
            </div>
            <button onclick="removeFile(${index})" class="ml-2 text-red-500 hover:text-red-700 transition">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
            </button>
        `;
        fileList.appendChild(fileItem);
    });
}

/**
 * Remove a file from the upload list
 */
function removeFile(index) {
    uploadedFiles.splice(index, 1);
    displayUploadedFiles();
    showToast('File removed', 'info');
}

/**
 * Scroll to templates section
 */
function scrollToTemplates() {
    document.getElementById('templates').scrollIntoView({ behavior: 'smooth' });
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
    document.getElementById('study-description').value = '';
    document.getElementById('desc-char-count').textContent = '0 characters';
    document.getElementById('age-group').value = '';
    document.getElementById('learning-style').value = '';
    document.getElementById('course-type').value = '';
    uploadedFiles = [];
    displayUploadedFiles();
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
        // Use the complete workflow endpoint (orchestrates analyze -> match -> generate)
        updateProgress('Analyzing content and generating study guide...', 50);

        const response = await fetch(`${API_BASE_URL}/api/complete-workflow`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: content,
                content_type: 'text',
                template_id: selectedTemplate?.id,  // Optional - AI will match if not provided
                customization_options: options
            })
        });

        const data = await response.json();
        console.log('📚 Workflow result:', data);

        if (data.status !== 'success') {
            throw new Error(data.message || 'Guide generation failed');
        }

        // Complete!
        updateProgress('Complete! Opening your study guide...', 100);

        setTimeout(() => {
            setLoadingState(false);
            hideProgress();
            closeModal();

            // Redirect to the generated guide page
            if (data.guide_id) {
                window.location.href = `${API_BASE_URL}/api/guide/${data.guide_id}`;
            } else {
                showToast('Study guide generated but URL missing!', 'error');
            }
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
