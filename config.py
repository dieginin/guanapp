import os

from dotenv import load_dotenv

load_dotenv()

FB_CONFIG = {
    "apiKey": os.getenv("DB_KEY"),
    "authDomain": f"{os.getenv("PROJECTID")}.firebaseapp.com",
    "databaseURL": f"https://{os.getenv("PROJECTID")}-default-rtdb.firebaseio.com",
    "projectId": os.getenv("PROJECTID"),
    "storageBucket": f"{os.getenv("PROJECTID")}.appspot.com",
    "messagingSenderId": os.getenv("MSG_SNDR_ID"),
    "appId": os.getenv("APPID"),
    "measurementId": os.getenv("MSRMTID"),
}
