# Entropy Wordle Bot 
A high-performance, information-theory-based Wordle solver that "learns" as it plays. This bot uses Shannon Entropy to identify the mathematically optimal guess at any given turn. 
It automatically fetches the official New York Times Wordle of the Day, simulates a "blind" solve, and logs its performance over time.

---
# Key Features:
#   * The "Blind" Solve: 
*  The bot acts as a true referee. It fetches the NYT word but keeps it a secret, solving the puzzle legally without "cheating" or looking at the answer.
#  *  Dynamic Strategy Engine: 
*  Most bots just do math; this one has a brain. It switches from Shannon Entropy (Information Gathering) to Win-Probability Targeting in the endgame to close the loop and secure the win.
#  *  Self-Learning Dictionary: 
*  If the NYT throws a curveball word not in the bot's memory, it automatically detects it and adds it to words.txt. The bot gets smarter every day.
#  *  Infinite Loop Protection:
*   Features a "No-Fail" loop fix with used-guess tracking, ensuring the bot never gets stuck repeating the same incorrect word.
*   Smart Cache: Remembers heavy Turn 2 calculations. If the bot sees a pattern it has solved before, it hits the cache for an instant response.
#  *  The "Juice": 
*  Fully color-coded terminal output, strategy readouts, and ASCII headers for a professional open-source look and feel.
---
#  How it Works: 
- The Entropy MathThe bot calculates the expected value of information for every possible word in its dictionary using the Shannon Entropy formula:
  <img width="278" height="89" alt="image" src="https://github.com/user-attachments/assets/61b8e20d-cb5c-4fc8-a03c-722151fd8148" /> 
- Where:
  - *(x_i)$* is the probability of a specific green/yellow/gray feedback pattern.
- The bot chooses the word that results in the most even distribution across "buckets," narrowing down the remaining possibilities as fast as possible.
---
#  Getting Started:
1. Prerequisites
  - Python 3.8+ installed. A words.txt file in the root directory (one 5-letter word per line).
2. Installation & Setup
  - Clone the repository:
    - `git clone https://github.com/your-username/entropy-wordle-bot.git`
  - `cd entropy-wordle-bot`
3. Create and Activate a Virtual Environment:
  - Windows:
    - ` python -m venv venv`
    - `venv\Scripts\activate`
  - Mac/Linux:
    - ` python3 -m venv venv`
    - `source venv/bin/activate`
4. Install Dependencies:
  - `pip install -r requirements.txt`
5. Run the Bot:
  - `python main.py`
---
#  Statistics & Logging
- The bot tracks its own history in history.txt. You can view your lifetime average score, win rate, and best games by selecting the "View Stats" option in the main menu.
---
# Contributing 
#  This is an open-source project! We are looking for help with:
  - Performance: Making the Entropy calculation loop even faster.
  - Advanced Strategy: Implementing "Deep Lookahead" Advanced.
  - UI/UX: Adding a progress bar for heavy calculations.
