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


# import tzinfo
# import timedelta
# import random


def parsRBC ( request, szCheckTIKER = "ALL", szAddCommand = "" ) :
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
        # Устанавливаем текущее время с метками часового пояаса. Если сделать просто datetime.datetime.now()
        # то получим текущее время без меток часового пояся, так что делаем так:
        szLogEntry = u"LOG SESSION BEGIN - "\
                     + datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog )\
                     + "\n"
        fileLog.write( szLogEntry )
        szHtml += szLogEntry

        # --- фаза 2: коннектимся к БД
        try:
            dbconnect = MySQLdb.connect(user='root',passwd='qwas',db='db_stocks')  #???,cursorclass=MySQLdb.cursors.DictCursor)
            # --- Коннект к БД есть. Пишем это событие в лог
            szLogEntry = u"DB CONNECT OPEN   - "\
                     + datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog )\
                     + "\n"
            fileLog.write( szLogEntry )
            szHtml += szLogEntry
            # --- создаем курсор БД ?? что-это
            dbcursor=dbconnect.cursor()
            # --- проверяем наличие тикеров
            dbcursor.execute( u"""SELECT tbIndexName.szTICKER
                           FROM tbIndexName
                           WHERE tbIndexName.szTICKER = \"%s\"""" % szCheckTIKER )
            szTMP = dbcursor.fetchone()
            # проверяем есть ли выдача в запросе
            if dbcursor.rowcount != 0 :
                szHtml += "%s\n" % szTMP
                szLogEntry = u"PARS   #%11s - " % szTMP
                szLogEntry += datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog ) + "\n"
                fileLog.write( szLogEntry )
                szHtml += szLogEntry
            else:
                szHtml += "%s\n" % szTMP
                szLogEntry = u"UNKNOW #%11s - " % szCheckTIKER
                szLogEntry += datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog ) + "\n"
                fileLog.write( szLogEntry )
                szHtml += szLogEntry


            # --- закрываем курсор
            dbcursor.close()
            # --- закрываем коннект с базой
            dbconnect.close( )
            szLogEntry = u"DB CONNECT CLOSE  - "\
                         + datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog )\
                         + "\n"
            fileLog.write( szLogEntry )
            szHtml += szLogEntry
        except Exception, szErrorCode:
            # --- нет коннекта к БД. Фаза 2 стала последней!
            szLogEntry = "DB ERROR (%s) - " % szErrorCode
            szLogEntry += datetime.datetime.now(timezone.get_default_timezone()).strftime( szDataForamtForLog ) + "\n"
            fileLog.write( szLogEntry )
            szHtml += szLogEntry

        fileLog.close()
    finally:
        szHtml += "</pre>"
        szHtml += u"Hello world! Привет питон! <b>1=%s //// 2=%s</b>" % (szCheckTIKER, szAddCommand)
        return HttpResponse ( szHtml )


    # try:
    #    iNum = int ( iNum )
    # except ValueError:
    #    raise Http404 ( )

    # формат log-файлов
    # ДЕЙСТВИЕ - РЕЗУЛЬТАТ - [ДАТА][29/Jan/2013:18:29:56 +0400]



