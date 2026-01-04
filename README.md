🧠 Entropy Wordle Bot A high-performance, information-theory-based Wordle solver that "learns" as it plays. This bot uses Shannon Entropy to identify the mathematically optimal guess at any given turn. It automatically fetches the official New York Times Wordle of the Day, simulates a "blind" solve, and logs its performance over time.
✨ Key Features:
- Optimal Strategy: Uses Entropy (Information Theory) to maximize information gain per guess.- Automatic Fetching: Plugs into the NYT Wordle API to solve the daily puzzle.
- Self-Healing Memory: Automatically updates its local dictionary if a new word is detected in the wild.
- Persistent Caching: Remembers complex Turn 2 calculations to ensure instant performance.
- User Friendly: Features a "juiced-up" terminal interface with color-coded feedback and ASCII art.
The "Blind" Solve: The bot is a true referee. It fetches the NYT word but keeps it a secret, solving the puzzle legally without "cheating" or looking at the answer.

Dynamic Strategy Engine: Most bots just do math. This one has a brain. It switches from Shannon Entropy (Information Gathering) to Win-Probability Targeting in the endgame to close the loop and secure the win.

Self-Learning Dictionary: If the NYT throws a curveball word that isn't in the bot's memory, it automatically detects it and adds it to words.txt. The bot gets smarter every day.

Infinite Loop Protection: Features a "No-Fail" loop fix with used-guess tracking, ensuring the bot never gets stuck repeating the same incorrect word.

Smart Cache: Remembers heavy Turn 2 calculations. If the bot sees a pattern it has solved before, it hits the cache for an instant response.

The "Juice": Fully color-coded terminal output, strategy readouts, and ASCII headers to make the open-source experience look and feel professional.

🛠️ How it Works: The Entropy MathThe bot calculates the expected value of information for every possible word in its dictionary. It uses the Shannon Entropy formula:$$E[G] = \sum_{i=1}^{n} P(x_i) \log_2 \left( \frac{1}{P(x_i)} \right)$$Where:$P(x_i)$ is the probability of a specific green/yellow/gray feedback pattern.The bot chooses the word that results in the most even distribution across "buckets," narrowing down the remaining possibilities as fast as possible.
🚀 Getting Started
Prerequisites
- Create the environment: python -m venv venv
Activate it:
- Windows: venv\Scripts\activate
- Mac/Linux: source venv/bin/activate
- Install exactly what's needed: pip install -r requirements.txt
- Make sure you have Python 3.8+ installed. You will need two external libraries:Bashpip install requests colorama
- Installation Clone this repository. Ensure you have a words.txt file in the root directory (one 5-letter word per line). Run the bot:Bashpython main.py
📊 Statistics & Logging
- The bot tracks its own history in history.txt. You can view its average score and win rate by selecting the "View Stats" option in the main menu.
🤝 Contributing
- This is an open-source project! We are looking for:
- Performance: Can we make the Entropy loop even faster?
- Strategy: Implement "Deep Lookahead" (calculating Turn 3 entropy during Turn 2).
- UI: Add a progress bar for long calculations.

