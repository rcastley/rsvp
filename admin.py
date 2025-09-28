import streamlit as st
import pandas as pd
import os
from datetime import datetime
import time

# CSV file path
CSV_FILE = "wedding_rsvps.csv"

# Admin password (change this to your desired password)
ADMIN_PASSWORD = "wedding2024"

st.set_page_config(
    page_title="Wedding RSVP Tracker",
    page_icon="💍",
    #layout="wide"
)

def load_rsvps():
    """Load existing RSVP data from CSV file"""
    if os.path.exists(CSV_FILE):
        try:
            return pd.read_csv(CSV_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def show_login_success():
    """Display a comprehensive login success acknowledgment"""
    st.balloons()  # Add celebratory animation
    
    # Create a prominent success container
    with st.container():
        st.markdown("""
        <div style="
            background: linear-gradient(90deg, #4CAF50, #45a049);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        ">
            <h2>🎉 Welcome to Admin Dashboard! 🎉</h2>
            <p>Login successful! You now have access to all RSVP management features.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Brief pause to show the success message
    time.sleep(1)

def admin_welcome_header():
    """Display a welcome header for authenticated admin users"""
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin-bottom: 20px;
        text-align: center;
    ">
        <h3>👋 Welcome, Admin!</h3>
        <p>You are successfully logged in to the Wedding RSVP Management System</p>
    </div>
    """, unsafe_allow_html=True)

def admin_login_page():
    """Admin login page"""
    st.title("🔐 Admin Login")
    st.write("Please enter the password to access the RSVP admin dashboard.")
    
    password = st.text_input("Password:", type="password", key="admin_password")
    
    if st.button("Login", type="primary"):
        if password == ADMIN_PASSWORD:
            # Set authentication state
            st.session_state.authenticated = True
            st.session_state.just_logged_in = True
            
            # Show immediate success feedback
            st.success("✅ Access granted! Welcome to the admin dashboard!")
            
            # Show comprehensive login success acknowledgment
            show_login_success()
            
            # Display login timestamp
            login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.info(f"🕐 Login successful at: {login_time}")
            
            # Auto-redirect message
            st.markdown("**Redirecting to admin dashboard in 3 seconds...**")
            
            # Add a brief delay before rerun for better UX
            time.sleep(3)
            st.rerun()
        else:
            st.error("❌ Incorrect password. Please try again.")
            st.warning("🔔 Access denied - Invalid credentials")
    
    st.markdown("---")
    st.info("💡 If you're a guest looking to submit your RSVP, please use the RSVP form instead.")

def admin_summary_page():
    """Admin summary page"""
    if not st.session_state.authenticated:
        st.error("🔐 Please log in to access this page.")
        st.stop()
    
    # Show welcome header for authenticated users
    admin_welcome_header()
    
    # Check if user just logged in to show additional acknowledgment
    if st.session_state.get('just_logged_in', False):
        st.success("🎯 Successfully accessed RSVP Summary Dashboard!")
        st.session_state.just_logged_in = False  # Reset the flag
    
    st.title("📊 RSVP Summary")
    
    # Logout button
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.just_logged_in = False
        st.success("👋 Successfully logged out!")
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
    
    # Show welcome header for authenticated users
    admin_welcome_header()
    
    st.title("🍽️ Menu Planning")
    
    # Logout button
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.just_logged_in = False
        st.success("👋 Successfully logged out!")
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
    
    # Show welcome header for authenticated users
    admin_welcome_header()
    
    st.title("📋 Detailed Data")
    
    # Logout button
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.authenticated = False
        st.session_state.just_logged_in = False
        st.success("👋 Successfully logged out!")
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