from flask import Flask, render_template, url_for
#from bot.config import dateBaseConfig
from os import getenv, path

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{dateBaseConfig["name"]}:{dateBaseConfig["dppass"]}@{dateBaseConfig["dbhost"]}/{dateBaseConfig["dbname"]}'
#app.config['SECRET_KEY'] = getenv('SECRET_KEY')
#app.config['BOT_TOKEN'] = getenv('BOT_TOKEN')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 299,
    'pool_pre_ping': True,
}

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)