import socket
import time

# Client Configuration
HOST = 'localhost'
PORT = 12345
CONN_TIMEOUT = 5
MAX_RETRIES = 3
SHIFT = 11  # Caesar Cipher Shift Value

# Caesar Cipher Encryption
def encrypt_message(message):
    encrypted = []
    for char in message:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            encrypted.append(chr((ord(char) - offset + SHIFT) % 26 + offset))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

# Caesar Cipher Decryption
def decrypt_message(message):
    decrypted = []
    for char in message:
        if char.isalpha():
            offset = 65 if char.isupper() else 97
            decrypted.append(chr((ord(char) - offset - SHIFT) % 26 + offset))
        else:
            decrypted.append(char)
    return ''.join(decrypted)


def initiate_client():
    attempt_count = 0

    while attempt_count < MAX_RETRIES:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.settimeout(CONN_TIMEOUT)
                client.connect((HOST, PORT))
                print("Successfully connected to the server.")
                
                while True:
                    user_choice = display_menu()

                    if user_choice == '1':
                        user_input = input("Enter a string for palindrome check: ")
                        request_message = f"simple|{user_input}"
                        transmit_message(client, request_message)
                            
                    elif user_choice == '2':
                        user_input = input("Enter a string for complex palindrome check: ")
                        request_message = f"complex|{user_input}"
                        transmit_message(client, request_message)

                    elif user_choice == '3':
                        print("Closing the client application...")
                        break
                    
                    else:
                        print("Invalid option. Please select 1, 2, or 3.")
            break
        except socket.timeout:
            attempt_count += 1
            print(f"Connection timed out. Retrying {attempt_count}/{MAX_RETRIES}...")
            time.sleep(2)
        except ConnectionRefusedError:
            attempt_count += 1
            print(f"Connection refused. Retrying {attempt_count}/{MAX_RETRIES}...")
            time.sleep(2)
        except Exception as error:
            attempt_count += 1
            print(f"Unexpected error: {error}. Retrying {attempt_count}/{MAX_RETRIES}...")
            time.sleep(2)

    if attempt_count == MAX_RETRIES:
        print("Unable to connect to the server after several attempts. Exiting.")

def display_menu():
    print("\nOptions Menu:")
    print("1. Basic Palindrome Check")
    print("2. Advanced Palindrome Analysis")
    print("3. Quit")
    return input("Choose an option (1/2/3): ").strip()

def transmit_message(client, message):
    try:
        encrypted_message = encrypt_message(message)  # Encrypt before sending
        client.send(encrypted_message.encode())
        server_reply = client.recv(1024).decode()
        decrypted_reply = decrypt_message(server_reply)  # Decrypt the server response
        print(f"Response from Server:\n{decrypted_reply}")
    except socket.timeout:
        print("No response received from the server (timeout).")

if __name__ == "__main__":
    initiate_client()
