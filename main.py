def load_words(all_words):
    with open('words.txt', 'r') as f:
        all_words = [line.strip().lower() for line in file if len(line.strip()) == 5]

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