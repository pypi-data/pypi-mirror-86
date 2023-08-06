import os
import pickle
from sklearn.model_selection import train_test_split
from DataProcessing.DataProcessor import DataProcessor
from sklearn.svm import LinearSVC


class Detector(object):
    # this method is used for train the mode
    def train(self, X_train, y_train):

        clf = LinearSVC()  # create svc linear mode
        clf.fit(X_train, y_train)  # train the mode

        with open(self.father_path + "/svm-xss-train.pkl", 'wb') as file:
            pickle.dump(clf, file)
        return clf

    # this method is used for testing accruacy of the mode
    def test(self):
        if self.clf is None:
            print("No clf mode slected")
            return
        print("xss module test start!")

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=0)
        resnum = 0

        for i in range(len(X_test)):
            result = self.clf.predict([X_test[i]])  # get the prediction
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

    # this is used for detecting user input
    def detect_input(self, user_input):
        if self.clf is None:
            return "No clf mode selected!"
        # create vector of input
        wordvec = self.dataProcessor.inputProcessingForSVM(user_input)

        result = self.clf.predict([wordvec])
        print("final result:")
        print("total hits")
        print(result)
        return result

    def load_mode(self):
        with open(self.father_path + "/svm-xss-train.pkl", 'rb') as file:
            clf = pickle.load(file)
        self.clf = clf

    def __init__(self):
        self.current_path = os.path.abspath(__file__)
        self.father_path = os.path.abspath(os.path.dirname(self.current_path) + os.path.sep + ".")
        self.dataProcessor = DataProcessor(5)
        self.X, self.Y = self.dataProcessor.dataProcessingForSVM(self.father_path + "/DataProcessing/xss-20000.txt",
                                                       self.father_path + "/DataProcessing/labeled_data.csv")
        self.clf = None

#if __name__ == '__main__':

    # initialization

    # detector = Detector()
    # detector.load_mode()

    # test accuracy:

    # detector.test()

    # train the mode:

    # detector.train(X,Y)

    # detect the user input:
    # if return 0 which means this is a XSS attack payload
    # print(detector.detect_input("<xmp onkeydown='alert(1)' contenteditable>test</xmp>"))
    # print(detector.detect_input("<script> alert(1) </script>"))
    # if return 1 which means this is not a XSS attck payload
    # print(detector.detect_input("this is a normal input 234556"))
    # print(detector.detect_input("12345 12345 12345 12345"))
    # print(detector.detect_input("11111111"))

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
