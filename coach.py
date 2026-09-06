import os
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google import genai

# Read environment variables set in daily.yml
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SENDER_APP_PASSWORD = os.environ.get("SENDER_APP_PASSWORD")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "thepushkarsingh@gmail.com")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "superkunnusingh@gmail.com")

# Start date to track day progression
START_DATE = datetime(2026, 1, 1)

def get_current_day_and_tier():
    today = datetime.now()
    day_count = (today - START_DATE).days + 1
    
    if day_count <= 7:
        tier = "Beginner (5M-7M Bounty Level)"
        difficulty = "Focus on basic 3-move true combos, simple Ken Trick escapes, and landing stun moves."
    elif day_count <= 20:
        tier = "Intermediate (7M-15M Bounty Level)"
        difficulty = "Focus on advanced Kentrick baiting, air mobility/flash-step positioning, and fast weapon swapping."
    else:
        tier = "Master (15M-30M Bounty Level)"
        difficulty = "Focus on zero-delay high-APM combos, predicting enemy dodges, frame-perfect counters, and defeating toxic meta runners."
        
    return day_count, tier, difficulty

def generate_pvp_tip() -> str:
    day_count, tier, difficulty = get_current_day_and_tier()
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    You are a 30M Bounty Blox Fruits PvP Coach. 
    Write a daily PvP coaching email for a player on DAY {day_count} of their training program.

    Progression Tier: {tier}
    Current Difficulty Focus: {difficulty}

    Constraints & Rules:
    - Player Fruits/Builds: Focus ONLY on builds using Dragon, Pain, Ice, Dark, or Light (paired with obtainable swords like CDK, Gravity Cane, or Dragon Trident).
    - Never repeat previous standard advice. Provide a unique focus for Day {day_count}.
    - Email Structure:
      1. Today's Lesson Topic (Day {day_count} Challenge)
      2. 1 Progression Combo (Exact keybinds & timing)
      3. 1 Tactical Mechanic (e.g., flash step angles, baiting instinct, or air stalling)
      4. Today's Homework Drill (A specific target to practice in public servers today)
    - Keep total email length under 200 words using bullet points.
    """
    
    # Retry up to 3 times if Gemini encounters high traffic
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            if attempt == 2:
                raise e
            time.sleep(5)

def send_email(content: str):
    if not SENDER_EMAIL or not SENDER_APP_PASSWORD:
        raise ValueError("Missing SENDER_EMAIL or SENDER_APP_PASSWORD environment variables.")

    day_count, _, _ = get_current_day_and_tier()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"⚔️ Blox Fruits PvP Coaching | Day {day_count} Lesson"
    msg["From"] = f"Blox Fruits Coach <{SENDER_EMAIL}>"
    msg["To"] = RECIPIENT_EMAIL
    
    # Priority headers to assist deliverability
    msg["X-Priority"] = "1"
    msg["X-MSMail-Priority"] = "High"

    msg.attach(MIMEText(content, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

if __name__ == "__main__":
    tip = generate_pvp_tip()
    send_email(tip)
