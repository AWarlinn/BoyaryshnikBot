#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
import time
import datetime
import random
import config
import dbworker
import configh
import dbinvites
import rusyllab

bot = telebot.TeleBot(config.token)

restricted_messages = ["я не пидор, а натурал", "я веган", "я натурал", "забань меня", "я не гей", "я не пью"]

regex_msg = ("^.*((я не пид.р.*(а|я) натурал)|(я веган)|(я натурал)|(забань меня)|(я не гей)|(я не пью)).*$")

def huevo(sent):
    sx = rusyllab.split_words(''.join(filter(str.isalnum, sent)).lower().split())
    
    try:
        if sx[0][-1] in ('а', 'я'):
            sx[0] = 'хуя'
        elif sx[0][-1] in ('ё', 'о'):
            sx[0] = 'хуё'
        elif sx[0][-1] in ('е', 'э'):
            sx[0] = 'хуе'
        elif sx[0][-1] in ('ю', 'у'):
            sx[0] = 'хую'
        elif sx[0][-1] in ('и', 'ы'):
            sx[0] = 'хуи'
        else:
            last_word = sx[0][-1]
            if sx[0][-2] in ('а', 'я'):
                sx[0] = 'хуя' + last_word
            elif sx[0][-2] in ('ё', 'о'):
                sx[0] = 'хуё' + last_word
            elif sx[0][-2] in ('е', 'э'):
                sx[0] = 'хуе' + last_word
            elif sx[0][-2] in ('ю', 'у'):
                sx[0] = 'хую' + last_word
            elif sx[0][-2] in ('и', 'ы'):
                sx[0] = 'хуи' + last_word
            else:
                sx[0] = 'хуе' + last_word
        word = ''.join(sx).capitalize() + '!'
        return word
    
    except:
        pass

try:        

    def convert(n):
        return str(datetime.timedelta(seconds = n))
    
    @bot.message_handler(commands=['start'])
    def send_text(message):
        bot.send_message(message.chat.id, 'Moi, perkele!')
    
    @bot.message_handler(commands=['voicerageon'])
    def send_text(message):
        dbworker.set_state(message.chat.id, config.States.V_RAGEON.value)
        bot.send_message(message.chat.id, 'Voicerage on')
    
    @bot.message_handler(commands=['voicerageoff'])
    def send_text(message):
        dbworker.set_state(message.chat.id, config.States.V_RAGEOFF.value)
        bot.send_message(message.chat.id, 'Voicerage off')
    
    @bot.message_handler(commands=['checkstate'])
    def send_text(message):
        if dbworker.get_current_state(message.chat.id) == config.States.V_RAGEOFF.value and dbinvites.get_current_hate(message.chat.id) == configh.Hates.N_HATEOFF.value:
            bot.send_message(message.chat.id, 'Voicerage Off\nNewbie hate disabled')
        if dbworker.get_current_state(message.chat.id) == config.States.V_RAGEON.value and dbinvites.get_current_hate(message.chat.id) == configh.Hates.N_HATEOFF.value:
            bot.send_message(message.chat.id, 'Voicerage On\nNewbie hate disabled')
        if dbworker.get_current_state(message.chat.id) == config.States.V_RAGEOFF.value and dbinvites.get_current_hate(message.chat.id) == configh.Hates.N_HATEON.value:
            bot.send_message(message.chat.id, 'Voicerage Off\nNewbie hate enabled')
        if dbworker.get_current_state(message.chat.id) == config.States.V_RAGEON.value and dbinvites.get_current_hate(message.chat.id) == configh.Hates.N_HATEON.value:
            bot.send_message(message.chat.id, 'Voicerage On\nNewbie hate enabled')
    
    @bot.message_handler(content_types=['voice'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.V_RAGEON.value)
    def send_text(message):
        voicerate = int(random.randrange(1,8, 1))
        if voicerate == 1:
            bot.send_photo(message.chat.id, photo=open('voiceforpidors.jpg', 'rb'), reply_to_message_id=message.message_id)
        if voicerate == 2:
            bot.send_photo(message.chat.id, photo=open('Bethoven.jpg', 'rb'), reply_to_message_id=message.message_id)
        if voicerate == 3:
            bot.send_photo(message.chat.id, photo=open('Druzhko.jpg', 'rb'), reply_to_message_id=message.message_id)
        if voicerate == 4:
            bot.send_photo(message.chat.id, photo=open('voice4.jpg', 'rb'), reply_to_message_id=message.message_id)
        if voicerate == 5:
            bot.send_photo(message.chat.id, photo=open('voice5.jpg', 'rb'), reply_to_message_id=message.message_id)
        if voicerate == 6:
            bot.send_photo(message.chat.id, photo=open('voice6.jpg', 'rb'), reply_to_message_id=message.message_id)
        if voicerate == 7:
            bot.send_photo(message.chat.id, photo=open('voice7.jpg', 'rb'), reply_to_message_id=message.message_id)
    
    @bot.message_handler(content_types=['voice'], func=lambda message: message.from_user.username == 'Warlinn')
    def send_text(message):
        bot.send_message(message.chat.id, message)
        print(message)
    
    @bot.message_handler(commands=['newhateon'])
    def send_text(message):
        dbinvites.set_hate(message.chat.id, configh.Hates.N_HATEON.value)
        bot.send_message(message.chat.id, 'Newbie hate enabled')
    
    @bot.message_handler(commands=['newhateoff'])
    def send_text(message):
        dbinvites.set_hate(message.chat.id, configh.Hates.N_HATEOFF.value)
        bot.send_message(message.chat.id, 'Newbie hate disabled')
    
    @bot.message_handler(content_types=['new_chat_members'], func=lambda message: dbinvites.get_current_hate(message.chat.id) == configh.Hates.N_HATEON.value)
    def send_text(message):
        bot.send_video(message.chat.id, open('newone.mp4', 'rb'))
        bot.restrict_chat_member(message.chat.id,message.new_chat_member.id,until_date=time.time()+120)
        bot.send_message(message.chat.id, '@' + str(message.new_chat_member.first_name) + ' выигрывает свой первый бан на 2 минуты')
    
    @bot.message_handler(commands=['print'])
    def send_text(message):
        bot.send_message(message.chat.id, message)
        print(message)
    
    @bot.message_handler(commands=['regex'])
    def send_text(message):
        bot.send_message(message.chat.id, regex_msg)
    
    @bot.message_handler(commands=['help'])
    def send_text(message):
        bot.send_message(message.chat.id, 'Бот для супергрупп, нужны права админа\nВ некоторых случаях принимает участие в разговоре\nМожет забанить вас на 10 минут за некоторые фразы\nВы можете сделать себе сеппуку или самозабаниться командой /banme (есть шанс пермача)\nВведите /testban, чтобы увидеть, как это работает\nНовый функционал в разработке')
    
    @bot.message_handler(commands=['banme'])
    def handle_message(message):
        rate = (random.weibullvariate(1,0.5))
        if rate <= 1:
            bantime = int(random.randrange(60,300, 1))
        elif rate > 1 and rate <= 5:
            bantime = int(random.randrange(300,600, 1))
        elif rate > 5 and rate <= 7:
            bantime = int(random.randrange(600, 3600, 1))
        elif rate > 7 and rate <= 9:
            bantime = int(random.randrange(3600, 86400, 1))
        elif rate > 20 and rate <= 60:
            bantime = int(random.randrange(86400, 259200, 1))
        elif rate > 69 and rate <= 71:
            bantime = int(999999999)
        else:
            bantime = int(666)
        if bantime != int(666):
            bot.restrict_chat_member(message.chat.id,message.from_user.id,until_date=time.time()+bantime)
            bot.reply_to(message, "Поздравляю! Ты выиграл бан на " + convert(bantime))
        elif bantime == int(999999999):
            bot.restrict_chat_member(message.chat.id,message.from_user.id)
            bot.reply_to(message, "И ПЕРЕД НАМИ ПОБЕДИТЕЛЬ! Ты выиграл ПЕРМАЧ!")
        else:
            bot.restrict_chat_member(message.chat.id,message.from_user.id,until_date=time.time()+bantime)
            bot.reply_to(message, "Тебе чертовски повезло! Ты выиграл бан на 666 сек")
    
    @bot.message_handler(commands=['testban'])
    def handle_message(message):
        rate = (random.weibullvariate(1,0.5))
        if rate <= 1:
            bantime = int(random.randrange(60,300, 1))
        elif rate > 1 and rate <= 5:
            bantime = int(random.randrange(300,600, 1))
        elif rate > 5 and rate <= 7:
            bantime = int(random.randrange(600, 3600, 1))
        elif rate > 7 and rate <= 9:
            bantime = int(random.randrange(3600, 86400, 1))
        elif rate > 20 and rate <= 50:
            bantime = int(random.randrange(86400, 259200, 1))
        elif rate > 69 and rate <= 71:
            bantime = int(999999999)
        else:
            bantime = int(666)
        if bantime != int(666):
            bot.reply_to(message, "Поздравляю! Ты выиграл бан на " + convert(bantime))
        elif bantime == int(999999999):
            bot.reply_to(message, "И ПЕРЕД НАМИ ПОБЕДИТЕЛЬ! Ты выиграл ПЕРМАЧ!")
        else:
            bot.reply_to(message, "Тебе чертовски повезло! Ты выиграл бан на 666 сек")
    
    @bot.message_handler(commands=['restricted'])
    def send_text(message):
        bot.send_message(message.chat.id, "; ".join([str(x) for x in restricted_messages]))
    
    @bot.message_handler(regexp="^.*ты(?:(?!не).)*?пид(.?)р.*$")
    def handle_message(message):
        bot.reply_to(message, "+")
    
    # @bot.message_handler(regexp="^(?:(?!не).)*?пид(.?)р.*$")
    # def handle_message(message):
    #     bot.reply_to(message, "+")
    
    @bot.message_handler(regexp="(?i)(^сеппуку$)|(^сепуку$)")
    def handle_message(message):
        rate = (random.weibullvariate(1,0.5))
        bantime = int(random.randrange(86400, 432000, 1))
        if rate >= 100:
            bot.restrict_chat_member(message.chat.id,message.from_user.id)
            if message.from_user.username is not None:
                bot.reply_to(message, "@completelyordinarybot помог сделать сеппуку @" +  message.from_user.username + ". Респаун через " + convert(bantime))
            else:
                bot.reply_to(message, "@completelyordinarybot помог сделать сеппуку " +  message.from_user.first_name + ". Респаун через " + convert(bantime))
        else:
            bot.restrict_chat_member(message.chat.id,message.from_user.id,until_date=time.time()+bantime)
    
    
    
    @bot.message_handler(regexp="(трист.$|300$|300\?$|трист.\?$|300\!$|трист.\!$)")
    def handle_message(message):
        bot.reply_to(message, "Отсоси у тракториста")
    
    @bot.message_handler(regexp="(отс.си у тр.кт.риста)")
    def handle_message(message):
        bot.reply_to(message, "Тракторист сегодня я, отсоси-ка у меня")
    
    @bot.message_handler(regexp="(отс.си ты у м.ня|отс.си.ка у м.ня)")
    def handle_message(message):
        bot.reply_to(message, "В трактористы ты не годен, отсоси и будь свободен")
    
    @bot.message_handler(regexp="(отсоси*. и будь св.боден)")
    def handle_message(message):
        bot.reply_to(message, "Годен я, сомнений нет, лучше сделай мне минет")
    
    @bot.message_handler(regexp="(нет*. лучш. сделай мне м.нет)")
    def handle_message(message):
        bot.reply_to(message, "А сомнения есть всегда, отсоси-ка три хуя")
    
    @bot.message_handler(regexp="(сомнен.я.* всегда.* ((отсоси.*|лучше.*нюхай).*(три|3).*хуя))")
    def handle_message(message):
        bot.reply_to(message, "Извини, спина не гнётся, отсосать тебе придётся")
    
    @bot.message_handler(regexp="^.*(сп.на.*(гн.тся|гн.ться).*((отсосать.*|пососать.*).*т.бе.*(пр.д.тся|пр.д.ться))).*$")
    def handle_message(message):
        bot.reply_to(message, "Можешь стоя отсосать, я не буду возражать")
    
    @bot.message_handler(regexp="^.*(стоя.*((отсосать.*|пососать.*).*буду.*возр.жать)).*$")
    def handle_message(message):
        if message.from_user.username is not None:
            bot.reply_to(message, "@completelyordinarybot ушёл за боярышник, отсасывать стоя у @" +  message.from_user.username)
        else:
            bot.reply_to(message, "@completelyordinarybot ушёл за боярышник, отсасывать стоя у " +  message.from_user.first_name)
    
    @bot.message_handler(regexp="^.*(где б.яр.шник\?).*$")
    def set_ro(message):
        bot.reply_to(message, 'А вот прямо здесь, пойдём, покажу минут на 10...')
        time.sleep(0.5)
        bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time()+600)
        if message.from_user.username is not None:
            bot.send_message(message.chat.id, '@completelyordinarybot уводит @' +  message.from_user.username + ' за боярышник')
        else:
            bot.send_message(message.chat.id, '@completelyordinarybot уводит ' +  message.from_user.first_name + ' за боярышник')
    
    @bot.message_handler(regexp = regex_msg)
    def handle_message(message):
        bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time()+600)
        bot.reply_to(message, 'Мы тут таких осуждаем. Иди отсасывать за боярышником на 10 минут')
    
    #@bot.message_handler(func=lambda message: ' ' not in message.text)
    @bot.message_handler(regexp="^[А-Яа-я]\S+$")
    def send_text(message):
        mes = huevo(message.text)
        bot.reply_to(message, mes)
except:
    pass

# @bot.message_handler(func=lambda message: message.from_user.username == 'NoMarks')
# def handle_message(message):
#     bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time()+600)
#     bot.send_message(message.chat.id, 'Get your ass back here, гнусный натурал ' +  message.from_user.username + '! Начинаю нагибательный процесс ....')
#     time.sleep(5)
#     bot.send_message(message.chat.id, 'Пенетрация началась, процесс займёт 10 минут')


bot.polling(none_stop=True, interval=0, timeout=200)