# Add dashboard and login/register stuff
# Validate email and password

# TODO: add logout feature

import validators
import csv
import re
import time
import sys
from datetime import date
from math import sqrt
from tabulate import tabulate

# global variable to keep track of email and password with default email
emailsAndPasswords = {"test@123.com": "123"} 

# reading the email and password file, add to the dictionary to keep track of users' accounts
try:
    with open("manage.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            emailsAndPasswords[row["Email"]] = row["Password"] 
except IOError:
    pass

# USER INFORMATION CLASS WITH LOGIN and REGISTER FEATURE
class User:
    def __init__(self):
        print("="*35)
        print("== 1. Login in existing account  ==")
        print("== 2. Register a new account     ==")
        print("="*35)

        print()
        option = input("Choose an option: ")
        while option not in "12" or option == "":
            option = input("Please choose a valid option: ")

        match option:
            case "1": # login case
                # check for email and password
                self.email = self.get_email_login()
                self.password = self.get_password_login()
                self.number = self.get_number()
                self.date = date.today()
                
                # calculating score
                number_properties = NumberProperties(self.number)
                score = number_properties.calculate_score()

                # modify the leaderboard results with that existing account
                if self.email != "test@123.com":
                    ResultManager.modify_existing_account(self.email, self.number, score, self.date)

            case "2": # register case
                # check for email and password
                self.email = self.get_email_register()
                self.password = self.get_password_register()

                # update the newly created account in the manage.csv file
                ResultManager.update_manage_file(self.email, self.password)

                # add the existing account into the dictionary 
                emailsAndPasswords[self.email] = self.password

                # add for personal information and the number
                self.name = self.get_name()
                self.dob = self.get_dob()
                self.number = self.get_number()
                self.date = date.today()

                # calculating score
                number_properties = NumberProperties(self.number)
                score = number_properties.calculate_score()
                
                # saving the new result to the leaderboard
                ResultManager.save_new_results(score, self.email, self.name, self.dob, self.number, self.date)

    # get user's email when login in
    def get_email_login(self):
        # providing default account
        print("Default account: test@123.com - Password: 123") 
        # ask for user's email
        email = input("Enter your email to login: ")

        # check if the email is in the system or not, if yes, ask for the password, if not, return that the email is not exist
        while True:
            if not validators.email(email):
                email = input("Please enter a valid email: ")
            elif validators.email(email) and email not in emailsAndPasswords:
                email = input("Your email have not been registered before, please enter the email again: ")
            else: 
                return email
    
    # get user's password corresponding to the email they logged in
    def get_password_login(self):
        # ask for password
        password = input("Enter your password: ")
        attempt = 3

        # continue checking password
        while True:
            if password != emailsAndPasswords[self.email]:
                password = input(f"You have entered the wrong password, please enter your password again ({attempt} attempts left): ") # TODO: trials left
                attempt -= 1
                if attempt == 0:
                    sys.exit("You have been logged out of the game!")
            else: 
                print("You have login successfully !!!")
                return password
    
    # get user's email when registering, check for validation and duplication
    def get_email_register(self):

        email = input("Enter your email to register: ")

        while True:
            if not validators.email(email):
                email = input("Please enter a valid email: ")
            elif validators.email(email) and email in emailsAndPasswords:
                email = input("Your email has been registered before, please enter a new email: ")
            else: 
                return email
    
    # get user's new password for the account
    def get_password_register(self):
        return input("Enter your new password for your account: ")
    
    # get user's name
    def get_name(self):
        return input("Enter your name to play: ")

    # get user's number
    def get_number(self):
        while True:
            try:
                num = int(input("Please enter a positive integer number (2-3 digits recommended): "))
                if num > 0:
                    return num
            except ValueError:
                print("Please enter a valid number.")

    # get user's date of birth
    def get_dob(self):
        while True:
            dob = input("Type in your date of birth in yyyy-mm-dd format: ")
            if self.is_valid_dob(dob):
                return dob
            print("Invalid date format or date. Please enter in yyyy-mm-dd format.")

    # validate user's date of birth
    def is_valid_dob(self, dob):
        if re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", dob):
            year, month, day = map(int, dob.split('-'))
            if year > 2024: 
                return False
            if month == 2 and day > 29:
                return False
            if month == 2 and day == 29 and not self.is_leap_year(year):
                return False
            return True
        return False

    @staticmethod
    def is_leap_year(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Number Properties Class
class NumberProperties:
    def __init__(self, number):
        self.number = number

    # calculating score and displaying the results
    def calculate_score(self):
        score = 0
        properties = {
            "Is a Prime number": self.prime,
            "Is a Perfect number": self.perfect,
            "Is a number that sum of the square of all digits equals itself": self.sum_all_square_digits,
            "Divisibe by sum of all digits": self.harsard,
            "Only contains consecutive digts": self.consecutive_rearrange,
            "Is a Squared Number": self.square,
            "Is a Prime number itself or itself reversed": self.erimp,
            "Is almost a Strong number": self.strong,
            "Is a Happy number": self.happy
            # ... include other properties as methods
        }

        # Displaying calculating text
        print("Calculating result ", end="")
        for _ in range(3):
            print(".", end="")
            time.sleep(0.5)
        print()

        # Print out number's traits
        for description, func in properties.items():
            if func(self.number):
                score += 1
                print(f"- Your number {description}!")
        
        if score == 0:
            print("Your number is so unique that I have not updated its trait yet!")

        print(f"You have received {score} scores. Congratulations!")
        return score

    # BELOW IS ALL NUMBERS' TRAITS CHECKING FUNCTIONS 

    # Prime number check
    def prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
     
    # Perfect number check
    def perfect(self, n): 
        return sum(i for i in range(1, n) if n % i == 0) == n

    # Sum of all square digits of num equal num
    def sum_all_square_digits(self, n): 
        if sum(int(i)**2 for i in str(n)) == n:
            return True
        else: return False

    # Divisible by sum of all digits
    def harsard(self, n): 
        if n % sum(int(i) for i in str(n)) == 0:
            return True
        else: return False

    # If all the unique digits reaaranged can be consecutive e.g 335542 --> 2345 --> True
    def consecutive_rearrange(self, n): 
        n = sorted(list(set(str(n))))
        for idx in range(1,len(n)):
            if int(n[idx]) - int(n[idx-1]) != 1: return False
        return True

    # Square root integer
    def square(self, n): 
        return int(sqrt(n)) == sqrt(n)

    # A prime number if reversed still a prime number
    def erimp(self, n): 
        if self.prime(n) == True:
            newnum = ""
            for i in str(n)[::-1]:
                newnum += i
            if self.prime(int(newnum)) == True:
                return True
        return False

    # Divisible by any prime number and the square of that prime number
    def strong(self, n): 
        i = 2
        while True:
            if i**2 > n: return False
            elif self.prime(i) == True:
                if n%i==0:
                    if n%(i**2)==0: return True
            i+=1

    # Sum square of all digits until reaches 1
    def happy(self, n): 
        lst = []
        while n != 1:
            total = 0
            for i in str(n):
                total += int(i)**2
            n = total
            if n in lst: return False
            else: lst.append(n)
        return True
    
        # ... Implement other methods if necessary ... 
    
# RESULT MANAGER CLASS
class ResultManager:
    
    # method for saving results of a new account (register)
    @staticmethod
    def save_new_results(score, email, name, dob, number, date):
        fieldnames = ["Score", "Email", "Name", "Date Of Birth", "Number Chosen", "Date Played"]
        try:
            with open("result.csv", "a", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0:  # Check if file is empty
                    writer.writeheader()
                writer.writerow({"Score": score, "Email": email, "Name": name, "Date Of Birth": dob, 
                                "Number Chosen": number, "Date Played": date})
        except IOError:
            print("Error in saving the results.")

    # method for modifying results of a existing account (login)
    @staticmethod
    def modify_existing_account(email, number, score, date):
         # Read the data from the file and store the modified rows
        modified_rows = []
        with open("result.csv", mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Email'] == email:
                    row['Number Chosen'] = number  # Modify the 'Number Chosen' field
                    row['Score'] = score  # Modify the 'Score field' 
                    row['Date Played'] = date  # Modify the 'Date Played' field
                modified_rows.append(row)

        # Write the modified data back to the file
        with open("result.csv", mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(modified_rows)

    # method for updating the email and password csv file
    @staticmethod
    def update_manage_file(email, password):
        fieldnames = ["Email", "Password"]
        try:
            with open("manage.csv", "a", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0:  # Check if file is empty
                    writer.writeheader()
                writer.writerow({"Email": email, "Password": password})
        except IOError:
            print("Error in saving the results.")

    # display the table, sorted by score (larger to smaller)
    @staticmethod 
    def display_leaderboard():
        try:
            with open("result.csv") as file:
                reader = csv.DictReader(file)
                table = sorted(reader, key=lambda row: int(row["Score"]), reverse=True)
                print(tabulate(table, headers="keys", tablefmt="grid", numalign="center"))
        except IOError:
            print("Error in reading the results.")

# DASHBOARD CLASS - MAIN FUNCTION
class Dashboard:
    def print_instructions(self):
        print("#"*61)
        print("## 1. Display Instructions                                 ##")
        print("## 2. Play                                                 ##")
        print("## 3. Display LeaderBoard                                  ##")
        print("## 4. Fast check number traits (only after logging in)     ##")
        print("## 5. Exit                                                 ##")
        print("#"*61)
        print()

    def matching_options(self):
        def __init__(self):
            self.user = None

        option = input("Choose an option: ")
        while option not in "12345" or option == "":
            option = input("Please choose a valid option: ")

        match option:

            case "1": # Display Instructions
                print("Welcome to the number test game!")
                print("The game is pretty simple, all you need to do is choose a number, and for each unique traits your number have, you get 1 point.")
                print()
                print("All of the number's unique traits are list here:")
                print("1. Prime number: A number that is divisible only by itself and 1. It must be greater than 1.")
                print("2. Perfect Number: A number that is equal to the sum of its proper divisors (excluding itself).")
                print("3. Sum of All Square Digits: A number whose sum of the squares of its digits equals the number itself.")
                print("4. Harshad Number: A number that is divisible by the sum of its digits.")
                print("5. Consecutive Rearrange: A number whose unique digits can be rearranged to form a sequence of consecutive numbers.")
                print("6. Square Number: A number that is the square of an integer.")
                print("7. Erimp Number: A prime number that remains prime when its digits are reversed.")
                print("8. Strong Number: A number that is divisible by a prime number and the square of that prime number.")
                print("9. Happy Number: A number which eventually reaches 1 when replaced by the sum of the square of each digit.")
                print()
                print("Note that if you are using the default test account, your score will not be display in the leaderboard.")
                ...
                print()
                input("Press any key to get back to the menu: ")

            case "2": # Play
                print("You have chosen the option to play")
                self.user = User()
                input("Press any key to get back to the menu: ")

            case "3": # Display LeaderBoard
                ResultManager.display_leaderboard()
                print()
                input("Press any key to get back to the menu: ")
            
            case "4": # Fast check after login in
                try:
                    number = self.user.get_number()
                except AttributeError:
                    print("You must register by an email first or login into an account by choosing option 2")
                else:
                    number_properties = NumberProperties(number)
                    number_properties.calculate_score()
                print()
                input("Press any key to get back to the menu: ")

            case "5": # Exit Game
                sys.exit("Thank you for playing !!!")

def main():

    print()
    print("Welcome to the Number Test Game, please see the instructions below: ")
    print()
    
    dashboard = Dashboard()
    while True:    
        dashboard.print_instructions()
        dashboard.matching_options()

if __name__ == "__main__":
    main()
