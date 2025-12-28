def load_words(filename):
    with open(filename, 'r') as f:
        return [line.strip().lower() for line in f.readlines()]