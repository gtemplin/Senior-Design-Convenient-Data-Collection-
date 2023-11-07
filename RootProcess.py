import os
import multiprocessing
import subprocess
import time
import contextlib

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

    with contextlib.suppress(KeyboardInterrupt):
        pool = multiprocessing.Pool(processes=3)
        pool.map(execute_script, processes)
        pool.close()
        pool.join()
