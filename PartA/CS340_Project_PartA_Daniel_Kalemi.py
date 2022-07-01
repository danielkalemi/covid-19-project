# CS340 FINAL COURSE PROJECT
# **************************
# PART A: COVID-19 GLOBAL PANDEMIC EPIDEMIOLOGICAL DATA ANALYSIS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The following Python Code should greet the user & present a 6-option menu with error trapping.
# ------------- 6 MENU OPTIONS ARE AS FOLLOW --------------
# 1. Display cumulative cases and deaths per continent
# 2. List a country’s population, cases and deaths per month
# 3. Perform statistical analysis and save into an output data file
# 4. Display statistical analysis results per continent
# 5. Visualize data for 3 countries, starting on the day of the 10th death
# 6. Exit the program
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Released under the GNU Open Source license agreement
# Daniel Kalemi   20170259@student.act.edu
# 19/6/2020


# IMPORTED LIBRARIES
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
import itertools
import datetime
import matplotlib.pyplot as plt
import sys


# THE PROJECT WAS DESIGNED TO BE MODULAR (USING AS MANY FUNCTIONS)
def menu():
    print("""
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        WELCOME TO COVID-19 DATA ANALYSIS PROGRAM!
       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Menu option 1: Display cumulative cases and deaths per continent
Menu option 2: List a country’s population, cases and deaths per month
Menu option 3: Perform statistical analysis and save into an output data file
Menu option 4: Display statistical analysis results per continent
Menu option 5: Visualize data for 3 countries, starting on the day of the 10th death
Menu option 6: Exits the program.
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
        option5()
        menu()
    elif ask_user == 6:
        print("Goodbye")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("END OF COVID-19 DATA ANALYSIS PROGRAM!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        input("press any button to exit...")
        sys.exit()
    else:
        print("Please type integers from 1-6")
        menu()


# Function for modular option 1
def option1():
    print("~~~~~~~~~~~~~~~~~~~~")
    print("WELCOME TO OPTION #1")
    print("~~~~~~~~~~~~~~~~~~~~")
    # try catch expression handling if file does not exist
    try:
        # reads from file the specified columns using pandas library
        file2 = pd.read_csv('partA_input_data.txt', usecols=['continentExp', 'cases', 'deaths'])
        group = file2.groupby('continentExp')
        # performs the addition required based on the condition set above
        sumgrup = group.sum()
        # resets the index columns
        sumgrup = sumgrup.reset_index()
        # display results
        print(sumgrup, "\n")
        # press any button to continue to exit
        input("\npress any button to continue...")

    except IOError as e:
        print("An error happened while trying to read your input file\n")



def option2():
    print("~~~~~~~~~~~~~~~~~~~~")
    print("WELCOME TO OPTION #2")
    print("~~~~~~~~~~~~~~~~~~~~")
    # try catch expression handling if file does not exist
    try:
        # reads from file the specified columns using pandas library
        file2 = pd.read_csv('partA_input_data.txt',
                            usecols=['countriesAndTerritories', 'popData2019', 'month', 'year', 'cases', 'deaths'])
        # user input for the country name to search
        country_month = input("Enter the country name you are looking for: ")
        # filter results based on the user input
        data_filtered = file2[file2['countriesAndTerritories'] == country_month]
        # variable that holds the way of turning months from integer to strings
        month_d = {1: 'January',
                   2: 'February',
                   3: 'March',
                   4: 'April',
                   5: 'May',
                   6: 'June',
                   7: 'July',
                   8: 'August',
                   9: 'September',
                   10: 'October',
                   11: 'November',
                   12: 'December'	}
        # variable that does the replacement of the column month with the above variable
        data_filtered['month'].replace(month_d, inplace = True)
        # ready function to sort the month names based on month order based on a new index column created for it
        data_filtered['month_nr'] = pd.DatetimeIndex(pd.to_datetime(data_filtered['month'], format='%B')).month
        data_filtered.set_index('month').sort_index()

        # grouping and performing the addition based on the following columns
        group = data_filtered.groupby(['countriesAndTerritories','month_nr' ,'month' ,'year'])
        sumgrup = group.sum()

        # display results
        print(sumgrup, "\n")
        # press any button to continue to exit
        input("\npress any button to continue...")
    except IOError as e:
        print("An error happened while trying to read your input file\n")


def option3():
    print("~~~~~~~~~~~~~~~~~~~~")
    print("WELCOME TO OPTION #3")
    print("~~~~~~~~~~~~~~~~~~~~")
    # try catch expression handling if file does not exist
    try:
        # reads from file columns using pandas library
        file2 = pd.read_csv('partA_input_data.txt')
        # performs the calculations on a new varibale to find cummulative cases
        file2['CumulativeCases'] = file2['cases'].cumsum()
        # performs the calculations on a new varibale to find cummulative deaths
        file2['CumulativeDeaths'] = file2['deaths'].cumsum()
        # performs the calculations on a new varibale to find  cases per capita
        file2['AvgCasesPerCapita'] = file2['cases'] / file2['popData2019']
        # performs the calculations on a new varibale to find  deaths per capita
        file2['AvgDeathsPerCapita'] = file2['deaths'] / file2['popData2019']
        # adds the variables created as new colums to the series of the file
        pd.Series(file2['CumulativeCases'])
        pd.Series(file2['CumulativeDeaths'])
        pd.Series(file2['AvgCasesPerCapita'])
        pd.Series(file2['AvgDeathsPerCapita'])
        # writes the changes to a new file
        file2.to_csv('partA_output_data.txt', index = False)
        # displays results
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("SUCCESS!!! YOUR FILE IS CREATED. BELOW IS A SNEAK PEEK")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(file2)
        # press any button to continue to exit
        input("\npress any button to continue...")

    except IOError as e:
        print("An error happened while trying to read your input file\n")


def option4():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("WELCOME TO OPTION #4! HERE ARE THE ADDED COLUMNS!!!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # try catch expression handling if file does not exist
    try:
        # reads from file the specified columns using pandas library
        file2 = pd.read_csv('partA_output_data.txt', usecols = ['continentExp', 'cases', 'AvgCasesPerCapita', 'deaths', 'AvgDeathsPerCapita', 'popData2019'])
        file2['AvgCasesPerCapita'] =  file2['AvgCasesPerCapita'] * 1000
        file2['AvgDeathsPerCapita'] =  file2['AvgDeathsPerCapita'] * 1000
        # calculates on a new variable the percentage of pop infected
        file2['PopInfected'] = ( file2['cases'] + file2['deaths'] / file2['popData2019'] ) / 100
        # adds that new variable to a column in the file series
        pd.Series(file2['PopInfected'])
        # groups by the continents
        group = file2.groupby('continentExp')
        # does the addition per continents per each columns
        sumgrup = group.sum()
        sumgrup = sumgrup.reset_index()
        # displays results
        print(sumgrup, "\n")
        # sumgrup.to_csv('sara.txt', index = False)
        # press any button to continue to exit
        input("\npress any button to continue...")


    except IOError as e:
        print("An error happened while trying to read your input file\n")
        print("You must complete option 3 before this one!\n")


def option5():
    print("~~~~~~~~~~~~~~~~~~~~")
    print("WELCOME TO OPTION #5")
    print("~~~~~~~~~~~~~~~~~~~~")
    try:
        file2 = pd.read_csv('partA_output_data.txt', delimiter=',')

    except IOError as e:
        print("An error happened while trying to read your input file\n")
        print("You must complete option 3 before this one!\n")

    file2 = file2.where(file2['CumulativeDeaths'] > 10)


    inp1 = input \
        ("Enter the name for the first country you want to see data in graph or enter for default: ")       # Get the input


    if inp1 in file2['countriesAndTerritories'].values:
        country1 = file2[file2['countriesAndTerritories'] == inp1]
        value = country1['AvgCasesPerCapita']
        arr1 = value.to_numpy()
        plt.plot(arr1, color = 'red', label=inp1)
    elif inp1 == "":
        inp1 = "Greece"
        country1 = file2[file2['countriesAndTerritories'] == inp1]
        value = country1['AvgCasesPerCapita']
        arr1 = value.to_numpy()
        plt.plot(arr1, color = 'red', label="Greece")
    else:
        print("Try again! This country is not accepted")

    inp2 = input \
        ("Enter the name for the second country you want to see data in graph or enter for default: ")       # Get the input

    if inp2 in file2['countriesAndTerritories'].values:
        country2 = file2[file2['countriesAndTerritories'] == inp2]
        value2 = country2['AvgCasesPerCapita']
        arr2 = value2.to_numpy()
        plt.plot(arr2, color = 'green', label=inp2)
    elif inp2 == "":
        inp2 = "China"
        country2 = file2[file2['countriesAndTerritories'] == inp2]
        value2 = country2['AvgCasesPerCapita']
        arr2 = value2.to_numpy()
        plt.plot(arr2, color = 'green', label="China")
    else:
        print("Try again! This country is not accepted")

    inp3 = input \
        ("Enter the name for the third country you want to see data in graph or enter for default: ")       # Get the input

    if inp3 in file2['countriesAndTerritories'].values:
        country3 = file2[file2['countriesAndTerritories'] == inp3]
        value3 = country3['AvgCasesPerCapita']
        arr3 = value3.to_numpy()
        plt.plot(arr3 ,color='blue', label=inp3)
    elif inp3 == "":
        inp3 = "United_States_of_America"
        country3 = file2[file2['countriesAndTerritories'] == inp3]
        value3 = country3['AvgCasesPerCapita']
        arr3 = value3.to_numpy()
        plt.plot(arr3, color='blue', label="United_States_of_America")
    else:
        print("Try again! This country is not accepted")
        # press any button to continue to exit
        input("\npress any button to continue...")
    # display graph and titles for axes and legend
    plt.title("Data visualisation for 3 countries")
    plt.xlabel("10th cummulative days")
    plt.ylabel("New cases")
    plt.legend(loc="upper left")
    plt.show()


# Main method ----------------------------------------------------------------------------------------------------------
def main():
    menu()


# Run the main def here -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()






























































