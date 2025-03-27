import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import sqlite3
import hashlib
from PIL import Image
import base64
from io import BytesIO
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def img_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# Hashing functions for password security
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# Database functions
def create_user_table():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)")
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO userstable(username, password) VALUES (?,?)", (username, password))
    conn.commit()
    conn.close()

def create_feedback_table():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS feedback(username TEXT, feedback TEXT, rating INTEGER)")
    conn.commit()
    conn.close()

def add_feedback(username, feedback, rating):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO feedback(username, feedback, rating) VALUES (?,?,?)", (username, feedback, rating))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM userstable WHERE username = ? AND password = ?", (username, password))
    data = c.fetchall()
    conn.close()
    return data
def send_email(username, feedback_text, rating):
    SMTP_SERVER = "smtp.office365.com"  # Your SMTP server
    SMTP_PORT = 587
    EMAIL_SENDER = "support@aptpath.in"  # Your sender email
    EMAIL_PASSWORD = "kjydtmsbmbqtnydk"  # Your SMTP App Password
    RECEIVER_EMAIL = "geethikaraokalakonda@gmail.com"  # Feedback recipient

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = RECEIVER_EMAIL  # Send feedback to your inbox
        msg["Subject"] = "New Feedback Received"

        # Email Body
        body = f"Username: {username}\nRating: {rating}/5\nFeedback:\n{feedback_text}"
        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP Server & Send Email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False




create_user_table()
create_feedback_table()

# Initialize database
create_user_table()

# Set page title
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")


# Animated Heading with Slider Effect
st.markdown(
    """
    <style>
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .animated-heading {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        font-family: 'Poppins', sans-serif;
        color: #007bff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: slideIn 1.5s ease-in-out;
    }
    </style>
    <h1 class="animated-heading">Air Quality Visualization</h1>
    """,
    unsafe_allow_html=True
)


# Login System
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Login", key="login_button", help="Click to login", use_container_width=True):
        st.session_state.show_login = True
        st.session_state.show_signup = False
        st.rerun()
    if st.button("Sign Up", key="signup_button", help="Click to sign up", use_container_width=True):
        st.session_state.show_signup = True
        st.session_state.show_login = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    if "show_login" in st.session_state and st.session_state.show_login:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login Now"):
            if login_user(username, make_hashes(password)):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}")
                st.rerun()
            else:
                st.error("Invalid credentials")

    if "show_signup" in st.session_state and st.session_state.show_signup:
        st.subheader("Sign Up")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')
        if st.button("Register"):
            add_user(new_username, make_hashes(new_password))
            st.success("Account created successfully! You can now log in.")

    st.stop()

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "Navigation", ["Home", "Overview of Pollution", "City Comparisons", "Impacts and Insights", "AQI Status","Quiz","Key Takeaways","Feedback","Logout"],
        icons=["house", "file-earmark-text", "graph-up", "bar-chart", "cloud-sun","star",":speed_balloon:","settings","box-arrow-left"],
        menu_icon="list",
        default_index=0,
        styles={
            "nav-link": {"font-size": "18px", "text-align": "left", "margin": "10px"},
            "nav-link-selected": {"background-color": "#FF4B4B"},
        }
    )

# Home Page
if selected == "Home":
    st.title("Welcome to the Air Quality Index Dashboard")
    try:
        st.image("air_quality.jpg", caption="Air Pollution Visualization")
    except Exception:
        st.image("https://www.epa.gov/sites/default/files/2014-05/aqi-chart.png", caption="Air Pollution Visualization")
    
    st.write("""
### 🌍 Overview  
- **📊 Real-Time Monitoring** – Displays current air pollution levels.  
- **🌫️ AQI (Air Quality Index)** – Color-coded scale for air quality.  
- **📍 Geographic Mapping** – Shows pollution levels on maps.  
- **💨 Pollutant Breakdown** – Monitors PM2.5, PM10, CO, NO₂, etc.  
- **📅 Historical Trends** – Tracks past air quality data.  
- **🚥 Health Risk Alerts** – Provides recommendations based on pollution levels.  
""")

# Power BI Pages
elif selected == "Overview of Pollution":
    st.title("Air Quality Trends")
    components.iframe("https://app.powerbi.com/view?r=eyJrIjoiODE2MDdmMGQtOWY2NS00NTc5LWE4Y2QtMWM2YTQyYWMxYzUwIiwidCI6IjFkNmVkNThjLTMyODktNGMwOS1hZmI3LWJjODlkNTE4NDg0OCJ9", height=600, width=900)
    st.write("## 📊 Key Insights from the Dashboard")  

    st.write("### 📅 Pollution Trends Over Time")  
    st.write("- A **time-series graph** (top-left) shows the sum of **NO₂, RSPM, SO₂, and SPM** pollution levels over the years.")  
    st.write("- There has been a **significant rise in pollution levels post-2010**.")  

    st.write("### 📌 Geographic Distribution of NO₂")  
    st.write("- A **map visualization** (bottom-left) highlights NO₂ pollution levels across different states.")  
    st.write("- **Warangal, Telangana**, appears to have noticeable pollution levels.")  

    st.write("### 📊 Major Pollutant Concentrations")  
    st.write("- **🟦 RSPM (Respirable Suspended Particulate Matter):** 51.97K")  
    st.write("- **🟧 SO₂ (Sulfur Dioxide):** 2.54K")  
    st.write("- **🟪 SPM (Suspended Particulate Matter):** 5.02M")  
    st.write("- **🟪 NO₂ (Nitrogen Dioxide):** 13.89K")  

    st.write("### 🏭 Pollution by Area Type")  
    st.write("- A **pie chart** (bottom-right) categorizes pollution levels by **Residential, Industrial, and Sensitive areas**.")  
    st.write("- The **industrial areas** seem to have the highest pollution levels.")  

    st.write("### 📍 City-Wise Pollution Breakdown")  
    st.write("- A **filterable list** (bottom-right) allows selection of cities like **Agra, Ahmedabad, Aizawl, Akola, etc.**")  
    st.write("- This helps in analyzing pollution levels at a **city level** for deeper insights.")  

    st.write("## 🚨 Conclusion")  
    st.write("- **Air pollution has worsened significantly over the past decade**, with increasing levels of SPM, NO₂, and RSPM.")  
    st.write("- **Industrial zones contribute the most to pollution**, as seen in the area type breakdown.")  
    st.write("- **City-wise pollution tracking enables authorities to focus on high-risk areas** and implement better air quality measures.")  

    st.write("🌍 This dashboard provides a **comprehensive visualization** of air pollution trends, helping policymakers and citizens make informed decisions.")  

elif selected == "City Comparisons":
    st.title("City Comparisons")
    components.iframe("https://app.powerbi.com/view?r=eyJrIjoiODE2MDdmMGQtOWY2NS00NTc5LWE4Y2QtMWM2YTQyYWMxYzUwIiwidCI6IjFkNmVkNThjLTMyODktNGMwOS1hZmI3LWJjODlkNTE4NDg0OCJ9", height=600, width=900)
    st.write("## 🌆 City-Wise Air Pollution Comparison")  

    st.write("### 📊 Pollution Levels Across Cities")  
    st.write("- A **bar chart** (top-left) shows NO₂, RSPM, and SO₂ pollution levels across major cities.")  
    st.write("- Cities like **Delhi, Kolkata, Jaipur, and Agra** exhibit **higher pollution levels**.")  

    st.write("### 🎨 City-Wise Pollution Heatmap")  
    st.write("- A **color-coded heatmap** (center) visually represents pollutant concentration levels across various cities.")  
    st.write("- Darker shades indicate **higher pollution intensity** in specific locations.")  

    st.write("### 📈 Pollution Trends Over Time")  
    st.write("- A **line graph** (bottom) displays the sum of **SPM, SO₂, RSPM, and NO₂** across cities.")  
    st.write("- Pollution levels appear to **decline slightly** over time in some cities but remain high in others.")  

    st.write("### 🏙️ City & State Selection")  
    st.write("- A **dropdown filter** (bottom-right) allows selection of specific cities and states for a detailed view.")  
    st.write("- This helps in analyzing pollution data for targeted **decision-making and policy enforcement**.")  

    st.write("### 📌 Sampling Trends by State")  
    st.write("- A **state-wise sampling count** (top-right) shows the number of air quality samples collected.")  
    st.write("- **Maharashtra, Uttar Pradesh, and Kerala** have the highest sampling counts.")  

    st.write("## 🚨 Key Takeaways")  
    st.write("- **Urban cities show significantly higher pollution levels**, affecting air quality and public health.")  
    st.write("- **Industrial and densely populated cities** face the most severe air pollution challenges.")  
    st.write("- **Consistent sampling and monitoring efforts** help track pollution trends over time.")  

    st.write("🌍 This dashboard provides an **interactive city-wise breakdown** of pollution levels, enabling better environmental management strategies.")  

elif selected == "Impacts and Insights":
    st.title("Impacts and Insights")
    components.iframe("https://app.powerbi.com/view?r=eyJrIjoiODE2MDdmMGQtOWY2NS00NTc5LWE4Y2QtMWM2YTQyYWMxYzUwIiwidCI6IjFkNmVkNThjLTMyODktNGMwOS1hZmI3LWJjODlkNTE4NDg0OCJ9", height=600, width=900)
    st.write("## 📢 Impact and Insights on Pollution Levels")  

    st.write("### 📊 Yearly Pollution Trends")  
    st.write("- A **bar chart** (top-left) shows the yearly sum of **SO₂, SPM, RSPM, and NO₂** pollution levels.")  
    st.write("- Significant **increase in pollution levels after 2000**, with a sharp rise post-2010.")  

    st.write("### 📈 Pollution Composition Over Time")  
    st.write("- The **area chart** (top-center) highlights the proportion of pollutants over different years.")  
    st.write("- Sudden **dips and spikes** indicate periods of extreme pollution levels and potential interventions.")  

    st.write("### 🌍 State-Wise RSPM Distribution")  
    st.write("- A **color-coded map** (bottom-center) visually represents RSPM levels across different Indian states.")  
    st.write("- **Darker shades indicate higher RSPM concentration**, suggesting regions with more severe pollution.")  

    st.write("### 🏭 Location Monitoring Stations")  
    st.write("- A **semi-circular gauge** (bottom-left) displays the total count of monitoring stations.")  
    st.write("- Currently, **30.42K stations** are operational, providing crucial data for pollution analysis.")  

    st.write("### 📜 Historical Data Insights")  
    st.write("- A **table (top-right)** shows historical pollution data, including RSPM, SO₂, and NO₂ levels from 1987.")  
    st.write("- Pollution levels have been recorded consistently, helping in **long-term trend analysis**.")  

    st.write("### 🔍 Interactive Data Exploration")  
    st.write("- A **query box (bottom-right)** allows users to explore data by asking questions.")  
    st.write("- Predefined queries like **'maximum SO₂', 'average RSPM', and 'total RSPM over time'** help in quick analysis.")  

    st.write("## 🚀 Key Takeaways")  
    st.write("- **Pollution levels have drastically increased over the years**, requiring urgent action.")  
    st.write("- **Some regions experience consistently high pollution**, highlighting the need for localized interventions.")  
    st.write("- **More monitoring stations are needed** to improve pollution tracking and mitigation efforts.")  
    st.write("- **Interactive data exploration** empowers users to analyze pollution trends efficiently.")  

    st.write("🌱 This dashboard provides a **comprehensive view of pollution trends**, helping policymakers and researchers take data-driven actions.")  

# Separate Page for AQI Status
elif selected == "AQI Status":
    st.title("Check Air Quality Status")
    st.write("enter the aqi value and know what kind of pollution you are in!")
    
    # AQI Input
    aqi = st.number_input("Enter AQI Value:", min_value=0, max_value=500, value=0, step=5)

    # Select image based on AQI
    if aqi <= 50:
        img = Image.open("clean_air.jpg")
        status = "🟢 Good"
    elif aqi <= 100:
        img = Image.open("moderate_air.png")
        status = "🟡 Moderate"
    elif aqi <= 150:
        img = Image.open("unhealthy_air.jpg")
        status = "🟠 Unhealthy for Sensitive Groups"
    else:
        img = Image.open("polluted_air.png")
        status = "🔴 Unhealthy"

    # Display AQI status and image
    st.markdown(f"### AQI Status: {status} (AQI: {aqi})")    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{img_to_base64(img)}" 
                 style="width: 400px; height: auto; border-radius: 10px;">
        </div>
        """,
        unsafe_allow_html=True
    )
elif selected == "Feedback":
    st.title("We value your feedback! 📝")
    
    username = st.text_input("Enter your username:")
    feedback_text = st.text_area("Please share your thoughts, suggestions, or report any issues:")
    rating = st.slider("Rate your experience:", 0, 5, 0)

    if st.button("Submit Feedback"):
        if username.strip() and feedback_text.strip():
            if send_email(username, feedback_text, rating):
                st.success("✅ Thank you for your feedback! Your response has been sent.")
            else:
                st.error("❌ Failed to send feedback. Please try again.")
        else:
            st.error("⚠️ Username and feedback cannot be empty.")

elif selected == "Quiz":
    st.title("Air Quality Quiz 🧠")
    
    quiz_questions = [
        {"question": "Which pollutant is primarily responsible for smog formation?", "options": ["Ozone", "Carbon Monoxide", "Sulfur Dioxide", "Nitrogen Dioxide"], "answer": "Ozone"},
        {"question": "Which city in India has the highest air pollution levels on average?", "options": ["Delhi", "Mumbai", "Kolkata", "Bangalore"], "answer": "Delhi"},
        {"question": "What does RSPM stand for in air pollution measurement?", "options": ["Respirable Suspended Particulate Matter", "Recyclable Sulfuric Pollution Material", "Random Smoke Pollution Measure", "Radioactive Substance Particulate Monitor"], "answer": "Respirable Suspended Particulate Matter"},
        {"question": "Which gas is a major contributor to acid rain?", "options": ["Sulfur Dioxide", "Carbon Dioxide", "Nitrogen", "Oxygen"], "answer": "Sulfur Dioxide"},
        {"question": "What is the major source of NO₂ pollution?", "options": ["Vehicles", "Industrial emissions", "Power plants", "All of the above"], "answer": "All of the above"},
        {"question": "Which pollutant is a key component of vehicle emissions?", "options": ["Carbon Monoxide", "Methane", "Ozone", "Sulfur Dioxide"], "answer": "Carbon Monoxide"},
        {"question": "Which of these can help reduce air pollution?", "options": ["Planting trees", "Using public transport", "Reducing fossil fuel use", "All of the above"], "answer": "All of the above"},
        {"question": "Which pollutant is most harmful to respiratory health?", "options": ["PM2.5", "Ozone", "Sulfur Dioxide", "Nitrogen Dioxide"], "answer": "PM2.5"},
        {"question": "What is the primary reason for increasing AQI levels in urban areas?", "options": ["Industrialization", "Deforestation", "Urbanization", "All of the above"], "answer": "All of the above"},
        {"question": "Which state pollution board monitors air quality in Hyderabad?", "options": ["Andhra Pradesh SPCB", "Telangana SPCB", "Karnataka SPCB", "Maharashtra SPCB"], "answer": "Telangana SPCB"}
    ]
    
    score = 0
    for i, q in enumerate(quiz_questions):
        user_answer = st.selectbox(q["question"], q["options"], key=f"quiz_{i}")
        if user_answer == q["answer"]:
            score += 1
    
    if st.button("Submit Quiz"):
        st.success(f"You scored {score}/10! 🎉")


elif selected=="Key Takeaways":
    st.title("Conclusion:")
    st.write("### 🔍 Key Takeaways:")
    st.write("✅ **The average AQI is around 100**, indicating **moderate air quality**.")
    st.write("⚠️ **Some regions have extremely poor air quality (AQI 500, hazardous).**")
    st.write("📈 **Nearly 25% of the locations have AQI above 128, which is unhealthy for sensitive groups.**")
    st.write("📊 **Around 50% of the areas fall under moderate pollution levels.**")
    st.write("🌿 **A small number of places have very good air quality (AQI close to 0).**")

    st.write("---")  # Adds a separator line

    st.write("### 📊 AQI Analysis Summary:")
    st.write("🌎 **Mean AQI**: ~100 (**Moderate air quality**)")
    st.write("💨 **Minimum AQI**: 0 (**Excellent air quality in some areas**)")
    st.write("🔥 **Maximum AQI**: 500 (**Hazardous air quality in some areas**)")
    st.write("🟢 **25th Percentile**: 56.7 (**Good to moderate air quality**)")
    st.write("🟡 **50th Percentile (Median)**: 89 (**Moderate air quality**)")
    st.write("🟠 **75th Percentile**: 128.2 (**Unhealthy for sensitive groups**)")
# Logout
elif selected == "Logout":
    st.session_state.logged_in = False
    st.rerun()
