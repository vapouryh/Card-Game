# Captcha authentication.
# Checks the authenticity of a user on sign in or registration.
# Import modules for ASCII Text, Random Number Generation and system exceptions

import pyfiglet
import random
import sys
from clear import main as clr


# Main function
# Generates a random number which is then converted to ASCII art
# The input is then checked and returns boolean value.

def main(attempts=1):
  check_number = random.randint(0, 9999)
  check_string = f"{check_number:>04}"
  print(pyfiglet.Figlet().renderText(check_string))

  response = input("Please enter the number shown above to proceed: ")
  if response != check_string:
    if attempts < 3:
      print("Attempt %d out of 3" % attempts, file=sys.stderr)
      print("Failed verification check! Please try again.", file=sys.stderr)
      attempts += 1
      clr(3)
      main(attempts)
    else:
      print("Maximum number of attempts succeeded.", file=sys.stderr)
      exit()
  return True


if __name__ == "__main__":
  main()
