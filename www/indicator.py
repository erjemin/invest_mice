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
from PIL import Image, ImageDraw

# import tzinfo
# import random

def indicator ( request ) :
    szHTML = ""
    tmStart = datetime.datetime.now( timezone.get_default_timezone( ) )  # <-- для отладки, измерялка скорости
    szPathToFile = "/static/img/test.png"      # <-- путь будем вычислять и сворачивать в хеш
                                               # каждому тикеру для каждой даты отдельный имидж
    iSize = 480
    fGoldenRatio = ( math.sqrt( 5 ) - 1 ) / 2
    imgBox = Image.new("RGBA", ( int ( iSize / fGoldenRatio), iSize), (0,0,0,128) )
    def fuCutLine ( iNum, iLengthLine = iSize ) :
        # функуия нарезка отрезка...
        # iNum - итерация
        if iNum == 0:
            return (iLengthLine )
        else:
            dot1 = int ( iLengthLine * (fGoldenRatio ** iNum) )
            return  ( dot1 )

    szHTML += str ( fuCutLine( 0, 1000)) + "<br />"
    szHTML += str ( fuCutLine( 1, 1000)) + "<br />"
    szHTML += str ( fuCutLine( 2, 1000)) + "<br />"
    szHTML += str ( fuCutLine( 3, 1000)) + "<br />"
    szHTML += str ( fuCutLine( 4, 1000)) + "<br />"
    szHTML += str ( fuCutLine( 5, 1000)) + "<br />"
    szHTML += str ( fuCutLine( 6, 1000)) + "<br />"
    szHTML += str ( fuCutLine( 7, 1000)) + "<br />"
    szHTML += str ( fuCutLine( 8, 1000)) + "<br />"


    draw = ImageDraw.Draw(imgBox)
    draw.rectangle( (
         0 , 0 ,
        fuCutLine( 1 ),
        fuCutLine( 1, int ( iSize * fGoldenRatio) ),
        ), (0,0,0,128), outline="blue")
    del draw
    imgBox.save("." + szPathToFile, "PNG")

# отладка
    szHTML += "<center><img src='%s' />" % szPathToFile
    szHTML += u"<br />Время выполнения: %s" % \
              str( datetime.datetime.now( timezone.get_default_timezone( ) ) - tmStart )
# отладка
    return HttpResponse ( szHTML )
