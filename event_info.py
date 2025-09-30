import streamlit as st

def event_info_page():
    """Event information page showing venue, timeline, and guest information"""
    
    st.title(f":material/celebration: {st.secrets['wedding']['wedding_couple']} Wedding")
    st.write(st.secrets['event']['welcome_text'])
    
    st.markdown("---")
    
    # Wedding Date and Time
    st.header(":material/calendar_today: Date & Time")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Wedding Date")
        st.write(st.secrets['event']['wedding_date'])
        
    with col2:
        st.subheader("Ceremony Time")
        st.write(st.secrets['event']['ceremony_time'])
    
    st.markdown("---")
    
    # Ceremony Venue (Church)
    if st.secrets['event'].get('ceremony_venue_name'):
        st.header(":material/church: Ceremony Venue")
        
        ceremony_col1, ceremony_col2 = st.columns([2, 1])
        
        with ceremony_col1:
            st.subheader(st.secrets['event']['ceremony_venue_name'])
            st.write(st.secrets['event']['ceremony_venue_address'])
            
            if st.secrets['event'].get('ceremony_venue_description'):
                st.write("")
                st.write(st.secrets['event']['ceremony_venue_description'])
            
            # Add map if URL provided
            if st.secrets['event'].get('ceremony_venue_map_url'):
                st.page_link(st.secrets['event']['ceremony_venue_map_url'], label='Open in Maps', icon=":material/map:")

        with ceremony_col2:
            # Ceremony venue image if provided
            if st.secrets['event'].get('ceremony_venue_image'):
                st.image(st.secrets['event']['ceremony_venue_image'], width="content")
        
        # Map display if coordinates provided
        if st.secrets['event'].get('ceremony_venue_latitude') and st.secrets['event'].get('ceremony_venue_longitude'):
            st.map(
                data={'lat': [st.secrets['event']['ceremony_venue_latitude']], 
                      'lon': [st.secrets['event']['ceremony_venue_longitude']]},
                zoom=15,
                size=20
            )
        
        st.markdown("---")
    
    # Reception Venue
    st.header(":material/celebration: Reception Venue")
    
    venue_col1, venue_col2 = st.columns([2, 1])
    
    with venue_col1:
        st.subheader(st.secrets['event']['venue_name'])
        st.write(st.secrets['event']['venue_address'])
        
        if st.secrets['event'].get('venue_description'):
            st.write("")
            st.write(st.secrets['event']['venue_description'])
        
        # Add map if URL provided
        if st.secrets['event'].get('venue_map_url'):
            st.page_link(st.secrets['event']['venue_map_url'], label='Open in Maps', icon=":material/map:")

    with venue_col2:
        # Venue image if provided
        if st.secrets['event'].get('venue_image'):
            st.image(st.secrets['event']['venue_image'], width="content")
    
    # Map display if coordinates provided
    if st.secrets['event'].get('venue_latitude') and st.secrets['event'].get('venue_longitude'):
        st.map(
            data={'lat': [st.secrets['event']['venue_latitude']], 
                  'lon': [st.secrets['event']['venue_longitude']]},
            zoom=15,
            size=20
        )
    
    st.markdown("---")
    
    # Timeline
    st.header(":material/schedule: Timeline")
    
    timeline_items = st.secrets['event'].get('timeline', [])
    if timeline_items:
        for item in timeline_items:
            with st.container():
                time_col, event_col = st.columns([1, 3])
                with time_col:
                    st.markdown(f"**{item['time']}**")
                with event_col:
                    st.write(item['event'])
                    if item.get('description'):
                        st.caption(item['description'])
        st.markdown("")
    
    st.markdown("---")

    # Menu Information
    if st.secrets.get('menu'):
        menu_info = st.secrets['menu']

        # Check if there are any detailed menu items to display
        starters_detailed = menu_info.get('starters_detailed', [])
        mains_detailed = menu_info.get('mains_detailed', [])
        desserts_detailed = menu_info.get('desserts_detailed', [])

        # Helper function to check if items exist and are valid
        def has_valid_items(items):
            if not items:
                return False
            for item in items:
                if isinstance(item, dict):
                    if item.get('name', '').strip():
                        return True
                elif isinstance(item, str) and item.strip():
                    return True
            return False

        has_starters = has_valid_items(starters_detailed)
        has_mains = has_valid_items(mains_detailed)
        has_desserts = has_valid_items(desserts_detailed)

        if has_starters or has_mains or has_desserts:
            st.header(":material/restaurant_menu: Menu")

            # Optional menu description
            if menu_info.get('menu_description'):
                st.write(menu_info['menu_description'])

            menu_col1, menu_col2, menu_col3 = st.columns(3)

            if has_starters:
                with menu_col1:
                    st.subheader(":material/restaurant: Starters")
                    for item in starters_detailed:
                        if isinstance(item, dict):
                            if item.get('name', '').strip():
                                st.markdown(f"**{item['name']}**")
                                if item.get('description'):
                                    st.caption(item['description'])
                                st.write("")
                        elif isinstance(item, str) and item.strip():
                            st.write(f"• {item}")

            if has_mains:
                with menu_col2:
                    st.subheader(":material/hand_meal: Main Courses")
                    for item in mains_detailed:
                        if isinstance(item, dict):
                            if item.get('name', '').strip():
                                st.markdown(f"**{item['name']}**")
                                if item.get('description'):
                                    st.caption(item['description'])
                                st.write("")
                        elif isinstance(item, str) and item.strip():
                            st.write(f"• {item}")

            if has_desserts:
                with menu_col3:
                    st.subheader(":material/cake: Desserts")
                    for item in desserts_detailed:
                        if isinstance(item, dict):
                            if item.get('name', '').strip():
                                st.markdown(f"**{item['name']}**")
                                if item.get('description'):
                                    st.caption(item['description'])
                                st.write("")
                        elif isinstance(item, str) and item.strip():
                            st.write(f"• {item}")

            # Optional menu notes
            if menu_info.get('menu_notes'):
                st.info(f":material/info: {menu_info['menu_notes']}")

            st.markdown("---")

    # Accommodations
    if st.secrets['event'].get('accommodations'):
        st.header(":material/hotel: Accommodations")
        st.write(st.secrets['event'].get('accommodations_intro', 
                 'We have reserved room blocks at the following hotels:'))
        
        accommodations = st.secrets['event']['accommodations']
        
        for hotel in accommodations:
            with st.expander(f":material/hotel: {hotel['name']}", expanded=False):
                st.write(f"**Address:** {hotel['address']}")
                
                if hotel.get('distance'):
                    st.write(f"**Distance from venue:** {hotel['distance']}")
                
                if hotel.get('phone'):
                    st.write(f"**Phone:** {hotel['phone']}")
                
                if hotel.get('booking_code'):
                    st.info(f":material/info: Use booking code: **{hotel['booking_code']}** for our group rate")
                
                if hotel.get('website'):
                    st.markdown(f"[:material/link: Visit Website]({hotel['website']})")
                
                if hotel.get('notes'):
                    st.write(hotel['notes'])
        
        st.markdown("---")
    
    # Transportation
    if st.secrets['event'].get('transportation'):
        st.header(":material/directions_car: Transportation & Parking")
        
        transport_info = st.secrets['event']['transportation']
        
        if transport_info.get('parking'):
            st.subheader("Parking")
            st.write(transport_info['parking'])
        
        if transport_info.get('public_transport'):
            st.subheader("Public Transportation")
            st.write(transport_info['public_transport'])
        
        if transport_info.get('taxi_info'):
            st.subheader("Taxi Services")
            st.write(transport_info['taxi_info'])
        
        st.markdown("---")
    
    # Dress Code
    dress_code = st.secrets['event'].get('dress_code')
    if dress_code:
        st.header(":material/checkroom: Dress Code")
        st.write(dress_code)
        
        dress_code_notes = st.secrets['event'].get('dress_code_notes')
        if dress_code_notes:
            st.info(dress_code_notes)
        
        st.markdown("---")
    
    # Gift Registry
    registries = st.secrets['event'].get('registry')
    if registries:
        # Filter out registries with empty name or URL
        valid_registries = [
            r for r in registries
            if r.get('name', '').strip() and r.get('url', '').strip()
        ]

        if valid_registries:
            st.header(":material/card_giftcard: Gift Registry")
            st.write(st.secrets['event'].get('registry_message',
                     'Your presence is the greatest gift, but if you wish to give something, we are registered at:'))

            reg_cols = st.columns(len(valid_registries))
            for idx, registry in enumerate(valid_registries):
                with reg_cols[idx]:
                    st.markdown(f"""
                    <div style='
                        text-align: center;
                        padding: 20px;
                        border: 1px solid #ddd;
                        border-radius: 10px;
                        background-color: #f9f9f9;
                    '>
                        <h3>{registry['name']}</h3>
                        <a href='{registry['url']}' target='_blank' style='
                            text-decoration: none;
                            background-color: #4CAF50;
                            color: white;
                            padding: 10px 20px;
                            border-radius: 5px;
                            display: inline-block;
                            margin-top: 10px;
                        '>View Registry</a>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")
    
    # Additional Information
    additional_info = st.secrets['event'].get('additional_info')
    if additional_info:
        # Filter out items with empty title or content
        valid_info = [
            item for item in additional_info
            if item.get('title', '').strip() and item.get('content', '').strip()
        ]

        if valid_info:
            st.header(":material/info: Additional Information")

            for info_item in valid_info:
                with st.expander(info_item['title']):
                    st.write(info_item['content'])

            st.markdown("---")
    
    # Contact Information
    if st.secrets['event'].get('contact'):
        st.header(":material/contact_mail: Questions?")
        
        contact = st.secrets['event']['contact']
        
        st.write("If you have any questions, please don't hesitate to reach out:")
        
        contact_col1, contact_col2 = st.columns(2)
        
        if contact.get('bride'):
            with contact_col1:
                st.subheader(contact['bride']['name'])
                if contact['bride'].get('phone'):
                    st.write(f":material/phone: {contact['bride']['phone']}")
                if contact['bride'].get('email'):
                    st.write(f":material/email: {contact['bride']['email']}")

        if contact.get('groom'):
            with contact_col2:
                st.subheader(contact['groom']['name'])
                if contact['groom'].get('email'):
                    st.write(f":material/phone: {contact['groom']['email']}")
                if contact['groom'].get('phone'):
                    st.write(f":material/email: {contact['groom']['phone']}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        f"We can't wait to celebrate with you! :material/favorite:<br>"
        f"{st.secrets['wedding']['wedding_couple']}"
        "</div>",
        unsafe_allow_html=True
    )