import subprocess
import time
from os import getenv, path
from sys import path as sys_path

current_directory = path.dirname(__file__)
project_root = path.abspath(path.join(current_directory, '..'))
sys_path.insert(1, project_root)

from flask import Flask
from views import bp
from bot.config import dateBaseConfig
from create_db import db
import db_models
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def start_redis_server():
    # Путь к конфигурационному файлу Redis
    redis_conf_path = path.abspath('redis.conf')

    redis_conf = f"""
    bind 127.0.0.1
    port 6380
    protected-mode yes
    requirepass {getenv('REDIS_PASS')}
    """

    with open(redis_conf_path, 'w') as conf_file:
        conf_file.write(redis_conf)

    redis_process = subprocess.Popen(['redis-server', redis_conf_path])
    time.sleep(2)  # Даем время серверу запуститься
    return redis_process

redis_process = start_redis_server()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{dateBaseConfig["name"]}:{dateBaseConfig["dppass"]}@{dateBaseConfig["dbhost"]}/{dateBaseConfig["dbname"]}'
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['BOT_TOKEN'] = getenv('BOT_TOKEN')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 299,
    'pool_pre_ping': True,
}

def setup_limiter(app):
    redis_password = getenv('REDIS_PASS')
    redis_url = getenv('REDIS_URL', f'redis://default:{redis_password}@localhost:6380/0')

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        storage_uri=redis_url,
        default_limits=["30 per minute"]
    )
    return limiter


limiter = setup_limiter(app)
bp.limiter = limiter

app.register_blueprint(bp)

db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        redis_process.terminate()
        redis_process.wait()
