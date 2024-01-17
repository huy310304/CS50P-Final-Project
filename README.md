# NUMBER TESTS GAME

# TODO: Update this

#### Description:
File Description:  
- In project.py is the code for my project which tests the uiqueness of users'number and calculate their total score.  
- In test_project.py is the my number test functions.  
- In result.csv will be the storage of user's information and their total score.  
- In requirement.txt is the pip-installable library that I used.  

Running code:  
- The game is about testing a number to see if it has unique traits(prime, square, perfect, ...) or not.  
- Users will be asked to type in their valid email, date of birth in yyyy-mm-dd format, and a positive integer number. All of the inputs will be tested.  
- For each unique trait the number has, the user receives 1 point. Their total score will then be recorded.  
- All of the results(email, date of birth, number chosen, score) will be stored in a file called result.csv by using csv.Dictwriter.    
- After finishing typing in the number, each unique trait that the number has will be printed out with the total score.  
- The player will be asked if he/she wants to continue or not. Entering any key except 0 will trigger the game to continue and ask for user's inputs again.  
- Whenever the game is ended(only by entering 0 at the "continue or stop" prompt), there will be a table printed out on the command prompt including all of the previous attempts sorted by scores from highest to lowest by using tabulate module.  
- No one can get a perfect score since one number cannot has all the traits.  

Testing Code:  
- There will be a test_project.py file that contains tests for prime, perfect, square, and consecutively arranged numbers

pip installable library used:  
- tabulate: to print the table at the end of the code  
- validators: to fully validate the user's email

# Number Test Game

## Project Description
The Number Test Game is an engaging Python-based game that allows users to discover fascinating properties of numbers while competing on a leaderboard. It integrates mathematical exploration with gaming fun, perfect for users of all ages and backgrounds. The game features user authentication, interactive gameplay, a dynamic scoring system, and a leaderboard. It aims to make learning about numbers engaging and competitive.

## Table of Contents
1. Installation
2. Usage
3. Features
4. Demo

## Installation
**Prerequisites:** Python 3.x

**Steps:**
1. Clone the repository: `git clone [Repository-URL]`
2. Navigate to the directory: `cd number_test_game`
3. Run the game: `python number_test_game.py`

## Usage
After starting the game, users can:
- Register or log in to an account.
- Choose numbers and receive feedback on their properties.
- View the leaderboard.
- Explore number properties in a quick check mode.

## Features
- **User Authentication:** Secure registration and login.
- **Interactive Gameplay:** Users choose numbers and learn about their properties.
- **Scoring System:** Points awarded based on number uniqueness.
- **Leaderboard:** View rankings and compete with others.
- **Data Management:** Efficient handling of user data using CSV files.
- **User Experience:** Personalized gameplay with profile management.

## Demo
A demo video or screenshots will be added here to guide users through:
- The registration and login process.
- Gameplay experience.
- Leaderboard interaction.
- [Demo Video/Screenshots Link] 
