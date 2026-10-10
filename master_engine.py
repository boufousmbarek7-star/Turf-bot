name: French Trot Racing Engine

on:
  schedule:
    - cron: '0 8 * * *'  # يعمل تلقائياً كل يوم على الساعة 08:00 صباحاً
  workflow_dispatch:      # يتيح لك التشغيل اليدوي في أي وقت

jobs:
  run-engine:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4

      - name: Run Master Engine
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          python master_engine.py
