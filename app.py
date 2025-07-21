import streamlit as st
import json
import os
import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image
import base64
from helpers import (
    load_entries, save_entry, get_categories, get_languages,
    text_to_speech, speech_to_text, geocode_location,
    export_to_jsonl, export_to_csv, search_entries,
    register_user, authenticate_user, get_user_info, update_user_entry_count,
    translate_text, detect_language
)

# Set page config
st.set_page_config(
    page_title="Farming Wisdom Archive",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'entries' not in st.session_state:
    st.session_state.entries = load_entries()
if 'audio_recording' not in st.session_state:
    st.session_state.audio_recording = False
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'show_login' not in st.session_state:
    st.session_state.show_login = True

# Authentication check
if not st.session_state.authenticated:
    st.title("🌾 Farming Wisdom Archive")
    st.markdown("*Preserving Traditional Indian Farming Knowledge*")
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Welcome Back!")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login", type="primary")
            
            if login_button:
                if username and password:
                    if authenticate_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
    
    with tab2:
        st.subheader("Join Our Community")
        with st.form("register_form"):
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")
            reg_username = st.text_input("Choose Username")
            reg_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register_button = st.form_submit_button("Register", type="primary")
            
            if register_button:
                if full_name and email and reg_username and reg_password and confirm_password:
                    if reg_password == confirm_password:
                        if register_user(reg_username, email, reg_password, full_name):
                            st.success("Registration successful! Please login.")
                        else:
                            st.error("Registration failed. Please try again.")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")
    
    # Info about the platform
    st.markdown("---")
    st.markdown("### About This Platform")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🌱 What We Collect:**
        - Traditional seed selection methods
        - Soil management techniques
        - Natural fertilizer recipes
        - Pest control methods
        - Water conservation practices
        - Seasonal farming wisdom
        """)
    
    with col2:
        st.markdown("""
        **🔧 Features:**
        - Multi-language support
        - Speech-to-text input
        - GPS location tracking
        - Automatic translation
        - Audio/visual documentation
        - Offline-ready design
        """)
    
    st.stop()

# Main application for authenticated users
user_info = get_user_info(st.session_state.username)

# App header with user info
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌾 Farming Wisdom Archive")
    st.markdown("*Preserving Traditional Indian Farming Knowledge*")
with col2:
    st.write(f"Welcome, **{user_info.get('full_name', st.session_state.username)}**!")
    st.write(f"Entries submitted: {user_info.get('entries_submitted', 0)}")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "✍️ Submit Farming Wisdom",
    "📖 Browse Farming Knowledge",
    "🗺️ Farming Wisdom Map",
    "🔍 Search Knowledge",
    "🌐 Translation Hub",
    "📊 Export Data",
    "👤 Profile"
])

# Home Page
if page == "🏠 Home":
    st.header("Welcome to Farming Wisdom Archive")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌱 About This Platform
        This platform is dedicated to collecting, preserving, and sharing traditional Indian farming wisdom:
        - 🌰 Seed selection and storage techniques
        - 🌱 Soil management and natural fertilizers
        - 🔄 Crop rotation and sustainable practices
        - 🐛 Natural pest control methods
        - 💧 Water conservation techniques
        - 🌾 Harvest and post-harvest processing
        - 🌦️ Weather prediction and seasonal farming
        - 🔧 Traditional farming tools and techniques
        """)
    
    with col2:
        st.markdown("### 📊 Archive Statistics")
        total_entries = len(st.session_state.entries)
        languages = len(set(entry.get('language', 'Unknown') for entry in st.session_state.entries))
        categories = len(set(entry.get('category', 'Unknown') for entry in st.session_state.entries))
        
        st.metric("Total Farming Entries", total_entries)
        st.metric("Languages", languages)
        st.metric("Farming Categories", categories)
    
    st.markdown("---")
    st.markdown("### 🚀 Getting Started")
    st.markdown("1. **Submit Farming Wisdom**: Share your traditional farming knowledge")
    st.markdown("2. **Browse Knowledge**: Explore farming wisdom from across India")
    st.markdown("3. **Use Map**: Discover location-based farming practices")
    st.markdown("4. **Search**: Find specific farming techniques and wisdom")
    st.markdown("5. **Translation**: Translate farming knowledge between languages")

# Submit Farming Wisdom Page
elif page == "✍️ Submit Farming Wisdom":
    st.header("Submit Farming Wisdom")
    
    # Initialize session state for form data
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'title': '',
            'description': '',
            'language': get_languages()[0],
            'category': get_categories()[0],
            'location_name': '',
            'manual_lat': 0.0,
            'manual_lon': 0.0
        }
    
    # Location helper tools (outside form)
    st.subheader("Location Helper Tools")
    col_help1, col_help2 = st.columns(2)
    
    with col_help1:
        if st.button("📍 Get Current Location"):
            st.info("Click on the map below to select location, or use the geocoding tool")
    
    with col_help2:
        geocode_location_input = st.text_input("Enter location to geocode", 
                                             placeholder="e.g., Mumbai, Maharashtra")
        if st.button("🌍 Geocode Location") and geocode_location_input:
            coords = geocode_location(geocode_location_input)
            if coords:
                st.session_state.form_data['manual_lat'] = coords[0]
                st.session_state.form_data['manual_lon'] = coords[1]
                st.success(f"Found coordinates: {coords[0]:.6f}, {coords[1]:.6f}")
            else:
                st.error("Could not find coordinates for the location")
    
    # Map for location selection (outside form)
    if st.session_state.form_data['manual_lat'] != 0.0 or st.session_state.form_data['manual_lon'] != 0.0:
        st.subheader("Location Map")
        m = folium.Map(location=[st.session_state.form_data['manual_lat'], 
                                st.session_state.form_data['manual_lon']], zoom_start=10)
        folium.Marker([st.session_state.form_data['manual_lat'], 
                      st.session_state.form_data['manual_lon']]).add_to(m)
        map_data = st_folium(m, width=700, height=300)
        
        if map_data['last_clicked']:
            st.session_state.form_data['manual_lat'] = map_data['last_clicked']['lat']
            st.session_state.form_data['manual_lon'] = map_data['last_clicked']['lng']
            st.success(f"Selected coordinates: {st.session_state.form_data['manual_lat']:.6f}, {st.session_state.form_data['manual_lon']:.6f}")
    
    # Speech-to-text tool (outside form)
    st.subheader("Speech Input Helper")
    speech_language = st.selectbox("Language for Speech Recognition", get_languages(), key="speech_lang")
    if st.button("🎤 Record Description"):
        with st.spinner("Listening... Speak now!"):
            recorded_text = speech_to_text(speech_language)
            if recorded_text:
                st.session_state.form_data['description'] = recorded_text
                st.success(f"Recorded: {recorded_text}")
            else:
                st.error("Could not record speech. Please try again.")
    
    # Main form
    st.subheader("Entry Details")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title*", 
                                value=st.session_state.form_data['title'],
                                placeholder="Enter the title of your wisdom")
            language = st.selectbox("Language*", get_languages(), 
                                  index=get_languages().index(st.session_state.form_data['language']))
            category = st.selectbox("Category*", get_categories(),
                                  index=get_categories().index(st.session_state.form_data['category']))
            location_name = st.text_input("Location", 
                                        value=st.session_state.form_data['location_name'],
                                        placeholder="e.g., Mumbai, Maharashtra")
        
        with col2:
            description = st.text_area("Description*", 
                                     value=st.session_state.form_data['description'],
                                     height=100, 
                                     placeholder="Describe the wisdom, practice, or story...")
            
            # Media upload
            st.subheader("Media (Optional)")
            uploaded_image = st.file_uploader("Upload Image", type=['jpg', 'jpeg', 'png'])
            uploaded_audio = st.file_uploader("Upload Audio", type=['mp3', 'wav', 'ogg'])
        
        # Location coordinates (read-only display)
        st.subheader("Location Coordinates")
        col3, col4 = st.columns(2)
        
        with col3:
            manual_lat = st.number_input("Latitude", 
                                       value=st.session_state.form_data['manual_lat'], 
                                       format="%.6f", 
                                       help="Use tools above to set coordinates")
            manual_lon = st.number_input("Longitude", 
                                       value=st.session_state.form_data['manual_lon'], 
                                       format="%.6f",
                                       help="Use tools above to set coordinates")
        
        with col4:
            st.info("💡 Use the location helper tools above to set coordinates")
        
        # Form submission
        submitted = st.form_submit_button("Submit Entry", type="primary")
        
        if submitted:
            if title and description and language and category:
                # Save media files
                image_path = None
                audio_path = None
                
                if uploaded_image:
                    image_path = f"data_entries/media/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_image.name}"
                    os.makedirs("data_entries/media", exist_ok=True)
                    with open(image_path, "wb") as f:
                        f.write(uploaded_image.getbuffer())
                
                if uploaded_audio:
                    audio_path = f"data_entries/media/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_audio.name}"
                    os.makedirs("data_entries/media", exist_ok=True)
                    with open(audio_path, "wb") as f:
                        f.write(uploaded_audio.getbuffer())
                
                # Create entry
                entry = {
                    'id': len(st.session_state.entries) + 1,
                    'title': title,
                    'description': description,
                    'language': language,
                    'category': category,
                    'location_name': location_name,
                    'latitude': manual_lat if manual_lat != 0.0 else None,
                    'longitude': manual_lon if manual_lon != 0.0 else None,
                    'image_path': image_path,
                    'audio_path': audio_path,
                    'timestamp': datetime.datetime.now().isoformat(),
                    'contributor': st.session_state.username,
                    'contributor_full_name': user_info.get('full_name', st.session_state.username)
                }
                
                if save_entry(entry):
                    st.session_state.entries.append(entry)
                    update_user_entry_count(st.session_state.username)
                    st.success("Farming wisdom submitted successfully!")
                    # Reset form data
                    st.session_state.form_data = {
                        'title': '',
                        'description': '',
                        'language': get_languages()[0],
                        'category': get_categories()[0],
                        'location_name': '',
                        'manual_lat': 0.0,
                        'manual_lon': 0.0
                    }
                    st.rerun()
                else:
                    st.error("Failed to save entry. Please try again.")
            else:
                st.error("Please fill in all required fields marked with *")

# Browse Farming Knowledge Page
elif page == "📖 Browse Farming Knowledge":
    st.header("Browse Farming Knowledge")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_language = st.selectbox("Filter by Language", ["All"] + get_languages())
    with col2:
        filter_category = st.selectbox("Filter by Category", ["All"] + get_categories())
    with col3:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Title A-Z"])
    
    # Filter entries
    filtered_entries = st.session_state.entries.copy()
    
    if filter_language != "All":
        filtered_entries = [e for e in filtered_entries if e.get('language') == filter_language]
    
    if filter_category != "All":
        filtered_entries = [e for e in filtered_entries if e.get('category') == filter_category]
    
    # Sort entries
    if sort_by == "Newest First":
        filtered_entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    elif sort_by == "Oldest First":
        filtered_entries.sort(key=lambda x: x.get('timestamp', ''))
    elif sort_by == "Title A-Z":
        filtered_entries.sort(key=lambda x: x.get('title', '').lower())
    
    st.write(f"Showing {len(filtered_entries)} entries")
    
    # Display entries
    for entry in filtered_entries:
        with st.expander(f"📖 {entry.get('title', 'Untitled')} ({entry.get('language', 'Unknown')})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Category:** {entry.get('category', 'Unknown')}")
                st.markdown(f"**Location:** {entry.get('location_name', 'Not specified')}")
                st.markdown(f"**Description:**")
                st.write(entry.get('description', 'No description'))
                
                # TTS button
                if st.button(f"🔊 Listen", key=f"tts_{entry.get('id')}"):
                    text_to_speech(entry.get('description', ''), entry.get('language', 'en'))
            
            with col2:
                # Display image if available
                if entry.get('image_path') and os.path.exists(entry['image_path']):
                    try:
                        image = Image.open(entry['image_path'])
                        st.image(image, caption="Attached Image", use_column_width=True)
                    except Exception as e:
                        st.error(f"Error loading image: {str(e)}")
                
                # Display audio if available
                if entry.get('audio_path') and os.path.exists(entry['audio_path']):
                    try:
                        st.audio(entry['audio_path'])
                    except Exception as e:
                        st.error(f"Error loading audio: {str(e)}")
                
                # Metadata
                st.markdown(f"**Submitted:** {entry.get('timestamp', 'Unknown')[:10]}")
                if entry.get('latitude') and entry.get('longitude'):
                    st.markdown(f"**Coordinates:** {entry['latitude']:.4f}, {entry['longitude']:.4f}")

# Farming Wisdom Map Page
elif page == "🗺️ Farming Wisdom Map":
    st.header("Farming Wisdom Map")
    st.markdown("Explore traditional farming knowledge geographically")
    
    # Get entries with coordinates
    geo_entries = [e for e in st.session_state.entries if e.get('latitude') and e.get('longitude')]
    
    if geo_entries:
        # Create map centered on India
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        
        # Add markers for each entry
        for entry in geo_entries:
            folium.Marker(
                [entry['latitude'], entry['longitude']],
                popup=f"<b>{entry.get('title', 'Untitled')}</b><br>"
                      f"Category: {entry.get('category', 'Unknown')}<br>"
                      f"Language: {entry.get('language', 'Unknown')}<br>"
                      f"Location: {entry.get('location_name', 'Unknown')}",
                tooltip=entry.get('title', 'Untitled')
            ).add_to(m)
        
        # Display map
        st_folium(m, width=1200, height=600)
        
        st.write(f"Showing {len(geo_entries)} entries with location data")
    else:
        st.info("No entries with location data found. Submit entries with coordinates to see them on the map!")

# Search Knowledge Page
elif page == "🔍 Search Knowledge":
    st.header("Search Farming Knowledge")
    
    # Search input
    search_query = st.text_input("Search for farming practices, techniques, or knowledge...")
    
    # Advanced filters
    with st.expander("Advanced Filters"):
        col1, col2 = st.columns(2)
        with col1:
            search_language = st.selectbox("Language", ["All"] + get_languages(), key="search_lang")
            search_category = st.selectbox("Category", ["All"] + get_categories(), key="search_cat")
        with col2:
            has_media = st.checkbox("Has Media")
            has_location = st.checkbox("Has Location Data")
    
    if search_query:
        results = search_entries(
            st.session_state.entries,
            search_query,
            language=search_language if search_language != "All" else None,
            category=search_category if search_category != "All" else None,
            has_media=has_media,
            has_location=has_location
        )
        
        st.write(f"Found {len(results)} results")
        
        for entry in results:
            with st.expander(f"📖 {entry.get('title', 'Untitled')}"):
                st.markdown(f"**Category:** {entry.get('category', 'Unknown')}")
                st.markdown(f"**Language:** {entry.get('language', 'Unknown')}")
                st.markdown(f"**Location:** {entry.get('location_name', 'Not specified')}")
                st.write(entry.get('description', 'No description'))
                
                if st.button(f"🔊 Listen", key=f"search_tts_{entry.get('id')}"):
                    text_to_speech(entry.get('description', ''), entry.get('language', 'en'))

# Translation Hub Page
elif page == "🌐 Translation Hub":
    st.header("Translation Hub")
    st.markdown("Translate farming knowledge between different Indian languages")
    
    # Translation interface
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Text")
        source_language = st.selectbox("Source Language", ["Auto-detect"] + get_languages())
        source_text = st.text_area("Text to translate", height=200, 
                                 placeholder="Enter farming knowledge in any Indian language...")
        
        if st.button("🔍 Detect Language") and source_text:
            detected_lang = detect_language(source_text)
            st.success(f"Detected language: {detected_lang}")
    
    with col2:
        st.subheader("Translation")
        target_language = st.selectbox("Target Language", get_languages())
        
        if st.button("🌐 Translate", type="primary") and source_text and target_language:
            source_lang = source_language if source_language != "Auto-detect" else "auto"
            with st.spinner("Translating..."):
                translated_text = translate_text(source_text, target_language, source_lang)
                st.text_area("Translated Text", value=translated_text, height=200)
                
                # Option to save as entry
                if st.button("💾 Save as Entry"):
                    st.session_state.form_data = {
                        'title': f"Translated: {source_text[:50]}...",
                        'description': translated_text,
                        'language': target_language,
                        'category': get_categories()[0],
                        'location_name': '',
                        'manual_lat': 0.0,
                        'manual_lon': 0.0
                    }
                    st.success("Content saved to form data! Go to Submit page to complete the entry.")
    
    # Show popular translations
    st.markdown("---")
    st.subheader("Popular Farming Terms Translation")
    
    farming_terms = {
        "Organic Fertilizer": "जैविक उर्वरक",
        "Crop Rotation": "फसल चक्र",
        "Irrigation": "सिंचाई",
        "Pest Control": "कीट नियंत्रण",
        "Soil Health": "मिट्टी की स्वास्थ्य",
        "Harvest": "फसल कटाई",
        "Seeds": "बीज",
        "Monsoon": "मानसून"
    }
    
    cols = st.columns(4)
    for i, (eng, hindi) in enumerate(farming_terms.items()):
        with cols[i % 4]:
            st.info(f"**{eng}**\n{hindi}")

# Export Data Page
elif page == "📊 Export Data":
    st.header("Export Data")
    st.markdown("Export collected farming wisdom for research and analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Options")
        export_format = st.selectbox("Format", ["JSONL", "CSV"])
        include_media_paths = st.checkbox("Include Media File Paths", value=True)
        include_coordinates = st.checkbox("Include Geo-coordinates", value=True)
        
        # Filter options
        export_language = st.selectbox("Language Filter", ["All"] + get_languages(), key="export_lang")
        export_category = st.selectbox("Category Filter", ["All"] + get_categories(), key="export_cat")
    
    with col2:
        st.subheader("Export Statistics")
        total_entries = len(st.session_state.entries)
        entries_with_media = len([e for e in st.session_state.entries if e.get('image_path') or e.get('audio_path')])
        entries_with_coords = len([e for e in st.session_state.entries if e.get('latitude') and e.get('longitude')])
        
        st.metric("Total Entries", total_entries)
        st.metric("Entries with Media", entries_with_media)
        st.metric("Entries with Coordinates", entries_with_coords)
    
    # Export button
    if st.button("Generate Export", type="primary"):
        if st.session_state.entries:
            # Filter entries based on selection
            filtered_entries = st.session_state.entries.copy()
            
            if export_language != "All":
                filtered_entries = [e for e in filtered_entries if e.get('language') == export_language]
            
            if export_category != "All":
                filtered_entries = [e for e in filtered_entries if e.get('category') == export_category]
            
            if export_format == "JSONL":
                export_data = export_to_jsonl(filtered_entries, include_media_paths, include_coordinates)
                st.download_button(
                    label="Download JSONL",
                    data=export_data,
                    file_name=f"ancestral_archive_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl",
                    mime="application/json"
                )
            else:
                export_data = export_to_csv(filtered_entries, include_media_paths, include_coordinates)
                st.download_button(
                    label="Download CSV",
                    data=export_data,
                    file_name=f"ancestral_archive_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            st.success(f"Export ready! {len(filtered_entries)} entries included.")
        else:
            st.warning("No entries to export. Please submit some entries first.")

# Profile Page
elif page == "👤 Profile":
    st.header("User Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Profile Information")
        st.write(f"**Full Name:** {user_info.get('full_name', 'Not provided')}")
        st.write(f"**Username:** {st.session_state.username}")
        st.write(f"**Email:** {user_info.get('email', 'Not provided')}")
        st.write(f"**Member since:** {user_info.get('registration_date', 'Unknown')[:10]}")
        st.write(f"**Entries submitted:** {user_info.get('entries_submitted', 0)}")
    
    with col2:
        st.subheader("My Contributions")
        my_entries = [e for e in st.session_state.entries if e.get('contributor') == st.session_state.username]
        
        if my_entries:
            st.write(f"You have contributed {len(my_entries)} farming knowledge entries:")
            for entry in my_entries[-5:]:  # Show last 5 entries
                st.write(f"• {entry.get('title', 'Untitled')} ({entry.get('category', 'Unknown')})")
            
            if len(my_entries) > 5:
                st.write(f"... and {len(my_entries) - 5} more entries")
        else:
            st.info("You haven't submitted any entries yet. Share your farming wisdom!")
    
    st.markdown("---")
    st.subheader("Account Settings")
    
    # Language preference
    preferred_language = st.selectbox("Preferred Language", get_languages(), 
                                    index=0)
    
    # Notification settings
    st.subheader("Preferences")
    email_notifications = st.checkbox("Email notifications for new entries in my area")
    tts_enabled = st.checkbox("Enable text-to-speech by default", value=True)
    
    if st.button("Update Profile", type="primary"):
        st.success("Profile updated successfully!")

# Settings Page  
elif page == "🔧 Settings":
    st.header("Settings")
    
    st.subheader("Data Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Refresh Data", type="secondary"):
            st.session_state.entries = load_entries()
            st.success("Data refreshed!")
            st.rerun()
    
    with col2:
        if st.button("Clear All Data", type="secondary"):
            if st.checkbox("I understand this will delete all entries"):
                if st.button("Confirm Delete", type="primary"):
                    try:
                        # Clear the entries file
                        with open("data_entries/entries.json", "w") as f:
                            json.dump([], f)
                        st.session_state.entries = []
                        st.success("All data cleared!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error clearing data: {str(e)}")
    
    st.subheader("About")
    st.markdown("""
    **Farming Wisdom Archive** - Version 1.0
    
    A multilingual platform for collecting, preserving, and sharing traditional Indian farming knowledge.
    
    - **Offline-first design** for low-bandwidth regions
    - **Multilingual support** for Indian languages
    - **Accessibility features** with TTS/STT
    - **Geographic mapping** of farming wisdom
    - **Translation hub** for cross-language knowledge sharing
    - **Open-source corpus** for agricultural research
    """)

# Footer
