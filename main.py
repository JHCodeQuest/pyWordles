import math

def load_words():
    with open('words.txt', 'r') as f:
        words = [line.strip().lower() for line in f if len(line.strip()) == 5]
    return words #sends list out of the function

all_words = load_words()

print(f"Loaded {len(all_words)} words!")

def load_all_guessable_words():
    pass

def is_possible(word, guess, feedback):
    for i in range(5):
        if feedback[i] == "2": #green
            if word[i] != guess[i]:
                return False
        elif feedback[i] == "1": #yelow
            #must contain the letter, but not in this spot
            if guess[i] not in word or word[i] == guess[i]:
                return False
        elif feedback[i] == '0': #gray
            #Letter is not in the word
            if guess[i] in word:
                return False
    return True


def get_frequencies(words):
    frequencies = {}
    for word in words:
        for letter in word:
            #If letter is already in dictionary, add 1
            #If not, start at 0 and add 1
            frequencies[letter] = frequencies.get(letter, 0) + 1
    return frequencies

def get_best_word_entropy(possible_words, allowed_guesses):
    best_word = ""
    max_entropy = -1

    for guess in allowed_guesses:
        e = calculate_entropy(guess, possible_words)
        if e > max_entropy:
            max_entropy = e
            best_word = guess
    
    return best_word

    
    #load the dictionary
    all_words = load_words()

    while len(all_words) > 1:
        #pick a word
        guess = get_best_word_entropy(all_words)
        print(f"\nBot suggests: {guess.upper()}")

       #Get feedback
        feedback = input("Enter feedback (0=Gray, 1=Yellow, 2=Green): ")
        
        if feedback == "22222":
            print("🎉 We got it!")
            return
        
        #filter the list
        all_words = [word for word in all_words if is_possible(word, guess, feedback)]

        print(f"Words remaining: {len(all_words)}")
        if len(all_words) < 10:
            print(f"Possible matches: {all_words}")
        
    if len(all_words) == 1:
        print(f"The answer must be: {all_words[0].upper()}")

def get_feedback_pattern(guess, secret):
    """returns a string of 0s, 1s, and 2s, representing the Wordle feedback"""
    feedback = [0] * 5
    secret_list = list(secret)
    guess_list = list(guess)

    #Find greens
    for i in range(5):
        if guess_list[i] == secret_list[i]:
            feedback[i] = 2
            secret_list[i] = None #Mark used so does not show as yellow
            guess_list[i] = None
    
    #find yellows
    for i in range(5):
        if guess_list[i] is not None and guess_list[i] in secret_list:
            feedback[i] = 1
            #remove first instance of the letter from secret_list
            secret_list[secret_list.index(guess_list[i])] = None
    
    return "".join(map(str, feedback))

def calculate_entropy(guess, possible_words):
    #dictonary to count how many words fall into each feedback bucket
    buckets = {}

    for word in possible_words:
        #resue a simplified version of thw feedback logic
        pattern = get_feedback_pattern(guess, word)
        buckets[pattern] = buckets.get(pattern, 0) + 1
    
    entropy = 0
    total_words = len(possible_words)

    for count in buckets.values():
        probability = count / total_words
        # Shannon Entropy formula: p * log2(1/p)
        entropy += probability * math.log2(1 / probability)

    
def solve_wordle():
    all_words = load_words() #list of words
    allowed_guesses = load_all_guessable_words()

    turn = 1
    while True:
        #pick the guess
        if turn == 1:
            guess = "awoke" #JHCodeQuest's starter word
        elif len(all_words) == 1:
            guess = all_words[0]
        else:
            print(f"Best guess from {len(all_words)} is...")
            guess = get_best_word_entropy(all_words, allowed_guesses)
        
        print(f"\Turn {turn} | bot suggests: {guess.upper()}")

        #Get feedback
        feedback = input("Enter feedback (e.g., 02101): ")
        if feedback == "22222":
            print(f"We did it! In {turn} guesses!")
            break

        #filter the list
        all_words = [w for w in all_words if get_feedback_pattern(guess, w) == feedback]

        turn += 1
        if not all_words:
            print("No words match that feedback. Try again!")
            break



