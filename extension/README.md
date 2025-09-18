# PaperBiceps Chrome Extension

A Chrome extension that brings AI-powered podcast generation and voice explanations to any research paper or article.

## Features

### Phase 1: Podcast Generation
- **Context Menu**: Right-click on any page and select "Generate Podcast from this page"
- **Popup Interface**: Clean UI with Tailwind CSS for generating podcasts
- **Audio Player**: Built-in audio player with download functionality
- **Floating Button**: Microphone button that appears on all pages

### Phase 2: Voice Explanations
- **Query Input**: Ask for explanations of specific figures or sections
- **AI-Powered**: Uses Gemini AI to generate contextual explanations
- **Deepgram TTS**: High-quality text-to-speech using Deepgram's Aura models
- **Smart Detection**: Automatically detects figure vs section queries

## Installation

1. **Load the Extension**:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `extension/` folder

2. **Configure Backend**:
   - Ensure your FastAPI backend is running on `http://localhost:8000`
   - Add your Deepgram API key to the backend environment variables

## Usage

### Generating Podcasts
1. **Via Context Menu**: Right-click on any page → "Generate Podcast from this page"
2. **Via Popup**: Click the extension icon → "Generate Podcast" button
3. **Via Floating Button**: Click the 🎙 button on any page

### Getting Voice Explanations
1. Click the extension icon to open the popup
2. Enter your query in the text field (e.g., "Explain figure 1.2", "Read abstract")
3. Click "Explain" to generate audio explanation
4. Use the audio player to listen and download

## API Endpoints

The extension communicates with these FastAPI endpoints:

- `GET /api/podcast?url=<url>` - Generate podcast from URL
- `POST /api/explain/figure` - Generate figure explanation
- `POST /api/explain/section` - Generate section explanation
- `GET /health` - Health check

## File Structure

```
extension/
├── manifest.json          # Extension configuration
├── background.js          # Service worker for API calls
├── content.js            # Content script with floating button
├── content.css           # Styles for injected elements
├── popup.html            # Popup interface
├── popup.js              # Popup functionality
├── icon16.png            # Extension icons
├── icon48.png
└── icon128.png
```

## Development

### Backend Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   ```
   GEMINI_API_KEY=your_gemini_key
   DEEPGRAM_API_KEY=your_deepgram_key
   ```
3. Run the backend: `uvicorn main:app --reload`

### Extension Development
1. Make changes to extension files
2. Go to `chrome://extensions/`
3. Click the refresh button on the extension
4. Test your changes

## Troubleshooting

- **Extension not loading**: Check that all files are in the `extension/` folder
- **API errors**: Ensure backend is running and API keys are configured
- **Audio not playing**: Check browser permissions and audio codec support

## Permissions

The extension requires these permissions:
- `activeTab`: Access current tab URL
- `storage`: Store user preferences
- `scripting`: Inject content scripts
- `contextMenus`: Add right-click menu options
- `tabs`: Communicate with tabs

## Security

- All API calls are made to your local backend
- No data is sent to external services except Deepgram for TTS
- Audio files are temporarily stored and cleaned up automatically
