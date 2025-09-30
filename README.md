# Wedding RSVP Application

A Streamlit-based web application for managing wedding RSVPs with menu selections, deadline tracking, and administrative dashboard.

## Features

- **Guest RSVP Form** - Allow guests to RSVP with menu selections (starters, mains, desserts)
- **Multi-guest Support** - Submit RSVPs for multiple guests in one submission
- **Deadline Management** - Automatic deadline tracking with warning and grace periods
- **Event Information Page** - Display venue details, timeline, accommodations, and transportation
- **Admin Dashboard** - Secure admin panel with:
  - RSVP summary statistics and charts
  - Menu planning with choice counts
  - Dietary requirements tracking
  - Data export to CSV
  - Search and filter functionality

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/rcastley/rsvp
   cd rsvp
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure secrets**

   Create a `.streamlit/secrets.toml` file with the following structure:

   ```toml
   [wedding]
   wedding_couple = "John & Jane"
   page_title = "Wedding RSVP"
   page_icon = "💍"
   banner_image = "https://example.com/banner.jpg"  # optional

   [ui]
   welcome_message = "We're excited to celebrate with you!"

   [files]
   csv_file = "rsvps.csv"

   [admin]
   password = "your_secure_password_here"

   [menu]
   starters = ["Soup", "Salad", "Bruschetta"]
   mains = ["Chicken", "Beef", "Vegetarian"]
   desserts = ["Cake", "Ice Cream", "Fruit"]

   [deadline]
   deadline_datetime = "2025-12-31 23:59"
   timezone = "America/New_York"
   warning_days = 7
   grace_period_hours = 24

   [event]
   wedding_date = "January 1, 2026"
   ceremony_time = "3:00 PM"
   welcome_text = "Join us for our special day!"

   # Ceremony venue (optional)
   ceremony_venue_name = "St. Mary's Church"
   ceremony_venue_address = "123 Church St, City, State"
   ceremony_venue_description = "Beautiful historic church"
   ceremony_venue_map_url = "https://maps.google.com/?q=..."
   ceremony_venue_latitude = 40.7128
   ceremony_venue_longitude = -74.0060
   ceremony_venue_image = "https://example.com/church.jpg"

   # Reception venue
   venue_name = "Grand Ballroom"
   venue_address = "456 Main St, City, State"
   venue_description = "Elegant venue with gardens"
   venue_map_url = "https://maps.google.com/?q=..."
   venue_latitude = 40.7128
   venue_longitude = -74.0060
   venue_image = "https://example.com/venue.jpg"

   # Timeline
   [[event.timeline]]
   time = "3:00 PM"
   event = "Ceremony"
   description = "Please arrive 15 minutes early"

   [[event.timeline]]
   time = "4:00 PM"
   event = "Cocktail Hour"

   [[event.timeline]]
   time = "5:00 PM"
   event = "Reception"

   # Accommodations (optional)
   accommodations_intro = "Room blocks available at:"
   [[event.accommodations]]
   name = "Hotel Name"
   address = "789 Hotel Ave, City, State"
   distance = "2 miles from venue"
   phone = "(555) 123-4567"
   booking_code = "WEDDING2026"
   website = "https://hotel.com"
   notes = "Mention the wedding for group rate"

   # Transportation (optional)
   [event.transportation]
   parking = "Free parking available on-site"
   public_transport = "Bus line 42 stops nearby"
   taxi_info = "Local taxi: (555) 987-6543"

   # Dress code (optional)
   dress_code = "Formal / Black Tie Optional"
   dress_code_notes = "Outdoor ceremony - heels not recommended"

   # Registry (optional)
   registry_message = "Your presence is our present!"
   [[event.registry]]
   name = "Store Name"
   url = "https://registry.com/johnandjane"

   # Additional info (optional)
   [[event.additional_info]]
   title = "COVID-19 Information"
   content = "We ask that all guests be vaccinated"

   # Contact info (optional)
   [event.contact.bride]
   name = "Jane Doe"
   email = "jane@email.com"
   phone = "(555) 111-2222"

   [event.contact.groom]
   name = "John Smith"
   email = "john@email.com"
   phone = "(555) 333-4444"
   ```

## Running the Application

1. **Start the Streamlit app**

   ```bash
   streamlit run app.py
   ```

2. **Access the application**
   - Open your browser to `http://localhost:8501`
   - The RSVP form will be the default landing page

3. **Admin access**
   - Navigate to "Admin Login" from the sidebar
   - Enter the password configured in secrets.toml
   - Access admin features: summary, menu planning, data export
