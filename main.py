import os
import sys
import psutil
from flask import Flask
from routes.status import status_bp
from routes.print import print_bp
from routes.api_ticket import api_ticket_bp

app = Flask(__name__)
PORT = 8000

def is_running():
    """
    Check if the program is already running.

    :return: True if the program is running, False otherwise.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'main.py' and proc.info['pid'] != os.getpid():
            return True
    return False

app.register_blueprint(status_bp)
app.register_blueprint(print_bp)
app.register_blueprint(api_ticket_bp)

def main():
    if is_running():
        print("The program is already running.")
        sys.exit(1)

    app.run(host='0.0.0.0', port=PORT)

if __name__ == "__main__":
    main()
