def load_words():
    with open('words.txt', 'r') as f:
        words = [line.strip().lower() for line in f if len(line.strip()) == 5]
    return words #sends list out of the function

all_words = load_words()

print(f"Loaded {len(all_words)} words!")

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

def get_best_word(words):
    pass

def solve_wordle():
    #load the dictionary
    all_words = load_words()

    while len(all_words) > 1:
        #pick a word
        guess = all_words[0]
        print(f"\nBot suggests: {guess.upper()}")

       #Get feedback from YOU
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

