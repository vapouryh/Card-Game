import os
import time


# Open credits file, print to screen when called.
def credits():
  creds = open("creds.txt", "r")
  print(creds.read())


def clear(seconds=None):
  # If seconds parameter if passed, delay clear for specified amount.
  if seconds:
    time.sleep(seconds)
  # Use the correct clear function depending on OS type.
  os.system("cls" if os.name == "nt" else "clear")
  # Call credits function.
  credits()


# Call clear function with seconds paremeter if passed.
def main(seconds=None):
  clear(seconds)


if __name__ == "__main__":
  main()
