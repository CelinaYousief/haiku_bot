

#Written by Celina Yousief                                                                   

from lxml import html
import tweepy
import requests
import re
import random
import string
from num2words import num2words
from nltk.corpus import cmudict

#---------------------------------------------------------------------------

def main():

    #connect to twitter API
    auth =tweepy.OAuthHandler(CONSUMER,CONSUMER_SECRET)
    auth.set_access_token(ACCESS, ACCESS_SECRET)

    api = tweepy.API(auth)
    
    #get text from online textbook
    raw_text = get_text()
    #raw_text = format_text(raw_text)
    markoved_text = markov_it(raw_text)
    
    #create haiku from lines
    line1 = generate(markoved_text,5)
    last = line1[-1]
    out_line1 = ' '.join(line1)
    out_line1 = out_line1[0] + out_line1[1:].lower()
    
    line2 = generate(markoved_text,7,last)
    last=line2[-1]
    out_line2 = ' '.join(line2)
    out_line2 = out_line2[0].title() + out_line2[1:].lower()
    
    line3 = generate(markoved_text,5,last)
    out_line3 = ' '.join(line3)
    out_line3 = out_line3[0].title() + out_line3[1:].lower()

    haiku = out_line1 + '\n' + out_line2 + '\n' + out_line3
    haiku = re.sub(' +',' ',haiku)
    print(haiku)
    
    answer = input("Would you like to post?\n")
    if answer == 'y':
        api.update_status(haiku)
    else:
        return 0
    


    return 0

#-----------------------------------------------------------------------------

def get_text():
    out_text = []
    sect_arr = []

    url = 'http://greenteapress.com/thinkpython2/html/index.html'
    page = requests.get(url)

    #find possible links for all chapters in book
    tree = html.fromstring(page.content)
    text = tree.xpath('//a/@href')
    text = text[2:-18]
    
    #create url for random chapter
    url = 'http://greenteapress.com/thinkpython2/html/' + random.choice(text)
    page = requests.get(url)

    #get text from url
    tree = html.fromstring(page.content)
    text = tree.xpath('//p/text()')

    out_text = " ".join(text)
    out_text = re.sub(r"[^a-zA-Z0-9\']+"," ",out_text)
    out_array = out_text.split()

    #if is a digit, change it to a word
    for i in range(0,len(out_array)):
        if out_array[i].isdigit():
            out_array[i] = num2words(out_array[i])

    return out_array 
    

#------------------------------------------------------------------------------

def markov_it(original_text):
    #build markov dictionary word(key)->list of words(value)
    markov_dict = {}
   
    for x in range(0,len(original_text)-1):
        
        if original_text[x] not in markov_dict:
            markov_dict[original_text[x]] = []
            markov_dict[original_text[x]].append(original_text[x+1])
        else:
            markov_dict[original_text[x]].append(original_text[x+1])

    #print(markov_dict)
    return markov_dict

#-------------------------------------------------------------------------------

def syllable_count(words):
    
    d = cmudict.dict()
    count = 0
    
    #count syllables using nltk dictionary
    for word in words:
        print(word)
        syl_result =[len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
        count = count + syl_result[0]
    
    print(count)
    return count
#----------------------------------------------------------------------------------

def generate(markoved_text,length,last_word = ' '):
    #generate individual lines

    curr_word = ' '
    line_list = []
    caps = [w for w in markoved_text if w[0].isupper()]
    #print(caps)


    if last_word == ' ':
        curr_word = random.choice(caps)
    else:
        curr_word = random.choice(markoved_text[last_word])
        
    line_list.append(curr_word)
                
    
    if syllable_count(line_list) == length:
        return line_list
    elif syllable_count(line_list) > length:
        generate(markoved_text,length,last_word)
    else:      
        while 1:
            line_list.append(random.choice(markoved_text[curr_word]))
                
            if syllable_count(line_list) == length:
                return line_list
            elif syllable_count(line_list) > length:
                break
            else:
                curr_word = line_list[-1]
    
    return generate(markoved_text, length, last_word)

#----------------------------------------------------------------------------------



if __name__=="__main__":
    main()

