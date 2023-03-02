#!/usr/bin/python
# -*- coding: utf-8 -*-
from vedis import Vedis
import configh

def get_current_hate(chat_id):
    with Vedis(configh.db_file) as db:
        try:
            return db[chat_id].decode()
        except KeyError:
            return configh.Hates.N_HATEOFF.value

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_hate(chat_id, value):
    with Vedis(configh.db_file) as db:
        try:
            db[chat_id] = value
            return True
        except:
            return False