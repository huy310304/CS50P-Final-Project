import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from tkinter import *
import validators
import csv
from math import sqrt

# Global variable to keep track of all registered emails
emailsAndPasswords = {}

try:
    with open("manage.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            emailsAndPasswords[row["Email"]] = row["Password"]
except IOError:
    pass


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Test Game")
        self.geometry("450x350")
        self.configure(bg='#334257')

        # Initialize the UI
        self.initialize_ui()

    def initialize_ui(self):
        # Fonts
        title_font = ("Times New Roman", 20, "bold")
        label_font = ("Arial", 12)
        entry_font = ("Arial", 10)
        button_font = ("Arial", 12, "bold")

        # Title
        tk.Label(self, text="Welcome to Number Test Game", bg='#334257', fg='#FF4C29', font=title_font).pack(pady=(10, 20))

        # Login/Register selection
        self.mode = tk.StringVar()
        self.mode.set("login")  # Set default mode to login

        login_frame = tk.Frame(self, bg='#334257')
        login_frame.pack(fill='x', padx=50)

        tk.Radiobutton(login_frame, text="Login", variable=self.mode, value="login", bg='#334257', fg='white', font=label_font).pack(side='left')
        tk.Radiobutton(login_frame, text="Register", variable=self.mode, value="register", bg='#334257', fg='white', font=label_font).pack(side='right')

        # Email field
        tk.Label(self, text="Email:", bg='#334257', fg='white', font=label_font).pack(anchor='w', padx=50, pady=(20, 0))
        self.email_entry = tk.Entry(self, font=entry_font)
        self.email_entry.pack(fill='x', padx=50, pady=(0, 10))

        # Password field
        tk.Label(self, text="Password:", bg='#334257', fg='white', font=label_font).pack(anchor='w', padx=50, pady=(10, 0))
        self.password_entry = tk.Entry(self, show="*", font=entry_font)
        self.password_entry.pack(fill='x', padx=50, pady=(0, 20))
        
        # Frame
        button_frame = tk.Frame(self, bg='#334257')
        button_frame.pack(pady=20)

        # Submit button
        submit_button = tk.Button(button_frame, text="Submit", bg='#FF4C29', fg='white', font=button_font, command=self.submit)
        submit_button.pack(side='left', padx=10)

        # Exit button
        exit_button = tk.Button(button_frame, text="Exit", bg='#FF4C29', fg='white', font=button_font, command=self.destroy)
        exit_button.pack(side='right', padx=10)

    # Click Submit Function
    def submit(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not validators.email(email):
            messagebox.showerror("Error", "Invalid email format")
            return

        if self.mode.get() == "login":
            if self.validate_login(email, password):
                messagebox.showinfo("Success", "Logged in successfully")
                self.start_game()
            else:
                messagebox.showerror("Error", "Invalid login credentials")
        elif self.mode.get() == "register":
            self.register_new_user(email, password)
    
    def validate_login(self, email, password):
        return email in emailsAndPasswords and emailsAndPasswords[email] == password

    def register_new_user(self, email, password):
        fieldnames = ["Email", "Password"]

        if email in emailsAndPasswords:
            messagebox.showerror("Error", "Your email has been registered before, please enter a new email")
        else: 
            try:
                with open("manage.csv", "a", newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    if file.tell() == 0:  # Check if file is empty
                        writer.writeheader()
                    writer.writerow({"Email": email, "Password": password})
            except IOError:
                    print("Error in saving the results.")
            messagebox.showinfo("Success", "Registered successfully")
            self.start_game()

    def start_game(self):
        # Hide the main login/register window
        self.withdraw()

        # Create a new top-level window for the game
        self.game_window = tk.Toplevel(self)
        self.game_window.title("Game")
        self.game_window.geometry("500x400")  # Updated size
        self.game_window.configure(bg='#101820')  # Darker background

        # Custom fonts for the game window
        game_label_font = tkfont.Font(family="Helvetica", size=14)
        game_entry_font = tkfont.Font(family="Helvetica", size=12)
        game_button_font = tkfont.Font(family="Helvetica", size=14, weight="bold")

        # Font
        tk.Label(self.game_window, text="Enter a number:", bg='#101820', fg='#F2AA4C', font=game_label_font).pack(pady=(20, 10))

        # Input number field
        self.number_entry = tk.Entry(self.game_window, font=game_entry_font, bg="#F2AA4C", fg="black")
        self.number_entry.pack(pady=(0, 20))

        # Submit Button
        submit_button = tk.Button(self.game_window, text="Submit", bg='#F2AA4C', fg='black', font=game_button_font, command=self.evaluate_number)
        submit_button.pack(pady=(0, 20))

        # Exit button
        exit_button = tk.Button(self.game_window, text="Exit", bg='#F2AA4C', fg='black', font=game_button_font, command=self.destroy)
        exit_button.pack(pady=(0, 20))

        # Display the results
        self.result_label = tk.Label(self.game_window, text="", bg='#101820', fg='white', font=game_label_font)
        self.result_label.pack(pady=(20, 0))

    # Get the score and text, display them
    def evaluate_number(self):
        try:
            number = int(self.number_entry.get())
            score, trait_text = self.calculate_score(number)
            self.result_label.config(text=f"Score: {score}, " + trait_text)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.", parent=self.game_window)
    
    # Function that return the score and text
    def calculate_score(self, number):
        trait_text = "Your number"
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
        }

        for text, func in properties.items():
            if func(number):
                score += 1
                trait_text += "\n" + text
        return score, trait_text

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

# Can add other trait checking function here in the future ...

# Run the tkinter app
def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()