import streamlit as st
import requests
import os
from urllib.parse import urlparse

st.set_page_config(page_title="The PaperBiceps Show", page_icon="🎙️")

st.title("The PaperBiceps Show Podcast ")
st.markdown("Upload a file or enter a URL to generate a podcast")

# Input section
input_option = st.radio("Choose input method:", ("Upload File", "Enter URL"))
file = None
url = None

if input_option == "Upload File":
    file = st.file_uploader(" 📥 Upload a PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])
else:
    url = st.text_input("Enter URL")

# Generate button
if st.button("🎙️ Generate Podcast"):
    if not file and not url:
        st.error("Please upload a file or enter a URL")
    else:
        with st.spinner("Generating your podcast..."):
            try:
                # Prepare request
                if file:
                    files = {"file": (file.name, file.getvalue(), file.type)}
                    data = {}
                else:
                    files = None
                    data = {"url": url}

                # Make request to FastAPI backend
                response = requests.post(
                    "http://localhost:8000/generate-podcast/",
                    files=files,
                    data=data
                )

                if response.status_code == 200:
                    # Download the audio
                    temp_audio = f"temp_podcast_{os.urandom(8).hex()}.mp3"
                    with open(temp_audio, "wb") as f:
                        f.write(response.content)
                    
                    st.audio(temp_audio, format="audio/mp3")
                    st.download_button(
                        label="⬇️ Download Podcast",
                        data=open(temp_audio, "rb"),
                        file_name="podcast_audio.mp3",
                        mime="audio/mp3"
                    )
                    
                    # Clean up
                    os.remove(temp_audio)
                    
                    st.success("Podcast generated successfully!")
                else:
                    st.error(f"Error: {response.json()['detail']}")

            except Exception as e:
                st.error(f"Error generating podcast: {str(e)}")

st.markdown("---")
st.markdown("Powered by The Paper Biceps Show 🎧")
