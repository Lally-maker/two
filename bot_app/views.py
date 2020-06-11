from django.shortcuts import render
import requests
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime
import emoji
import random
import json

@csrf_exempt
def index(request):
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        incoming_msg = request.POST['Body'].lower()

        # create Twilio XML response
        resp = MessagingResponse()
        msg = resp.message()

        responded = False
        
        #insert/merge chatbot components here (minus response code)
        # Importing modules
        import re
        from nltk.corpus import wordnet
        
        # Building a list of Keywords
        list_words=['hello','timings','trim','date', 'tomorrow','walk','open'] #added cut (was changed to barber here) to algorithm to see what i would need to add to facilitate a barber bot
        list_syn={}
        for word in list_words:
            synonyms=[]
            for syn in wordnet.synsets(word):
                for lem in syn.lemmas():
                    
                    # Remove any special characters from synonym strings
                    lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
                    synonyms.append(lem_name)
           
            list_syn[word]=set(synonyms)
            
        print (list_syn)
        
        #the below lines of codes allows me to create a dictionary [..ie keywords] of intents based on the synonyms within the keyword list...ie list_syn
        #the keyword dictionary is appended and the synonyms of the keyword from list_syn is added to the dictionary
        #another line of code is [down below] is used to find the keywrods from the dictionary in the...... 
        #customer's response to find their, the customer's, intent.
        
        # Building dictionary of Intents & Keywords
        keywords={}
        keywords_dict={}
        
        keywords = {
            'weekday':['.*\\bmonday\\b.*','.*\\btuesday\\b.*','.*\\bwednesday\\b.*','.*\\bthursday\\b.*','.*\\bfriday\\b.*'],
            'weekend':['.*\\bsaturday\\b.*','.*\\bsunday\\b.*'],
            }
        
        #to be added to the dictionary
        #niceties
        #some local slang....eg 'Yo!'
        
        # Defining a new key in the keywords dictionary
        keywords['greet']=[]
        
        # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
        for synonym in list(list_syn['hello']):
            keywords['greet'].append('.*\\b'+synonym+'\\b.*') #this regex expression tells the code to search from beginning to end .* and \b indicates that the parameter is the keyword
        
        #if i leave the below two lines of code attached to the above lines,
        #it will repeatedly print yo and cap     
        #keywords['greet'].append('yo') #any word that begins with yo is being represented as yo
        keywords['greet'].append('.*\\byo\\b.*') #this regex fixes the above line of code
        keywords['greet'].append('.*\\bcap\\b.*')
        keywords['greet'].append('.*\\bi love you\\b.*') #can use multiple words hear to represent intent
        
        # Defining a new key in the keywords dictionary
        keywords['timings']=[]
        
        # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
        for synonym in list(list_syn['timings']):
            keywords['timings'].append('.*\\b'+synonym+'\\b.*')
         
        for intent, keys in keywords.items():
            
            # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
            keywords_dict[intent]=re.compile('|'.join(keys)) #| is the OR operator 
                                                    #AND re.compile(str) creates a pattern object hence line 74 & 77 not being defined traditionally
        for synonym in list(list_syn['open']):
            keywords['timings'].append('.*\\b'+synonym+'\\b.*')
         
        for intent, keys in keywords.items():
            
            # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
            keywords_dict[intent]=re.compile('|'.join(keys)) #| is the OR operator 
                                                    #AND re.compile(str) creates a pattern object hence line 74 & 77 not being defined traditionally
          
        # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
        for synonym in list(list_syn['tomorrow']):
            keywords['timings'].append('.*\\b'+synonym+'\\b.*') #doesnt contain 'a hair cut' but i should be able to add it to the dictionary
         
        for intent, keys in keywords.items():
            
            # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
            keywords_dict[intent]=re.compile('|'.join(keys)) #| is the OR operator 
                                                    #AND re.compile(str) creates a pattern object hence line 74 & 77 not being defined traditionally
        keywords['hair cut']=[]
        
        # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
        for synonym in list(list_syn['trim']):
            keywords['hair cut'].append('.*\\b'+synonym+'\\b.*') #doesnt contain 'a hair cut' but i should be able to add it to the dictionary
         
        for intent, keys in keywords.items():
            
            # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
            keywords_dict[intent]=re.compile('|'.join(keys)) #| is the OR operator 
                                                    #AND re.compile(str) creates a pattern object hence line 74 & 77 not being defined traditionally
        #the below code is COMMENTED OUT because 
        #tomorrow was added tot he timings key in the dictionary
        
        #keywords['tomorrow']=[] #no idea why tomorrow wasnt working at first!
        
        # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
        #for synonym in list(list_syn['tomorrow']):
           # keywords['tomorrow'].append('.*\\b'+synonym+'\\b.*') #doesnt contain 'a hair cut' but i should be able to add it to the dictionary
         
        #for intent, keys in keywords.items():
            
            # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
            keywords_dict[intent]=re.compile('|'.join(keys)) #| is the OR operator 
                                                    #AND re.compile(str) creates a pattern object hence line 74 & 77 not being defined traditionally
        
        # Defining a new key in the keywords dictionary
        keywords['date']=[]
        
        # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
        for synonym in list(list_syn['date']):
            keywords['date'].append('.*\\b'+synonym+'\\b.*')
         
        for intent, keys in keywords.items():
            
            # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
            keywords_dict[intent]=re.compile('|'.join(keys)) #| is the OR operator 
                                                    #AND re.compile(str) creates a pattern object hence line 74 & 77 not being defined traditionally
        
        # Defining a new key in the keywords dictionary
        keywords['walk']=[]
        
        # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
        for synonym in list(list_syn['walk']):
            keywords['walk'].append('.*\\b'+synonym+'\\b.*')
         
        for intent, keys in keywords.items():
            
            # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
            keywords_dict[intent]=re.compile('|'.join(keys)) #| is the OR operator 
                                                    #AND re.compile(str) creates a pattern object hence line 74 & 77 not being defined traditionally
        
        # Defining a new key in the keywords dictionary
        keywords['walk']=[]
        
        # Populating the values in the keywords dictionary with synonyms of keywords formatted with RegEx metacharacters 
        for synonym in list(list_syn['walk']):
            keywords['walk'].append('.*\\b'+synonym+'\\b.*')
         
        for intent, keys in keywords.items():
            
            # Joining the values in the keywords dictionary with the OR (|) operator updating them in keywords_dict dictionary
            keywords_dict[intent]=re.compile('|'.join(keys)) #| is the OR operator 
                                                    #AND re.compile(str) creates a pattern object hence line 74 & 77 not being defined traditionally
        
        
        #merge response code with below code
        # Building a dictionary of responses
        responses={
            'greet':'Hello! How can I help you?',
            'timings':'We are open from 9AM to 5PM, Monday to Friday. We are closed on weekends and public holidays.',
            #'tomorrow': 'what time my nigga?',
            'fallback':['I dont quite understand. Could you repeat that?','repeat MOTHERFUCKER'],
            'hair cut':['np.that is doable. When?','standard'],
            'date':['What day?','WHEN?'],
            'weekday':'what time?',
        }
        
        print ("\nWelcome to the xXx Barber. How may I help you?\n") #Welcome to MyBank. How may I help you?
        
        #this response algo is not much different from the ML approach because that approach tokenize and lemmatizes the word and chooses
        #the appropriate response based on the class and patterm...ultimately choosing a predefined response to answer the consumer's question
        #tokenizing and lemmatizing can be sueful for sentences which contain multiple keywords; such as...
            #what time do you open tomorrow. the algo responds to the keyword 'tomorrow'

        

        if incoming_msg == 'hello':
            response = emoji.emojize("""
*Hi! I am the Quarantine Bot* :wave:
Let's be friends :wink:

You can give me the following commands:
:black_small_square: *'quote':* Hear an inspirational quote to start your day! :rocket:
:black_small_square: *'cat'*: Who doesn't love cat pictures? :cat:
:black_small_square: *'dog'*: Don't worry, we have dogs too! :dog:
:black_small_square: *'meme'*: The top memes of today, fresh from r/memes. :hankey:
:black_small_square: *'news'*: Latest news from around the world. :newspaper:
:black_small_square: *'recipe'*: Searches Allrecipes.com for the best recommended recipes. :fork_and_knife:
:black_small_square: *'recipe <query>'*: Searches Allrecipes.com for the best recipes based on your query. :mag:
:black_small_square: *'get recipe'*: Run this after the 'recipe' or 'recipe <query>' command to fetch your recipes! :stew:
:black_small_square: *'statistics <country>'*: Show the latest COVID19 statistics for each country. :earth_americas:
:black_small_square: *'statistics <prefix>'*: Show the latest COVID19 statistics for all countries starting with that prefix. :globe_with_meridians:
""", use_aliases=True)
            msg.body(response)
            responded = True

        import random
        # While loop to run the chatbot indefinetely
        while (True):  
            
            # Takes the user input and converts all characters to lowercase
            #user_input = input().lower()
            #i think i would be able to put tokenize and lemmatizer here by user input
            
            # Defining the Chatbot's exit condition, can a synonym type list be used to add more quit 'words'?
            if incoming_msg == 'a':#change back 'a' to 'quit' when finished 
                def_res = print ("Thank you for visiting.")
                responded = True
                break  
            
            for intent,pattern in keywords_dict.items(): #pattern acts as an object because it was created by re.compile(str)
            
                #will have toc reate bigrams here and add to keywords_dict.items() or create a new dictionary
                        
                # Using the regular expression search function to look for keywords in user input
                if re.search(pattern, incoming_msg): 
                    
                    # if a keyword matches, select the corresponding intent from the keywords_dict dictionary
                    matched_intent=intent  
            
            # The fallback intent is selected by default
            key='fallback' 
            if matched_intent in responses:
                
                # If a keyword matches, the fallback intent is replaced by the matched intent as the key for the responses dictionary
                key = matched_intent 
            
            # The chatbot prints the response that matches the selected intent
            please_work = print (responses[key]) #random.choice will allow for random responses by the chatbot
                                    #the random.choice function is return random LETTERS from the responses instead of the responses, hence it was removed temporarily   
                
            responded = True
            
            if not responded:
                 msg.body("Sorry, I don't understand. Send 'hello' for a list of commands.")

            return HttpResponse(str(resp))
