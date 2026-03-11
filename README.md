<div align="center"><h1>LocalAudioServer</h1>
<b>Web UI for remote volume contol</b>
</div>
<br><br>

LocalAudioServer представляет собой **web-интрерфейс для удаленного контроля уровня громкости** вашего устройства из **домашней сети**.<br>
Сервер использует диапазон адресов **192.168.x.x** (если вы используете другой диапазон, поменяйте соответсвующую строчку в коде *server.py*).<br>
Если хост не доступен из домашней сети, убедитесь что Python добавлен в исключения брандмауэра.

# Install
<pre>pip install -r requirements.txt</pre>

# Start
### Windows:

```start.bat``` для запуска сервера в консоли<br>
```start.vbs``` для запуска в фоновом режиме

Для автозапуска добавьте ярлык на любой из этих файлов в папку автозагрузки приложений.

### Linux:

```python3 server py``` для запуска сервера в консоли<br>
```nohup python server.py > /dev/null 2>&1 &``` для запуска в фоновом режиме

Для автозапуска добавьте в Startup Applications одну из этих команд:<br>
```cd /path/to/LocalAudioServer && python3 server py```<br>
```cd /path/to/LocalAudioServer && nohup python server.py > /dev/null 2>&1 &```

# Requirements
- Windows (7, 8, 10, 11, Server editions)
- Visual C++ Build Tools
- Python 3.8 и выше<br>

or
- Linux

# Preview
<div align="left">
  <img src="https://raw.githubusercontent.com/4eckme/LocalAudioServer/refs/heads/main/screenshots/web-ui.png" height="256" />&nbsp;&nbsp;<img src="https://raw.githubusercontent.com/4eckme/LocalAudioServer/refs/heads/main/screenshots/console.png" height="256" /> 
</div>
