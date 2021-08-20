from database.connect_db import cur, conn
import asyncio
from loader import bot
from time import sleep

while(1):
    conn.commit()
    cur.execute("select name, answer, modified_by from tabTelegramUsers where answer!=' ' and enable=0")
    data = cur.fetchall()
    if(data):
        for throw in data:
            await bot.send_message(int(throw[0]), "Сообщение от: " + throw[2] + "\n" + throw[1])
            teleid = int(throw[0])
            cur.execute("delete from tabTelegramUsers where name=%d" %teleid)
            conn.commit()
    cur.execute("select name, answer, modified_by from tabTelegramUsers where "
                "answer!=' ' and enable=1")
    data = cur.fetchall()
    if (data):
        for throw in data:
            await bot.send_message(int(throw[0]), "Сообщение от: " + throw[2] + "\n" + throw[1])
            teleid = int(throw[0])
            cur.execute("update tabTelegramUsers set answer=' ' where name=%d" %teleid)
            conn.commit()
    sleep(120)