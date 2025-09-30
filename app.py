import streamlit as st
from datetime import datetime, timedelta

# Import admin functions
from admin import admin_login_page, admin_summary_page, admin_menu_page, admin_data_page

# Import event info page
from event_info import event_info_page

# Import shared utilities
from utils import (
    save_rsvp, get_deadline_datetime, is_past_deadline,
    is_within_grace_period, is_within_warning_period, get_time_until_deadline,
    format_time_remaining
)

# Configure the page
st.set_page_config(
    page_title=st.secrets["wedding"]["page_title"],
    page_icon=st.secrets["wedding"]["page_icon"],
    #layout="wide"
)
# Custom HTML/CSS for the banner
custom_html = f"""
<div style="
            padding: 0px;
            margin: 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    <img src="{st.secrets['wedding']['banner_image']}" alt="Banner Image">
</div>
"""
# Display the custom HTML
st.components.v1.html(custom_html)
# Menu options
STARTERS = st.secrets["menu"]["starters"]
MAINS = st.secrets["menu"]["mains"]
DESSERTS = st.secrets["menu"]["desserts"]

def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        'guests': [{}],
        'form_submitted': False,
        'submission_in_progress': False,
        'authenticated': False,
        'form_data': {}
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

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
    # Reset main form state
    form_state_reset = {
        'guests': [{}],
        'form_submitted': False,
        'submission_in_progress': False,
        'form_data': {}
    }

    for key, value in form_state_reset.items():
        st.session_state[key] = value

    # Clear form fields
    form_keys = ["attending", "contact_name", "contact_email", "contact_phone", "comments"]

    # Add guest-specific fields
    for i in range(10):  # Clear up to 10 guests worth of data
        form_keys.extend([
            f"guest_name_{i}", f"starter_{i}", f"main_{i}",
            f"dessert_{i}", f"dietary_{i}"
        ])

    # Remove the keys from session state
    for key in form_keys:
        st.session_state.pop(key, None)

def process_submission():
    """Process the RSVP submission"""
    form_data = st.session_state.form_data

    # Check deadline enforcement first
    if is_past_deadline() and not is_within_grace_period():
        st.error(":material/block: RSVP deadline has passed. Submissions are no longer accepted.")
        st.info("Please contact the wedding couple directly if you need to make changes to your RSVP.")
        st.session_state.submission_in_progress = False
        return False

    # Show warning if in grace period
    if is_within_grace_period():
        st.warning(":material/timer: Submitting during grace period - deadline has passed but submissions are still being accepted.")

    # Show urgency warning if within warning period
    if is_within_warning_period():
        time_remaining = get_time_until_deadline()
        formatted_time = format_time_remaining(time_remaining)
        st.warning(f":material/schedule: Submitting close to deadline - {formatted_time} remaining!")

    # Validation
    errors = []
    
    if not form_data.get('contact_name', '').strip():
        errors.append("Primary contact name is required")
    
    if form_data.get('attending') == "Yes, I/we will attend":
        for i, _ in enumerate(st.session_state.guests):
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
            for i, _ in enumerate(st.session_state.guests):
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
    st.markdown("---")
    st.subheader(f"{st.secrets['wedding']['wedding_couple']} Wedding RSVP")
    st.write(st.secrets["ui"]["welcome_message"])

    # Check deadline status and display countdown/warning
    deadline = get_deadline_datetime()
    if deadline:
        if is_past_deadline():
            if is_within_grace_period():
                st.error(":material/schedule: RSVP deadline has passed, but submissions are still being accepted for a limited time.")
                grace_end = deadline + timedelta(hours=st.secrets["deadline"].get("grace_period_hours", 24))
                st.warning(f":material/timer: Grace period ends: {grace_end.strftime('%B %d, %Y at %I:%M %p %Z')}")
            else:
                st.error(":material/block: RSVP deadline has passed. New submissions are no longer accepted.")
                st.info("Please contact the wedding couple directly if you need to make changes to your RSVP.")
                return  # Stop rendering the form
        elif is_within_warning_period():
            time_remaining = get_time_until_deadline()
            formatted_time = format_time_remaining(time_remaining)

            st.warning(f":material/schedule: **RSVP Deadline Approaching!**")

            # Create a prominent countdown display
            with st.container():
                st.markdown(f"""
                <div style="
                    background: linear-gradient(90deg, #ff6b6b, #ee5a52);
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    color: white;
                    margin: 10px 0;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                ">
                    <h3>⏰ Time Remaining: {formatted_time}</h3>
                    <p>Deadline: {deadline.strftime('%B %d, %Y at %I:%M %p %Z')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Show normal deadline info
            time_remaining = get_time_until_deadline()
            formatted_time = format_time_remaining(time_remaining)
            st.info(f":material/schedule: RSVP Deadline: {deadline.strftime('%B %d, %Y at %I:%M %p %Z')} ({formatted_time} remaining)")

    st.markdown("---")
    
    # Initialize session state
    initialize_session_state()
    
    # Check if form has been successfully submitted
    if st.session_state.form_submitted:
        st.success(":material/check_circle: RSVP submitted successfully! Thank you for your response.")
        st.balloons()
        
        if st.button("Submit Another RSVP", type="primary"):
            reset_form()
            st.rerun()
        
        st.info(":material/lightbulb: If you need to submit another RSVP or make changes, please click the button above.")
        return
    
    # Check if submission is in progress
    if st.session_state.submission_in_progress:
        st.info(":material/refresh: Processing your RSVP submission...")
        with st.spinner("Please wait..."):
            if process_submission():
                st.rerun()
            else:
                st.rerun()
        return
    
    # RSVP Response
    st.markdown("**Will you be attending our wedding?**")
    attending = st.radio(
        "**Will you be attending our wedding?**",
        ["Yes, I/we will attend", "No, I/we cannot attend"],
        key="attending", horizontal=True, label_visibility="collapsed"
    )
    
    # Contact Information
    st.markdown("**Contact Information**")
    contact_col1, contact_col2, contact_col3 = st.columns([3, 4, 2])
    with contact_col1:
        contact_name = st.text_input("Primary Contact Name*", key="contact_name", width=300)
    with contact_col2:
        contact_email = st.text_input("Email Address", key="contact_email", width=350)
    with contact_col3:
        contact_phone = st.text_input("Phone Number", key="contact_phone", width=200)
    
    if attending == "Yes, I/we will attend":
        st.markdown("**Guest Details & Menu Choices**")
        st.write("Please provide details for each guest attending:")
        
        # Display guests
        for i, _ in enumerate(st.session_state.guests):
            with st.container(border=True):
                st.markdown(f"**Guest {i + 1}**")

                # Create columns for guest details
                guest_col1, guest_col2 = st.columns([3, 1])

                with guest_col1:
                    st.text_input(
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
                menu_col1, menu_col2, menu_col3 = st.columns([1.2, 1.8, 1.1])

                with menu_col1:
                    st.selectbox(
                        "Starter Choice*",
                        [""] + STARTERS,
                        key=f"starter_{i}",
                        index=0
                    )

                with menu_col2:
                    st.selectbox(
                        "Main Course*",
                        [""] + MAINS,
                        key=f"main_{i}",
                        index=0
                    )

                with menu_col3:
                    st.selectbox(
                        "Dessert Choice*",
                        [""] + DESSERTS,
                        key=f"dessert_{i}",
                        index=0
                    )

                # Dietary requirements
                st.text_area(
                    "Dietary Requirements/Allergies",
                    key=f"dietary_{i}",
                    placeholder="Please list any allergies or dietary requirements",
                    height=60
                )


        # Add guest button
        if st.button("**Add Another Guest**", icon=":material/add:"):
            add_guest()
            st.rerun()
    
    # Additional comments
    st.markdown("**Additional Comments**")
    comments = st.text_area(
        "Any additional comments or special requests:",
        key="comments",
        height=100
    )
    
    # Submit button
    st.markdown("---")
    if st.button("Submit RSVP", type="primary", width="content"):
        # Store form data in session state before processing
        st.session_state.form_data = {
            'attending': attending,
            'contact_name': contact_name,
            'contact_email': contact_email,
            'contact_phone': contact_phone,
            'comments': comments
        }
        
        # Store guest data
        for i, _ in enumerate(st.session_state.guests):
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

    # Define admin pages
    admin_pages = {
        ":material/bar_chart: Summary": admin_summary_page,
        ":material/restaurant: Menu Planning": admin_menu_page,
        ":material/download: Data Export": admin_data_page,
    }

    if st.session_state.authenticated:
        # Admin is authenticated - show all pages including RSVP form
        with st.sidebar:
            st.markdown("**Admin Panel**")

            # Create admin page navigation
            st.radio(
                "Navigate to:",
                list(admin_pages.keys()),
                key="admin_nav",
                label_visibility="collapsed"
            )

            st.markdown("---")
            if st.button(":material/logout: Logout", type="secondary", width="content"):
                st.session_state.authenticated = False
                st.session_state.just_logged_in = False
                st.success("Successfully logged out!")
                st.rerun()

        # Define pages for authenticated admin (including RSVP form)
        admin_all_pages = [
            st.Page(event_info_page, title="Event Info", icon=":material/celebration:", default=True),
            st.Page(rsvp_form_page, title="RSVP Form", icon=":material/favorite:"),
            st.Page(admin_summary_page, title="Admin Summary", icon=":material/bar_chart:"),
            st.Page(admin_menu_page, title="Menu Planning", icon=":material/restaurant:"),
            st.Page(admin_data_page, title="Data Export", icon=":material/download:"),
        ]

        # Check if admin navigation is selected, if so show that page
        selected_admin_page = st.session_state.get("admin_nav")
        if selected_admin_page and selected_admin_page in admin_pages:
            admin_pages[selected_admin_page]()
        else:
            # Show regular navigation with all pages
            pg = st.navigation(admin_all_pages)
            pg.run()
    else:
        # Define and run main pages for non-authenticated users
        pages = [
            st.Page(event_info_page, title="Event Info", icon=":material/celebration:", default=True),
            st.Page(rsvp_form_page, title="RSVP Form", icon=":material/favorite:"),
            st.Page(admin_login_page, title="Admin Login", icon=":material/lock:"),
        ]
        pg = st.navigation(pages)
        pg.run()

if __name__ == "__main__":
    main()