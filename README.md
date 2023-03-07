# NUMBER TESTS GAME
#### Video Demo:  https://www.youtube.com/watch?v=ezhuq74t8P8
#### Description:
File Description:
-In project.py is the code for my project which tests the uiqueness of users'number and calculate their total score
-In test_project.py is the my number test functions
-In result.csv will be the storage of user's information and their total score
-In requirement.txt is the pip-installable library that I used.

Running code:
-The game is about testing a number to see if it has unique traits(prime, square, perfect, ...) or not.
-Users will be asked to type in their valid email, date of birth in yyyy-mm-dd format, and a positive integer number. All of the inputs will be tested.
-For each unique trait the number has, the user receives 1 point. Their total score will then be recorded.
-All of the results(email, date of birth, number chosen, score) will be stored in a file called result.csv by using csv.Dictwriter
-After finishing typing in the number, each unique trait that the number has will be printed out with the total score.
-The player will be asked if he/she wants to continue or not. Entering any key except 0 will trigger the game to continue and ask for user's inputs again.
-Whenever the game is ended(only by entering 0 at the "continue or stop" prompt), there will be a table printed out on the command prompt including all of the previous attempts sorted by scores from highest to lowest by using tabulate module.
-No one can get a perfect score since one number cannot has all the traits.

Testing Code:
-There will be a test_project.py file that contains tests for prime, perfect, square, and consecutively arranged numbers

pip installable library used:
-tabulate: to print the table at the end of the code
-validators: to fully validate the user's email
