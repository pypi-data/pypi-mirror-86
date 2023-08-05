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
from DataProcessing.DataProcessor import DataProcessor
from sklearn.svm import LinearSVC

# this method is used for train the mode
def train(X_train,y_train):

    clf = LinearSVC()  # create svc linear mode
    clf.fit(X_train, y_train)  # train the mode
    resnum = 0
    with open("../svm-xss-train.pkl", 'wb') as file:
        pickle.dump(clf, file)
    return clf


#this method is used for testing accruacy of the mode
def test():
    print("xss module test start!")
    dataProcessor = DataProcessor(5)
    # svm process

    # clf = create_xss_svc('./xssfile.txt' , './normalinput.txt')
    # data process from source xss and white sample file
    X, Y = dataProcessor.dataProcessingForSVM("./DataProcessing/xss-20000.txt",
                                              "./DataProcessing/labeled_data.csv")  # For SVM
    print(X)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    resnum = 0
    with open("./svm-xss-train.pkl", 'rb') as file:
        clf = pickle.load(file)
    for i in range(len(X_test)):
        result = clf.predict([X_test[i]])  # get the prediction
        print('predict result vs label：', result[0], y_test[i])
        a = str(result[0]).strip()
        b = str(y_test[i]).strip()
        if a == b:
            resnum += 1
    print("final result:")
    print("total hits")
    print(resnum)
    print("total test sample")
    print(len(X_test))
    print("accuracy:")
    print(resnum / len(X_test))



#this is used for detecting user input
def detect_input(user_input):
    #create vector of input

    dataProcessor = DataProcessor(5)
    X, Y = dataProcessor.dataProcessingForSVM("./DataProcessing/xss-20000.txt", "./DataProcessing/labeled_data.csv")
    wordvec = dataProcessor.inputProcessingForSVM(user_input)
    print(wordvec)
    with open("./svm-xss-train.pkl", 'rb') as file:
        clf = pickle.load(file)
    result = clf.predict([wordvec])
    print("final result:")
    print("total hits")
    print(result)
    return result




if __name__ == '__main__':
    #test accuracy:
    #test()

    #train the mode:
    #dataProcessor = DataProcessor(5)
    #X, Y = dataProcessor.dataProcessingForSVM("./DataProcessing/xss-20000.txt",
    #                                         "./DataProcessing/labeled_data.csv")  # For SVM
    #train(X,Y)

    #detect the user input:
    #if return 0 which means this is a XSS attack payload
    print(detect_input("<script> alert(1) </script>"))
    #if return 1 which means this is not a XSS attck payload
    print(detect_input("this is a normal input 234556"))

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
