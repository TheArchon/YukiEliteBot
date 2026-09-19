# YukiEliteBot
Professional Telegram group tagging bot built with Kurigram.

## Features
- `/hitag`, `/entag`, `/gmtag`, `/gntag`, `/tagall`, `/jtag`, `/vctag`
- `/admin`, `@admin`, `/all`, `@all` with custom messages
- `/stop`, `/pause`, `/resume` with one independent task per group
- Online/recently-active members prioritized for `/vctag`
- Six mentions per message by default
- FloodWait-safe sending and configurable pacing
- Owner-only `/broadcast` and `/stats`
- SQLite persistence for discovered users, groups and tag statistics
- Central custom-emoji ID mapping
- Professional inline help navigation

## Structure
```text
YukiEliteBot/
├── app/
│   ├── handlers/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   ├── database.py
│   ├── emojis.py
│   ├── keyboards.py
│   ├── main.py
│   └── __main__.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python -m app
```

Set `BOT_TOKEN`, `API_ID`, `API_HASH`, and `OWNER_IDS`. Add the bot to the target group and promote it to administrator.

`BOT_USERNAME` should be the bot username without `@`. `SUPPORT_URL` and `UPDATES_URL` should point to the desired Telegram destinations.
