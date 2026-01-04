import math

def load_words(filename='words.txt'):
    """Loads 5-letter words from a file."""
    try:
        with open(filename, 'r') as f:
            return [line.strip().lower() for line in f if len(line.strip()) == 5]
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []

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

def solve_wordle():
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
    solve_wordle()