# Import database, encryption and input modules
import bcrypt
import inquirer
import captcha_gen
import sys
import game
import os
from clear import main as clr
from termcolor import colored

os.environ["REPLIT_DB_URL"] = "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2ODc1NDM3OTksImlhdCI6MTY4NzQzMjE5OSwiZGF0YWJhc2VfaWQiOiI4NjE4OGUxYi0xZjE5LTQyNjUtODFiMC1hYTczY2M2YTdkYWMiLCJ1c2VyIjoiYmVja21hbm4xOSIsInNsdWciOiJDYXJkLUdhbWUifQ.CwPMibXsnx_4dUNl6FhOkdnRwl63gWrylbXt0KoUtqaE-niwRtj6Hlj9nSeazhATM6ChMRiGvJmAjCYo6IZBQA"

from replit import db

# Database debugging.

# VIEW CURRENT ENTRIES
print("Current database entries:", db.keys())

# DELETE SINGLE ENTRY
# del db['ENTER_ENTRY_HERE']

# DELETE ALL ENTRIES
# for key in db.keys():
#   del db[key]

# Check password function. Returns bool value.
def check_password(username, msg=None, check=None):
  # If no value is given to check against, it will prompt the user for a password with the given message and return a bool based on user response.
  if check is None: return bcrypt.checkpw(inquirer.password(message=msg).encode('utf-8'), db[username].encode('utf-8'))
  # If a value is given, it will check against the value and return a bool.
  elif msg is None: return bcrypt.checkpw(check.encode('utf-8'), db[username].encode('utf-8'))

# Password hashing function. Returns hashed password.
def hash_password(username, msg=None, check=None):
  # If there's no value to hash, it will prompt the user to input their password and return the hashed response.
  if check is None: return bcrypt.hashpw(inquirer.password(message=msg).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
  # If there's a value given, it will return the result of the hashed value.
  elif msg is None: return bcrypt.hashpw(check.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def login(player):
  # Player requests choice of login
  login_reg = inquirer.list_input("Player %d: Sign In or Register" % player, choices=['Sign In', 'Register', 'Exit'])
  
  # Sign In and Register selections
  if login_reg == 'Sign In':
    clr()
    # Request username
    username = inquirer.text(message="Enter your username")
    if player == 1: global p1_username; p1_username = username
    if player == 2 and username == p1_username: print("\nThis player has already signed in.", file=sys.stderr); clr(2); login(player)
    elif username not in db: print("\nUser not found.", file=sys.stderr); clr(2); login(player)
    # Check password against the hashed database, prompt captcha.
    while check_password(username, "Enter your password") & captcha_gen.main(): clr(); main_menu(player, username)
    else: print('\nIncorrect password.', file=sys.stderr); clr(2); login(player)
      
  elif login_reg == 'Register':
    clr()
    # Request username, check if it exists in db.
    username = inquirer.text(message="Enter your username")
    while username in db.keys(): print('\nThis user has already been registered.', file=sys.stderr); clr(2); username = inquirer.text(message="Enter your username")
    if player == 1: p1_username = username
    # Store the database entry if captcha is valid.
    temp_pass = hash_password(username, "Enter your password")
    if captcha_gen.main(): db[username] = temp_pass; print(colored('\nRegistration successful.', 'green')); clr(2); main_menu(player, username)

  elif login_reg == 'Exit': exit()

# Main menu function.
def main_menu(player, username):

  help = open('help.txt', 'r')
  
  # If player 1 is logged in, require player 2 to login.
  if player == 1: continue_option = 'Login Player 2'
  # If player 2 is logged in, enable the option to play the game.
  elif player == 2: continue_option = 'Play Game'

  main_options = inquirer.list_input("Welcome Player %d (%s)" % (player, username), choices=[continue_option, 'How to play', 'Edit Account', 'Logout'])
  
  if main_options == 'Login Player 2': clr(); login(player+1)
  elif main_options == "Play Game": clr(); game.main(p1_username, username)
  elif main_options == "How to play": clr(); print(help.read()); input(colored('Press Enter to continue...', 'yellow')); clr(); main_menu(player, username)
  elif main_options == 'Edit Account': clr(); edit_account(player, username)
  elif main_options == 'Logout' and player == 1: clr(); login(player)
  elif main_options == 'Logout' and player == 2: clr(); main_menu(player-1, p1_username)

# Edit account function provides a menu to change the user's username, password, delete their account or to return to main menu.
def edit_account(player, username):
  account_options = inquirer.list_input("Player %d (%s)- Edit Account" % (player, username), choices=['Change Username', 'Change Password', 'Delete Account', 'Return'])
  
  if account_options == 'Change Username': change_username(player, username)
  elif account_options == 'Change Password': change_password(player, username)
  elif account_options == 'Delete Account': delete_account(player, username)
  elif account_options == 'Return': clr(); main_menu(player, username)

# Change username function. Prevent the use of existing usernames. Update the username in the db.
def change_username(player, username):
  clr()
  new_username = inquirer.text(message="Enter your new username")
  while new_username in db.keys():
    if new_username == username: print("Cannot enter the existing username.", file=sys.stderr); clr(2)
    else: print('This username has already been taken.', file=sys.stderr)
    new_username = inquirer.text(message="Enter your new username")
  temp_pass = db[username]
  del db[username]
  db[new_username] = temp_pass
  print(colored("\nUsername updated. Returning to main menu...", 'green'))
  clr(2)
  main_menu(player, new_username)

# Change password function. Prevent using the previous password. Update the password if old password was valid.
def change_password(player, username):
  clr()
  if check_password(username, "Enter your old password"):
    temp_pass = inquirer.password(message="Enter your new password")
    while check_password(username, check=temp_pass):
      print("\nYou cannot use the same password", file=sys.stderr)
      clr(2)
      temp_pass = inquirer.password(message="Enter your new password")
    db[username] = hash_password(username, check=temp_pass)
    print(colored("\nPassword updated. Returning to main menu...", 'green'))
    clr(2)
    main_menu(player, username)
  else: print("\nPassword Incorrect. Returning...", file=sys.stderr); clr(2); edit_account(player, username)

# Delete account function. Confirm that the user wants to delete the account. If yes, prompt for user's password.
def delete_account(player, username):
  clr()
  verify_deletion = inquirer.confirm("Are you sure, player %d (%s)?" % (player, username), default=False)
  if not verify_deletion: print("Returning to main menu..."); clr(2); main_menu(player, username)
  elif verify_deletion & check_password(username, "Enter your password to confirm"): del db[username]; print(colored("\nAccount deleted. Returning to main menu.", 'yellow')); clr(2); login(player)
  else: print("\nPassword incorrect. Returning...", file=sys.stderr); clr(2); edit_account(player, username)


# Main function. Sets the value to player 1. Calls the login function.
def main(player=1):
  login(player)

if __name__ == "__main__":
  main()