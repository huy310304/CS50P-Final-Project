# Organize code into OOP format, add small features

import validators
import csv
import re
import time
from datetime import date
from math import sqrt
from tabulate import tabulate

# User information class
class User:
    def __init__(self):
        self.name = self.get_name()
        self.email = self.get_email()
        self.dob = self.get_dob()
        self.number = self.get_number()
        self.date = date.today()

    # get user's name
    def get_name(self):
        return input("Enter your name to play: ")

    # get user's email
    def get_email(self):
        while True:
            email = input("Enter your email to register: ")
            if validators.email(email):
                return email
            print("Please enter a valid email.")

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

        print("Calculating result ", end="")

        for _ in range(3):
            print(".", end="")
            time.sleep(0.5)
        
        print()

        for description, func in properties.items():
            if func(self.number):
                score += 1
                print(f"- Your number {description}!")
        
        if score == 0:
            print("Your number is so unique that I have not updated its trait yet!")

        return score


    # Additional number checking function

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
    
        # ... Implement other methods like sum_all_square_digits, harsard, etc.


# Result Manager Class
class ResultManager:
    # write results into result.csv file
    @staticmethod
    def save_results(user, score):
        fieldnames = ["Score", "Name", "Email", "Date Of Birth", "Number Chosen", "Date Played"]
        try:
            with open("result.csv", "a", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0:  # Check if file is empty
                    writer.writeheader()
                writer.writerow({"Score": score, "Name": user.name,"Email": user.email, "Date Of Birth": user.dob, 
                                 "Number Chosen": user.number, "Date Played": user.date})
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


def main():
    user = User()
    number_properties = NumberProperties(user.number)
    score = number_properties.calculate_score()

    ResultManager.save_results(user, score)
    if input("Show leaderboard? (y/n): ").lower() == 'y':
        ResultManager.display_leaderboard()

if __name__ == "__main__":
    main()
