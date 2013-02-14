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
import PIL                                      # библиоткеа работы с графикой
from PIL import Image, ImageDraw

# import tzinfo
# import random

def indicator ( request ) :
    szHTML = ""
    tmStart = datetime.datetime.now( timezone.get_default_timezone( ) )  # <-- для отладки, измерялка скорости
    szPathToFile = "/static/img/test.png"      # <-- путь будем вычислять и сворачивать в хеш
                                                # каждому тикеру для каждой даты отдельный имидж
    iSize = 480
    image = Image.new("RGBA", (iSize, iSize), (0,0,0,128) )
    draw = ImageDraw.Draw(image)
    draw.ellipse( (20,20,460,400), fill="yellow", outline="blue")
    del draw
    image.save("." + szPathToFile, "PNG")

# отладка
    szHTML += "<center><img src='%s' />" % szPathToFile
    szHTML += u"<br />Время выполнения: %s" % \
              str( datetime.datetime.now( timezone.get_default_timezone( ) ) - tmStart )
# отладка
    return HttpResponse ( szHTML )
