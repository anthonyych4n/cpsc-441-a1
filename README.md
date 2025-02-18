# Palindrome Checker Application CPSC 441 Assignment 1

This is a client-server application to check for palindromes using two modes:

Basic Palindrome Check: Verifies if a string is a palindrome.

Advanced Palindrome Analysis: Checks if a string can be rearranged into a palindrome and calculates the minimum swaps needed.



# How to Run

1. Start the Server

Open a terminal and run:

python server.py

The server listens on localhost:12345.

Logs activity in server_activity.log.

2. Start the Client

Open another terminal and run:
````
python client.py
````
The client connects to the server and displays a menu:
````
1. Basic Palindrome Check

2. Advanced Palindrome Analysis

3. Quit
````
# Example Interaction

````
Options Menu:
1. Basic Palindrome Check
2. Advanced Palindrome Analysis
3. Quit
Choose an option (1/2/3): 1
Enter a string for palindrome check: radar
Response from Server:
Is palindrome: True
````
Notes

Both client and server use localhost:12345. Change to the server's IP for network use.

Check server_activity.log for detailed logs and errors.

Enjoy using the Palindrome Checker!
