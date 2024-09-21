alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
import random
random.seed()
import math
#############################################################
# The following code doesn't need to be edited. It allows   #
# you to read a text file and store it in a single string,  #
# and also to write a single string to a text file. This is #
# not an ideal way to work with files, but it will suffice  #
# for this assignment.                                      #
#############################################################

def file_to_string(filename):
    with open(filename, "r") as f:
        x = f.read()
    return x

def string_to_file(filename, s):
    with open(filename, "w") as f:
        f.write(s)



#############################################################
# A working Caesar cipher                                   #
#############################################################

def simplify_string(s):
    "your code here"
    word_return = ''
    for char in s:
        if char.upper() in alpha:
            word_return += char.upper()
    return word_return


def num_to_let(x):
    "your code here"
    return alpha[x%26]

    
def let_to_num(a):
    "your code here"
    ctr = 0
    for char in alpha:
        if char == a:
            return ctr
        ctr += 1
        


def shift_char(char, shift):
    "your code here"
    return num_to_let((let_to_num(shift) + let_to_num(char)) % 26)



def caesar_enc(plain, key):
    "your code here"
    caesar_return = ''
    for letter in plain:
        caesar_return += shift_char(letter, key)
    return caesar_return



def caesar_dec(cipher, key):
    "your code here"
    caesar_dec_add = ''
    for letter in cipher:
        caesar_dec_add += shift_char(letter, num_to_let(26 - let_to_num(key)))
    return caesar_dec_add



#############################################################
# Breaking the Caesar cipher                                #
#############################################################

def letter_counts(s):
    "your code here"
    dict_of_letters = {}
    ctr = 0
    for letter1 in alpha:
        dict_of_letters[letter1] = ctr
        for letter2 in s:
            if letter1 == letter2:
                ctr += 1
                dict_of_letters[letter1] = ctr
        ctr = 0
    return dict_of_letters


    
def normalize(counts):
    "your code here"
    ctr = 0
    for value1 in counts.values():
        ctr += value1
    for key, value2 in counts.items():
        if ctr == 0:
            ctr = 1
        counts[key] = value2 / ctr  
    return counts



# Uncomment the code below once the functions above are complete
english_freqs = letter_counts(simplify_string(file_to_string("twocities_full.txt")))
normalize(english_freqs)

def distance(observed, expected):
    "your code here"
    count = 0
    for key1, value1 in observed.items():
        for key2, value2 in expected.items():
            if key1 == key2:
                count += (((value1 - value2)**2)/value2)
    return count


    
def break_caesar(cipher, frequencies):
    "your code here"
    answer_key = ''
    answer_text = ''
    start_result = math.inf
    for key in alpha:
        decryption = caesar_dec(cipher, key)
        freq = normalize(letter_counts(decryption))
        results = distance(freq, frequencies)
        if results < start_result:
            start_result = results
            answer_key = key
            answer_text = decryption
    return [answer_key, answer_text]



#############################################################
# A working Vigenere cipher                                 #
#############################################################

def vigenere_enc(plain, key):
    "your code here"
    v_enc = ''
    index = 0
    for char1 in plain:
        new_index = index % len(key)
        v_enc += shift_char(char1, key[new_index])
        index += 1
    return v_enc


        

def vigenere_dec(cipher, key):
    "your code here"
    v_dec = ''
    index = 0 
    for char1 in cipher:
        new_index = index % len(key)
        v_dec += shift_char(char1, num_to_let(26 - let_to_num(key[new_index])))
        index += 1
    return v_dec



#############################################################
# Breaking the Vigenere cipher                              #
#############################################################

def split_string(s, parts):
    "your code here"
    list_of_parts = []
    for num in range(parts):
        list_of_parts.append(s[num::parts])
    return list_of_parts



def vigenere_break_for_length(cipher, klen, frequencies):
    "your code here"
    common1 = ''
    common2 = []
    for char1 in split_string(cipher, klen):
        r = break_caesar(char1, frequencies)
        common1 += r[0]
        common2.append(r[1])
    combine = ''
    count = 0
    while len(combine) < (len(cipher)):
        for char2 in common2:
            if count >= (len(char2)):
                continue
            combine += char2[count]
        count += 1
    return [common1, combine]

    
    
def vigenere_break(c, maxlen, frequencies):
    "your code here"
    ctr = 1
    start = math.inf
    key = ''
    value = ''
    while ctr <= maxlen:
        operate = vigenere_break_for_length(c, ctr, frequencies)
        freq = normalize(letter_counts(operate[1]))
        answer = distance(freq, frequencies)
        if  answer < start:
            start = answer
            key = operate[0]
            value = operate[1]
        ctr += 1
    return [key, value]


#############################################################
# A working substitution cipher                             #
#############################################################

def sub_gen_key():
    "your code here"
    gen_key = ''
    while len(gen_key)< 26:
        letter = alpha[random.randint(0, 25)]
        if letter not in gen_key:
            gen_key += letter
    return gen_key


def sub_enc(s, k):
    "your code here"
    encrypted = ""
    for char1 in s:
        for num in range(len(k)):
            if let_to_num(char1) == num:
                encrypted += k[num]
    return encrypted


def sub_dec(s, k):
    "your code here"
    decrypted = ""
    for char1 in s:
        for num in range(len(k)):
            if char1 == k[num]:
                decrypted += alpha[num]
    return decrypted


#############################################################
# Breaking the substitution cipher                          #
#############################################################

def count_trigrams(s):
    "your code here"
    d ={}
    index1 = 0
    index2 = 3
    while index2 <= len(s):
        char = s[index1:index2]
        if char in d:
            d[char] += 1
        else:
            d[char] = 1
        index1 += 1
        index2 += 1
    return d 


# Uncomment the code below once the functions above are complete
english_trigrams = count_trigrams(simplify_string(file_to_string("twocities_full.txt")))
normalize(english_trigrams)

def map_log(d):
    "your code here"
    for key, value in d.items():
        d[key] = math.log(value)
    return d


# Uncomment the code below once the functions above are complete
map_log(english_trigrams) 
english_trigrams

def trigram_score(s, english_trigrams):
    "your code here"
    ctr = 0
    g = count_trigrams(s)
    for key1 in g.keys():
        if key1 in english_trigrams.keys():
            ctr += english_trigrams[key1]
        if key1 not in english_trigrams.keys():
            ctr += (-15)
    return ctr 

                
def sub_break(cipher, english_trigrams):
    "your code here"
    first_key = sub_gen_key()
    first_txt = sub_dec(cipher, first_key)
    first_score = trigram_score(first_txt, english_trigrams)
    ctr = 0 
    while ctr <= 1000:
        convert_to_lst = list(first_key)
        nums = [random.randint(0, 25), random.randint(0, 25)]
        convert_to_lst[nums[0]], convert_to_lst[nums[1]] = convert_to_lst[nums[1]], convert_to_lst[nums[0]]
        new_key = ''
        for char in convert_to_lst:
            new_key+= char
        new_txt = sub_dec(cipher, new_key)                                       
        new_score = trigram_score(new_txt, english_trigrams)
        if new_score > first_score:
            first_score = new_score
            first_key = new_key
            first_txt = new_txt
        ctr += 1
    return [first_key, first_txt]
