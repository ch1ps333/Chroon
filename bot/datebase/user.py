import aiomysql
from config import dateBaseConfig

async def get_con():
    try:
        con = await aiomysql.connect(
                                    host=dateBaseConfig['dbhost'], 
                                    port=dateBaseConfig['dbport'],
                                    user=dateBaseConfig['name'],
                                    password=dateBaseConfig['dppass'],
                                    db=dateBaseConfig['dbname'])
        return con
    except Exception as err:
        print(err)

async def reg_user(tg_id, username, invited_id = None, invited_username = None):
    con = await get_con()
    async with con.cursor() as cur:
        if invited_id == None:
            await cur.execute("INSERT INTO users (name, tg_id, balance, town_population, town_rank, town_last_money_take_time, town_balance_limit, lang, town_balance, last_tap_time, town_residential_places, town_entertainments, town_medicine, town_workplaces) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (username, tg_id, 0, 0, 1, 0, 100000, 'en', 0, 0, 0, 0, 0, 0))
            await con.commit()
        else:
            await cur.execute("INSERT INTO users (name, tg_id, invited_id, balance, town_population, town_rank, town_last_money_take_time, town_balance_limit, lang, town_balance, last_tap_time, town_residential_places, town_entertainments, town_medicine, town_workplaces) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (username, tg_id, invited_id, 0, 0, 1, 0, 100000, 'en', 0, 0, 0, 0, 0, 0))
            await cur.execute("UPDATE users SET balance = (balance + 100000) WHERE tg_id = %s;", (tg_id,))
            await cur.execute("UPDATE users SET balance = (balance + 100000) WHERE tg_id = %s;", (invited_id,))
            await cur.execute("INSERT INTO referals (referrer_tg_id, tg_id, name) VALUES (%s, %s, %s);", (invited_id, tg_id, username))
            await con.commit()       

async def isReg(tg_id):
    try:
        con = await get_con()
        async with con.cursor() as cur:
            await cur.execute("SELECT tg_id FROM users WHERE tg_id=%s;", (tg_id,))
            data = await cur.fetchone()
            if data is None:
                return False
            else:
                return True
    except Exception as err:
        print(err)
    finally:
        con.close()