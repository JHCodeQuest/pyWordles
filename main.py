import math
import requests
import json
import os
import time
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform colors
init(autoreset=True)

# --- Configuration ---
WORDS_FILE = 'words.txt'
HISTORY_FILE = 'history.txt'
CACHE_FILE = 'cache.json'
STARTER_WORD = 'awoke'

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + """
    ╔════════════════════════════════════╗
    ║        ENTROPY WORDLE BOT          ║
    ║      The Open-Source Solver        ║
    ╚════════════════════════════════════╝
    """)

def ensure_word_in_dictionary(word, filename=WORDS_FILE):
    if not os.path.exists(filename):
        with open(filename, 'w') as f: f.write(word)
        return True
    
    with open(filename, 'r') as f:
        words = [line.strip().lower() for line in f]
    
    if word not in words:
        print(f"{Fore.MAGENTA}✨ New vocabulary detected: Adding '{word.upper()}' to brain...")
        with open(filename, 'a') as f:
            f.write(f"\n{word}")
        return True
    return False

def load_words(filename=WORDS_FILE):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f if len(line.strip()) == 5]
    except FileNotFoundError:
        return []

def get_nyt_wordle_word():
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://www.nytimes.com/svc/wordle/v2/{today}.json"
    try:
        response = requests.get(url, timeout=5)
        return response.json()['solution'].lower()
    except:
        print(f"{Fore.RED}⚠️ Could not connect to NYT API.")
        return None

def get_feedback_pattern(guess, secret):
    feedback = [0] * 5
    secret_list = list(secret)
    guess_list = list(guess)

    for i in range(5):
        if guess_list[i] == secret_list[i]:
            feedback[i] = 2
            secret_list[i] = guess_list[i] = None
    
    for i in range(5):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            feedback[i] = 1
            secret_list[secret_list.index(guess_list[i])] = None
    
    return "".join(map(str, feedback))

def print_styled_feedback(guess, pattern):
    """Prints the guess with Wordle-style background colors."""
    output = "      "
    for char, p in zip(guess.upper(), pattern):
        if p == '2':
            output += f"{Back.GREEN}{Fore.BLACK} {char} {Style.RESET_ALL} "
        elif p == '1':
            output += f"{Back.YELLOW}{Fore.BLACK} {char} {Style.RESET_ALL} "
        else:
            output += f"{Back.WHITE}{Fore.BLACK} {char} {Style.RESET_ALL} "
    print(output + "\n")

def calculate_entropy(guess, possible_words):
    buckets = {}
    for word in possible_words:
        pattern = get_feedback_pattern(guess, word)
        buckets[pattern] = buckets.get(pattern, 0) + 1
    
    entropy = 0
    total = len(possible_words)
    for count in buckets.values():
        p = count / total
        entropy += p * math.log2(1 / p)
    return entropy

def get_best_word_entropy(possible_words, allowed_guesses):
    best_word = ""
    max_entropy = -1
    # Optimization: Use current possibilities if the list is huge to save CPU
    search_list = allowed_guesses if len(possible_words) < 250 else possible_words

    for guess in search_list:
        e = calculate_entropy(guess, possible_words)
        if e > max_entropy:
            max_entropy = e
            best_word = guess
    return best_word

def log_result(word, turns):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    with open(HISTORY_FILE, 'a') as f:
        f.write(f"{timestamp} | Word: {word.upper()} | Turns: {turns}\n")

def solve_wordle_auto():
    print_header()
    actual_answer = get_nyt_wordle_word()
    if not actual_answer: return

    ensure_word_in_dictionary(actual_answer)
    all_words = load_words()
    possible_words = all_words.copy()
    
    print(f"{Fore.YELLOW}Target: NYT Wordle for {datetime.now().strftime('%B %d')}")
    print(f"{Fore.WHITE}Bot Memory: {len(all_words)} words loaded.\n")

    turn = 1
    while True:
        if turn == 1:
            guess = STARTER_WORD
        elif turn == 2:
            cache = load_cache()
            first_pattern = get_feedback_pattern(STARTER_WORD, actual_answer)
            if first_pattern in cache:
                print(f"{Fore.CYAN}🚀 Cache Hit! Using pre-calculated move...")
                guess = cache[first_pattern]
            else:
                print(f"{Fore.YELLOW}🧠 Calculating optimal Turn 2 response (Thinking...)...")
                guess = get_best_word_entropy(possible_words, all_words)
                # Save to cache
                cache[first_pattern] = guess
                with open(CACHE_FILE, 'w') as f: json.dump(cache, f)
        else:
            print(f"{Fore.YELLOW}🧠 Narrowing down {len(possible_words)} possibilities...")
            guess = get_best_word_entropy(possible_words, all_words)

        feedback = get_feedback_pattern(guess, actual_answer)
        print(f"{Fore.WHITE}TURN {turn}:")
        print_styled_feedback(guess, feedback)

        if guess == actual_answer:
            print(f"{Fore.GREEN}{Style.BRIGHT}✨ SOLVED! The answer was {guess.upper()}.")
            log_result(guess, turn)
            break
            
        possible_words = [w for w in possible_words if get_feedback_pattern(guess, w) == feedback]
        turn += 1
        time.sleep(1.5) # The "Juice" delay

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f: return json.load(f)
    return {}

def show_stats():
    try:
        with open(HISTORY_FILE, 'r') as f:
            lines = f.readlines()
        scores = [int(line.split('Turns: ')[1]) for line in lines]
        if scores:
            print(f"\n{Fore.CYAN}--- BOT CAREER STATS ---")
            print(f"Games Won: {len(scores)}")
            print(f"Average:   {sum(scores)/len(scores):.2f} turns")
            print(f"Best:      {min(scores)} turns")
    except:
        print("No history found.")

if __name__ == "__main__":
    print_header()
    choice = input(f"{Fore.WHITE}1. Start Bot Solver\n2. View Lifetime Stats\nSelection: ")
    if choice == "1":
        solve_wordle_auto()
    else:
        show_stats()