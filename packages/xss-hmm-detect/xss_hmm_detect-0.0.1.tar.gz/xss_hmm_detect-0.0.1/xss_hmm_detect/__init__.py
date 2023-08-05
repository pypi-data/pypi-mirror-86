import sys
import urllib
from urllib.parse import urlparse
import re
from hmmlearn import hmm
import numpy as np
import html
from html.parser import HTMLParser
import nltk
import pickle
from sklearn.model_selection import train_test_split

# minium length of the input
MIN_LEN = 10

# components amount
N = 5

# Special characters for possible input
SEN=['<','>',',',':','\'','/',';','"','{','}','(',')']

index_wordbag=1 #word bag index
wordbag={} # word bag dict

# regular expression for extracting words in an input
tokens_pattern = r'''(?x)
 "[^"]+"
|http://\S+
|</\w+>
|<\w+>
|<\w+
|\w+=
|>
|\w+\([^<]+\)
|\w+
'''




def do_str(line):
    words = nltk.regexp_tokenize(line, tokens_pattern)
    return words

def load_wordbag(filename,max=100):
    X = [[0]]
    X_lens = [1]
    tokens_list=[]
    global wordbag
    global index_wordbag

    with open(filename) as f:
        for line in f:
            line=line.strip('\n')
            # url decode
            line=urllib.parse.unquote(line)
            # handle html
            h = HTMLParser()
            line=html.unescape(line)
            if len(line) >= MIN_LEN:
                #print "Learning xss query param:(%s)" % line
                #replace number with 8
                line, number = re.subn(r'\d+', "8", line)
                #replace https url header with http://u
                line, number = re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?:=]+', "http://u", line)
                #remove the comment
                line, number = re.subn(r'\/\*.?\*\/', "", line)
                tokens_list+=do_str(line)



    fredist = nltk.FreqDist(tokens_list)  # create wordbag with each word's frequency
    fredist = fredist.most_common(60)

    #print(fredist)
    keys = []
    for i in fredist:
        if i[0] != '8' and i[0] != 'test':
            keys.append(i[0])
    #print(keys)

    for localkey in keys:
        if localkey in wordbag.keys():
            continue
        else:
            wordbag[localkey] = index_wordbag
            index_wordbag+=1

def main(filename):
    X = [[-1]]
    X_lens = [1]

    global wordbag
    global index_wordbag

    with open(filename) as f:
        for line in f:
            line=line.strip('\n')
            #url decode
            line=urllib.parse.unquote(line)
            #handle html
            h = HTMLParser()
            line=html.unescape(line)
            vers=[]
            if len(line) >= MIN_LEN:
                # pre-process of the input
                # replace all numeric parameters with number 8
                line, number = re.subn(r'\d+', "8", line)
                # replace url content with http://u
                line, number = re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?:]+', "http://u", line)
                # replace comment
                line, number = re.subn(r'\/\*.?\*\/', "", line)
                # vectorization
                words=do_str(line)
                for word in words:
                    if word in wordbag.keys():
                        vers.append([wordbag[word]])
                    else:
                        vers.append([-1])
                    print(word, vers)
            np_vers = np.array(vers)
            print ("np_vers:", np_vers, "X:", X)
            X=np.concatenate([X,np_vers])
            X_lens.append(len(np_vers))


    # create hmm model based on the wordbag matrix
    remodel = hmm.GaussianHMM(n_components=N, covariance_type="full", n_iter=100)
    remodel.fit(X,X_lens)
    with open("hmm-xss-train.pkl", 'wb') as file:
        pickle.dump(remodel, file)
    return remodel

def test(remodel,filename):
    num = 0
    wordbagflag = 0
    for line in filename:
        line = line.strip('\n')

        line = urllib.parse.unquote(line)

        h = HTMLParser()
        line = html.unescape(line)

        if len(line) >= MIN_LEN:


            line, number = re.subn(r'\d+', "8", line)

            line, number = re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?:]+', "http://u", line)

            line, number = re.subn(r'\/\*.?\*\/', "", line)

            words = do_str(line)

            vers = []
            #print(words)
            #print(wordbag)
            for word in words:
                # print "ADD %s" % word
                if word in wordbag.keys():
                    #print(word)
                    vers.append([wordbag[word]])
                else:
                    vers.append([-1])

            np_vers = np.array(vers)
            #print(np_vers)

            pro = remodel.score(np_vers)
            #print(pro)
            if pro <= 20:
                num+=1
            # print("this is not a attack")
            # print(line, pro)
        # print("result:")
        # print(num/len(filename))
    return num

def detect_userinput(user_input):
    load_wordbag('./xssfile.txt', 8000)
    with open("./hmm-xss-train.pkl", 'rb') as file:
        remodel = pickle.load(file)
    res = test(remodel, [user_input])
    return res
if __name__ == '__main__':


    # The input should be longer or the detect result will be inaccurate
    print(detect_userinput("<script> alert(1) </script>"))
    print(detect_userinput("this is a normal input hi hi hi hi sad xic sjaildijlij "))


    #
    # load_wordbag('./xssfile.txt',8000)
    # #remodel = main('./xssfile.txt')
    # filelist = []
    # f = open("./xssfile.txt", "r")
    # lines = f.readlines()  # read all files
    # for line in lines:
    #     filelist.append(line)
    # f.close()
    # #
    # train_list, test_list = train_test_split(filelist,test_size=0.2, random_state=0)
    #print(train_list, test_list)
    #print(len(train_list), len(test_list))
    # with open("./hmm-xss-train.pkl", 'rb') as file:
    #     remodel = pickle.load(file)
    # #test(remodel, ["I alert I can use a alert to explain alert assume <script> can o  assume I can use a website </script>"])
    # #test(remodel,["<script> alert(1) </script>"])
    # test(remodel,test_list)
    #test(remodel,["<source id=x tabindex=1 onbeforedeactivate=alert(1)></source><input autofocus>"])
    #test(remodel,["hi this is <surce with onhold andd alert ou sstt urlaa big hi this is <surce with onhold andd alert ou sstt urlaa big "])



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
