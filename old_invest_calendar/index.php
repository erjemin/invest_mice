<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<?
date_default_timezone_set( 'Europe/Moscow' ) ;
$dtCurentDataTime = time();
$dtCurentDataTime = mktime (12, 0, 0, date('n', $dtCurentDataTime), date('j', $dtCurentDataTime), date('Y', $dtCurentDataTime) );
if ( isset ( $_GET[t] ) && 0 != $_GET[t] )
   $dtCurentDataTime = $_GET[t] ;
$dszMounthRuLong = array('январь','февраль','март','апрель','май','июнь','июль','август','сентабрь','октябрь','ноябрь','декабрь');
$dszMounthRuShort = array('янв','фев','мар','апр','май','июн','июл','авг','сен','окт','ноя','дек');
$dszWeekDayRuLong = array('воскресенье','понедельник','вторник','среда','четверг','пятница','суббота','воскресенье');
$dszWeekDayRuShort = array('вс','пн','вт','ср','чт','пт','сб','вс');

// http://lect.by.ru/lekcium/nymeng.htm
// http://web.archive.org/web/20080504163207/http://home.att.net/~srschmitt/lunarphasecalc.html
// http://aztips.blogspot.com/2010/06/php.html

// http://ru2.php.net/manual/en/pdostatement.fetchall.php
// http://www.php.ru/manual/language.operators.arithmetic.html
?>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Поведение российский биржевых индексов <? echo date('d', $dtCurentDataTime) . '-' . $dszMounthRuShort[date('n', $dtCurentDataTime)-1] . '-xxxx (' . $dszWeekDayRuShort[date('w', $dtCurentDataTime)] . ')' ; ?></title>

<style type="text/css">
* {			/* стандартный прием для перегрузки стилей reset.css */
    padding:0;
    margin:0;
    }

.calendar { 	/* Оформление длока календаря */
	float:left;
	background-color:#FFC;
	font-size:4em;
	padding:20px;
	text-align:center;
	text-shadow:#999;
	width:48%; }
.weekday {		/* Оформление "день недели" */
	font-family: "Times New Roman", Times, serif, serif;
	float:left;
	background-color:#FF9;
	font-weight:400; }
.day {			/* Оформление "число" */
	font-family: "Times New Roman", Times, serif;
	float:left;
	background-color: #CFC;
	font-size:2.4em;
	font-weight:800;
	letter-spacing:-.1em;
	-webkit-border-radius:0.1em;
    -moz-border-radius:0.1em;
    border-radius:0.1em;
    -webkit-box-shadow:0.1ex 0.1ex 0.1ex rgba(0,0,0,.2);
    -moz-box-shadow:0.1ex 0.1ex 0.1ex rgba(0,0,0,.2);
    box-shadow:0.1ex 0.1ex 0.1ex rgba(0,0,0,.2);
	}
.MoYe {			/* Оформление "Месяц и Год"*/
    font-family: "Times New Roman", Times, serif, serif;
	float:left;
	background-color:#FFF;
	font-size:.6em;
	font-weight:100
	}
.nc {			/* Навигация-календарь (NaviCalendar)  */
    border:none;
	padding-left:0.7em;
	padding-top:0.2em;
	font-size:0.25em;
	}
.ncH {			/* Навигация-календарь Заголовок (NaviCalendar Header) вложен в CLASS:nc)  */
    font-weight:bold;
	color:#006;
	}
.ncH th {
    padding-left:0.3em;
	padding-right:0.3em;
	}
.ncHwknd {
	color:#F30;
	}
.ncT, .ncA, .ncTwknd, .ncAwknd {
    -webkit-border-radius:0.5em;
    -moz-border-radius:0.5em;
    border-radius:0.5em;
	-webkit-box-shadow:0.3em 0.3em 0.3em rgba(0,0,0,.2);
    -moz-box-shadow:0.3em 0.3em 0.3em rgba(0,0,0,.2);
    box-shadow:0.3em 0.3em 0.3em rgba(0,0,0,.2);
	}
.ncT, .ncTwknd, .ncA, .ncAwknd  {			/* Навигация-календарь День (NaviCalendar Header) вложен в CLASS:nc)  */
    padding:0.3em;
    font-weight:lighter;
	}
.ncT {			/* Навигация-календарь День (NaviCalendar Header) вложен в CLASS:nc)  */
	background-color:#CFC;
	}
.ncTwknd {			/* Навигация-календарь День (NaviCalendar Header) вложен в CLASS:nc)  */
	background-color:#AFA;
	}
/* .ncT:before , .ncTwknd:before {
	content: "X";
    } */
.ncA, .ncAwknd {			/* Навигация-календарь День (NaviCalendar Header) вложен в CLASS:nc)  */
    background-color:#FFC;
	}
.ncAwknd {			/* Навигация-календарь День (NaviCalendar Header) вложен в CLASS:nc)  */
    background-color:#EFC;
	}
.ncT a, .ncTwknd a,  .ncA a, .ncAwknd a {
	border-bottom:1px dotted;
	text-decoration:none;
	color:#399;
   }
.ncT a:link, .ncTwknd a:link {
    color:#003;
   }
.ncA a:link, .ncAwknd a:link  {
    color:#999;
   }
.ncT a:visited, .ncTwknd a:visited {
    color:#063;
   }
.ncA a:visited, .ncAwknd a:visited {
    color:#9C9;
   }
.ncT a:hover, .ncT a:active, .ncTwknd a:hover, .ncTwknd a:active {
	color:#f00;
   }
.ncA a:hover, .ncA a:active, .ncAwknd a:hover, .ncAwknd a:active {
	color:#f99;
   }
</style>
</head>
<body>

<h1 style="background-color:#60F;">Поведение российский биржевых индексов <? echo date('d', $dtCurentDataTime) . '-' . $dszMounthRuShort[date('n', $dtCurentDataTime)-1] . '-xxxx' ; ?></h1>

<?


//function foo($arg_1, $arg_2, /* ..., */ $arg_n)
//{
//    echo "Example function.\n";
//    return $retval;
//}

echo '<div class="calendar"><span class="weekday">' . $dszWeekDayRuLong[date('w', $dtCurentDataTime)]
   . '</span><br /><span class="day">'
   . date('d', $dtCurentDataTime) . '</span><span class="MoYe">&nbsp;'
   . $dszMounthRuLong[date('n', $dtCurentDataTime)-1] . ', ' . date('Y', $dtCurentDataTime) . '&nbsp;</span>';



$iCount = mktime (12, 0, 0, date('n', $dtCurentDataTime), 1, date('Y', $dtCurentDataTime) ); // Ставим маркер $iCount на первое число месяца
// **************************************************************************************************
//
// Кусок кода ниже, нужен из-за того что в России неделя начинается с пондельника а не с воскресенья
//
// **************************************************************************************************
if ( 0 == date ( 'w', $iCount ) )		// ЕСЛИ :: Первое число месяца пришлось на воскресенье (0)
   $iCount -= 86400 * 6 ;				// ТО :: Ставим маркер $iCount на 6 дней назад (захватить предыдущий месяц)
elseif ( 1 == date ( 'w', $iCount ) )	// ЕСЛИ :: Первое число месяца пришлось на понедельник (1)
   $iCount -= 86400 * 7 ;				// ТО :: Ставим маркер $iCount на неделю назад (иначе на предыдущий месяц не перейти)
else 									// ЕСЛИ :: Первое число месяца пришлось на вт-сб (2-6)
   $iCount -= 86400 * ( date ( 'w', $iCount ) - 1 ) ; // ТО :: перемещаем метку $iCount на ближайший (последний) предыдущего месяца

//
// Навигация по календарю
//
echo '<table class="nc">';
echo '<tr class="ncH">';
for ( $iCount1 = 0 ; $iCount1 < 14 ; $iCount1++ )
   if ( $iCount1 == 5 || $iCount1 == 6 || $iCount1 == 12 || $iCount1 == 13 )		// условие определения выходных ("сб" и "вс"
     echo '<th class="ncHwknd">' . $dszWeekDayRuShort[1 + $iCount1 % 7] . '</th>';	// добавляем стиль для оформления выходных
   else
     echo '<th>' . $dszWeekDayRuShort[1 + $iCount1 % 7] . '</th>';					// обычные дни
echo '</tr>';
do {
  echo '<tr class="ncD">';
  for ( $iCount1 = 0 ; $iCount1 < 14 ; $iCount1++, $iCount += 86400 ) {
     if ( date('n', $iCount) == date('n', $dtCurentDataTime) )
	   echo '<td class="ncT';
	 else
	   echo '<td class="ncA';
     if ( $iCount1 == 5 || $iCount1 == 6 || $iCount1 == 12 || $iCount1 == 13 )		// условие определения выходных
	   echo 'wknd';																	// добавляем суфикс стиля "wknd" для оформления выходных
	 echo '"><a href="?t=' . ($iCount). '">' . date('d', $iCount) . '</a></td>';
	 }
  echo '</tr>';
} while ( date('n', $iCount) == date('n', $dtCurentDataTime) );
echo '</table>';

echo '</div><br clear="all" />';
echo 'время:       ' . date('H:i:s', $dtCurentDataTime) . '<br />';

// echo '<tt><b><a href="?t=' . ($dtCurentDataTime - 86400). '">&lt;&lt; Предыдущий день</a> | <a href="index.php">Сегодня</a> | <a href="?t=' . ($dtCurentDataTime + 86400) . '">Следующий день &gt;&gt;</a></b></tt> ' .  '<br />';

// $arNameIndex = array (	'MICEX10INDEX',	'MICEXBNDPRCI',	'MICEXCBICP',	'MICEXCBICP3Y',	'MICEXCBICP5Y',
//						  'MICEXCBIGP', 	'MICEXCBIGP3Y',	'MICEXCBIGP5Y',	'MICEXCBITR',	'MICEXCBITR3Y',
//						  'MICEXCBITR5Y',	'MICEXCGS',		'MICEXCHM',		'MICEXFNL',		'MICEXINDEXCF',
//						  'MICEXLC',		'MICEXMANDM',	'MICEXMBICP',	'MICEXMBIGP',	'MICEXMBITR',
//						  'MICEXMC',		'MICEXMNF',		'MICEXOANDG',	'MICEXPWR',		'MICEXSC',
//						  'MICEXTLC',		'RGBI',			'RGBIG',		'RGBITR',		'RTS2',
//						  'RTScr',		'RTSeu',		'RTSfn',		'RTSI',			'RTSin',
//						 	'RTSmm',		'RTSog',		'RTSSIB',		'RTSSTD',		'RTStl',
//						 	'TECHIND',		'TECHINDBOND',	'TECHINDSHARE' );

 $arNameIndex = array ( 'MICEXINDEXCF',	// Индеск ММВБ
					   'RTSI',);		// Индекс РТС

// Соединяемся с БД
try {
  $db = new PDO ('mysql:host=фиг_вам;dbname=db_invest_index', 'erjemin' , 'нескажу' );
  $qIndexValueList = $db->query(
	'SELECT UNIX_TIMESTAMP( tbIndexValue.tmDATE ) as tmDATE2,
			tbIndexValue.szTICKER,
	 	    tbIndexValue.fCLOSE,
			tbIndexValue.fCLOSEpercent,
			tbIndexName.szTICKERfullnameRU,
			tbIndexName.szTICKERfullnameEN
     FROM   tbIndexName INNER JOIN tbIndexValue
                        ON tbIndexName.szTICKER = tbIndexValue.szTICKER
	 WHERE  DAYOFMONTH( tbIndexValue.tmDATE ) = ' . date('d', $dtCurentDataTime)
	      . '&& MONTH( tbIndexValue.tmDATE ) = ' . date('n', $dtCurentDataTime) . '
     ORDER BY tbIndexValue.tmDATE' );
    }
catch (PDOException $err) {
  echo 'Что-то пошло сикось накось... похоже нет коннекта к базе данных. Кина не будет.<br />';
  header('Location: http://google.com'); // переадресация на страницу ERROR
  }
// Рисуем Два Главных Индекса
// Находим максимум и минимум, что бы псле по ним отнормировать цвет



// Начинаем рисовать таблицу.
echo 'коннект с БД есть. В запросе вернулось <b>' . $qIndexValueList->rowCount() . '</b> строк<br />' ;
$qrIndexValueList = $qIndexValueList->fetchAll( PDO::FETCH_ASSOC );
echo '<table border=0 style="font-family:\'Courier New\',Courier,monospace; white-space:pre">';
// Выводим список годов
echo '<tr><th colspan="2">ИНДЕКС</th>';
for ($iYear = date( 'Y', $qrIndexValueList[0][tmDATE2] ) ; $iYear < date('Y', $dtCurentDataTime) ; $iYear++ )
  echo '<th>' . $iYear . '</th>';
echo '<th>Среднее значение</th></tr>';

for ( $iCountIndex = 0 , $iTotalIndex = count($arNameIndex) ; $iCountIndex < $iTotalIndex ; $iCountIndex++ )
  {


  // Выводим значения для MICEXINDEXCF
  echo '<tr><td>'. $arNameIndex[$iCountIndex] . '</td><td style="font-size:xx-small">какой-то индекс?</td>';
  $fAverageValue = 0;
  $iCountOfValue = 0;
  for ($iYear = date( 'Y', $qrIndexValueList[0][tmDATE2] ) ; $iYear < date('Y', $dtCurentDataTime) ; $iYear++ )
    {
	for ( $iCount = 0 ; $iCount < $qIndexValueList->rowCount() ; $iCount++ )
	   if ( ( $iYear == date( 'Y', $qrIndexValueList[$iCount][tmDATE2] ) ) &&
		  ( $qrIndexValueList[$iCount][szTICKER] == $arNameIndex[$iCountIndex] ) )
	     {
		 $iCountOfValue++;
		 $fAverageValue = $fAverageValue + $qrIndexValueList[$iCount][fCLOSEpercent];
		 if ( $qrIndexValueList[$iCount][fCLOSEpercent] >= 0 )
	        printf ('<td bgcolor=#00CC66 title="%s=%3.2f">+%01.2f%%</td>', $arNameIndex[$iCountIndex] , $qrIndexValueList[$iCount][fCLOSE], $qrIndexValueList[$iCount][fCLOSEpercent]*100 );
		 else
	        printf ('<td bgcolor=#FF6666 title="%s=%3.2f">%01.2f%%</td>', $arNameIndex[$iCountIndex] , $qrIndexValueList[$iCount][fCLOSE], $qrIndexValueList[$iCount][fCLOSEpercent]*100 );
		 $iCount = 0;
		 break;
	     }
	if ( $iCount == 0 )
	   continue;
	else
 	  echo '<th bgcolor="silver">-</th>';
    }

  if ( $iCountOfValue != 0 )
    if ( $fAverageValue >= 0 )
      printf ('<th bgcolor=#00CC66>+%01.2f%%</th></tr>', 100*$fAverageValue/$iCountOfValue );
    else
      printf ('<th bgcolor=#FF6666>%01.2f%%</th></tr>', 100*$fAverageValue/$iCountOfValue );
  else
    echo '<th bgcolor="silver">-</th>';

  }
  echo '</table>';

  $db = null;



?>


<br /><!--Rating@Mail.ru counter-->
<script language="javascript" type="text/javascript"><!--
d=document;var a='';a+=';r='+escape(d.referrer);js=10;//--></script>
<script language="javascript1.1" type="text/javascript"><!--
a+=';j='+navigator.javaEnabled();js=11;//--></script>
<script language="javascript1.2" type="text/javascript"><!--
s=screen;a+=';s='+s.width+'*'+s.height;
a+=';d='+(s.colorDepth?s.colorDepth:s.pixelDepth);js=12;//--></script>
<script language="javascript1.3" type="text/javascript"><!--
js=13;//--></script><script language="javascript" type="text/javascript"><!--
d.write('<a href="http://top.mail.ru/jump?from=1603042" target="_top">'+
'<img src="http://d5.c7.b8.a1.top.mail.ru/counter?id=1603042;t=216;js='+js+
a+';rand='+Math.random()+'" alt="Рейтинг@Mail.ru" border="0" '+
'height="31" width="88"><\/a>');if(11<js)d.write('<'+'!-- ');//--></script>
<noscript><a target="_top" href="http://top.mail.ru/jump?from=1603042">
<img src="http://d5.c7.b8.a1.top.mail.ru/counter?js=na;id=1603042;t=216"
height="31" width="88" border="0" alt="Рейтинг@Mail.ru"></a></noscript>
<script language="javascript" type="text/javascript"><!--
if(11<js)d.write('--'+'>');//--></script>
<!--// Rating@Mail.ru counter-->



<!-- tt><big><strong>Бот стартует с:</strong></big></tt>
<form action="start.php" method="post">
<input name="szStartURL" type="text" size="80" maxlength="255" />
<br />&nbsp;
<br />
<input name="startform" type="submit" value="    Пуск    " />
<input name="resetform" type="reset"  value="Ой" />
</form -->

</body>
</html>