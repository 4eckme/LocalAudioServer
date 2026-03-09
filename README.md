# LocalAudioServer
**Web UI for remote volume contol.**

LocalAudioServer представляет собой **web-интрерфейс для удаленного контроля уровня громкости** устройства из **домашней сети**.<br>
Сервер использует диапазон адресов **192.168.x.x** (если вы используете другой диапазон, поменяйте соответсвующую строчку в коде).<br>
Если хост не доступен из домашней сети, убедитесь что Python добавлен в исключения брандмауэра.<br>
Для контроля уровня громкости используется библиотека <a href="https://github.com/AndreMiras/pycaw">pycaw</a> для **Windows**.

# Установка
<pre>pip install -r requirements.txt</pre>

# Требования
- Windows (7, 8, 10, 11, Server editions)
- Visual C++ Build Tools
- Python 3.12.10 или выше
