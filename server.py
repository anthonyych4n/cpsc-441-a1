import socket
import threading
import logging
from collections import Counter

# Configure logging to write to a file with detailed format
logging.basicConfig(filename='server_activity.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Server Configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
CONNECTION_TIMEOUT = 40

def client_handler(conn_socket, addr):
    """ Manage communication with a connected client. """
    logging.info(f"New connection established from {addr}")
    
    try:
        while True:
            # Receive message from client
            message = conn_socket.recv(1024).decode()
            if not message:
                logging.info(f"Client at {addr} disconnected.")
                break

            logging.info(f"Message received: {message}")
            
            # Handle the request and craft a response
            reply = process_message(message)
            conn_socket.send(reply.encode())
            logging.info(f"Response sent: {reply}")
    except Exception as error:
        logging.error(f"Error with client {addr}: {error}")
    finally:
        conn_socket.close()
        logging.info(f"Connection closed for {addr}")

def process_message(message):
    """ Interpret and respond to the client's message. """
    try:
        command, text = message.split('|')
        clean_text = ''.join(char for char in text if char.isalnum()).lower()
        
        if command == 'simple':
            is_pal = check_palindrome(clean_text)
            return f"Is palindrome: {is_pal}"
        elif command == 'complex':
            possible, score = evaluate_palindrome_possibility(clean_text)
            return f"Can form palindrome: {possible}\nComplexity score: {score}"
        else:
            return "Error: Invalid command type."
    except Exception as ex:
        return f"Processing error: {str(ex)}"

def check_palindrome(text):
    """ Verify if the input text is a palindrome. """
    return text == text[::-1]

def evaluate_palindrome_possibility(text):
    """ Determine if the text can be rearranged into a palindrome. """
    frequency = Counter(text)
    odd_count = sum(1 for count in frequency.values() if count % 2 != 0)

    is_possible = odd_count <= 1
    if not is_possible:
        logging.info(f"Cannot rearrange '{text}' into a palindrome.")
        return False, -1 

    characters = list(text)
    left, right = 0, len(characters) - 1
    swap_count = 0  

    logging.info(f"Processing string: {''.join(characters)}")

    while left < right:
        if characters[left] == characters[right]:
            left += 1
            right -= 1
        else:
            match_pos = right
            while match_pos > left and characters[match_pos] != characters[left]:
                match_pos -= 1

            if match_pos == left:  
                middle = len(characters) // 2
                characters[left], characters[middle] = characters[middle], characters[left]
                swap_count += 1
                left += 1
                right -= 1
            else:
                characters[match_pos], characters[right] = characters[right], characters[match_pos]
                swap_count += 1
                left += 1
                right -= 1

        if characters == characters[::-1]:
            logging.info(f"Palindrome achieved: {''.join(characters)}")
            break

    logging.info(f"Final palindrome: {''.join(characters)}, Swaps: {swap_count}")
    return is_possible, swap_count

def initialize_server():
    """ Initialize the server and handle incoming connections. """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((SERVER_HOST, SERVER_PORT))
        server.listen(5)
        server.settimeout(CONNECTION_TIMEOUT)  
        logging.info(f"Server running on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            try:
                client_conn, client_addr = server.accept()
                threading.Thread(target=client_handler, args=(client_conn, client_addr)).start()
            except socket.timeout:
                logging.warning("Server timeout: No new connections.")
                break

        logging.info("Shutting down the server.")

if __name__ == '__main__':
    initialize_server()
