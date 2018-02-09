Skip to content
This repository
Search
Pull requests
Issues
Marketplace
Explore
 @yodahekinsew
 Sign out
 Watch 0
  Star 0  Fork 0 yodahekinsew/living-boolean
 Code  Issues 0  Pull requests 0  Projects 0  Wiki  Insights  Settings
Branch: master Find file Copy pathliving-boolean/Hangman Game
3862b7e  on Dec 19, 2017
@yodahekinsew yodahekinsew Create Hangman Game
1 contributor
RawBlameHistory     
280 lines (225 sloc)  10.4 KB
# Hangman Game

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    testlist = []
    for i in secret_word:
        if i in letters_guessed:
            testlist.append(i)
    if "".join(testlist) == secret_word:
        return True
    else:
        return False
    

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters and underscores (_) that represents
      which letters in secret_word have been guessed so far.
    '''
    correct_letters = ""
    for i in secret_word:
        if i in letters_guessed:
            correct_letters += i
        else:
            correct_letters += "_"
    return correct_letters


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which 
      letters have not yet been guessed.
    '''
    str1 = ""
    all_letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    for i in letters_guessed:
        if i in all_letters:
            all_letters.remove(i)
    for x in all_letters:
        str1 += x
    return str1
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 10 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    print("Welcome to Hangman!")
    print("I am thinking of a word that is ", len(secret_word), " letters long.")
    print('---------')
    guesses_remaining = 10
    letters_guessed = [""]
    
    while (guesses_remaining > 0):
        if guesses_remaining == 1:
            print("You have ", guesses_remaining, " guess left.")
        else:
            print("You have ", guesses_remaining, " guesses left.")
        print("Available letters: ", get_available_letters(letters_guessed))
        
        guess = input("Please guess a letter: ").lower()
        
        if not guess.isalpha() or len(guess) > 1:
           print("Oops! That is not a valid letter: ", get_guessed_word(secret_word, letters_guessed))
        else:
            if guess in letters_guessed:
                print("Oops! You've already guessed that letter: ", get_guessed_word(secret_word, letters_guessed))
            else:
                if guess in secret_word:
                    letters_guessed.append(guess)
                    print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
                else:
                    if guess in ['a','e','i','o','u']:
                        guesses_remaining = guesses_remaining - 2
                        letters_guessed.append(guess)
                        print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
                    else:
                        guesses_remaining = guesses_remaining - 1
                        letters_guessed.append(guess)
                        print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))      
        
        print('---------')
        
        unique_letters = ""
        for i in range(0,len(secret_word)):
            if secret_word[i] not in unique_letters:
                unique_letters += secret_word[i]
        
        total_score = guesses_remaining + (len(unique_letters)*len(secret_word))

        if is_word_guessed(secret_word, letters_guessed) == True:
            print("Congratulations, you won!")
            print("Your total score for this game is: ", total_score) 
            break

    if guesses_remaining == 0:
        print("Sorry, you ran out of guesses. The word was", secret_word )

# -----------------------------------

def hangman_with_help(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 10 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol #, you should reveal to the user one of the 
      letters missing from the word at the cost of 2 guesses. If the user does 
      not have 2 guesses remaining, print a warning message. Otherwise, add 
      this letter to their guessed word and continue playing normally.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to Hangman!")
    print("I am thinking of a word that is ", len(secret_word), " letters long.")
    print('---------')
    counter = 10
    letters_guessed = [""]
    available_letters = get_available_letters(letters_guessed)
    choose_from = ''
    correct_guess = False
    while (correct_guess == False and counter > 0):
        print("You have ", counter, " guesses left.")
        print("Available letters: ", get_available_letters(letters_guessed))
        
        guess = str(input("Please guess a letter: ").lower())
        if not guess.isalpha() or len(guess) > 1:
            if guess == "#":
                if counter > 2:
                    for i in range(0,len(secret_word)):
                        if secret_word[i] in available_letters and secret_word[i] not in choose_from:
                            choose_from += secret_word[i]
                    new = random.randint(0,len(choose_from)-1)
                    exposed_letter = choose_from[new]
                    letters_guessed.append(exposed_letter)
                    counter = counter - 2
                    print("Revealed letter: ", exposed_letter)
                    print(get_guessed_word(secret_word, letters_guessed))
                else:
                     print("Oops! Not enough guesses left: ", get_guessed_word(secret_word, letters_guessed))
            else:
                print("Oops! That is not a valid letter: ", get_guessed_word(secret_word, letters_guessed))
        else: 
            if guess in secret_word:
                if guess in letters_guessed:
                    print("Oops! You've already guessed that letter: ", get_guessed_word(secret_word, letters_guessed))
                else:
                    letters_guessed.append(guess)
                    print("Good guess: ", get_guessed_word(secret_word, letters_guessed))
            else:
                if guess in letters_guessed:
                    print("Oops! You've already guessed that letter: ", get_guessed_word(secret_word, letters_guessed))
                elif guess in ['a','e','i','o','u']:
                    counter = counter - 2
                    letters_guessed.append(guess)
                    print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
                else:
                    counter = counter - 1
                    letters_guessed.append(guess)
                    print("Oops! That letter is not in my word: ", get_guessed_word(secret_word, letters_guessed))
        print('---------')
        if is_word_guessed(secret_word, letters_guessed) == True:
            break
        
    unique_letters = ""
    for i in range(0,len(secret_word)):
        if secret_word[i] not in unique_letters:
            unique_letters += secret_word[i]
    total_score = counter + (len(unique_letters)*len(secret_word))
    if is_word_guessed(secret_word, letters_guessed) == True:
        print("Congratulations, you won!")
        print("Your total score for this game is: ", total_score) 
    elif counter == 0:
        print("Sorry, you ran out of guesses. The word was ", secret_word )


if __name__ == "__main__":
#    pass
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
  
#    secret_word = choose_word(wordlist)
#    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_help(secret_word)
