import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SENDER_APP_PASSWORD = os.environ.get("SENDER_APP_PASSWORD")
SENDER_EMAIL = "YOUR_EMAIL@gmail.com"     # Make sure your email is here
RECIPIENT_EMAIL = "superkunnusingh@gmail.com" # Make sure your email is here

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
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

def send_email(content: str):
    msg = MIMEText(content, "plain")
    msg["Subject"] = f"⚔️ Blox Fruits Coaching | Day Progress & Tip"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

if __name__ == "__main__":
    tip = generate_pvp_tip()
    send_email(tip)
