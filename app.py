import streamlit as st
from streamlit_option_menu import option_menu
import json
import requests
import time
import pandas as pd
import os
from io import BytesIO
from streamlit_lottie import st_lottie
import random
import time
import datetime
import plotly.express as px
from datetime import date, timedelta
from datetime import date
from datetime import datetime
import openai
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Configure Streamlit page
st.set_page_config(page_title="Growth Mindset Tracker", layout="wide")

# Load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://assets7.lottiefiles.com/packages/lf20_tutvdkg0.json")

# Custom CSS for Animated Horizontal Navigation Bar and Enhanced UI
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');
        body, html { font-family: 'Poppins', sans-serif; }
        
        .nav-container {
            display: flex;
            justify-content: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 10px;
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
            animation: slideDown 0.8s ease-in-out;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .nav-item {
            margin: 0 15px;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: 600;
            color: #fff;
            text-decoration: none;
            transition: all 0.3s ease-in-out;
            border-radius: 10px;
        }
        
        .nav-item:hover, .nav-selected {
            background: #764ba2;
            box-shadow: 0px 5px 20px rgba(118, 75, 162, 0.6);
        }
        
        .stTitle {
            font-size: 2.5em;
            font-weight: 800;
            color: #ffffff;
            text-shadow: 2px 2px 15px rgba(255, 255, 255, 0.5);
            animation: fadeIn 1.5s ease-in-out;
            background: linear-gradient(45deg, #ff9a9e, #fad0c4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Horizontal Navigation Menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Quiz", "Daily Challenge", "Future Letter", "Streak Tracker", "Community Wall", "AI Coach", "Data Sweeper"],
    icons=["house", "question-circle", "award", "mailbox", "clock", "people", "robot", "database"],
    menu_icon="graph-up",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "background": "transparent", "class": "nav-container"},
        "icon": {"color": "#ffffff", "font-size": "20px"},
        "nav-link": {"color": "#ffffff", "padding": "10px", "border-radius": "10px", "class": "nav-item"},
        "nav-link-selected": {"background": "#764ba2", "class": "nav-selected"}
    }
)

# Home Page
if selected == "Home":
    st.title("🌱 Growth Mindset Tracker & AI Coach", anchor="stTitle")
    st.write("Welcome to your personal growth journey! Choose a feature from the navigation bar to get started.")
    if lottie_animation:
        st.lottie(lottie_animation, height=200, key="home_animation")



elif selected == "Quiz":
    st.markdown(
        """
        <style>
            .quiz-container {
                text-align: center;
                padding: 25px;
                border-radius: 15px;
                background: linear-gradient(135deg, #36D1DC, #5B86E5);
                color: white;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
                animation: fadeIn 1.2s ease-in-out;
            }

            .quiz-card {
                padding: 20px;
                border-radius: 12px;
                background: #ffffff;
                color: #333;
                font-size: 16px;
                text-align: left;
                font-weight: bold;
                box-shadow: 0px 5px 25px rgba(0, 0, 0, 0.15);
                margin-top: 20px;
                border-left: 6px solid #36D1DC;
                font-family: 'Poppins', sans-serif;
                animation: slideUp 0.8s ease-in-out;
            }

            .score-display {
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                margin-top: 15px;
                box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.15);
            }

            .success { background: #4CAF50; color: white; }
            .info { background: #FFA500; color: white; }
            .warning { background: #FF3D00; color: white; }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes slideUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='quiz-container'><h2>🧠 Growth Mindset Quiz</h2><p>Test your mindset and see where you stand!</p></div>", unsafe_allow_html=True)

    # Quiz Questions
    questions = [
        {"question": "How do you approach a difficult problem?", "options": ["Avoid it", "Try different strategies", "Wait for help", "Complain about it"], "correct": 1},
        {"question": "What is your reaction when you make a mistake?", "options": ["Learn from it", "Ignore it", "Feel ashamed", "Quit trying"], "correct": 0},
        {"question": "How do you feel about constructive criticism?", "options": ["It helps me improve", "I take it personally", "I ignore it", "I avoid feedback"], "correct": 0},
        {"question": "What do you believe about intelligence and skills?", "options": ["They can be developed", "They are fixed", "Some people are just lucky", "Only talent matters"], "correct": 0},
        {"question": "How do you handle setbacks in achieving a goal?", "options": ["Keep pushing forward", "Blame external factors", "Give up", "Complain about the difficulty"], "correct": 0}
    ]

    score = 0

    for i, q in enumerate(questions):
        st.markdown(f"<div class='quiz-card'>📌 **Q{i+1}:** {q['question']}</div>", unsafe_allow_html=True)
        choice = st.radio("", q["options"], key=f"q{i}")
        if choice == q["options"][q["correct"]]:
            score += 1

    # Submit Button
    if st.button("✅ Submit Quiz"):
        time.sleep(0.5)  # Small delay for a smooth UI effect
        st.markdown(f"<div class='score-display'>📝 Your Score: **{score}/{len(questions)}**</div>", unsafe_allow_html=True)
        
        if score == len(questions):
            st.markdown("<div class='score-display success'>🏆 Excellent! You have a strong growth mindset! 🚀</div>", unsafe_allow_html=True)
        elif score >= len(questions) // 2:
            st.markdown("<div class='score-display info'>💡 Good effort! Keep practicing a growth mindset. ✨</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='score-display warning'>🔄 You can improve! Focus on learning and growing. 📈</div>", unsafe_allow_html=True)




elif selected == "Daily Challenge":
    st.markdown(
        """
        <style>
            .challenge-container {
                text-align: center;
                padding: 30px;
                border-radius: 15px;
                background: linear-gradient(135deg, #ff9a9e, #fad0c4);
                color: white;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
                animation: fadeIn 1.2s ease-in-out;
            }
            
            .challenge-card {
                padding: 25px;
                border-radius: 15px;
                background: #ffffff;
                color: #333;
                font-size: 18px;
                text-align: center;
                font-weight: bold;
                box-shadow: 0px 5px 25px rgba(0, 0, 0, 0.15);
                margin-top: 25px;
                animation: slideUp 1s ease-in-out;
                border-left: 8px solid transparent;
                border-image: linear-gradient(180deg, #FFD700, #FF5733);
                border-image-slice: 1;
                font-family: 'Merriweather', serif;
            }

            .streak-container {
                font-size: 16px;
                font-weight: bold;
                color: #FFD700;
                margin-top: 15px;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes slideUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='challenge-container'><h2>🏆 Your Daily Growth Mindset Challenge</h2><p>Complete your challenge to strengthen your mindset every day!</p></div>", unsafe_allow_html=True)

    # List of daily challenges
    daily_challenges = [
        "🔥 Practice gratitude by writing down 3 things you're thankful for.",
        "🚀 Step out of your comfort zone and try something new today.",
        "💡 Help someone without expecting anything in return.",
        "🔄 Reframe a past failure as a learning opportunity.",
        "🧘 Spend 10 minutes practicing mindfulness or meditation.",
        "✍️ Write a short note to your future self with words of encouragement.",
        "💭 Replace a negative thought with a positive one.",
        "📖 Read about a successful person who overcame challenges.",
        "⛔ Identify one limiting belief and take action to challenge it.",
        "✨ Spend time reflecting on your personal strengths."
    ]

    # Initialize session state for challenge index & streak tracking
    if "challenge_index" not in st.session_state:
        st.session_state.challenge_index = random.randint(0, len(daily_challenges) - 1)
    
    if "streak_count" not in st.session_state:
        st.session_state.streak_count = 0

    # Display the current challenge
    current_challenge = daily_challenges[st.session_state.challenge_index]
    st.markdown(f"<div class='challenge-card'>📌 **Today's Challenge:** {current_challenge}</div>", unsafe_allow_html=True)

    # Streak Tracker Display
    st.markdown(f"<div class='streak-container'>🔥 Streak: {st.session_state.streak_count} Days</div>", unsafe_allow_html=True)

    # Buttons for user interaction
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🎯 Complete Challenge"):
            st.session_state.streak_count += 1
            st.success("✅ Well done! Your streak continues! 🚀")
    
    with col2:
        if st.button("🔄 Next Challenge"):
            st.session_state.challenge_index = random.randint(0, len(daily_challenges) - 1)
            st.rerun()




            


elif selected == "Future Letter":
    st.markdown(
        """
        <style>
            .future-container {
                text-align: center;
                padding: 30px;
                border-radius: 15px;
                background: linear-gradient(135deg, #764ba2, #667eea);
                color: white;
                box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
                animation: fadeIn 1.2s ease-in-out;
            }
            
            .future-input {
                text-align: center;
                margin-top: 20px;
                padding: 10px;
                font-size: 18px;
                border-radius: 8px;
                width: 80%;
                border: none;
                outline: none;
                background: rgba(255, 255, 255, 0.2);
                color: white;
            }
            
            .future-input::placeholder {
                color: rgba(255, 255, 255, 0.7);
            }
            
            .future-letter {
                padding: 25px;
                border-radius: 15px;
                background: #ffffff;
                color: #333;
                font-size: 17px;
                text-align: left;
                box-shadow: 0px 5px 25px rgba(0, 0, 0, 0.15);
                margin-top: 25px;
                animation: slideUp 1s ease-in-out;
                border-left: 8px solid transparent;
                border-image: linear-gradient(180deg, #FFD700, #8A2BE2);
                border-image-slice: 1;
                font-family: 'Merriweather', serif;
            }
            
            .signature {
                font-family: 'Dancing Script', cursive;
                font-size: 20px;
                font-weight: bold;
                color: #764ba2;
                text-align: right;
                margin-top: 15px;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            @keyframes slideUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='future-container'><h2>📜 A Letter from Your Future Self</h2><p>Imagine receiving a motivational letter from your future self! Fill in your details and see what the future holds.</p></div>", unsafe_allow_html=True)

    # User Input Fields
    user_name = st.text_input("Enter your Name:", placeholder="Your Name")
    future_goal = st.text_input("What do you want to become?", placeholder="Your Future Goal")

    # Generate Future Letter
    if st.button("📩 Generate Your Future Letter"):
        if user_name and future_goal:
            future_letter = f"""
            <div class='future-letter'>
                <h3>Dear {user_name},</h3>
                <p>I am writing to you from the future, where you have already achieved your dreams of becoming a <b>{future_goal}</b>.</p>
                <p>Looking back, I remember all the challenges, doubts, and obstacles you faced. But you never gave up. You embraced every difficulty, learned from every mistake, and kept moving forward with confidence.</p>
                <p>Right now, you might feel unsure or overwhelmed, but trust me—you are on the right path. Every step you take today is shaping the incredible future that awaits you.</p>
                <p>Keep learning, keep growing, and most importantly, keep believing in yourself.</p>
                <p><b>I am proud of you, and I can't wait for you to see what lies ahead!</b></p>
                <p>With love and confidence,</p>
                <p class='signature'>Future You ✍️</p>
            </div>
            """
            st.markdown(future_letter, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please enter both your name and future goal to generate the letter.")

# Streak Tracker Feature
elif selected == "Streak Tracker":
    # Ensure session state for streak tracking
    if "streak_count" not in st.session_state:
        st.session_state.streak_count = 0
    if "streak_history" not in st.session_state:
        st.session_state.streak_history = []
    if "last_activity_date" not in st.session_state:
        st.session_state.last_activity_date = None

    st.title("🔥 Streak Tracker & Progress Analytics")
    st.write("Stay consistent and track your growth mindset journey with streak analytics!")

    # Check if user has completed today's challenge
    today = date.today()
    if st.session_state.last_activity_date != today:
        if st.button("✅ Mark Today as Completed"):
            st.session_state.streak_count += 1
            st.session_state.streak_history.append({"date": today, "streak": st.session_state.streak_count})
            st.session_state.last_activity_date = today
            st.success("Great job! Your streak has been updated.")
            st.rerun()

    # Show current streak count
    st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>🔥 Current Streak: {st.session_state.streak_count} Days</h2>", unsafe_allow_html=True)

    # Convert streak history to DataFrame
    if st.session_state.streak_history:
        df = pd.DataFrame(st.session_state.streak_history)
        df["date"] = pd.to_datetime(df["date"])

        # Streak Progress Chart
        st.subheader("📊 Streak Progress Analytics")
        fig = px.line(df, x="date", y="streak", title="Streak Progress Over Time",
                      markers=True, line_shape="spline",
                      template="plotly_dark",
                      labels={"streak": "Streak Days", "date": "Date"})
        fig.update_traces(marker=dict(size=8, color='red', line=dict(width=2, color='white')))
        fig.update_layout(plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e", font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)

        # Streak Summary Stats
        col1, col2 = st.columns(2)
        with col1:
            max_streak = max(df["streak"])
            st.metric("🔥 Longest Streak", f"{max_streak} Days")
        with col2:
            avg_streak = round(df["streak"].mean(), 2)
            st.metric("📊 Average Streak", f"{avg_streak} Days")
    else:
        st.info("Start tracking your streak by marking today's challenge as completed!")



# Community Growth Wall Feature
elif selected == "Community Wall":
    st.title("🌱 Community Wall")
    st.write("Share your growth journey, achievements, and insights with the community!")

    # Ensure session state for posts
    if "community_posts" not in st.session_state:
        st.session_state.community_posts = []

    # Input for new post
    with st.form("post_form"):
        post_content = st.text_area("✍️ Share your growth journey:")
        post_author = st.text_input("👤 Your Name:")
        submit_post = st.form_submit_button("Post")

    if submit_post and post_content and post_author:
        new_post = {
            "author": post_author,
            "content": post_content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "comments": []
        }
        st.session_state.community_posts.insert(0, new_post)  # Insert at the top for latest posts first
        st.success("✅ Your growth journey has been shared with the community! 🚀")
        st.rerun()

    # Display posts
    if st.session_state.community_posts:
        for idx, post in enumerate(st.session_state.community_posts):
            with st.container():
                st.markdown(f"""
                    <div style='padding: 15px; border-radius: 10px; background-color: #ffffff; 
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.1); margin-bottom: 15px; border-left: 5px solid #4CAF50;'>
                        <h4 style='color: #2E8B57; margin-bottom: 5px;'>{post['author']}</h4>
                        <p style='font-size: 16px; color: #333; margin-bottom: 5px;'><b>🌱 Growth Journey:</b> {post['content']}</p>
                        <small style='color: grey;'>📅 {post['timestamp']}</small>
                    </div>
                """, unsafe_allow_html=True)

                # Comment section
                comment_key = f"comment_{idx}"
                comment = st.text_input("💬 Add a comment:", key=comment_key)
                if st.button("Comment", key=f"comment_btn_{idx}") and comment:
                    post["comments"].append(comment)
                    st.session_state.community_posts[idx] = post  # Update the post with the new comment
                    st.success("💬 Comment added!")
                    st.rerun()

                # Show comments
                if post["comments"]:
                    st.markdown("**📝 Comments:**")
                    for c in post["comments"]:
                        st.markdown(f"- {c}")
    else:
        st.info("✨ Be the first to share your growth journey!")


        



elif  selected == "AI Coach":
    st.title("🤖 AI Coach")
    st.write("🚀 **Welcome to AI Coach!**")
    st.write("AI Coach will guide you with personalized growth insights and daily mindset challenges.")
    
    st.subheader("🌟 Coming Soon")
    st.info("We are working hard to bring AI-powered coaching to life! Stay tuned for exciting updates.")

elif selected == "Data Sweeper":
    st.title("🧹 Advanced Data Sweeper")
    st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

    uploaded_files = st.file_uploader("📤 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[-1].lower()
            
            with st.spinner(f"Processing {file.name}..."):
                time.sleep(1)  # Simulating loading effect
                
                if file_extension == ".csv":
                    df = pd.read_csv(file)
                elif file_extension == ".xlsx":
                    df = pd.read_excel(file)
                else:
                    st.error(f"❌ Unsupported file type: {file_extension}")
                    continue
            
            st.markdown(f'<p class="success-msg">✅ {file.name} Uploaded Successfully!</p>', unsafe_allow_html=True)
            st.write(f"**📄 File Name:** `{file.name}`")
            st.write(f"**📏 File Size:** `{file.size / 1024:.2f} KB`")
            st.write("🔍 **Preview of the Uploaded File:**")
            st.dataframe(df.head(), use_container_width=True)
            
            st.subheader("🛠️ Data Cleaning Options")
            if st.checkbox(f"✨ Clean Data for `{file.name}`"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🗑️ Remove Duplicates from `{file.name}`"):
                        df.drop_duplicates(inplace=True)
                        st.success("✔️ Duplicates Removed!")
                with col2:
                    if st.button(f"🔄 Fill Missing Values for `{file.name}`"):
                        numeric_cols = df.select_dtypes(include=['number']).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✔️ Missing Values in Numeric Columns Filled with Column Means!")

            st.subheader("🎯 Select Columns to Convert")
            columns = st.multiselect(f"📌 Choose Columns for `{file.name}`", df.columns, default=df.columns)
            df = df[columns]
            
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"📈 Show Visualization for `{file.name}`"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
            
            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"🔃 Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"💾 Convert `{file.name}`"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_extension, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine='openpyxl')
                    file_name = file.name.replace(file_extension, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                
                st.download_button(
                    label=f"⬇️ Download `{file.name}` as `{conversion_type}`",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )


            
# st.success("🎉 Enhanced Animated Horizontal Navigation Bar & UI with Quiz + Daily Challenge Feature!")
