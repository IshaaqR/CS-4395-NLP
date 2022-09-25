import sys
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
from random import randint


# The user specifies the relative path in a sysarg
# cd "c:\Users\iront\Documents\Classes (New)\CS 4395\Portfolio\Guessing Game"
# python "Guessing Game.py" "anat19.txt"
path = sys.argv[1]

# Read in the text file as raw text
with open(path) as f:
    text = ''
    for line in f.readlines():
        text += line + ' '

# Lowercase the text
text = text.lower()

# Lexical diversity
print("\nLexical diversity: %.2f" % (len(set(word_tokenize(text))) / len(word_tokenize(text))))

# Write a function to preprocess the raw text
def preprocess(text):
    # Tokenize the lower-case raw text, reduce the tokens to only those that are alpha, not in the NLTK stopword list, and have length > 5
    tokens = [t for t in word_tokenize(text) if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]

    # Lemmatize the tokens and use set() to make a list of unique lemmas
    lemmas = set([wnl.lemmatize(t) for t in tokens])

    # Do pos tagging on the unique lemmas and print the first 20 tagged items
    print('\nPOS for the first 20 words:', nltk.pos_tag(tokens)[:20])

    # Create a list of only those lemmas that are nouns
    nouns = [lemma for lemma, pos in nltk.pos_tag(lemmas) if 'NN' in pos]

    # Print the number of tokens (from step a) and the number of nouns (step d)
    print('\nNumber of tokens:', len(tokens))
    print('\nNumber of nouns:', len(nouns))

    # Return tokens(not unique tokens) from step a, and nouns from the function
    return tokens, nouns

# Make a dictionary of {noun:count of noun in tokens} items from the nouns and tokens lists
tokens, nouns = preprocess(text)
noun_counts = dict.fromkeys(nouns)
for noun in nouns:
    noun_counts[noun] = tokens.count(noun)

# Sort the dict by count and print the 50 most common words and their counts
common_nouns_counts = sorted(noun_counts.items(), key=lambda item: item[1], reverse=True)[:50]
print('\nThe 50 most common words are:', common_nouns_counts)
common_nouns = [x[0] for x in common_nouns_counts]

# Make a guessing game function:
print('\nLet\'s play a word guessing game!')
def guessing_game(points):
    # Randomly choose one of the 50 words in the top 50 list
    word = common_nouns[randint(0, 49)]
    letters = list(word)
    guessed = []
    letter = None

    # Guessing for a word ends if the user guesses the word or has a negative score
    while len(set(letters)) != len(guessed) and points >= 0 and letter != '!':
        # Output to console an “underscore space” for each letter in the word 
        print_word(letters, guessed)

        # Ask the user for a letter
        letter = input('Guess a letter: ')

        # If the letter is in the word, print ‘Right!’, fill in all matching letter _ with the letter and add 1 point to their score
        if letter in letters and letter not in guessed:
            points += 1
            print('Right!',end='')
            guessed.append(letter)
        # If the letter is not in the word, subtract 1 from their score, print ‘Sorry, guess again’ 
        elif letter != '!':
            points -= 1
            if points >= 0:
                print('Sorry, guess again.', end='')

        if points >= 0 and letter != '!':
            print(' Score is', points)

    if len(set(letters)) == len(guessed):
        print_word(letters, guessed)
        print('You solved it!')
    elif letter != '!':
        print('\nThe correct word was', word)

    return points, letter

def print_word(letters, guessed):
    for i in letters:
        if i in guessed:
            print(i, end='')
        else:
            print('_ ', end='')
    print()

# Give the user 5 points to start with; the game ends when their total score is negative, or they guess ‘!’ as a letter 
points = 5
letter = None
while points >= 0 and letter != '!':
    # Right or wrong, give user feedback on their score for this word after each guess
    points, letter = guessing_game(points)

    if letter != '!':
        if points >= 0:
            print('\nCurrent score is:', points)
            print('Guess another word')
        else:
            print('\nYou have lost. Play again another time!')
    else:
        print('\nYou have quit the game')
