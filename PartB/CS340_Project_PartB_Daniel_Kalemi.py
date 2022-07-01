# CS340 FINAL COURSE PROJECT
# **************************
# PART B: MACHINE LEARNING & NEURAL TRAINING
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The following Python Code should greet the user & present a 5-option menu with error trapping.
# ------------- 5 MENU OPTIONS ARE AS FOLLOW --------------
# Menu option 1: Enter size of middle layer
# Menu option 2: Initiate a training pass
# Menu option 3: Classify test data
# Menu option 4: Display training result graphics
# Menu option 5: Exits the program.
# 6. Exit the program
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Released under the GNU Open Source license agreement
# Daniel Kalemi   20170259@student.act.edu
# 19/6/2020

import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import warnings
import pandas as pd


#default variables used throughout the code in the menu options where the user does not input data
defaultFile = "training_data.txt"
defaultLearningRate = 0.5
defaultEpochNumber = 5500
hidden_layer = 6

def menu():
    print("""
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          WELCOME TO OUR MACHINE LEARNING PROGRAM!
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Option 1: Enter size of middle layer
Option 2: Initiate a training pass
Option 3: Classify test data
Option 4: Display training result graphics
Option 5: Exits the program.
            """)
    ask_user = input("Choose an option: ")
    try:
        ask_user = int(ask_user)
    except:
        print("Please type integers from 1-6")
        menu()

    if ask_user == 1:
        option1()
        menu()
    elif ask_user == 2:
        option2()
        menu()
    elif ask_user == 3:
        option3()
        menu()
    elif ask_user == 4:
        option4()
        menu()
    elif ask_user == 5:
        print("Goodbye")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("END OF MACHINE LEARNING PROGRAM!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        input("press any button to exit...")
        sys.exit()
    else:
        print("Please type integers from 1-6")
        menu()

#sigmoid activation function
def sigmoid(x,derivative=False):
	if(derivative==True):
         return x*(1-x)
	return 1/(1+np.exp(-x))

#function for training the ANN
#takes 5 parameters that come from user input, or in the other case from default values
def ANN(trainingInputs, trainingOutputs, trainingEpoch, hiddenLayers, learningRate):

    np.random.seed(int(time.time()))

    # randomly initialize our weights with mean 0
    synMatrix0 = 2 * np.random.random((8, hiddenLayers)) - 1
    synMatrix1 = 2 * np.random.random((hiddenLayers, 2)) - 1

    #array to store the errors with their epochs
    training_progress = []
    for j in range(trainingEpoch):

        # Feed forward through layers 0, 1, and 2
        l0 = trainingInputs
        l1 = sigmoid(np.dot(l0, synMatrix0))
        l2 = sigmoid(np.dot(l1, synMatrix1))

        # how much did we miss the target value?
        l2_error = trainingOutputs - l2

        if (j % 100) == 0: #every 100 iterrations append the calculated error in the array
           training_progress.append([j, np.mean(np.abs(l2_error))])

        # calculating the change in the weights for the synapses between the hidden layer and output
        l2_delta = l2_error * learningRate

        # Starting the backpropagation.
        l1_error = l2_delta.dot(synMatrix1.T)

        #adjusting to the set learning rate
        l1_delta = l1_error * learningRate

        #update weights
        synMatrix1 += l1.T.dot(l2_delta)
        synMatrix0 += l0.T.dot(l1_delta)

        #save the error progress of the cost function to the file
        np.savetxt("training_progress.txt", training_progress, fmt="%s")

        #save the adjusted weight Matrices in their respective files
        np.savetxt("synMatrix0.txt", synMatrix0, fmt="%s")
        np.savetxt("synMatrix1.txt", synMatrix1, fmt="%s")
    return synMatrix0, synMatrix1

#function that reads input data and classifies the output according to the training done
#takes user data input to test from a file and looks at the matrices
# holding the correct weights from the training phase
def testDataClassification(TestData, synMatrix0, synMatrix1):
    l0 = TestData #test data from file
    l1 = sigmoid(np.dot(l0, synMatrix0))
    l2 = sigmoid(np.dot(l1, synMatrix1))
    return l2

def synMatrixReader(file):
    synM0 = []
    f = open(file)
    for line in f:
        line = line.strip("\n")  # strip from the uneccessary characters
        inData = map(str, line.split(" "))  # split each item
        synM0.append(list(map(float, inData)))  # map it into an integer while appending it into an array
    syn_data = np.array(synM0)  # turn it into a numpy array
    return syn_data

def classificationOption(file):
    # saving the values into this array
    testingData = []

    synM0 = synMatrixReader("synMatrix0.txt")
    synM1 = synMatrixReader("synMatrix1.txt")

    # for each line in the file
    for line in file:
        line = line.strip("\n")  # strip from the uneccessary characters
        inData = list(line)  # split each item
        testingData.append(list(map(int, inData)))  # map it into an integer while appending it into an array
    input_data = np.array(testingData)  # turn it into a numpy array
    # call the classification function
    # give per parameters the test data and the weights calculated in option 2
    outTestData = testDataClassification(input_data, synM0, synM1)

    # round the output and cast it as an integer
    rounded = np.round(outTestData).astype(int)

    # save the results into the file
    np.savetxt("training_output.txt", rounded, fmt="%s", delimiter=",")

    print("Congratulations your output have been predicted and saved in a file named training_output.txt!")

def displayGraph(file):
    # arrays that will store each column from the file
    epochNumber, errorValue = [], []
    # per each line
    for line in file:
        # divide lines according to the delimiter
        fistCol, secondCol = map(str, line.split(" "))
        epochNumber.append(float(fistCol))  # append to the arrays
        errorValue.append(float(secondCol))

    # plot the graph
    plt.plot(epochNumber, errorValue, color='purple')

    # give the labels
    plt.xlabel('Number of training epochs')
    plt.ylabel('Cost function output')
    plt.title('THE TRAINING PROGRESS OF THE ANN.')

    # show the graph
    plt.show()

def option1():
        print("\n" + "WELCOME TO OPTION #1!" + "\n")

        try:
            # ask the user for the number of neurons he wants in the hidden layer
            hidden_layer_input = str(input(
                "Please enter the number of neurons the hidden layer of the ANN should have (Preferably 6 neurons): "))

            # if hidden_layer not in range(3,8):
            # print("Please enter a value in the range 2 to 8.")
            # in case he doesn't press "ENTER" change  the default value to the user input
            if hidden_layer_input != "":
                if int(hidden_layer_input) not in range(3, 8):
                    print("Enter a proper number.")
                else:
                    hidden_layer = int(hidden_layer_input)  # cast it as a string
                    print("Congratulations you have chosen a network with a 8 - {} - 2 topology!".format(hidden_layer))
            else:
                print("Congratulations you have chosen a network with a 8 - {} - 2 topology!".format(hidden_layer))
                # press any button to continue to exit
                input("\npress any button to continue...")
        except ValueError:
            print("Please enter a proper value.")

    # second option is chosen


def option2():
    print("\n" + "WELCOME TO OPTION #2!" + "\n")

    try:
        # take user input
        trainingFileName = str(input("Please enter the name of the training data set file: "))

        # when the user presses "ENTER" set the variables to their default values
        if trainingFileName == "":
            trainingFileName = defaultFile

        learningRate = str(input("Please enter the learning step: "))  # learning step input
        if learningRate == "":
            learningRate = defaultLearningRate
        else:  # if the user inputs data cast it from string to its datatype
            learningRate = float(learningRate)  # casted to float

        epochNumber = str(input("Please enter the number of the training epochs: "))  # epoch number input
        if epochNumber == "":
            epochNumber = defaultEpochNumber
        else:
            epochNumber = int(epochNumber)  # casted to int

        # arrays that will contain the prespective column data read from the training_data.txt file
        trainingInput, trainingOutput = [], []

        # opening file to read
        fName = open(trainingFileName, "r")

        # per each line in the file
        for line in fName:
            line.strip("\n")  # strip the unecessary characters
            fistCol, secondCol, thirdCol = map(str, line.split(","))  # split into three columns
            trainingInput.append(list(map(int, list(fistCol))))  # input training data
            trainingOutput.append(
                [int(secondCol), int(thirdCol)])  # output training data needed to check the error scale
        # turning them to numpy arrays
        npTrainingInput = np.array(trainingInput)
        npTrainingOutput = np.array(trainingOutput)

        # calling the function giving the input parameters
        # save the weights into the arrays
        synMatrix0, synMatrix1 = ANN(npTrainingInput, npTrainingOutput, epochNumber, hidden_layer, learningRate)

        print("\n" + "Congratulations your network has been sucessfully trained!")
        print("Its' cost function progress has been saved in a file named training_progress!" + "\n")
        # press any button to continue to exit
        input("\npress any button to continue...")
    except ValueError:
        print("Please enter a proper value.")
    except FileNotFoundError:
        print("Please make sure you have entered the proper file name.")


# second option is chosen
def option3():
    try:
        print("\n" + "WELCOME TO OPTION #3!" + "\n")

        # reading the testing data
        fName = open("input_data.txt")
        classificationOption(fName)
        # press any button to continue to exit
        input("\npress any button to continue...")
    except IOError as e:
        print("An error happened while trying to read your input file.")


def option4():
    try:
        # file to be read
        fName = open("training_progress.txt", "r")
        displayGraph(fName)
        # press any button to continue to exit
        input("\npress any button to continue...")
    except IOError as e:
        print("An error happened while trying to read your input file. Make sure you have gone through option 2!")


def main():


  warnings.filterwarnings("ignore")
  menu()

# Run the main def here -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()