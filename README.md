# TechBulletinBot Deployment Guide

## Setup Instructions

1. **API Keys**:
   - Get your Bot Token from [@BotFather](https://t.me/botfather).
   - Get your News API Key from [newsapi.org](https://newsapi.org/).

2. **GitHub**:
   - Upload `bot.py`, `database.py`, `news.py`, and `requirements.txt` to a GitHub repository.

3. **Render Deployment**:
   - Log in to [Render](https://render.com).
   - Click **New +** and select **Background Worker**.
   - Connect your GitHub repository.
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

4. **Environment Variables**:
   Navigate to the **Environment** tab on Render and add:
   - `BOT_TOKEN`: Your Telegram Bot Token.
   - `NEWS_API_KEY`: Your NewsAPI.org Key.
   - `PYTHON_VERSION`: `3.12.2`

## Automation
The bot automatically broadcasts news every day at:
- **08:00 AM**
- **08:00 PM**
*Times are based on the server's system clock (usually UTC).*
