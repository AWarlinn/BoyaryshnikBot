#!/usr/bin/python
# -*- coding: utf-8 -*-
from vedis import Vedis
import config

def get_current_state(chat_id):
    with Vedis(config.db_file) as db:
        try:
            return db[chat_id].decode()
        except KeyError:
            return config.States.V_RAGEOFF.value

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(chat_id, value):
    with Vedis(config.db_file) as db:
        try:
            db[chat_id] = value
            return True
        except:
            return False