import json
import os
import hashlib
import argparse
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

parser = argparse.ArgumentParser(description="Felhasználó hozzáadása a credentials.json fájlhoz")
parser.add_argument("username", help="A felhasználó neve")
parser.add_argument("password", help="A felhasználó jelszava")
args = parser.parse_args()

username = args.username
password = args.password

basedir = os.path.abspath(os.path.dirname(__file__))
credentials_file = os.path.join(basedir, "credentials.json")

password_hash = hashlib.sha256((password + SECRET_KEY).encode()).hexdigest()

try:
    with open(credentials_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = {"users": []}

data["users"].append({
    "username": username,
    "password_hash": password_hash
})

with open(credentials_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Felhasználó '{username}' sikeresen hozzáadva!")
