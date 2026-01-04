import math
import requests
from datetime import datetime

def ensure_word_in_dictionary(word, filename='words.txt'):
    """Checks if the NYT word is in your list; if not, adds it to the file."""
    with open(filename, 'r') as f:
        words = [line.strip().lower() for line in f]
    
    if word not in words:
        print(f"✨ New word detected! Adding '{word}' to {filename}...")
        with open(filename, 'a') as f:
            f.write(f"\n{word}")
        return True # We added a word
    return False # Word was already there

def load_words(filename='words.txt'):
    """Loads 5-letter words from a file."""
    try:
        with open(filename, 'r') as f:
            return [line.strip().lower() for line in f if len(line.strip()) == 5]
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []

def get_nyt_wordle_word():
    """Fetches today's offical NYT Wordle word."""
    today = datetime.now().strftime("%d-%m-%Y")
    url = f"https://www.nytimes.com/svc/wordle/v2/{today}.json"

    try:
        response = requests.get(url)
        data = response.json()
        return data['solution'].lower()
    except Exception as e:
        print(f"Could not fetch NYT word: {e}")
        return None


def get_feedback_pattern(guess, secret):
    """Generates the 0, 1, 2 pattern for a guess against a secret word."""
    feedback = [0] * 5
    secret_list = list(secret)
    guess_list = list(guess)

    # First pass: Find Greens
    for i in range(5):
        if guess_list[i] == secret_list[i]:
            feedback[i] = 2
            secret_list[i] = None
            guess_list[i] = None
    
    # Second pass: Find Yellows
    for i in range(5):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            feedback[i] = 1
            secret_list[secret_list.index(guess_list[i])] = None
    
    return "".join(map(str, feedback))

def calculate_entropy(guess, possible_words):
    """Calculates the expected information gain (bits) for a guess."""
    buckets = {}
    for word in possible_words:
        pattern = get_feedback_pattern(guess, word)
        buckets[pattern] = buckets.get(pattern, 0) + 1
    
    entropy = 0
    total_words = len(possible_words)
    for count in buckets.values():
        probability = count / total_words
        entropy += probability * math.log2(1 / probability)
    return entropy

def get_best_word_entropy(possible_words, allowed_guesses):
    """Finds the word that provides the highest entropy."""
    best_word = ""
    max_entropy = -1

    # Optimization: If the list is huge, only check words within the possible list
    # to save time. Otherwise, check the full dictionary for maximum strategy.
    search_list = allowed_guesses if len(possible_words) < 200 else possible_words

    for guess in search_list:
        e = calculate_entropy(guess, possible_words)
        if e > max_entropy:
            max_entropy = e
            best_word = guess
    
    return best_word

def log_result(word, turns):
    """Appends the game result to history.txt with a timestamp."""
    timestamp  = datetime.now().strftime("%d-%m-%Y %H:%M")
    with open('history.txt', 'a') as f:
        f.write(f"{timestamp} | Word: {word.upper()} | Turns: {turns}\n")
    print(f"Result saved to history.txt")

def show_stats():
    """Reads history.txt and calculates the bot's average performance."""
    try:
        with open('history.txt', 'r') as f:
            lines = f.readlines()
            
        # Extract the number after 'TURNS: ' in each line
        scores = [int(line.split('TURNS: ')[1]) for line in lines]
        
        if scores:
            avg = sum(scores) / len(scores)
            print(f"\n--- BOT STATISTICS ---")
            print(f"Games Played: {len(scores)}")
            print(f"Average Score: {avg:.2f} turns")
            print(f"Best Game: {min(scores)}")
    except (FileNotFoundError, IndexError):
        print("No stats available yet. Win some games first!")

def solve_wordle_blind():
    # Load the official NYT word (stored but not shown to the bot logic)
    actual_answer = get_nyt_wordle_word()
    
    if not actual_answer:
        print("Error fetching NYT word.")
        return

    #Safety check: make sure its in our dictionary
    did_add = ensure_word_in_dictionary(actual_answer, 'words.txt')

    # Load your local words list for the bot's 'memory'
    all_words = load_words('words.txt')
    allowed_guesses = all_words.copy()

    print(f"--- Bot is solving the NYT Wordle (Answer Hidden) ---")
    
    turn = 1
    while True:
        # 1. Bot makes a guess based on the words it THINKs are possible
        if turn == 1:
            guess = "awoke"
        elif len(all_words) == 1:
            guess = all_words[0]
        else:
            print(f"Analyzing {len(all_words)} possibilities...")
            guess = get_best_word_entropy(all_words, allowed_guesses)

        # 2. Generate feedback automatically (This is the 'Referee' step)
        feedback = get_feedback_pattern(guess, actual_answer)
        
        print(f"TURN {turn}: Bot guessed {guess.upper()} | Result: {feedback}")

        # 3. Check for Win
        if guess == actual_answer:
            print(f"\n🎯 The Bot solved it! The secret word was: {guess.upper()}")
            print(f"Score: {turn}/6")
            log_result(guess, turn)
            break
            
        # 4. Bot updates its brain based on the feedback it just received
        all_words = [w for w in all_words if get_feedback_pattern(guess, w) == feedback]
        
        if not all_words:
            print("❌ Error: The bot ran out of possibilities. Is the NYT word in your words.txt?")
            break
            
        turn += 1
    # Load your word lists
    all_words = load_words('words.txt')
    if not all_words: return

    # In a pro bot, allowed_guesses would be a larger dictionary, 
    # but using your words.txt for both works perfectly too.
    allowed_guesses = all_words.copy()

    turn = 1
    while True:
        # STEP 1: Pick the guess
        if turn == 1:
            guess = "awoke" # Your specific hardcoded starter
        elif len(all_words) == 1:
            guess = all_words[0]
        else:
            print(f"Analyzing {len(all_words)} possibilities...")
            guess = get_best_word_entropy(all_words, allowed_guesses)
        
        print(f"\n--- TURN {turn} ---")
        print(f"BOT SUGGESTS: {guess.upper()}")

        # STEP 2: Get feedback
        feedback = input("Enter feedback (e.g., 02100): ").strip()
        
        if feedback == "22222":
            print(f"🎉 Success! The word was {guess.upper()} in {turn} guesses.")
            #log the guess
            log_result(guess, turn)
            break

        # STEP 3: Filter the list
        # We keep words that would produce the EXACT same feedback pattern
        all_words = [w for w in all_words if get_feedback_pattern(guess, w) == feedback]

        if not all_words:
            print("❌ No words match that feedback. Please check your colors!")
            break
        
        turn += 1
        print(f"Remaining possibilities: {len(all_words)}")
        if len(all_words) <= 5:
            print(f"Potential answers: {all_words}")



# Start the bot
if __name__ == "__main__":
    choice = input("1. Play Wordle\n2. View Stats\nChoice: ")
    if choice == "1":
        solve_wordle_blind()
    else:
        show_stats()