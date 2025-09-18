// Background script for PaperBiceps Chrome Extension
const BACKEND_URL = 'http://localhost:8000';

// Helper function to convert blob to base64
function blobToBase64(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

// Context menu setup
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'generatePodcast',
    title: 'Generate Podcast from this page',
    contexts: ['page']
  });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === 'generatePodcast') {
    try {
      const response = await fetch(`${BACKEND_URL}/api/podcast?url=${encodeURIComponent(tab.url)}`);
      
      if (response.ok) {
        const blob = await response.blob();
        // Convert blob to base64 for cross-context transfer
        const base64Audio = await blobToBase64(blob);
        
        // Send audio data to content script
        chrome.tabs.sendMessage(tab.id, {
          action: 'playAudio',
          audioData: base64Audio,
          mimeType: blob.type,
          filename: 'podcast_audio.mp3'
        });
      } else {
        throw new Error('Failed to generate podcast');
      }
    } catch (error) {
      console.error('Error generating podcast:', error);
      chrome.tabs.sendMessage(tab.id, {
        action: 'showError',
        message: 'Failed to generate podcast. Please try again.'
      });
    }
  }
});

// Handle messages from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'generatePodcast') {
    handlePodcastGeneration(request.url, sendResponse);
    return true; // Keep message channel open for async response
  }
  
  if (request.action === 'explainFigure') {
    handleFigureExplanation(request.url, request.figureId, sendResponse);
    return true;
  }
  
  if (request.action === 'explainSection') {
    handleSectionExplanation(request.url, request.section, sendResponse);
    return true;
  }
});

// Generate podcast from URL
async function handlePodcastGeneration(url, sendResponse) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/podcast?url=${encodeURIComponent(url)}`);
    
    if (response.ok) {
      const blob = await response.blob();
      // Convert blob to base64 for cross-context transfer
      const base64Audio = await blobToBase64(blob);
      sendResponse({ 
        success: true, 
        audioData: base64Audio,
        mimeType: blob.type,
        filename: 'podcast_audio.mp3'
      });
    } else {
      throw new Error('Failed to generate podcast');
    }
  } catch (error) {
    console.error('Error generating podcast:', error);
    sendResponse({ 
      success: false, 
      error: error.message 
    });
  }
}

// Explain figure using Deepgram TTS
async function handleFigureExplanation(url, figureId, sendResponse) {
  try {
    const response = await fetch(`${BACKEND_URL}/api/explain/figure`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        figure_id: figureId
      })
    });
    
    if (response.ok) {
      const blob = await response.blob();
      // Convert blob to base64 for cross-context transfer
      const base64Audio = await blobToBase64(blob);
      sendResponse({ 
        success: true, 
        audioData: base64Audio,
        mimeType: blob.type,
        filename: `figure_${figureId}_explanation.mp3`
      });
    } else {
      throw new Error('Failed to generate figure explanation');
    }
  } catch (error) {
    console.error('Error generating figure explanation:', error);
    sendResponse({ 
      success: false, 
      error: error.message 
    });
  }
}

// Explain section using Deepgram TTS
async function handleSectionExplanation(url, section, sendResponse) {
  try {
    console.log(`Generating section explanation for: ${section} from ${url}`);
    
    const response = await fetch(`${BACKEND_URL}/api/explain/section`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        section: section
      })
    });
    
    console.log(`Response status: ${response.status}`);
    
    if (response.ok) {
      const blob = await response.blob();
      console.log(`Blob size: ${blob.size} bytes`);
      // Convert blob to base64 for cross-context transfer
      const base64Audio = await blobToBase64(blob);
      sendResponse({ 
        success: true, 
        audioData: base64Audio,
        mimeType: blob.type,
        filename: `${section}_explanation.mp3`
      });
    } else {
      const errorText = await response.text();
      console.error(`API Error: ${response.status} - ${errorText}`);
      throw new Error(`Failed to generate section explanation: ${response.status}`);
    }
  } catch (error) {
    console.error('Error generating section explanation:', error);
    sendResponse({ 
      success: false, 
      error: error.message 
    });
  }
}
