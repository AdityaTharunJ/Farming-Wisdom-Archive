import json
import os
import datetime
import pandas as pd
import streamlit as st
from typing import List, Dict, Optional
import re
import bcrypt
import yaml
# Changed from googletrans to deep_translator
from deep_translator import GoogleTranslator, MyMemoryTranslator # GoogleTranslator is more commonly used for general translation, MyMemoryTranslator can be a fallback

# Data storage functions
def load_entries() -> List[Dict]:
    """Load entries from JSON file."""
    try:
        os.makedirs("data_entries", exist_ok=True)
        if os.path.exists("data_entries/entries.json"):
            with open("data_entries/entries.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Error loading entries: {str(e)}")
        return []

def save_entry(entry: Dict) -> bool:
    """Save a single entry to JSON file."""
    try:
        entries = load_entries()
        entries.append(entry)

        os.makedirs("data_entries", exist_ok=True)
        with open("data_entries/entries.json", "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving entry: {str(e)}")
        return False

# Category and language definitions
def get_categories() -> List[str]:
    """Get list of available categories."""
    return [
        "Seed Selection & Storage",
        "Soil Management",
        "Crop Rotation",
        "Natural Fertilizers",
        "Pest Control",
        "Water Management",
        "Harvest Techniques",
        "Seasonal Farming",
        "Traditional Tools",
        "Weather Prediction",
        "Post-Harvest Processing",
        "Other Farming Practices"
    ]

def get_languages() -> List[str]:
    """Get list of supported languages."""
    return [
        "Hindi",
        "English",
        "Bengali",
        "Telugu",
        "Marathi",
        "Tamil",
        "Gujarati",
        "Urdu",
        "Kannada",
        "Malayalam",
        "Oriya",
        "Other" # 'Assamese', 'Nepali', 'Sanskrit' removed due to limited deep_translator support or common use cases, can be added back if needed
    ]

# Text-to-Speech functionality
def text_to_speech(text: str, language: str = "en") -> None:
    """Convert text to speech using gTTS."""
    try:
        from gtts import gTTS
        import tempfile
        # pygame is for local playback, not typically needed in Streamlit Cloud/Spaces
        # import pygame

        # Map language names to gTTS language codes
        lang_map = {
            "English": "en",
            "Hindi": "hi",
            "Bengali": "bn",
            "Telugu": "te",
            "Marathi": "mr",
            "Tamil": "ta",
            "Gujarati": "gu",
            "Urdu": "ur",
            "Kannada": "kn",
            "Malayalam": "ml",
            "Punjabi": "pa",
            "Oriya": "or", # Added for completeness if gTTS supports
            # "Assamese": "as", # gTTS might not support
            # "Nepali": "ne", # gTTS might not support
            "Sanskrit": "sa" # gTTS might have limited support
        }

        lang_code = lang_map.get(language, "en")

        # Generate TTS
        tts = gTTS(text=text, lang=lang_code, slow=False)

        # Save to temporary file and play using Streamlit
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)

            with open(tmp_file.name, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")

            # Clean up
            os.unlink(tmp_file.name)

    except ImportError:
        st.error("Text-to-speech library not available. Please ensure 'gtts' is installed.")
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")

# Speech-to-Text functionality
def speech_to_text(language: str = "en") -> Optional[str]:
    """Convert speech to text using speech recognition."""
    try:
        import speech_recognition as sr
        
        # Map language names to speech recognition language codes (Google Web Speech API)
        lang_map = {
            "English": "en-IN",
            "Hindi": "hi-IN",
            "Bengali": "bn-IN",
            "Telugu": "te-IN",
            "Marathi": "mr-IN",
            "Tamil": "ta-IN",
            "Gujarati": "gu-IN",
            "Urdu": "ur-IN",
            "Kannada": "kn-IN",
            "Malayalam": "ml-IN",
            "Punjabi": "pa-IN",
            "Oriya": "or-IN" # Assuming Indian dialect code exists
        }

        lang_code = lang_map.get(language, "en-IN")

        # Initialize recognizer
        r = sr.Recognizer()

        # Use microphone as source (This will only work in a local environment with mic access)
        # For deployment on Hugging Face Spaces, direct microphone access is typically not available
        # You might need to consider a different STT approach for cloud deployment (e.g., pre-recorded audio upload, or a paid STT API)
        st.warning("Microphone input for Speech-to-Text may not work in deployed environments like Hugging Face Spaces.")
        with sr.Microphone() as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source)

            # Listen for audio
            st.info("Listening... Speak now!")
            audio = r.listen(source, timeout=5, phrase_time_limit=10)

            # Recognize speech
            text = r.recognize_google(audio, language=lang_code)
            return text

    except ImportError:
        st.error("Speech recognition library not available. Please ensure 'SpeechRecognition' is installed.")
        return None
    except sr.UnknownValueError:
        st.error("Could not understand audio. Please try again or speak more clearly.")
        return None
    except sr.RequestError as e:
        st.error(f"Speech recognition service error (check internet/API): {str(e)}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred in speech recognition: {str(e)}")
        return None

# Geocoding functionality
def geocode_location(location_name: str) -> Optional[tuple]:
    """Get coordinates for a location name using Nominatim."""
    try:
        from geopy.geocoders import Nominatim
        
        # Initialize geolocator with a user_agent
        geolocator = Nominatim(user_agent="farming-wisdom-archive-app") # Changed user_agent
        location = geolocator.geocode(location_name)
        
        if location:
            return (location.latitude, location.longitude)
        return None
        
    except ImportError:
        st.error("Geocoding library not available. Please ensure 'geopy' is installed.")
        return None
    except Exception as e:
        st.error(f"Error in geocoding: {str(e)}")
        return None

# Search functionality
def search_entries(entries: List[Dict], query: str, language: str = None, 
                   category: str = None, has_media: bool = False, 
                   has_location: bool = False) -> List[Dict]:
    """Search entries based on query and filters."""
    results = []
    query_lower = query.lower()
    
    for entry in entries:
        # Text search in title and description
        title_match = query_lower in entry.get('title', '').lower()
        desc_match = query_lower in entry.get('description', '').lower()
        
        if not (title_match or desc_match):
            continue
        
        # Apply filters
        if language and entry.get('language') != language:
            continue
        
        if category and entry.get('category') != category:
            continue
        
        if has_media and not (entry.get('image_path') or entry.get('audio_path')):
            continue
        
        if has_location and not (entry.get('latitude') and entry.get('longitude')):
            continue
        
        results.append(entry)
    
    return results

# Export functionality
def export_to_jsonl(entries: List[Dict], include_media: bool = True, 
                    include_coordinates: bool = True) -> str:
    """Export entries to JSONL format."""
    lines = []
    
    for entry in entries:
        export_entry = {
            'id': entry.get('id'),
            'title': entry.get('title'),
            'description': entry.get('description'),
            'language': entry.get('language'),
            'category': entry.get('category'),
            'location_name': entry.get('location_name'),
            'timestamp': entry.get('timestamp'),
            'contributor': entry.get('contributor')
        }
        
        if include_coordinates:
            export_entry['latitude'] = entry.get('latitude')
            export_entry['longitude'] = entry.get('longitude')
        
        if include_media:
            export_entry['image_path'] = entry.get('image_path')
            export_entry['audio_path'] = entry.get('audio_path')
        
        lines.append(json.dumps(export_entry, ensure_ascii=False))
    
    return '\n'.join(lines)

def export_to_csv(entries: List[Dict], include_media: bool = True, 
                  include_coordinates: bool = True) -> str:
    """Export entries to CSV format."""
    data = []
    
    for entry in entries:
        row = {
            'id': entry.get('id'),
            'title': entry.get('title'),
            'description': entry.get('description'),
            'language': entry.get('language'),
            'category': entry.get('category'),
            'location_name': entry.get('location_name'),
            'timestamp': entry.get('timestamp'),
            'contributor': entry.get('contributor')
        }
        
        if include_coordinates:
            row['latitude'] = entry.get('latitude')
            row['longitude'] = entry.get('longitude')
        
        if include_media:
            row['image_path'] = entry.get('image_path')
            row['audio_path'] = entry.get('audio_path')
        
        data.append(row)
    
    df = pd.DataFrame(data)
    return df.to_csv(index=False)

# Utility functions
def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate latitude and longitude coordinates."""
    return -90 <= lat <= 90 and -180 <= lon <= 180

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display."""
    try:
        dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return timestamp

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

# File management
def cleanup_media_files():
    """Clean up orphaned media files."""
    try:
        entries = load_entries()
        used_files = set()
        
        for entry in entries:
            if entry.get('image_path'):
                used_files.add(entry['image_path'])
            if entry.get('audio_path'):
                used_files.add(entry['audio_path'])
        
        # Check media directory for unused files
        media_dir = "data_entries/media"
        if os.path.exists(media_dir):
            for filename in os.listdir(media_dir):
                filepath = os.path.join(media_dir, filename)
                if filepath not in used_files:
                    os.remove(filepath)
                    
    except Exception as e:
        st.error(f"Error cleaning up media files: {str(e)}")

def get_file_size(filepath: str) -> str:
    """Get human-readable file size."""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except:
        return "Unknown"

# Authentication functions
def load_user_data() -> Dict:
    """Load user authentication data."""
    try:
        os.makedirs("data_entries", exist_ok=True)
        if os.path.exists("data_entries/users.json"):
            with open("data_entries/users.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {"users": {}}
    except Exception as e:
        st.error(f"Error loading user data: {str(e)}")
        return {"users": {}}

def save_user_data(user_data: Dict) -> bool:
    """Save user authentication data."""
    try:
        os.makedirs("data_entries", exist_ok=True)
        with open("data_entries/users.json", "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"Error saving user data: {str(e)}")
        return False

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(username: str, email: str, password: str, full_name: str) -> bool:
    """Register a new user."""
    user_data = load_user_data()
    
    # Check if user already exists
    if username in user_data["users"]:
        st.error("Username already exists!")
        return False
    
    # Check if email already exists
    for user_info in user_data["users"].values():
        if user_info.get("email") == email:
            st.error("Email already registered!")
            return False
    
    # Add new user
    user_data["users"][username] = {
        "email": email,
        "password": hash_password(password),
        "full_name": full_name,
        "registration_date": datetime.datetime.now().isoformat(),
        "entries_submitted": 0
    }
    
    return save_user_data(user_data)

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user."""
    user_data = load_user_data()
    
    if username not in user_data["users"]:
        return False
    
    user_info = user_data["users"][username]
    return verify_password(password, user_info["password"])

def get_user_info(username: str) -> Dict:
    """Get user information."""
    user_data = load_user_data()
    return user_data["users"].get(username, {})

def update_user_entry_count(username: str):
    """Update user's entry submission count."""
    user_data = load_user_data()
    if username in user_data["users"]:
        user_data["users"][username]["entries_submitted"] += 1
        save_user_data(user_data)

# Translation functions (using deep_translator)
def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> str:
    """Translate text using deep_translator's GoogleTranslator."""
    try:
        # Language code mapping (deep_translator uses standard ISO codes)
        lang_mapping = {
            "Hindi": "hi",
            "English": "en",
            "Bengali": "bn",
            "Telugu": "te",
            "Marathi": "mr",
            "Tamil": "ta",
            "Gujarati": "gu",
            "Urdu": "ur",
            "Kannada": "kn",
            "Malayalam": "ml",
            "Punjabi": "pa",
            "Oriya": "or",
            "Assamese": "as",
            "Nepali": "ne",
            "Sanskrit": "sa"
        }
        
        target_code = lang_mapping.get(target_lang, "en")
        source_code = lang_mapping.get(source_lang, "auto") if source_lang != "auto" else "auto"
        
        translated = GoogleTranslator(source=source_code, target=target_code).translate(text)
        return translated
    except Exception as e:
        st.error(f"Translation error: {str(e)}. Please check internet connection or try again.")
        return text

def detect_language(text: str) -> str:
    """Detect the language of given text using deep_translator's GoogleTranslator."""
    try:
        detected_code = GoogleTranslator(source="auto", target="en").detect(text) # target 'en' is default, can be any valid language code

        # Reverse mapping for display (ensure this maps codes to names)
        lang_mapping_reverse = {
            "hi": "Hindi",
            "en": "English",
            "bn": "Bengali",
            "te": "Telugu",
            "mr": "Marathi",
            "ta": "Tamil",
            "gu": "Gujarati",
            "ur": "Urdu",
            "kn": "Kannada",
            "ml": "Malayalam",
            "pa": "Punjabi",
            "or": "Oriya",
            "as": "Assamese",
            "ne": "Nepali",
            "sa": "Sanskrit"
        }
        
        return lang_mapping_reverse.get(detected_code, "Unknown")
    except Exception as e:
        st.error(f"Language detection error: {str(e)}")
        return "Unknown"
