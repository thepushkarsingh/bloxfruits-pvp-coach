# ⚔️ Blox Fruits Daily PvP Coach

An automated, daily PvP coaching email system powered by Google's Gemini 3.6 Flash model and GitHub Actions.

## 📌 Overview

This project automatically generates personalized Blox Fruits PvP training tips, combos, tactical mechanics, and daily drills based on a progression timeline. The lessons are emailed directly to your inbox every day at **8:00 AM UTC**.

## 🛠️ Features

- **Gemini AI Content Generation**: Generates non-repetitive coaching content tailored to specific fruits, swords, and skill levels.
- **Automated Scheduling**: Powered by GitHub Actions (`cron`) so it runs completely free without external servers.
- **Custom Progression Tiers**:
  - **Days 1–7**: Beginner (5M–7M Bounty) — Basic 3-move true combos & Ken escapes.
  - **Days 8–20**: Intermediate (7M–15M Bounty) — Advanced Kentrick baiting & fast weapon swapping.
  - **Days 21+**: Master (15M–30M Bounty) — Zero-delay high-APM combos & meta counters.

## 🚀 Setup & Installation

### 1. Repository Secrets
Under **Settings** > **Secrets and variables** > **Actions**, configure the following repository secrets:

| Secret Name | Description |
| :--- | :--- |
| `GEMINI_API_KEY` | Google AI Studio API key |
| `SENDER_APP_PASSWORD` | 16-character Google App Password for the sending account |

### 2. File Structure

- `.github/workflows/daily.yml`: GitHub Actions workflow for daily automated execution.
- `coach.py`: Main Python script responsible for fetching AI coaching content and dispatching emails via Gmail SMTP.

## 🧪 Testing

To manually trigger a test email:
1. Navigate to the **Actions** tab in your GitHub repository.
2. Select **Daily Blox Fruits Tip** under Workflows.
3. Click **Run workflow** $\rightarrow$ **Run workflow**.
