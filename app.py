import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Import admin functions
from admin import admin_login_page, admin_summary_page, admin_menu_page, admin_data_page

# Configure the page
st.set_page_config(
    page_title="Wedding RSVP Tracker",
    page_icon="💍",
    #layout="wide"
)
# Custom HTML/CSS for the banner
custom_html = """
<div class="banner">
    <img src="https://www.realweddings.co.uk/detail/the-white-hart-ufford/m/v/showcase_hero/91652/459927009_18285199603224087_4291546012477049125_n.jpg" alt="Banner Image">
</div>
<style>
    .banner {
        width: 160%;
        height: 200px;
        overflow: hidden;
    }
    .banner img {
        width: 100%;
        object-fit: cover;
    }
</style>
"""
# Display the custom HTML
st.components.v1.html(custom_html)
# CSV file path
CSV_FILE = "wedding_rsvps.csv"

# Menu options
STARTERS = ["Prawn Cocktail", "Ham Hock Terrine (GF)", "Deep Fried Camembert (V)"]
MAINS = ["Braised and Confit Shoulder of Lamb", "Salmon en Papillote", "Wild Mushroom and Spinach Wellington (V/GF)"]
DESSERTS = ["Lemon Cheesecake (V)", "Eton Mess (V/GF)", "Cheeseboard"]

def load_rsvps():
    """Load existing RSVP data from CSV file"""
    if os.path.exists(CSV_FILE):
        try:
            return pd.read_csv(CSV_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_rsvp(rsvp_data):
    """Save RSVP data to CSV file"""
    df = load_rsvps()
    new_df = pd.DataFrame([rsvp_data])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def initialize_session_state():
    """Initialize session state variables"""
    if 'guests' not in st.session_state:
        st.session_state.guests = [{}]
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    if 'submission_in_progress' not in st.session_state:
        st.session_state.submission_in_progress = False
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

def add_guest():
    """Add a new guest to the session state"""
    if not st.session_state.submission_in_progress:
        st.session_state.guests.append({})

def remove_guest(index):
    """Remove a guest from the session state"""
    if len(st.session_state.guests) > 1 and not st.session_state.submission_in_progress:
        st.session_state.guests.pop(index)

def reset_form():
    """Reset the form after submission"""
    st.session_state.guests = [{}]
    st.session_state.form_submitted = False
    st.session_state.submission_in_progress = False
    st.session_state.form_data = {}
    
    # Clear all form fields
    form_keys_to_clear = [
        "attending", "contact_name", "contact_email", "contact_phone", "comments"
    ]
    
    # Clear guest-specific fields
    for i in range(10):  # Clear up to 10 guests worth of data
        guest_keys = [
            f"guest_name_{i}", f"starter_{i}", f"main_{i}", 
            f"dessert_{i}", f"dietary_{i}"
        ]
        form_keys_to_clear.extend(guest_keys)
    
    # Remove the keys from session state
    for key in form_keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def process_submission():
    """Process the RSVP submission"""
    form_data = st.session_state.form_data
    
    # Validation
    errors = []
    
    if not form_data.get('contact_name', '').strip():
        errors.append("Primary contact name is required")
    
    if form_data.get('attending') == "Yes, I/we will attend":
        for i, guest in enumerate(st.session_state.guests):
            guest_name = form_data.get(f"guest_name_{i}", "")
            starter = form_data.get(f"starter_{i}", "")
            main = form_data.get(f"main_{i}", "")
            dessert = form_data.get(f"dessert_{i}", "")
            
            if not guest_name.strip():
                errors.append(f"Guest {i + 1} name is required")
            if not starter:
                errors.append(f"Guest {i + 1} starter choice is required")
            if not main:
                errors.append(f"Guest {i + 1} main course choice is required")
            if not dessert:
                errors.append(f"Guest {i + 1} dessert choice is required")
    
    if errors:
        st.error("Please fix the following errors:")
        for error in errors:
            st.error(f"• {error}")
        
        # Reset submission state on error
        st.session_state.submission_in_progress = False
        return False
    
    # Prepare data for saving
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        if form_data.get('attending') == "Yes, I/we will attend":
            # Save each guest as a separate row
            for i, guest in enumerate(st.session_state.guests):
                rsvp_data = {
                    "timestamp": timestamp,
                    "contact_name": form_data.get('contact_name', ''),
                    "contact_email": form_data.get('contact_email', ''),
                    "contact_phone": form_data.get('contact_phone', ''),
                    "attending": "Yes",
                    "guest_name": form_data.get(f"guest_name_{i}", ""),
                    "starter_choice": form_data.get(f"starter_{i}", ""),
                    "main_choice": form_data.get(f"main_{i}", ""),
                    "dessert_choice": form_data.get(f"dessert_{i}", ""),
                    "dietary_requirements": form_data.get(f"dietary_{i}", ""),
                    "comments": form_data.get('comments', '')
                }
                save_rsvp(rsvp_data)
        else:
            # Save single "not attending" entry
            rsvp_data = {
                "timestamp": timestamp,
                "contact_name": form_data.get('contact_name', ''),
                "contact_email": form_data.get('contact_email', ''),
                "contact_phone": form_data.get('contact_phone', ''),
                "attending": "No",
                "guest_name": "",
                "starter_choice": "",
                "main_choice": "",
                "dessert_choice": "",
                "dietary_requirements": "",
                "comments": form_data.get('comments', '')
            }
            save_rsvp(rsvp_data)
        
        # Mark as successfully submitted
        st.session_state.form_submitted = True
        st.session_state.submission_in_progress = False
        return True
        
    except Exception as e:
        st.error(f"An error occurred while saving your RSVP: {str(e)}")
        st.session_state.submission_in_progress = False
        return False

def rsvp_form_page():
    """Main RSVP form page"""
    st.title("Robert & Charlotte Wedding RSVP")
    st.markdown("---")
    st.write("We're excited to celebrate our special day with you! Please let us know if you'll be joining us.")
    
    # Initialize session state
    initialize_session_state()
    
    # Check if form has been successfully submitted
    if st.session_state.form_submitted:
        st.success("✅ RSVP submitted successfully! Thank you for your response.")
        st.balloons()
        
        if st.button("Submit Another RSVP", type="primary"):
            reset_form()
            st.rerun()
        
        st.info("💡 If you need to submit another RSVP or make changes, please click the button above.")
        return
    
    # Check if submission is in progress
    if st.session_state.submission_in_progress:
        st.info("🔄 Processing your RSVP submission...")
        with st.spinner("Please wait..."):
            if process_submission():
                st.rerun()
            else:
                st.rerun()
        return
    
    # RSVP Response
    st.caption("Will you be attending our wedding?")
    attending = st.radio(
        "**Will you be attending our wedding?**",
        ["Yes, I/we will attend", "No, I/we cannot attend"],
        key="attending", horizontal=True, label_visibility="collapsed"
    )
    
    # Contact Information
    st.subheader("Contact Information")
    contact_name = st.text_input("Primary Contact Name*", key="contact_name")
    contact_email = st.text_input("Email Address", key="contact_email")
    contact_phone = st.text_input("Phone Number", key="contact_phone")
    
    if attending == "Yes, I/we will attend":
        st.subheader("Guest Details & Menu Choices")
        st.write("Please provide details for each guest attending:")
        
        # Display guests
        for i, guest in enumerate(st.session_state.guests):
            with st.container():
                st.markdown(f"**Guest {i + 1}**")
                
                # Create columns for guest details
                guest_col1, guest_col2, guest_col3 = st.columns([2, 1, 1])
                
                with guest_col1:
                    guest_name = st.text_input(
                        f"Guest Name*",
                        key=f"guest_name_{i}",
                        placeholder="Enter guest name"
                    )
                
                with guest_col2:
                    if i > 0:  # Don't show remove button for first guest
                        if st.button(f"Remove", key=f"remove_{i}"):
                            remove_guest(i)
                            st.rerun()
                
                # Menu selections
                menu_col1, menu_col2, menu_col3 = st.columns(3)
                
                with menu_col1:
                    starter = st.selectbox(
                        "Starter Choice*",
                        [""] + STARTERS,
                        key=f"starter_{i}",
                        index=0
                    )
                
                with menu_col2:
                    main = st.selectbox(
                        "Main Course*",
                        [""] + MAINS,
                        key=f"main_{i}",
                        index=0
                    )
                
                with menu_col3:
                    dessert = st.selectbox(
                        "Dessert Choice*",
                        [""] + DESSERTS,
                        key=f"dessert_{i}",
                        index=0
                    )
                
                # Dietary requirements
                dietary = st.text_area(
                    "Dietary Requirements/Allergies",
                    key=f"dietary_{i}",
                    placeholder="Please list any allergies or dietary requirements",
                    height=60
                )
                
                st.markdown("---")
        
        # Add guest button
        if st.button("**Add Another Guest**", icon=":material/add:"):
            add_guest()
            st.rerun()
    
    # Additional comments
    st.subheader("Additional Comments")
    comments = st.text_area(
        "Any additional comments or special requests:",
        key="comments",
        height=100
    )
    
    # Submit button
    st.markdown("---")
    if st.button("Submit RSVP", type="primary", use_container_width=True):
        # Store form data in session state before processing
        st.session_state.form_data = {
            'attending': attending,
            'contact_name': contact_name,
            'contact_email': contact_email,
            'contact_phone': contact_phone,
            'comments': comments
        }
        
        # Store guest data
        for i, guest in enumerate(st.session_state.guests):
            st.session_state.form_data[f"guest_name_{i}"] = st.session_state.get(f"guest_name_{i}", "")
            st.session_state.form_data[f"starter_{i}"] = st.session_state.get(f"starter_{i}", "")
            st.session_state.form_data[f"main_{i}"] = st.session_state.get(f"main_{i}", "")
            st.session_state.form_data[f"dessert_{i}"] = st.session_state.get(f"dessert_{i}", "")
            st.session_state.form_data[f"dietary_{i}"] = st.session_state.get(f"dietary_{i}", "")
        
        # Set submission in progress
        st.session_state.submission_in_progress = True
        st.rerun()

def main():
    # Initialize session state
    initialize_session_state()
    
    # Define pages based on authentication status
    pages = [
        st.Page(rsvp_form_page, title="RSVP Form", icon="💍", default=True),
        st.Page(admin_login_page, title="Admin Login", icon="🔐"),
    ]
    
    # Add admin pages only if authenticated
    if st.session_state.authenticated:
        admin_pages = [
            st.Page(admin_summary_page, title="Summary", icon="📊"),
            st.Page(admin_menu_page, title="Menu Planning", icon="🍽️"),
            st.Page(admin_data_page, title="Data Export", icon="📋"),
        ]
        pages.extend(admin_pages)
    
    # Navigation
    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    main()