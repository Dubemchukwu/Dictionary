from pynput import keyboard
import subprocess
import time
import psutil

def on_press(key):
    global ctrl_pressed, process
    try:

        # Detect 'S' key while Ctrl is pressed
        if hasattr(key, 'char') and key.char == '\x13':
            print("Ctrl+S detected.")

            if process and process.poll() is None:  # Check if the process is still running
                process_ = psutil.Process(process.pid)
                for child in process_.children(recursive=True):  # Get all child processes
                    child.terminate()
                process_.terminate()
                process_.wait(timeout=5)
                process.terminate()
                time.sleep(1)
                process.kill()
                print("Terminating the previous process...")

            print("Starting a new process...")
            # Start the new process (flet run)
            process = subprocess.Popen(["flet", "run"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"New process started with PID: {process.pid}")

    except AttributeError:
        pass

def on_release(key):
    global ctrl_pressed
    # Reset the Ctrl flag when Ctrl key is released
    if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        ctrl_pressed = False

    # Stop the listener on 'Esc' key
    if key == keyboard.Key.esc:
        print("Exiting...")
        if process and process.poll() is None:  # Ensure any running process is terminated
            process.terminate()
        return False

# Initialize the Ctrl flag and the process variable
ctrl_pressed = False
process = None  # This will hold the reference to the currently running process

# Start the listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
