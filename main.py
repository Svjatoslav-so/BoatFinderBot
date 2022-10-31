import os
import time
from threading import Thread

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import parser.NewParser as newParse
from handlers.user_handlers import register_user_handlers
from models.DBManager import BoatDB
from parser import sites
from parser.BoatsParser import BoatsParser
from parser.FastBoatsParser import FastParser

TOKEN = os.environ['token']

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = BoatDB(os.environ['database'])


def update_db_old():
    parser = BoatsParser()
    f_parser = FastParser(10)
    boats = []
    t1 = Thread(target=parser.parse, args=(sites.BOATSHOP24, boats))
    t2 = Thread(target=f_parser.parse, args=(sites.BOAT24, boats))
    t3 = Thread(target=f_parser.parse, args=(sites.YACHTWORLD, boats))
    thread = [t1, t2, t3]
    # start_time = time.perf_counter()
    for t in thread:
        t.start()
    for t in thread:
        t.join()
    # end_time = time.perf_counter()
    # print("ALL_TIME: ", end_time - start_time)
    # print("ALL_BOATS_COUNT: ", len(boats))
    db.add_boats(boats)


def update_db():
    boats = []
    t1 = Thread(target=newParse.parse, args=(15, boats))
    thread = [t1]
    start_time = time.perf_counter()
    for t in thread:
        t.start()
    for t in thread:
        t.join()
    end_time = time.perf_counter()
    print("ALL_TIME: ", end_time - start_time)
    print("ALL_BOATS_COUNT: ", len(boats))
    db.add_boats(boats)


def register_all_handlers():
    register_user_handlers(dp)


if __name__ == '__main__':
    print("Hello!")
    db.create_db()
    # update_db()
    print("DATABASE updated successfully")
    register_all_handlers()

    executor.start_polling(dp, skip_updates=True)
