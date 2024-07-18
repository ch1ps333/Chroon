import os

from dotenv import load_dotenv
load_dotenv()

current_directory = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_directory, '..'))
datebasePath = os.path.join(project_root, 'db', 'users.db')
siteDatebasePath = os.path.join(project_root, 'db', 'site.db')
logRequests = os.path.join(project_root, 'www', 'log.txt')

dateBaseConfig = {
    'dbhost': 'PashaRiabyi.mysql.pythonanywhere-services.com',
    'name': 'PashaRiabyi',
    'dbport': 3306,
    'dppass': 'Iftkn307',
    'dbname': 'PashaRiabyi$site',
}


class Settings():
    bot_token = os.getenv('BOT_TOKEN')
    

config = Settings()