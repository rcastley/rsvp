import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Wedding RSVP Tracker",
    page_icon="💍",
    layout="wide"
)

# CSV file path
CSV_FILE = "wedding_rsvps.csv"

# Admin password (change this to your desired password)
ADMIN_PASSWORD = "wedding2024"

# Menu options
STARTERS = ["Prawn Cocktail", "Ham Hock Terrine", "Deep Fried Camembert"]
MAINS = ["Beef", "Fish", "Vegetarian"]
DESSERTS = ["Cheesecake", "Eton Mess", "Cheeseboard"]

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
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

def add_guest():
    """Add a new guest to the session state"""
    st.session_state.guests.append({})

def remove_guest(index):
    """Remove a guest from the session state"""
    if len(st.session_state.guests) > 1:
        st.session_state.guests.pop(index)

def reset_form():
    """Reset the form after submission"""
    st.session_state.guests = [{}]
    st.session_state.form_submitted = False

def rsvp_form_page():
    """Main RSVP form page"""
    st.title("💍 Wedding RSVP")
    st.markdown("---")
    st.write("We're excited to celebrate our special day with you! Please let us know if you'll be joining us.")

    # Initialize session state
    initialize_session_state()

    # RSVP Response
    st.subheader("Will you be attending our wedding?")
    attending = st.radio(
        "Response:",
        ["Yes, I/we will attend", "No, I/we cannot attend"],
        key="attending"
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
        if st.button("+ Add Another Guest"):
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
        # Validation
        errors = []

        if not contact_name.strip():
            errors.append("Primary contact name is required")

        if attending == "Yes, I/we will attend":
            for i, guest in enumerate(st.session_state.guests):
                guest_name = st.session_state.get(f"guest_name_{i}", "")
                starter = st.session_state.get(f"starter_{i}", "")
                main = st.session_state.get(f"main_{i}", "")
                dessert = st.session_state.get(f"dessert_{i}", "")

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
        else:
            # Prepare data for saving
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if attending == "Yes, I/we will attend":
                # Save each guest as a separate row
                for i, guest in enumerate(st.session_state.guests):
                    rsvp_data = {
                        "timestamp": timestamp,
                        "contact_name": contact_name,
                        "contact_email": contact_email,
                        "contact_phone": contact_phone,
                        "attending": "Yes",
                        "guest_name": st.session_state.get(f"guest_name_{i}", ""),
                        "starter_choice": st.session_state.get(f"starter_{i}", ""),
                        "main_choice": st.session_state.get(f"main_{i}", ""),
                        "dessert_choice": st.session_state.get(f"dessert_{i}", ""),
                        "dietary_requirements": st.session_state.get(f"dietary_{i}", ""),
                        "comments": comments
                    }
                    save_rsvp(rsvp_data)
            else:
                # Save single "not attending" entry
                rsvp_data = {
                    "timestamp": timestamp,
                    "contact_name": contact_name,
                    "contact_email": contact_email,
                    "contact_phone": contact_phone,
                    "attending": "No",
                    "guest_name": "",
                    "starter_choice": "",
                    "main_choice": "",
                    "dessert_choice": "",
                    "dietary_requirements": "",
                    "comments": comments
                }
                save_rsvp(rsvp_data)

            st.success("✅ RSVP submitted successfully! Thank you for your response.")
            st.balloons()

            # Reset form
            st.session_state.form_submitted = True

            if st.button("Submit Another RSVP"):
                reset_form()
                st.rerun()

def admin_login_page():
    """Admin login page"""
    st.title("🔐 Admin Login")
    st.write("Please enter the password to access the RSVP admin dashboard.")

    password = st.text_input("Password:", type="password", key="admin_password")

    if st.button("Login", type="primary"):
        if password == ADMIN_PASSWORD:
            st.session_state.authenticated = True
            st.success("✅ Access granted! Redirecting to admin dashboard...")
            st.rerun()
        else:
            st.error("❌ Incorrect password. Please try again.")

    st.markdown("---")
    st.info("💡 If you're a guest looking to submit your RSVP, please use the RSVP form instead.")

def admin_summary_page():
    """Admin summary page"""
    if not st.session_state.authenticated:
        st.error("🔐 Please log in to access this page.")
        st.stop()

    st.title("📊 RSVP Summary")

    # Logout button
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.authenticated = False
        st.rerun()

    # Load data
    df = load_rsvps()

    if not df.empty:
        # Summary statistics
        st.header("RSVP Overview")

        # Main metrics
        col1, col2, col3, col4 = st.columns(4)

        total_contacts = df['contact_name'].nunique()
        attending_contacts = df[df['attending'] == 'Yes']['contact_name'].nunique()
        not_attending_contacts = df[df['attending'] == 'No']['contact_name'].nunique()
        total_guests = len(df[df['attending'] == 'Yes'])

        with col1:
            st.metric("Total Responses", total_contacts)
        with col2:
            st.metric("Attending", attending_contacts)
        with col3:
            st.metric("Not Attending", not_attending_contacts)
        with col4:
            st.metric("Total Guests", total_guests)

        # Attendance breakdown
        if total_contacts > 0:
            st.subheader("Response Breakdown")
            attendance_data = {
                'Response': ['Attending', 'Not Attending'],
                'Count': [attending_contacts, not_attending_contacts]
            }
            st.bar_chart(pd.DataFrame(attendance_data).set_index('Response'))

        # Recent RSVPs
        st.subheader("Recent RSVPs")
        recent_df = df.sort_values('timestamp', ascending=False).head(10)

        for _, row in recent_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{row['contact_name']}**")
                    if row['attending'] == 'Yes' and row['guest_name']:
                        st.write(f"Guest: {row['guest_name']}")
                with col2:
                    status_color = "🟢" if row['attending'] == 'Yes' else "🔴"
                    st.write(f"{status_color} {row['attending']}")
                with col3:
                    st.write(f"*{row['timestamp'].split()[0]}*")  # Just the date

                if row['comments']:
                    st.write(f"💬 {row['comments']}")

                st.markdown("---")
    else:
        st.info("📭 No RSVPs have been submitted yet.")

def admin_menu_page():
    """Admin menu planning page"""
    if not st.session_state.authenticated:
        st.error("🔐 Please log in to access this page.")
        st.stop()

    st.title("🍽️ Menu Planning")

    # Logout button
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.authenticated = False
        st.rerun()

    # Load data
    df = load_rsvps()
    total_guests = len(df[df['attending'] == 'Yes'])

    if total_guests > 0:
        attending_df = df[df['attending'] == 'Yes']

        # Menu summary in columns
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🥗 Starters")
            starter_counts = attending_df['starter_choice'].value_counts()
            for starter, count in starter_counts.items():
                st.write(f"**{starter}:** {count} guests")

            # Chart
            if not starter_counts.empty:
                st.bar_chart(starter_counts)

        with col2:
            st.subheader("🍽️ Main Courses")
            main_counts = attending_df['main_choice'].value_counts()
            for main, count in main_counts.items():
                st.write(f"**{main}:** {count} guests")

            # Chart
            if not main_counts.empty:
                st.bar_chart(main_counts)

        with col3:
            st.subheader("🍰 Desserts")
            dessert_counts = attending_df['dessert_choice'].value_counts()
            for dessert, count in dessert_counts.items():
                st.write(f"**{dessert}:** {count} guests")

            # Chart
            if not dessert_counts.empty:
                st.bar_chart(dessert_counts)

        # Dietary requirements
        st.subheader("🥜 Dietary Requirements & Allergies")
        dietary_df = attending_df[attending_df['dietary_requirements'].notna() &
                                (attending_df['dietary_requirements'] != '')]

        if not dietary_df.empty:
            for _, row in dietary_df.iterrows():
                st.write(f"**{row['guest_name']}:** {row['dietary_requirements']}")
        else:
            st.write("No special dietary requirements reported.")
    else:
        st.info("No attending guests yet to display menu planning data.")

def admin_data_page():
    """Admin detailed data page"""
    if not st.session_state.authenticated:
        st.error("🔐 Please log in to access this page.")
        st.stop()

    st.title("📋 Detailed Data")

    # Logout button
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.authenticated = False
        st.rerun()

    # Load data
    df = load_rsvps()

    if not df.empty:
        # Export functionality
        st.subheader("📥 Export Data")
        col1, col2 = st.columns(2)

        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download All Data (CSV)",
                data=csv,
                file_name=f"wedding_rsvps_all_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

        with col2:
            # Export only attending guests
            attending_df = df[df['attending'] == 'Yes']
            if not attending_df.empty:
                attending_csv = attending_df.to_csv(index=False)
                st.download_button(
                    label="✅ Download Attending Only (CSV)",
                    data=attending_csv,
                    file_name=f"wedding_rsvps_attending_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

        # Search and filter
        st.subheader("🔍 Search & Filter")
        search_term = st.text_input("Search by contact name or guest name:")

        filtered_df = df
        if search_term:
            filtered_df = df[
                df['contact_name'].str.contains(search_term, case=False, na=False) |
                df['guest_name'].str.contains(search_term, case=False, na=False)
            ]

        # Display data table
        st.subheader("📋 Complete RSVP Data")
        if not filtered_df.empty:
            st.dataframe(
                filtered_df,
                use_container_width=True,
                column_config={
                    "timestamp": "Submitted",
                    "contact_name": "Contact",
                    "contact_email": "Email",
                    "contact_phone": "Phone",
                    "attending": "Status",
                    "guest_name": "Guest",
                    "starter_choice": "Starter",
                    "main_choice": "Main",
                    "dessert_choice": "Dessert",
                    "dietary_requirements": "Dietary Notes",
                    "comments": "Comments"
                }
            )

            st.write(f"Showing {len(filtered_df)} of {len(df)} total responses")
        else:
            st.write("No data matches your search criteria.")
    else:
        st.info("📭 No RSVPs have been submitted yet.")

def main():
    # Initialize session state
    initialize_session_state()

    # Define pages
    pages = [
        st.Page(rsvp_form_page, title="RSVP Form", icon="💍", default=True),
        st.Page(admin_login_page, title="Admin Login", icon="🔐"),
        st.Page(admin_summary_page, title="Summary", icon="📊"),
        st.Page(admin_menu_page, title="Menu Planning", icon="🍽️"),
        st.Page(admin_data_page, title="Data Export", icon="📋"),
    ]

    # Navigation
    pg = st.navigation(pages)
    pg.run()

if __name__ == "__main__":
    main()
