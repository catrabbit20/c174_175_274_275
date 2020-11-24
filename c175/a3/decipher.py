from collections import defaultdict
import sys
import re
import operator

def main():
    #command line arguments
    dataFile = sys.argv[1]
    if len(sys.argv) < 3:
        n = 3
    else:
        n = int(sys.argv[2])        
    #creates n non-overlapping pairs list for cipher, overlapping for plaintext
    cipher_text_pairs = make_text(dataFile, n, 2)   
    plain_text_pairs = make_text("wells.txt", n, 1)        
    #to make loop exit on empty line, end program
    encoded_message = "not empty"
    while encoded_message != "":
        encoded_message = input("Input: ")
        if encoded_message != "":
            message_pair_list = []
            matched_pair_string = ""
            #makes message lowercase
            encoded_message = encoded_message.lower()
            #note: assumes always even number of letters in encoded message
            for i in range(0, len(encoded_message), 2):
                message_pair_list.append(encoded_message[i] + encoded_message[i+1])
            for i in range(len(message_pair_list)):
                if message_pair_list[i] in cipher_text_pairs:
                    matched_pair_string += (plain_text_pairs[cipher_text_pairs.index(message_pair_list[i])])
                else:
                    matched_pair_string += ("..")
            search(matched_pair_string)
        else:
            print("Blank line entered - End of program")

#finds n most common pairs in current file, returns as list. Iterate_by is used
#to determine if overlapping pairs for plaintext (1), or non-overlapping for 
#cipher text (2)
def make_text(filename, n, iterate_by):
    letter_dict = defaultdict(int)
    lines = []
    lettertext = []
    lettertextpairs = []
    ordered_list = []    
    #terminates program if error opening either file
    endofprogram = False
    try:
        current_file = open(filename, "r")               
    except IOError:
        print("Error opening file - End of program")
        endofprogram = True    
    if (endofprogram != True):
        #removes spaces and '/n' characters
        for line in current_file:
            line = line.strip()
            lines.append(line)
        #closes file
        current_file.close()        
        #makes letters lowercase, removes non-letter chars
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                if lines[i][j].isalpha():
                    lettertext.append(lines[i][j].lower())
        #the below for loop creates pairs (if iterate_by is 1, then "helloo"
        #becomes "he", "el", "ll","lo", "oo", if iterate_by is 2 then it becomes
        #"he","ll", "oo". The for used for wells.txt, the later for playfair.txt
        #there is an assumption that when iterate_by is 2, there is an even
        #number of letters due to how playfair cypher works
        for i in range(0,len(lettertext)-(2-iterate_by),iterate_by):
            lettertextpairs.append(lettertext[i] + lettertext[i+1])            
        #creates defaultdictionary with pairs as keys and frequencies as values    
        for i in range(len(lettertextpairs)):
            letter_dict[lettertextpairs[i]] += 1
        #creates two seperate lists for keys and values. Takes n elements based
        #on index of max of values list
        key_list = list(letter_dict.keys())
        value_list = list(letter_dict.values())
        #appends to new list
        for i in range(n):        
            ordered_list.append(key_list.pop(value_list.index(max(value_list))))
            value_list.pop(value_list.index(max(value_list)))    
        #returns the resulting list
        return(ordered_list)

#performs regular expressions to find all possible words. Calls order to sort
#these words in order of likelihood (or if same likelihood, by alphabet)
def search(wordstring):
    words = []
    matchingwordlist = []
    #terminates program if wordlist.txt cannot be opened
    endofprogram = False
    try:
        wordlist = open("wordlist.txt", "r")               
    except IOError:
        print("Error opening wordlist.txt - End of program")
        endofprogram = True    
    if (endofprogram != True):
        for word in wordlist:
            word = word.strip()
            words.append(word)
    #closes wordlist.txt file
    wordlist.close()
    #performs regular expression
    for i in range(len(words)):
        if re.search("^" + wordstring + "$", words[i]):
            matchingwordlist.append(words[i])
        #if last bigram unknown, check against words that are one letter shorter
        if re.search("^" + wordstring[:-1] + "$", words[i]) and wordstring[-1] == ".":
            matchingwordlist.append(words[i])
    
    order(matchingwordlist)

#places list in proper order (by freq. in wells.txt or alphabet if same freq.)
#prints output as string to match output in sample program runs
def order(unsortedwordlist):
    return_list = []
    freq_list = []
    word_dict = defaultdict(int)
    #we already checked if we could open wells.txt, don't need to do so again
    plaintextfile = open("wells.txt", "r")
    lines = []
    lettertext = []
    #places line in a list
    for line in plaintextfile:
        line = line.strip()
        line = line.split()
        lines.append(line)
    #closes wells.txt
    plaintextfile.close()
    #places each word in a list, makes lowercase
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            lettertext.append(lines[i][j].lower())
    #creates defaultdict with words as keys and frequencies as values
    for i in range(len(lettertext)):
        word_dict[lettertext[i]] += 1
    #creates list of touples, with first element being each possible word and
    #second being the frequency with which it appears in wells.txt
    for i in range(len(unsortedwordlist)):
        freq_list.append((unsortedwordlist[i], word_dict[unsortedwordlist[i]]))
        
    #part of the below line of code was taken from stackoverflow, url below:
    #http://stackoverflow.com/questions/8459231/sort-tuples-based-on-second-parameter
    #sorts based on second element, largest to smallest
    freq_list.sort(key=operator.itemgetter(1), reverse = True)
    #appends to new list
    for i in range(len(freq_list)):
        return_list.append(freq_list[i][0])
    #prints new list as a single string with spaces between elements
    print("output:", " ".join(return_list))

main()