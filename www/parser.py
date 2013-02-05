# -*- coding: utf-8 -*-
# Включили поддержку UTF-8 в Python. Без этого даже комментарии на русском языке нельзя писать.
# И не забывает следующих простых правил:
# 1. Помещаем оператор u перед каждой строкой, которая содержит символы не из кодировки ascii.
# 2. При обработке входящих запросов проверяем корректность использования request.encoding = "UTF-8"
# 3. Используем ugettext как псевдоним для _
# 4. В методах с параметрами в виде байтовой строки (например, quote() или hashlib.sha224() )
#    не забываем привести ее в формат unicode: theunicodestring.encode("utf-8")

from django.http import HttpResponse, Http404
# Для того чтобы работат с часовыми поясами надо ставить "import putz". Но он не взеде есть и не всегда
# пожно его в Python установить. Решается через "from django.utils import timezone" и см. ниже
from django.utils import timezone

import datetime
import pytz                                     # библиотеа не доступна, ??? Походе ее django забивает
import MySQLdb                                  # библиотеа не доступна, ??? Походе ее django забивает
import httplib                                  # библиотека работы с HTTP (скачиваем ссылки и все такое)
import urllib                                   # библиотека преобразования URL

# import tzinfo
# import timedelta
# import random


def parsRBC ( request, szCheckTIKER = "ALL", szAddCommand = "" ) :
    # szCheckTIKER -- тикер который надо распарсить
    # szAddCommand -- дополнительная комманда. Реагируем только на "NEW" (распарсить новый тиккер)
    # если вызов проиходит через DJANGO то при отсутствии параметро szCheckTIKER содержит
    # пустую строку. Если это так то заменим ее на "ALL"
    if szCheckTIKER == "" :
        szCheckTIKER = "ALL"
    szPathToLogFile = "./logs/parser-process.log"      # путь для лог-файла (если в пути есть директории убедитесь что ои
                                                       # созданы заранее
    szDataForamtForLog = "%d/%m/%Y %H:%M:%S.%f %z (%Z)"   # формат даты-времени спользуемый в ЛОГ-файле
    szHtml = "<pre>"   # для отладки. Сюда сваливаем всю выдачу... В конце ее покажем в вебе

    try:
        fileLog = open( szPathToLogFile , 'a' )        # открываем log-файл на добавление
    except IOError:
        szHtml += u"%s :лог-файл отсутсвует или поврежден<br />" % "ERROR"
    else:
        # --- фаза 1: начинаем LOG
        # формат log-файлов
        # ДЕЙСТВИЕ - РЕЗУЛЬТАТ - [ДАТА в формате 29/Jan/2013:18:29:56 +0400]
        # ---
        # Устанавливаем текущее время с метками часового пояаса. Если сделать просто datetime.datetime.now()
        # то получим текущее время без меток часового пояся, так что делаем так:
        szLogEntry = u"LOG SESSION BEGIN          - 200 - "\
                     + datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog )\
                     + "\n"
        fileLog.write( szLogEntry )
        szHtml += szLogEntry

        # --- фаза 2: коннектимся к БД
        try:
            dbconnect = MySQLdb.connect(user='root',passwd='qwas',db='db_stocks')  #???,cursorclass=MySQLdb.cursors.DictCursor)
            # --- Коннект к БД есть. Пишем это событие в лог
            szLogEntry = u"DB CONNECT OPEN            - 200 - "\
                     + datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog )\
                     + "\n"
            fileLog.write( szLogEntry )
            szHtml += szLogEntry
            # --- создаем курсор БД ?? что-это
            dbcursor=dbconnect.cursor()
            # --- проверяем наличие тикеров
            dbcursor.execute( u"""SELECT tbIndexName.szTICKER
                           FROM tbIndexName
                           WHERE tbIndexName.szTICKER = \"%s\";""" % szCheckTIKER )
#            szTMP = dbcursor.fetchone()
            # проверяем есть ли выдача в запросе или может это запрос на PARS нового тиккера
            if dbcursor.rowcount != 0 or szAddCommand == "NEW" :
                # --- надо парсить
                szLogEntry = u"PARS [%d] #%16s - 200 - " % (dbcursor.rowcount, szCheckTIKER)
                szLogEntry += datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog ) + "\n"
                fileLog.write( szLogEntry )
                szHtml += szLogEntry
                # предположим? что надо парсить новые данные.
                # Подставляем дату создания самого первого индекса в мире DJI
                szY1intoURL = "1928"
                szM1intoURL = "10"
                szD1intoURL = "1"

                if szAddCommand != "NEW" :
                    # если новые данные парсить ненадо, то проверим
                    # дату самых свежих котировок по тикеру в Базе.
                    dbcursor.execute( u"""
                        SELECT MAX(tbIndexValue.tmDate) AS dtLastDate
                        FROM tbIndexValue
                        WHERE tbIndexValue.szTICKER = \"%s\"
                        GROUP BY tbIndexValue.szTICKER;""" % szCheckTIKER )
                    # Добавляем к полученной дате еще один день
                    dtLastDateTicker = dbcursor.fetchone()[0] + datetime.timedelta(days=1)
                    # Подставляем дату самых свежих данных из базы
                    szY1intoURL = dtLastDateTicker.strftime( "%Y" )
                    szM1intoURL = dtLastDateTicker.strftime( "%m" )
                    szD1intoURL = dtLastDateTicker.strftime( "%d" )

                # проверяем и организуем коннект к сайту РБК
                webConnect = httplib.HTTPConnection("export.rbc.ru")
                # делаем запрос к странице сервера
                # формируем URL для вызова соответствующей странице по тиккеру |
                #                                                              |
                webConnect.request(                                        #   |
                    "GET",                                                 #   |
                    "/free/index.0/free.fcgi?" + urllib.urlencode( { "period": "DAILY",
                                                                     "tickers": szCheckTIKER,
                                                                     "d1": szD1intoURL,
                                                                     "m1": szM1intoURL,
                                                                     "y1": szY1intoURL,
                                                                     "separator": ";",
                                                                     "data_format": "BROWSER",
                                                                     "header": "0" }) ,
                    "",
                    { "Content-type": "application/x-www-form-urlencoded",
                      "Accept": "text/plain",
                      "Accept-Charset": "utf-8",
                      "User-Agent": "MadMouse/0.1" } )
                webResponse = webConnect.getresponse( )
                # пишем в лог статус сервера РБК
                szLogEntry = u">>>SERVER: %15s - %3d - " % (webResponse.reason, webResponse.status)
                szLogEntry += datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog ) + "\n"
                fileLog.write( szLogEntry )
                szHtml += szLogEntry
                # считаем и пишем в лог объем полученных данных с сервера РБК
                lszGettedData = webResponse.read().splitlines()
                szLogEntry = u">>>GET STRING: %011d - 200 - " % len(lszGettedData)
                szLogEntry += datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog ) + "\n"
                fileLog.write( szLogEntry )
                szHtml += szLogEntry
                # цикл по строчкам...
#                szHtml += "%s" % lszGettedData + "\n"
                for i in lszGettedData :
                    szHtml += u"LEN:%d - %s" % ( len(i), i.split(";")) + "\n"

                # szHtml += "%s" % len(webResponse.read().splitlines()) + "\n"



            else:
                # --- неизввестный тикер и ничего нового парсить не надо
                szLogEntry = u"UNKNOW TK#%16s - 404 - " % szCheckTIKER
                szLogEntry += datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog ) + "\n"
                fileLog.write( szLogEntry )
                szHtml += szLogEntry
                # --- досвиданья

#           szHtml += "%s\n" % szTMP
            # --- закрываем курсор
            dbcursor.close()
            # --- закрываем коннект с базой
            dbconnect.close( )
            szLogEntry = u"DB CONNECT CLOSE           - 200 - "\
                         + datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog )\
                         + "\n"
            fileLog.write( szLogEntry )
            szHtml += szLogEntry
        except Exception, szErrorCode:
            # --- нет коннекта к БД. Фаза 2 стала последней!
            szLogEntry = u"DB ERROR (%s) - 403 - " % szErrorCode
            szLogEntry += datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog ) + "\n"
            fileLog.write( szLogEntry )
            szHtml += szLogEntry

        fileLog.close()
    finally:
        szHtml += "</pre>"
        szHtml += u"<b>ARG1=%s //// ARG2=%s</b>" % (szCheckTIKER, szAddCommand)
        return HttpResponse ( szHtml )


    # try:
    #    iNum = int ( iNum )
    # except ValueError:
    #    raise Http404 ( )


# строчка для вызова эерана с котировками c RBC:
# http://export.rbc.ru/free/index.0/free.fcgi?period=DAILY&tickers=NASD&d1=20&m1=12&y1=2012&d2=25&m2=01&y2=2013&lastdays=09&separator=%3B&data_format=BROWSER&header=1
#
# Общий формат:
# Вызов http://export.rbc.ru/free/index.0/free.fcgi?
# - period=DAILY -- перод. бесплатно доступны только дневные
# - tickers=NASD -- тикет (проверить, кажется доступны несколько тикетов или группы)
# - d1=20 -- дата1, день,  (два символа, лидирующий ноль, не обязательно)
# - m1=12 -- дата1, месяц (два символа, лидирующий ноль,  не обязательно)
# - y1=2012 -- дата1, год (четыре символа,  не обязательно)
# - d2=25 -- дата2, стартуем с дня,  (два символа, лидирующий ноль, не обязательно)
# - m2=01 -- дата2, стартуем с месяца (два символа, лидирующий ноль,  не обязательно)
# - y2=2013 -- дата2, год (четыре символа,  не обязательно)
# - lastdays=09 -- покзать на это колличесто дней. Ели нет дата1 или дата2 то показывает lastdays последних дней из базы
# - separator=%3B -- сепаратор (в данном сслучае ";"
# - data_format=BROWSER -- выводить в броузер (можно в файл, но его сложнее парсить).
# - header=1 -- выводить заголовок (1) или нет (0)... TICKER;DATE;OPEN;HIGH;LOW;CLOSE;VOL;WAPRICE
# порядок выдачи:
# - TICKER -- тикер
# - DATE -- дата в формате YYYY-MM-DD
# - OPEN -- цена (уровень) открытия
# - HIGH -- цена (уровень) максимум дня
# - LOW -- цена (уровень) минимум дня
# - CLOSE --цена (уровень) закрытия
# - VOL -- объём (для индексов не доступен)
# - WAPRICE -- ???? фигня какая-то

