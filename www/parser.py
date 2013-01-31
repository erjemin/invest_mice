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


def parsRBC ( request, szCheckTIKER = "ALL" ) :
    # если вызов проиходит через DJANGO то при отсутствии параметро szCheckTIKER содержит
    # пустую строку. Если это так то заменим ее на "ALL"
    if szCheckTIKER == "" :
        szCheckTIKER = "ALL"

    szHtml = ""
    # Устанавливаем текущее время с метками часового пояаса. Если сделать просто datetime.datetime.now()
    # то получим текущее время без меток часового пояся, так что делаем так:
    szHtml += datetime.datetime.now(timezone.get_default_timezone()).strftime('%d/%m/%Y %H:%M:%S %z (%Z)') + "<br />"


#    try:
#        fileLog = open( "./logs/parser-process.log" , 'a' )
#    except IOError:
#        szHtml += u"%s :лог-файл отсутсвует или поврежден<br />" % "ERROR"
#    else:
#        fileLog.write('HELLO LOG -\n')
#        fileLog.close()


    # try:
    #    iNum = int ( iNum )
    # except ValueError:
    #    raise Http404 ( )
    szHtml += u"Hello world! Привет питон! %s" % szCheckTIKER
    return HttpResponse ( szHtml )

    # формат log-файлов
    # ДЕЙСТВИЕ - РЕЗУЛЬТАТ - [ДАТА][29/Jan/2013:18:29:56 +0400]



