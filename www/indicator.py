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
    # -----отладка ----
    # -----устанавливаем тикер----
    szTIKER = "SPX"
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


        # узнаем самую последююю дату
        dbcursor.execute(
            u"SELECT MAX( tbIndexValue.tmDATE )"
            u" FROM  tbIndexValue"
            u" WHERE tbIndexValue.szTICKER =  '%s';" % szTIKER )
        tmDataIndicator = dbcursor.fetchone()
        # ---- отладка BEGIN
        szHTML += u"<h2>{%s} <small><i>%s</i></small></h2>" % (szTIKER, str( tmDataIndicator[0] ) )
        # ---- отладка END
        dbcursor.execute(
            u"SELECT tbIndexValue.fCLOSE" # (*01*) можно вывести для отладки еще и ---> ", tbIndexValue.tmDATE"
            u" FROM tbIndexValue"
            u" WHERE tbIndexValue.szTICKER =  '%s'"
            u" ORDER BY tbIndexValue.tmDATE DESC"
            u" LIMIT 322;" % szTIKER )
        lstfDataAll = dbcursor.fetchall() # <--- Здесь результаты запроса. Цены закрытия в обратной хронологии
        lstfPercentAll = []               # <--- Здесь будет процент дневного роста/падения в %%

        iPreviousItem = ()  # <---------------------- на старте выставляем "нулевой" картеж
                                                    # Он является признаком перваой итерации
        for fCurrentItem in lstfDataAll :
            if iPreviousItem == ():
                iPreviousItem = fCurrentItem
            else:
                # Общая формула для прироста выглядит так:
                #
                # рост_в_%%х = Показатель_тек.периода / Показатель_пред.периода × 100% - 100%
                #
                #       или
                #
                # рост_в_%% = ( Показатель_тек.периода / Показатель_пред._периода -1 ) × 100%.
                #
                # но в наших рассчетах не забываеv, что все уже отсотировано в братном порядке,
                # т.е. iPreviousItem -- это предыдущий элемент, т.е. содержит следующее для
                # текущего периода значение...
                #
                # ----- ОТЛАДКА BEGIN
                # szHTML += u"<small><tt>%2.3f%%   --- %s //// %s</tt></small><br />" % (
                #    100. * ( iPreviousItem[0] / fCurrentItem[0] - 1. ) ,
                #    iPreviousItem[0],
                #    fCurrentItem[0]
                #    # iPreviousItem[1], # (*1*) Чобы еже выводить и дату надо разкомментировать (*01*)
                #    )
                # ----- ОТЛАДКА END
                lstfPercentAll.append( 100. * ( iPreviousItem[0] / fCurrentItem[0] - 1. ) )
                iPreviousItem = fCurrentItem
        # ---- отладка BEGIN
        # szHTML += u"<small><tt>%s</tt></small><br />" % lstfPercentAll
        # ---- отладка END

        # для простоты и скорости просто используем лист из уже предрассчитанных по правилам
        # золотого сечения значений. Для дневного идикатора и по дневным данным это:
        #   [ 1, 2, 4, 6, 11, 17, 29, 46, 76, 122, 199, 321, 521 ]
        # это обратные отрезки времени (в днях) от текущей даты. Их 12, но нулевог значения нет.
        # Т.е. 13 которые определяют 12 = 3*4 интервалов. Т.е. это три оборота индикатора.
        # Последовательность, если чо, можно рассчитать так:
        #   for iCount in range(-1, -14, -1) :
        #       iCurrentRow = fuCutLine( 1, iCount) - 1

        lstiDescendingDataCut = [ 1, 2, 4, 6, 11, 17, 29, 46, 76, 122, 199, 321] # , 521 ]

        lstfPercent4Indicator = []          # <--- Здесь будет процент средне-дневного роста/падения для дат индикатора
        lstfPercentAverage4Indicator = []   # <--- Здесь будет процент средне-дневного роста/падения для периодов индикатора
        lstfPercentMax4Indicator = []       # <--- Здесь будет процент максимального роста для периодов индикатора
        lstfPercentMin4Indicator = []       # <--- Здесь будет процент максимального падения для периодов индикатора

        iPreviousItem = 0                   # это будет признаком первой итерации
        for iCurrentItem in lstiDescendingDataCut :
            # Тут считаем средний прирост за период. Формула похожа на формула прироста:
            #
            # ср_рост_в_%% = ( Показатель_тек.периода / Показатель_пред._периода -1 ) × 100% / Число_периодов
            #
            # но в наших рассчетах не забываеv, что все уже отсотировано в братном порядке,
            # т.е. iPreviousItem -- это предыдущий элемент, т.е. содержит следующее для
           # текущего периода значение...
            lstfPercent4Indicator.append(
                (lstfDataAll[iPreviousItem][0] / lstfDataAll[iCurrentItem][0] - 1.)
                * 100. / ( iCurrentItem - iPreviousItem ) )
            lstfPercentAverage4Indicator.append(
                (lstfDataAll[0][0] / lstfDataAll[iCurrentItem][0] - 1.)
                * 100. / iCurrentItem )
            lstfPercentMax4Indicator.append( max( lstfPercentAll[ iPreviousItem : iCurrentItem ] ) )
            lstfPercentMin4Indicator.append( min( lstfPercentAll[ iPreviousItem : iCurrentItem ] ) )
            iPreviousItem = iCurrentItem
            # ---- отладка BEGIN
            # szHTML += u"<tt>%00d<br /><small>" \
            #          u"--- Ср.1: <b>%s</b><br />" \
            #          u"--- Cр2.: <i>%s</i><br />" \
            #          u"-=- макс: %s<br />" \
            #          u"-=- мин.: %s</small></tt><br />" % (
            #        iCurrentItem,
            #        lstfPercent4Indicator,
            #        lstfPercentAverage4Indicator,
            #        lstfPercentMax4Indicator,
            #        lstfPercentMin4Indicator,
            #    )
            # ---- отладка END

        # ---- отладка BEGIN
        szHTML += u"<tt><small>--- Ср.1: <b>%s</b><br />" \
                  u"--- Cр2.: <i>%s</i><br /" \
                  u">-=- макс: %s<br />" \
                  u"-=- мин.: %s</small></tt><br />" % (
            lstfPercent4Indicator,
            lstfPercentAverage4Indicator,
            lstfPercentMax4Indicator,
            lstfPercentMin4Indicator,
            )
        szHTML += u"<big>МАХ = %+03.5f // MIN = %+03.5f </big> ### %s<br />" % (
            max( lstfPercentAll ),
            min( lstfPercentAll ),
            int( 1 + 2. * max ( [ abs( max(lstfPercentAll )), abs(min( lstfPercentAll )) ] ) ) * 0.5,
            )
        # ---- отладка END

        # del lstfDataAll               # <--- этот список довольно большой и ее можно удалить если это поможе скорости
        # del lstfPercentAll            # <--- этот список довольно большой и ее можно удалить если это поможе скорости

        # базис нормирования (округленное вверх до ближайшего 0.5)
        # fValuationBasis = int( 1 + 2. * max ( [ abs( max( lstfPercentMax4Indicator ) ),
        #                                        abs( min( lstfPercentMin4Indicator ) ) ]) ) * 0.5
        fValuationBasis = int( 1 + 2. * max ( [ abs( max( lstfPercent4Indicator ) ),
                                                abs( min( lstfPercent4Indicator ) ) ]) ) * 0.5


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

        iCurrentItem = 0        # <--- Счетчик итераций (элементов индикатора)
        # рисуем вложенную структуру (1) -> (2) -> (3) -> (4)
        for iCount in range(3) :
            # ---- ( Фаза 1)
            # нормируем
            # html += "<td bgcolor='#%02xe0e0'>" % int(0x9d-((dim[iTmpX][iTmpY][0]-lstFocusInfo[5][0])*98.)/lstFocusInfo[5][1])
            if lstfPercent4Indicator[iCurrentItem] > 0 :
                # если больше нуля, то зеленое
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ),
                    (int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255 ,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255),
                    outline="silver"
                )
            elif lstfPercent4Indicator[iCurrentItem] == 0 :
                # если нуль, то серое
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ), (128,128,128,255), outline="silver" )
            else:
                # если мньше нуля, то красное
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ),
                    (255,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255),
                    outline="silver"
                )
            iCurrentItem += 1
            iX2 = fuCutLine( iX2 - iX1 ) + iX1

            # ---- ( Фаза 2)
            if lstfPercent4Indicator[iCurrentItem] > 0 :
                # если больше нуля, то зеленое
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ),
                    (int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255 ,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255),
                    outline="silver"
                )
            elif lstfPercent4Indicator[iCurrentItem] == 0 :
                # если нуль, то серое
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ), (128,128,128,255), outline="silver" )
            else:
                # если мньше нуля, то красное
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ),
                    (255,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255),
                    outline="silver"
                )
            iCurrentItem += 1
            iY1 = iY2 - fuCutLine( iY2 - iY1 )
            # ---- ( Фаза 3)
            if lstfPercent4Indicator[iCurrentItem] > 0 :
                # если больше нуля, то зеленое
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ),
                    (int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255 ,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255),
                    outline="silver"
                )
            elif lstfPercent4Indicator[iCurrentItem] == 0 :
                # если нуль, то серое
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ), (128,128,128,255), outline="silver")
            else:
                # если мньше нуля, то красное
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ),
                    (255,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255),
                    outline="silver"
                )
            iCurrentItem += 1
            iX1 = iX2 - fuCutLine( iX2 - iX1 )
            # ---- ( Фаза 4)
            if lstfPercent4Indicator[iCurrentItem] > 0 :
                # если больше нуля, то зеленое
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ),
                    (int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255 ,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255),
                    outline="silver"
                )
            elif lstfPercent4Indicator[iCurrentItem] == 0 :
                # если нуль, то серое
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ), (128,128,128,255), outline="silver")
            else:
                # если мньше нуля, то красное
                drwIndicator.rectangle( ( iX1 , iY1 , iX2, iY2 ),
                    (255,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     int (255. - 255. * abs( lstfPercent4Indicator[iCurrentItem]) / fValuationBasis ) ,
                     255),
                    outline="silver"
                )
            iCurrentItem += 1
            iY2 = iY1 + fuCutLine( iY2 - iY1 )


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
