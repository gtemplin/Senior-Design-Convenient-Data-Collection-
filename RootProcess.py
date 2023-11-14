import os
import multiprocessing  # allows for multiple CPU cores to be used to run different programs in parallel 
import subprocess  # allows for other programs/scripts to be called from this program
import time
import contextlib


# As a whole, this program seems to be a wrapper for the total functionality
# It will be important to ensure all of our processes are stored in a specific Curpath folder 

Curpath='C:/Users/liyae/IdeaProjects/IAC_HASS_EdgePC/IAC_SENSOR_PROG_V2'

def execute_script(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e}")

if __name__ == '__main__':
    try:
        os.remove(os.path.join(Curpath, ".oauth2_token"))
    except Exception:
        pass

    try:
        os.remove(os.path.join(Curpath, "CommunicationFlag.txt"))
    except Exception:
        pass

    processes = [
        os.path.join(Curpath, 'Sensing.py'),
        os.path.join(Curpath, 'ActuatorControl.py'),
        os.path.join(Curpath, 'DatabaseWrite.py')
    ]

 # this sets up the parallel processing
    with contextlib.suppress(KeyboardInterrupt):
        pool = multiprocessing.Pool(processes=3)
        pool.map(execute_script, processes)
        pool.close()
        pool.join()
