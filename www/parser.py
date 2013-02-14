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

def parsRBC ( request, szCheckTIKER = "TOTAL_TOTAL", szAddCommand = "", szURLtoPars="" ) :
    # szCheckTIKER -- тикер который надо распарсить.
    #   значение "TOTALALL" вызывает парсинг всего...
    # szAddCommand -- дополнительная комманда. Бывает:
    #   "" или "ADD" -- добавить новые значения
    #   "DEL" -- удалить тикер и все значения по нему
    #   "UPD" -- обновить данные по тиккеру (зачала DEL после NEW)
    #   "NEW" -- прописать новый тиккер и добавить все значения
    # szURLtoPars -- путь для парсинга... он нужен при добавлении тикера "NEW" чтобы
    #    система знала по какому адресу брать информаию и что парсить
    #
    # если вызов проиходит через DJANGO то при отсутствии параметро szCheckTIKER содержит
    # пустую строку. Если это так то все нафикЁ
    if szCheckTIKER == "" :
        return ()

    # если вызов проиходит через DJANGO то при отсутствии параметро szAddCommand содержит
    # пустую строку. Если это так, то предполагается "ADD" (добавление новых данных)
    if szAddCommand == "" :
        szAddCommand = "ADD"

    szPathToLogFile = "./logs/parser-process.log"       # Путь для лог-файла. Если в пути есть
                                                        # директории (типа /log/) убедитесь, что
                                                        # они созданы заранее
    szHtml = "<pre>"   # для отладки. Сюда сваливаем всю выдачу... В конце ее покажем в вебе

    try:
        fileLog = open( szPathToLogFile , 'a' )        # открываем log-файл на добавление
        # определяем функцию записи в лог
        def fuWriteLog ( szStatus= u"/TEST/TEST/TEST/TEST/TEST/ - 200" ) :
            # Это функция записи в лог... Все что в нее попадат в качестве переменной
            # обвязывается датой-временем и записывается в файл.
            # На всякий случай это еще и возвращаем в return()
            szLogEntry = "%32s - " % ( szStatus ) + \
                         datetime.datetime.now(
                             timezone.get_default_timezone( )
                         ).strftime( "%d/%m/%Y %H:%M:%S.%f %z (%Z)" ) + "\n"
            fileLog.write( szLogEntry )
            return ( szLogEntry )
        szHtml += fuWriteLog( u"-->PARSER START >>>>> %3s   - 100" % szAddCommand )

        # проверяем szAddCommand на принадлежность к дополнительным коммандам
        #
        if szAddCommand not in { "ADD", "NEW", "DEL", "UPD" } :
            szHtml += fuWriteLog( u"UNKNOW ADDITIONAL COMMAND   - 405" )
            return ()

        try:
            # пробуем приконнектится к базе и организовать курсор
            dbconnect = MySQLdb.connect( passwd='qwas', db='db_stocks')    # <--- для компа MCN
            # dbconnect = MySQLdb.connect( db='db_stocks')                 # <--- для компа JUNK01
            # dbconnect = MySQLdb.connect( host='192.168.1.105',
            #     user='root', passwd='****', db='db_stocks')              # <--- для компа JUNK02

            # --- Коннект к БД есть. Пишем это событие в лог
            szHtml += fuWriteLog( u"DB CONNECT OPEN             - 200" )

            def fuParsing ( szCheckTIKER = "", szAddCommand = "ADD", szURLtoPars="" ) :
                szHtml = ""
                # Это функция парсинга. Она нужна чтобы можно было вызывая ее в цикле распарсить
                # много тикеров... В обычном режиме она буждет вызываться единожды.
                # НА момент вызова функции должны быть открыты:
                # -- индефицикатор лог сфала -- fileLog
                # -- коннектор к базе данных с котировками -- dbconnect
                if szCheckTIKER == "" :
                    szHtml += fuWriteLog( u"UNKNOW TICKER               - 200" )
                else:
                    # --- создаем курсор БД ?? что-это
                    dbcursor=dbconnect.cursor()
                    #----------------------------------------------------------------------------
                    # Если если пришла комманда "UPD" или "DEL" то чистим базу"
                    if szAddCommand in { "UPD", "DEL" } :
                        # удаляем и пишем в лог
                        dbcursor.execute(
                            u"""DELETE FROM db_stocks.tbIndexValue
                            WHERE tbIndexValue.szTICKER = '%s';""" % szCheckTIKER )
                        szHtml += fuWriteLog( u">>> DELETED %011d ROW - 200" % dbcursor.rowcount )
                        # Если если пришла комманда "UPD", nто сначала делаем "DEL" а после "NEW"
                        if szAddCommand == "UPD" :
                            szAddCommand = "NEW"
                    if szAddCommand in { "NEW", "ADD"} :
                        # --- надо парсить
                        # узнаем путь по которому надо парсить
                        dbcursor.execute( u"""SELECT tbIndexName.szPathForParsing
                                   FROM tbIndexName
                                   WHERE tbIndexName.szTICKER = '%s';""" % szCheckTIKER )
                        if dbcursor.rowcount == 0 :
                            # если отклика не было
                            szHtml += fuWriteLog( u"UNKNOW PARSER PATH & TICKER - 200" )
                            return ( szHtml )
                        # пишем в лог
                        # сам путь попал в переменную: dbcursor.fetchone()[0]
                        szURLtoPars =  dbcursor.fetchone()[0]
                        szHtml += fuWriteLog( u"PARSE [%d] #%16s - 200" % (dbcursor.rowcount, szCheckTIKER) )
                        # szHtml += "%s" % dbcursor.fetchone()[0] + "\n"
                        # надо парсить новые данные.
                        # Подставляем дату создания самого первого индекса в мире DJI
                        szY1intoURL = "1928"
                        szM1intoURL = "10"
                        szD1intoURL = "1"
                        if szAddCommand == "ADD" :
                            # но еще нао проверить вдруг что-то в базе уже есть.
                            # Узнаем какие самые свежие данные в базе
                            dbcursor.execute( u"""
                                    SELECT MAX(tbIndexValue.tmDate) AS dtLastDate
                                    FROM tbIndexValue
                                    WHERE tbIndexValue.szTICKER = \"%s\"
                                    GROUP BY tbIndexValue.szTICKER;""" % szCheckTIKER )
                            if dbcursor.rowcount != 0 :
                                # мы получили какие-то данные (дату) из базы и начинаем парсить с этого времени
                                # только не забываем добавить к полученной дате еще один день
                                dtLastDateTicker = dbcursor.fetchone()[0] + datetime.timedelta(days=1)
                                # Подставляем дату самых свежих данных из базы
                                szY1intoURL = dtLastDateTicker.strftime( "%Y" )
                                szM1intoURL = dtLastDateTicker.strftime( "%m" )
                                szD1intoURL = dtLastDateTicker.strftime( "%d" )
                        # определились с датами начала парсинга и путем парсинг
                        # Мажно начинать парсить и записывать все это в базу
                        # Проверяем и организуем коннект к сайту РБК
                        webConnect = httplib.HTTPConnection("export.rbc.ru")
                        # общая структура URL для выдачи данныхс котировками c RBC:
                        # http://export.rbc.ru/free/index.0/free.fcgi?period=DAILY&tickers=NASD&d1=20&m1=12&y1=2012&d2=25&m2=01&y2=2013&lastdays=09&separator=%3B&data_format=BROWSER&header=1
                        #
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
                        # делаем запрос к странице сервера
                        #
                        # формируем URL для вызова соответствующей странице по тиккеру |
                        #                                                              |
                        webConnect.request(                       #   +----------------+
                            "GET",                                #   |
                            szURLtoPars + urllib.urlencode( { "period": "DAILY",
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
                              "User-Agent": "MadMouse/0.3" } )
# ------------- ОТЛАДКА
#                       szHtml += szURLtoPars + urllib.urlencode( { "period": "DAILY",
#                                                                   "tickers": szCheckTIKER,
#                                                                   "d1": szD1intoURL,
#                                                                   "m1": szM1intoURL,
#                                                                   "y1": szY1intoURL,
#                                                                   "separator": ";",
#                                                                   "data_format": "BROWSER",
#                                                                   "header": "0" }) + "\n"
# ------------- ОТЛАДКА
                        webResponse = webConnect.getresponse( )
                        # пишем в лог статус сервера РБК
                        szHtml += fuWriteLog( u">>> SERVER: %15s - %3d" % (webResponse.reason, webResponse.status) )
                        # считаем и пишем в лог объем полученных данных с сервера РБК
                        lszGettedData = webResponse.read().splitlines()
                        szHtml += fuWriteLog( u">>> GET STRING: %011d - 200" % len(lszGettedData) )
                        # цикл по строчкам...
# отладка               szHtml += "%s" % lszGettedData + "\n"
                        # у данных в строке следующая структура и порядок
                        # TICKER;DATE;OPEN;HIGH;LOW;CLOSE;VOL;WAPRICE
                        # где:
                        # - TICKER -- тикер
                        # - DATE -- дата в формате YYYY-MM-DD
                        # - OPEN -- цена (уровень) открытия
                        # - HIGH -- цена (уровень) максимум дня
                        # - LOW -- цена (уровень) минимум дня
                        # - CLOSE --цена (уровень) закрытия
                        # - VOL -- объём (для индексов не доступен)
                        # - WAPRICE -- ???? фигня какая-то
                        #
                        for szCurrentData in lszGettedData :
                            # разбиваем строку текущих данных и запоминаем во временном листе
                            lszCurrentData = szCurrentData.split(";")
                            # оказывается иногда бывают "дыры" в данных и пустые ячейки
                            # проще всего эти данные удалить но как-то неправильно это
                            # но иначе придумать не получается, т.к. лакуна в произвоьном месте
                            try :
                                lszCurrentData[2] = float( lszCurrentData[2] )
                                lszCurrentData[3] = float( lszCurrentData[3] )
                                lszCurrentData[4] = float( lszCurrentData[4] )
                                lszCurrentData[5] = float( lszCurrentData[5] )
                            except:
                                continue
                            # удаляем два ненужных элемента выдачи VOL и WAPRICE
                            lszCurrentData.pop()
                            lszCurrentData.pop()
                            # данные в строке распарщены и можно записать их в Базу Данных
                            dbcursor.execute( """
                                INSERT INTO db_stocks.tbIndexValue
                                ( szTICKER , tmDATE , fOPEN  , fHIGH , fLOW , fCLOSE )
                                VALUES
                                ( '%s', '%s', %f, %f, %f, %f );
                                """ % (lszCurrentData[0],
                                       lszCurrentData[1],
                                       lszCurrentData[2],
                                       lszCurrentData[3],
                                       lszCurrentData[4],
                                       lszCurrentData[5]) )
# отладка ---+------------>  szHtml += "'%s', '%s', %f, %f, %f, %f" %  (lszCurrentData[0],
         #   |                                                  lszCurrentData[1],
         #   |                                                  lszCurrentData[2],
         #   |                                                  lszCurrentData[3],
         #   |                                                  lszCurrentData[4],
         #   +---------------------------------------------->   lszCurrentData[5])  + "\n"
                        # пишем в лог что все ок
                        szHtml += fuWriteLog( u">>> WRITE ROW2DB: %09d - 200" % len(lszGettedData) )
                    # --- исполняем все накопленные для MySQL комманды разом
                    dbconnect.commit()
                    # --- закрываем курсор
                    dbcursor.close()
                return ( szHtml )

            # Теперь можно вызвать функцию...
            if szCheckTIKER == "TOTAL_TOTAL" :
                # надо распарсить все-все-все... Т.е. перебрать все тикеры по очереди и
                # проделать что велено с их данными
                # --- создаем курсор БД ?? что-это
                dbcursor = dbconnect.cursor()
                # получаем список всех тикеров в бвзе и путей для парсинга
                dbcursor.execute( u"""SELECT tbIndexName.szTICKER, tbIndexName.szPathForParsing
                                     FROM tbIndexName;""" )
                iNumRows =  dbcursor.rowcount
                # запишем в лог, что это груповой парсинг
                szHtml += fuWriteLog ( u"PARSE GROUP TIKERS: %07d - 200" % iNumRows )
                for i in range( iNumRows ):
                    lszCurentRaw = dbcursor.fetchone()
# отладка                     szHtml += " -- %s --%s" % (lszCurentRaw[0], lszCurentRaw[1] ) + "\n"
                    szHtml += fuParsing( lszCurentRaw[0], szAddCommand, lszCurentRaw[1] )
                # --- закрываем курсор
                dbcursor.close()
            else:
                # надо распарсить единственный тикер, т.е. вызвать функцию всего один раз
                szHtml += fuParsing( szCheckTIKER, szAddCommand, szURLtoPars )

            # --- закрываем коннект с базой
            dbconnect.close( )
            szHtml += fuWriteLog ( u"DB CONNECT CLOSE            - 200" )
        except Exception, szErrorCode:
            # --- нет коннекта к БД.
            szHtml += fuWriteLog ( u"DBERR %11s - 403" % szErrorCode )

    except IOError:
        szHtml += u"%s :лог-файл отсутсвует или поврежден<br />" % "ERROR"

    finally:
        szHtml += "</pre>"
        szHtml += u"<b>ARG1=%s //// ARG2=%s</b>" % (szCheckTIKER, szAddCommand)
        return HttpResponse ( szHtml )
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
