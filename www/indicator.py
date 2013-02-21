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

import datetime                                 # библиотека работы с датами и временем
# import timedelta
import pytz                                     # библиотека работы с временными зонами (TMZ, UTC и прочая фигня)
import MySQLdb                                  # библиотека доступа к MySQL
# import PIL                                      # библиоткеа работы с графикой
import math                                     # библиотека математическх вычислений
from PIL import Image, ImageDraw, ImageFont

# import tzinfo
# import random

def indicator ( request ) :
    szHTML = ""
    tmStart = datetime.datetime.now( timezone.get_default_timezone( ) )  # <-- для отладки, измерялка скорости
    szPathToFile = "/static/img/test.png"      # <-- путь будем вычислять и сворачивать в хеш
                                               # каждому тикеру для каждой даты отдельный имидж
    iSize = 320
    fGoldenRatio = ( math.sqrt( 5 ) - 1 ) / 2
    def fuCutLine ( iLengthLine = iSize, iNum = 1  ) :
        # функуия нарезка отрезка по закону залотого сечения...
        # iNum - итерация
        if iNum == 0:
            return ( iLengthLine )
        else:
            iDot = int ( iLengthLine * (fGoldenRatio ** iNum) )
            return  ( iDot )
    iX1 = 0
    iX2 = int ( iSize / fGoldenRatio )
    iY1 = 0
    iY2 = int ( iSize )
    try:
        # пробуем приконнектится к базе и организовать курсор
        dbconnect = MySQLdb.connect( passwd='qwas', db='db_stocks')    # <--- для компа MCN
        # dbconnect = MySQLdb.connect( db='db_stocks')                 # <--- для компа JUNK01
        # dbconnect = MySQLdb.connect( host='192.168.1.105',
        #     user='root', passwd='****', db='db_stocks')              # <--- для компа JUNK02

        # согдаем курсор базы
        dbcursor=dbconnect.cursor()

        # -----отладка ----
        # -----устанавливаем тикер----
        szTIKER = "DJI"

        # узнаем самую последююю дату
        dbcursor.execute(
            u"""SELECT MAX( tbIndexValue.tmDATE )
            FROM  tbIndexValue
            WHERE tbIndexValue.szTICKER =  '%s';""" % szTIKER )
        tmDataIndicator = dbcursor.fetchone()
        szHTML += "<h2>%s</h2>" % tmDataIndicator

        dbcursor.execute(
            u"""SELECT tbIndexValue.fOPEN
            FROM tbIndexValue
            WHERE tbIndexValue.szTICKER =  '%s'
            ORDER BY tbIndexValue.tmDATE DESC
            LIMIT 521;""" % szTIKER )
        lstDataAll = dbcursor.fetchall()
        lstfData4Indicator = []
        lstfPercent4Indicator = []


        for iCount in range(-1, -14, -1) :
            iCurrentRow = fuCutLine( 1, iCount) - 1
            lstfData4Indicator.append ( lstDataAll[ iCurrentRow ][ 0 ] )
            if iCount < -1 :
                lstfPercent4Indicator.append(
                    100 * ( lstfData4Indicator[0] - lstfData4Indicator[abs(iCount)-1] )
                    / iCurrentRow / lstfData4Indicator[abs(iCount)-1]
                )
            szHTML += "<tt>%02d: %05d // ~~ %s [%s] ~~~~ </tt><br />" % (
                abs(iCount),
                fuCutLine( 1, iCount ),
                str( lstDataAll[ iCurrentRow ][ 0 ] )  ,
                str( lstfPercent4Indicator ),
                # str( lstfData4Indicator ),
                )
        del lstDataAll

        imgBox = Image.new("RGBA", ( iX2+1, iY2+1 ), (0,0,0,0) )
        # Рисуем вот такую структуру индикаторв
        #
        #      X1,Y1-----------------+----------X2
        #      |                     |          |
        #      |        (2)          |          |
        #      |                     |          |
        #      +--------+------------+          |
        #      |        |            |   (1)    |
        #      |        |            |          |
        #      |  (3)   +------------+          |
        #      |        |    (4)     |          |
        #      Y2-------+------------+----------+

        drwIndicator = ImageDraw.Draw(imgBox)
        # ----- (ФАЗА 0) рисуем внешнюю коробочку
        drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ), (0,0,0,0), outline="blue")
        # рисуем вложенную структуру (1) -> (2) -> (3) -> (4)
        for iCount in range(3) :
            # ---- ( Фаза 1)
            iX2 = fuCutLine( iX2 - iX1 ) + iX1
            drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ), (100,100,0,255), outline="silver")
            # ---- ( Фаза 2)
            iY1 = iY2 - fuCutLine( iY2 - iY1 )
            drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ), (200,200,200,255), outline="blue")
            # ---- ( Фаза 3)
            iX1 = iX2 - fuCutLine( iX2 - iX1 )
            drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ), (0,0,0,255), outline="blue")
            # ---- ( Фаза 4)
            iY2 = iY1 + fuCutLine( iY2 - iY1 )
            drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ), (0,0,0,255), outline="blue")


            drwIndicator.rectangle( ( 10 , 10 , 20, 20 ), fill="red" , outline="red")
            # font = ImageFont.truetype("./static/fonts/arial.ttf", 10)
            font = ImageFont.load_default()
            drwIndicator.setink( "black" )
            drwIndicator.text( (25, 10), "100%", font = font  )

        del drwIndicator
        imgBox.save("." + szPathToFile, "PNG")

        # отладка
        # печатаем получившуюся картинку
        szHTML += "<center><img src='%s' />" % szPathToFile


        dbconnect.commit( )     # --- исполняем все накопленные для MySQL комманды разом
        dbcursor.close( )       # закрываем курсор базы данных
        dbconnect.close( )      # закрываем коннект к базе данных

    except Exception, szErrorCode:
        # --- нет коннекта к БД.
        szHtml += u"C базой даных какая-то фигня<br \>"
        szHtml += fuWriteLog ( u"DBERR %11s - 403" % szErrorCode )

    finally:
        # отладка
        szHTML += u"<br />Время выполнения: %s" % \
              str( datetime.datetime.now( timezone.get_default_timezone( ) ) - tmStart )
        # отладка
        return HttpResponse ( szHTML )
