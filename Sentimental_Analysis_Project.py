from nltk.corpus import twitter_samples,stopwords
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import classify,NaiveBayesClassifier
from nltk.tokenize import word_tokenize
import re, string, random,os,sys, time, threading
import tkinter
import tkinter.font as tkFont

#FUNCTION TO REMOVE NOISE FROM THE TWEET
def remove_noise(tweet_tokens, stop_words = ()):

    #Cleaned Token list
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        #this will remove all the unneccessary elements from the twwet
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        #lemmatizer is the technique which is used to normalise the word with its grammatical meaning
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        #if condition for checking that token's length should be greater than 0 and it should not be punctuator and not in stop_words
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


def the_process_function(positive_cleaned_tokens_list,negative_cleaned_tokens_list):
    #using stop words of english language
    stop_words = stopwords.words('english')

    #Tokenizing Each postive and negative tweet 
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    #Removing Noise from tweets
    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))


def animated_loading():
    # String to be displayed when the application is loading 
    load_str = "training your application...it may take some time to load"
    ls_len = len(load_str) 
  
  
    # String for creating the rotating line 
    animation = "|/-\\"
    anicount = 0
      
    # used to keep the track of 
    # the duration of animation 
    counttime = 0        
      
    # pointer for travelling the loading string 
    i = 0                     
  
    while (counttime != 115): 
          
        # used to change the animation speed 
        # smaller the value, faster will be the animation 
        time.sleep(0.075)  
                              
        # converting the string to list 
        # as string is immutable 
        load_str_list = list(load_str)  
          
        # x->obtaining the ASCII code 
        x = ord(load_str_list[i]) 
          
        # y->for storing altered ASCII code 
        y = 0                             
  
        # if the character is "." or " ", keep it unaltered 
        # switch uppercase to lowercase and vice-versa 

        if x != 32 and x != 46:              
            if x>90: 
                y = x-32
            else: 
                y = x + 32
            load_str_list[i]= chr(y) 
          
        # for storing the resultant string 
        res =''              
        for j in range(ls_len): 
            res = res + load_str_list[j] 
              
        # displaying the resultant string 
        sys.stdout.write("\r"+res + animation[anicount]) 
        sys.stdout.flush() 
  
        # Assigning loading string 
        # to the resultant string 
        load_str = res 
  
          
        anicount = (anicount + 1)% 4
        i =(i + 1)% ls_len 
        counttime = counttime + 1
      
    
#FUNCTION FOR ANALYSING TWEET
def check_tweet(custom_tweet):
    custom_tokens = remove_noise(word_tokenize(custom_tweet))
    return classifier.classify(dict([token, True] for token in custom_tokens))
    #return 'Positive'
    

def Interface():
    #App started
    root = tkinter.Tk()
    
    #CHANGE TITLE OF APP
    root.title("Sentimental Analysis")
    
    #FONTSTYLES USED IN PROGRAM
    fontStyle = tkFont.Font(family="Lucida Grande", size=20)
    fontStyle1 = tkFont.Font(family="Times New Roman", size=20)
    fontStyle2 = tkFont.Font(size=10)
    
    #FUNCTION FOR ABOUT MENU
    def About():
        root1 = tkinter.Toplevel(root)
        txt1 = "It's a project on Sentimental Analysis\ncreated in Python3.\n and has been created by"
        txt2 = "Anubhav Solanki(Univ. Roll no. : 2013642)"
        txt3 = "who is currenty a 2nd Year BTech CSE student of" 
        txt4 = "Graphic Era Deemed to be University" 
        txt5 = "and guided by" 
        txt6 = "Prof. Sharad Gupta."
        tkinter.Label(root1,text='ABOUT',font=fontStyle).pack()
        tkinter.Label(root1,text="                 ").pack()
        tkinter.Label(root1,text="                 ").pack()
        tkinter.Label(root1,text=txt1,font=fontStyle2).pack()
        tkinter.Label(root1,text=txt2,font=('Times New Roman', 10, 'bold')).pack()
        tkinter.Label(root1,text=txt3,font=fontStyle2).pack()
        tkinter.Label(root1,text=txt4,font=('Times New Roman', 10, 'bold')).pack()
        tkinter.Label(root1,text=txt5,font=fontStyle2).pack()
        tkinter.Label(root1,text=txt6,font=('Times New Roman', 10, 'bold')).pack()
        root1.geometry('300x250')
        
    #MENUBAR IS CREATED
    menubar = tkinter.Menu(root)
    helpmenu = tkinter.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=About)
    menubar.add_cascade(label="Help", menu=helpmenu)
    root.config(menu=menubar)
    
    #ANALYSE THE RESULT
    def Check():
        result = check_tweet(e1.get())
        if(result=="Positive"):
            color = "green"
        else:
            color = "red"
        label.configure(text=result,fg=color,font=fontStyle1)

    #EVENT HANDLER FOR KEYS
    def Check_with_event(event):
        if(event.keysym=='Return'):
            Check()
        elif(event.keysym=='Shift_R' or event.keysym=='Shift_L'):
            refresh()

    #CHANGE THE FIELD OF INPUT
    def setTextInput(text):
        e1.delete(0,"end")
        e1.insert(0, text)
    
    #FUNCTION FOR CLEARING THE FIELD
    def refresh():
        setTextInput("")
        label.configure(text="")
    
    #HEADING FOR APP
    frame1 = tkinter.Frame(root)
    tkinter.Label(frame1,text="Sentimental Analysis",font=fontStyle).pack()
    tkinter.Label(frame1,text="                 ").pack()
    tkinter.Label(frame1,text="Hotkeys :\nEnter - Analyse\nShift - Clear",font=fontStyle2).pack()
    tkinter.Label(frame1,text="               ").pack()
    frame1.pack()

    #BODY OF APP
    frame2 = tkinter.Frame(root)
    tkinter.Label(frame2, text='Enter your Tweet',font=fontStyle2).grid(row=0)
    e1 = tkinter.Entry(frame2) 
    e1.grid(row=0, column=1)
    tkinter.Label(frame2, text='   ').grid(row=0,column=2)
    button = tkinter.Button(frame2,text="Analyze",command=Check)
    button.grid(row=0,column=3)
    tkinter.Label(frame2,text='  ').grid(row=0,column=4)
    tkinter.Button(frame2,text="Clear",command=refresh).grid(row=0,column=5)
    frame2.pack()
    
    #FOOTER FOR APP
    frame3 = tkinter.Frame(root)
    tkinter.Label(frame3,text="                 ").pack()
    tkinter.Label(frame3,text="                 ").pack()
    label = tkinter.Label(frame3,text='       ')
    label.pack() 
    tkinter.Label(frame3,text="                 ").pack()
    tkinter.Label(frame3,text="                 ").pack()
    tkinter.Label(frame3,text='Created By - Anubhav Solanki',font=fontStyle2).pack()
    frame3.pack()
    root.bind('<KeyPress>', Check_with_event)
    root.geometry("450x300")
    root.mainloop()


if __name__ == "__main__":
    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []
    the_process = threading.Thread(name='process', target=the_process_function,args=(positive_cleaned_tokens_list,negative_cleaned_tokens_list,))
    the_process.start()
    os.system("cls")
    while the_process.is_alive():
        animated_loading()
    os.system("cls")  
    #TRAINING THE DATA
    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    #Shuffling the dataset
    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    #CLASSIFY THE DATA WITH NAIVE BAYES CLASSIFIER
    classifier = NaiveBayesClassifier.train(train_data)

    #GUI application
    Interface()
