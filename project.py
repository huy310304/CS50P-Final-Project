import validators
import csv
import re
import time
from math import sqrt
from tabulate import tabulate

def main():
    cont = True
    while cont != "0":
        score = 0
        email = get_info()
        dob = get_dob()
        num = get_number()
        print("Calculating result...")
        time.sleep(2.0)
        if prime(num) == True: score +=1; print("-Your number is a Prime number!")
        if perfect(num) == True: score +=1; print("-Your number is a Perfect number!")
        if sum_all_square_digits(num) == True: score +=1; print("-Sum of the square of all digits of your number equals itself!")
        if harsard(num) == True: score +=1; print("-Your number is divisibe by sum of all digits!")
        if consecutive_rearrange(num): score +=1; print("-Your number only contains consecutive digits!")
        if square(num) == True: score +=1; print("-Your number is a Square number!")
        if erimp(num) == True: score +=1; print("-Your number is a Prime number itself or itself reversed!")
        if strong(num) == True: score +=1; print("-Your number is almost a Strong number!")
        if happy(num) == True: score +=1; print("-Your number is a Happy number!")
        print(f"You get {score} point(s). Congratulations!")
        print()
        try:
            with open("result.csv") as file2:
                reader = csv.DictReader(file2)
                file2.close()
        except FileNotFoundError:
            with open("result.csv", "a") as file:
                writer = csv.DictWriter(file, fieldnames=["email","date of birth","number chosen","score"])
                writer.writeheader()
                writer.writerow({"email": email, "date of birth": dob, "number chosen": num, "score": score})
                file.close()
        else:
            with open("result.csv", "a") as file:
                writer = csv.DictWriter(file, fieldnames=["email","date of birth","number chosen","score"])
                writer.writerow({"email": email, "date of birth": dob, "number chosen": num, "score": score})
                file.close()
        cont = input("Enter any key to continue playing, enter 0 to stop: ")

    with open("result.csv") as file1:
        reader = csv.DictReader(file1)
        table, header = format(reader)
        print(tabulate(table, header, tablefmt="grid"))
        file1.close()

def get_info():
    email = input("Enter your email to register: ")
    while True:
        check = validators.email(email)
        if check == True: return email
        else: email = input("Please enter a valid email: ")

def get_number():
    while True:
        try:
            num = int(input("Please enter an positve integer number (2-3 digits recommended): "))
            if num <= 0: continue
        except ValueError:
            print("Please enter a valid number")
            pass
        else: return num

def get_dob():
    while True:
        dob = input("Type in your date of birth in yyyy-mm-dd format: ")
        if re.search(r"^\d{4}\-02\-([0][1-9]|[12][0-9])", dob): #format re, assume leap year
            y,m,_ = dob.split("-")
            check = leap(y)
            if m == "02" and check == False: #not leap year
                if re.search(r"^\d{4}\-02\-([0][1-9]|[1][0-9]|[2][0-8])$", dob):
                    return dob
            elif re.search(r"^\d{4}\-02\-([0][1-9]|[12][0-9])$", dob): #leap year
                return dob

        elif re.search(r"^\d{4}\-((([0][13578]|[1][02])\-([0][1-9]|[12][0-9]|[3][01]))|(([0][469]|11)\-([0][1-9]|[12][0-9]|30)))$", dob):
            return dob

def leap(y):
    if int(y)%4!=0: return False
    elif int(y)%100!=0: return True
    elif int(y)%400==0: return True
    else: return False

def format(r):
    table = []
    lst = []
    for dic1 in r:
        header = list(dic1.keys())
        lst.append(dic1)
    lst = sorted(lst, key = lambda d: d["score"], reverse=True)
    for dic in lst:
        table.append(list(dic.values()))
    return table, header

def prime(n): #test if a number is prime or not
    if n == 1: return False
    elif n == 2: return True
    for i in range(2,n//2+1):
        if n % i == 0: return False
    return True

def perfect(n): #sum of all divisors equal itself
    if n == 1: return True
    if sum(i for i in range(1,n//2+1) if n%i==0) == n:
        return True
    else: return False

def sum_all_square_digits(n): #sum of all square digits of num equal num
    if sum(int(i)**2 for i in str(n)) == n:
        return True
    else: return False

def harsard(n): #divisible by sum of all digits
    if n % sum(int(i) for i in str(n)) == 0:
        return True
    else: return False

def consecutive_rearrange(n): #if all the unique digits reaaranged can be consecutive e.g 335542 --> 2345 --> True
    n = sorted(list(set(str(n))))
    for idx in range(1,len(n)):
        if int(n[idx]) - int(n[idx-1]) != 1: return False
    return True

def square(n): #square root integer
    return int(sqrt(n)) == sqrt(n)

def erimp(n): #a prime number if reversed still a prime number
    if prime(n) == True:
        newnum = ""
        for i in str(n)[::-1]:
            newnum += i
        if prime(int(newnum)) == True:
            return True
    return False

def strong(n): #divisible by any prime number and the square of that prime number
    i = 2
    while True:
        if i**2 > n: return False
        elif prime(i) == True:
            if n%i==0:
                if n%(i**2)==0: return True
        i+=1

def happy(n): #sum square of all digits until reaches 1
    lst = []
    while n !=1:
        total = 0
        for i in str(n):
            total += int(i)**2
        n = total
        if n in lst: return False
        else: lst.append(n)
    return True

if __name__ == "__main__":
    main()
