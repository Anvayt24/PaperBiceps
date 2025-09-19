// Content script for PaperBiceps Chrome Extension
let floatingButton = null;
let isButtonVisible = false;

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

// Create floating microphone button
function createFloatingButton() {
  if (floatingButton) return;
  
  floatingButton = document.createElement('div');
  floatingButton.id = 'paperbiceps-floating-button';
  floatingButton.innerHTML = '🎙';
  floatingButton.className = 'paperbiceps-floating-btn';
  // Add inline styles to ensure visibility even if CSS fails or is overridden by the page
  try {
    floatingButton.style.position = 'fixed';
    floatingButton.style.bottom = '20px';
    floatingButton.style.right = '20px';
    floatingButton.style.width = '60px';
    floatingButton.style.height = '60px';
    floatingButton.style.borderRadius = '50%';
    floatingButton.style.display = 'flex';
    floatingButton.style.alignItems = 'center';
    floatingButton.style.justifyContent = 'center';
    floatingButton.style.fontSize = '24px';
    floatingButton.style.cursor = 'pointer';
    floatingButton.style.userSelect = 'none';
    // Use a very high z-index to sit above most site overlays
    floatingButton.style.zIndex = '2147483647';
    floatingButton.style.color = '#ffffff';
    floatingButton.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    floatingButton.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
  } catch (e) {
    // Non-fatal; styling best-effort
    console.warn('Unable to apply inline styles to floating button:', e);
  }
  // Accessibility improvements
  floatingButton.setAttribute('role', 'button');
  floatingButton.setAttribute('aria-label', 'Generate podcast with PaperBiceps');
  
  // Add click event
  floatingButton.addEventListener('click', handleFloatingButtonClick);
  
  document.body.appendChild(floatingButton);
  isButtonVisible = true;
}

// Handle floating button click
async function handleFloatingButtonClick() {
  try {
    // Show loading state
    floatingButton.innerHTML = '⏳';
    floatingButton.style.opacity = '0.7';
    
    // Send message to background script
    chrome.runtime.sendMessage({
      action: 'generatePodcast',
      url: window.location.href
    }, (response) => {
      // Handle service worker unreachable or other runtime errors
      if (chrome.runtime && chrome.runtime.lastError) {
        console.error('Runtime error:', chrome.runtime.lastError.message);
        showNotification('Extension background not responding. Please reload the extension.', 'error');
        // Reset button
        floatingButton.innerHTML = '🎙';
        floatingButton.style.opacity = '1';
        return;
      }
      if (response && response.success) {
        playAudio(response.audioData, response.mimeType);
        showNotification('Podcast generated successfully!', 'success');
      } else {
        showNotification('Failed to generate podcast. Please try again.', 'error');
      }
      
      // Reset button
      floatingButton.innerHTML = '🎙';
      floatingButton.style.opacity = '1';
    });
  } catch (error) {
    console.error('Error handling floating button click:', error);
    showNotification('An error occurred. Please try again.', 'error');
    
    // Reset button
    floatingButton.innerHTML = '🎙';
    floatingButton.style.opacity = '1';
  }
}

// Play audio
function playAudio(audioData, mimeType) {
  try {
    // Convert base64 back to blob and create object URL in content script context
    const blob = base64ToBlob(audioData, mimeType);
    const audioUrl = URL.createObjectURL(blob);
    
    const audio = new Audio(audioUrl);
    audio.play().catch(error => {
      console.error('Error playing audio:', error);
      showNotification('Error playing audio', 'error');
    });
  } catch (error) {
    console.error('Error processing audio data:', error);
    showNotification('Error processing audio data', 'error');
  }
}

// Show notification
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `paperbiceps-notification paperbiceps-notification-${type}`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  // Auto remove after 3 seconds
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 3000);
}

// Toggle floating button visibility
function toggleFloatingButton() {
  if (isButtonVisible) {
    if (floatingButton) {
      floatingButton.style.display = 'none';
    }
    isButtonVisible = false;
  } else {
    if (floatingButton) {
      floatingButton.style.display = 'flex';
    } else {
      createFloatingButton();
    }
    isButtonVisible = true;
  }
}

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'playAudio') {
    playAudio(request.audioData, request.mimeType);
    showNotification('Playing podcast...', 'success');
  }
  
  if (request.action === 'showError') {
    showNotification(request.message, 'error');
  }
  
  if (request.action === 'toggleButton') {
    toggleFloatingButton();
  }
});

// Initialize floating button on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', createFloatingButton);
} else {
  createFloatingButton();
}

// Re-create button if page content changes (for SPAs)
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.type === 'childList' && !floatingButton) {
      createFloatingButton();
    }
  });
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});
