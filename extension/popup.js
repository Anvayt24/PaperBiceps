// Popup script for PaperBiceps Chrome Extension
let currentTab = null;
let currentAudioUrl = null;
let currentMimeType = null;
let currentFilename = null;

// Helper function to convert base64 to blob
function base64ToBlob(base64Data, mimeType) {
    const byteCharacters = atob(base64Data.split(',')[1]);
    const byteNumbers = new Array(byteCharacters.length);
    
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: mimeType });
}

// DOM elements
const elements = {
    currentUrl: document.getElementById('currentUrl'),
    generatePodcastBtn: document.getElementById('generatePodcastBtn'),
    podcastBtnText: document.getElementById('podcastBtnText'),
    podcastSpinner: document.getElementById('podcastSpinner'),
    queryInput: document.getElementById('queryInput'),
    explainBtn: document.getElementById('explainBtn'),
    explainBtnText: document.getElementById('explainBtnText'),
    explainSpinner: document.getElementById('explainSpinner'),
    clearBtn: document.getElementById('clearBtn'),
    audioPlayerSection: document.getElementById('audioPlayerSection'),
    audioPlayer: document.getElementById('audioPlayer'),
    downloadBtn: document.getElementById('downloadBtn'),
    stopBtn: document.getElementById('stopBtn'),
    statusMessage: document.getElementById('statusMessage')
};

// Initialize popup
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Get current tab
        const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
        currentTab = tabs[0];
        
        if (currentTab) {
            elements.currentUrl.textContent = currentTab.url;
        }
        
        // Set up event listeners
        setupEventListeners();
        
    } catch (error) {
        console.error('Error initializing popup:', error);
        showStatus('Error initializing extension', 'error');
    }
});

// Set up event listeners
function setupEventListeners() {
    // Generate podcast button
    elements.generatePodcastBtn.addEventListener('click', handleGeneratePodcast);
    
    // Explain button
    elements.explainBtn.addEventListener('click', handleExplain);
    
    // Clear button
    elements.clearBtn.addEventListener('click', () => {
        elements.queryInput.value = '';
    });
    
    // Download button
    elements.downloadBtn.addEventListener('click', handleDownload);
    
    // Stop button
    elements.stopBtn.addEventListener('click', handleStop);
    
    // Enter key for query input
    elements.queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleExplain();
        }
    });
}

// Handle podcast generation
async function handleGeneratePodcast() {
    if (!currentTab) {
        showStatus('No active tab found', 'error');
        return;
    }
    
    setLoadingState('podcast', true);
    showStatus('Generating podcast...', 'info');
    
    try {
        chrome.runtime.sendMessage({
            action: 'generatePodcast',
            url: currentTab.url
        }, (response) => {
            setLoadingState('podcast', false);
            
            if (response && response.success) {
                currentAudioUrl = response.audioData;
                currentMimeType = response.mimeType;
                currentFilename = response.filename;
                playAudio(response.audioData, response.mimeType);
                showStatus('Podcast generated successfully!', 'success');
            } else {
                showStatus(response?.error || 'Failed to generate podcast', 'error');
            }
        });
    } catch (error) {
        setLoadingState('podcast', false);
        console.error('Error generating podcast:', error);
        showStatus('Error generating podcast', 'error');
    }
}

// Handle explanation request
async function handleExplain() {
    const query = elements.queryInput.value.trim();
    
    console.log('Explanation request:', query);
    
    if (!query) {
        showStatus('Please enter a query', 'error');
        return;
    }
    
    if (!currentTab) {
        showStatus('No active tab found', 'error');
        return;
    }
    
    setLoadingState('explain', true);
    showStatus('Generating explanation...', 'info');
    
    try {
        // Determine if it's a figure or section query
        const isFigureQuery = /figure\s+\d+\.?\d*/i.test(query) || /fig\s+\d+\.?\d*/i.test(query);
        
        console.log('Is figure query:', isFigureQuery);
        
        let response;
        if (isFigureQuery) {
            const figureMatch = query.match(/(?:figure|fig)\s+(\d+\.?\d*)/i);
            const figureId = figureMatch ? figureMatch[1] : '1';
            
            console.log('Sending figure explanation request:', figureId);
            
            chrome.runtime.sendMessage({
                action: 'explainFigure',
                url: currentTab.url,
                figureId: figureId
            }, (resp) => {
                console.log('Figure explanation response:', resp);
                handleExplanationResponse(resp, `figure_${figureId}_explanation.mp3`);
            });
        } else {
            console.log('Sending section explanation request:', query);
            
            chrome.runtime.sendMessage({
                action: 'explainSection',
                url: currentTab.url,
                section: query
            }, (resp) => {
                console.log('Section explanation response:', resp);
                handleExplanationResponse(resp, `${query.replace(/\s+/g, '_')}_explanation.mp3`);
            });
        }
    } catch (error) {
        setLoadingState('explain', false);
        console.error('Error generating explanation:', error);
        showStatus('Error generating explanation', 'error');
    }
}

// Handle explanation response
function handleExplanationResponse(response, filename) {
    setLoadingState('explain', false);
    
    if (response && response.success) {
        currentAudioUrl = response.audioData;
        currentMimeType = response.mimeType;
        currentFilename = filename;
        playAudio(response.audioData, response.mimeType);
        showStatus('Explanation generated successfully!', 'success');
    } else {
        showStatus(response?.error || 'Failed to generate explanation', 'error');
    }
}

// Play audio
function playAudio(audioData, mimeType) {
    // Convert base64 back to blob and create object URL in popup context
    try {
        const blob = base64ToBlob(audioData, mimeType);
        const audioUrl = URL.createObjectURL(blob);
        
        // Store the URL for cleanup
        if (currentAudioUrl && currentAudioUrl.startsWith('blob:')) {
            URL.revokeObjectURL(currentAudioUrl);
        }
        
        currentAudioUrl = audioUrl;
        elements.audioPlayer.src = audioUrl;
        elements.audioPlayerSection.style.display = 'block';
        
        elements.audioPlayer.play().catch(error => {
            console.error('Error playing audio:', error);
            showStatus('Error playing audio', 'error');
        });
    } catch (error) {
        console.error('Error processing audio data:', error);
        showStatus('Error processing audio data', 'error');
    }
}

// Handle download
function handleDownload() {
    if (!currentAudioUrl || !currentFilename) {
        showStatus('No audio to download', 'error');
        return;
    }
    
    try {
        const link = document.createElement('a');
        link.href = currentAudioUrl;
        link.download = currentFilename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showStatus('Download started', 'success');
    } catch (error) {
        console.error('Error downloading audio:', error);
        showStatus('Error downloading audio', 'error');
    }
}

// Handle stop
function handleStop() {
    elements.audioPlayer.pause();
    elements.audioPlayer.currentTime = 0;
    showStatus('Audio stopped', 'info');
}

// Set loading state
function setLoadingState(type, isLoading) {
    if (type === 'podcast') {
        elements.podcastBtnText.style.display = isLoading ? 'none' : 'inline';
        elements.podcastSpinner.style.display = isLoading ? 'inline' : 'none';
        elements.generatePodcastBtn.disabled = isLoading;
        
        // Disable other buttons during podcast generation
        elements.explainBtn.disabled = isLoading;
        elements.clearBtn.disabled = isLoading;
    } else if (type === 'explain') {
        elements.explainBtnText.style.display = isLoading ? 'none' : 'inline';
        elements.explainSpinner.style.display = isLoading ? 'inline' : 'none';
        elements.explainBtn.disabled = isLoading;
        
        // Disable other buttons during explanation generation
        elements.generatePodcastBtn.disabled = isLoading;
        elements.clearBtn.disabled = isLoading;
    }
}

// Show status message
function showStatus(message, type = 'info') {
    elements.statusMessage.textContent = message;
    elements.statusMessage.style.display = 'block';
    
    // Add type-specific styling
    switch (type) {
        case 'success':
            elements.statusMessage.style.background = '#dcfce7';
            elements.statusMessage.style.color = '#166534';
            elements.statusMessage.style.border = '1px solid #bbf7d0';
            break;
        case 'error':
            elements.statusMessage.style.background = '#fef2f2';
            elements.statusMessage.style.color = '#dc2626';
            elements.statusMessage.style.border = '1px solid #fecaca';
            break;
        case 'info':
            elements.statusMessage.style.background = '#dbeafe';
            elements.statusMessage.style.color = '#1e40af';
            elements.statusMessage.style.border = '1px solid #bfdbfe';
            break;
        default:
            elements.statusMessage.style.background = '#f3f4f6';
            elements.statusMessage.style.color = '#374151';
            elements.statusMessage.style.border = '1px solid #d1d5db';
    }
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        elements.statusMessage.style.display = 'none';
    }, 3000);
}
