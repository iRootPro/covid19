# @Covid19notice_bot - Telegram бот для получения оперативной информации о коронавирусной инфекции

Данный бот создан для получения статистики по заболеваемости **Covid-19** через Telegram.

**Бот умеет:**

- Выдавать статистику Online о ситуации в мире по количеству зараженных, умерших и выздоровевших.
- Показывать общую статистику по России, а так же показывать TOP-20 по случаям в регионах.
- Строить график TOP10 стран, где отображены такие данные как: количество зараженных, смертей и вылечившихся.
- Генерировать общие графики по заболеваемости, смертях и выздоровлениях, чтобы можно было отследить динамику развития коронавирусной инфекции.
- Отвечать на вопросы, связанные с covid-19.

Бот уже установлен и им могут пользоваться все желающие. Для этого в Telegram нужно найти *@Covid19notice_bot* и нажать на кнопку ``start``.

## Примеры работы бота:
![](img/preview.gif)



## Как установить?

Если по каким-то причинам Вам необходимо установить копию бота, то следует следовать следующим инструкциям:

Python3 должен быть уже установлен в системе.
Используя `pip` или `pip3` (если есть конфликт с python2) необходимо установить зависимости:

```
pip install -r requirements.txt
```

Рекомендуется использовать виртуальное окружение для изоляции проекта.
Подробности: [virtualenv/venv](https://docs.python.org/3/library/venv.html).

**Для работы бота вам потребуется сервер. Я использую VDS с досточно скромными характеристиками: *1x2.2ГГц, 1Гб RAM, 20Гб HDD* под управлением *Linux Ubuntu.***

Для работы с графиками, а именно для их сохранения с последующей отправкой в Telegram необходимо установить *orca*. 

Переходим по [ссылке](https://github.com/plotly/orca/releases) и скачиваем в домашнюю папку последнюю версию. На момент написания это [orca-1.3.1.AppImage](https://github.com/plotly/orca/releases/download/v1.3.1/orca-1.3.1.AppImage).

Распаковываем архив в домашней директории. Для того, чтобы система "видела" необходимые файлы создаем символьную ссылку:

```shell
ln -s /home/sasha/covid19/orca-1.3.0.AppImage /usr/local/sbin/orca
```

Проверяем с помощью ```which```:

```shell
sasha@ruvds-b74hk:~/covid19$ which orca
/usr/local/sbin/orca
sasha@ruvds-b74hk:~/covid19$ 
```

### Необходимые настройки

Все настройки хранятся в файле `.env`, создайте его в корне со скриптами.

Нам понадобится Telegram **TOKEN**, для его получения обратитесь к *@botfather*, создайте новый бот, после чего вам выдадут ключ.

В файл `.env` добавить:

```
TELEGRAM_TOKEN=ВАШ_TELEGRAM_TOKEN
```

Для формирования графиков, а также получение и сохранения данных используется ```crontab```. Подробно с ```crontab``` можно ознакомиться [здесь](https://help.ubuntu.ru/wiki/cron).

Для редактирования необходимо запустить команду ```crontab -e```. Вот так выглядит мой файл:

```shell
*/30 * * * * cd /home/sasha/covid19/ ; /usr/bin/python3 /home/sasha/covid19/gen_graph.py >> ~/cron.log 2>&1
10 0 * * * cd /home/sasha/covid19/ ; /usr/bin/python3 /home/sasha/covid19/data.py >> ~/cron.log 2>&1
*/5 * * * * cd /home/sasha/covid19/ ; /usr/bin/python3 /home/sasha/covid19/data_current.py >> ~/cron.log 2>&1
0 1 * * * cd /home/sasha/covid19/ ; /usr/bin/python3 /home/sasha/covid19/total_graphs.py >> ~/cron.log 2>&1
* */2 * * * cd /home/sasha/covid19/ ; /usr/bin/python3 /home/sasha/covid19/parse_rus.py >> ~/cron.log 2>&1
```

**gen_graph.py** - скрипт, который формирует график TOP10 стран. Так как данные собираются со всех стран, у меня генерация такого графика происходит раз в 30 минут.

**data.py** - скрипт раз в сутки собирает данны суммарные, а также по всем странам и записывает в файл для дальнейшего построения графиков.

**data_current.py** - каждые 5 минут собирает информацию по странам и записывает в файл.

**total_graph.py** - раз в сутки создает три графика о динамике заболеваемости, смертности и выздоровевших.

**parse_rus.py** - парсит данные каждые 2 часа для России.

Все временные значения вы можете регулировать самостоятельно, исходя из ваших потребностей.



Для автоматического запуска бота делаем скрипт, он может быть таким:

```shell
[Service]
WorkingDirectory=/home/sasha/covid19
User=sasha
ExecStart=/usr/bin/python3 main.py

[Install]
WantedBy=multi-user.target

```

Редактируем скрипт запуска под себя: изменяем имя пользователя, домашнюю директорию, а также путь к python3, если он у вас отличается. Путь к python3 можно узнать командой: ```which python3```.

Сохраняем под именем **covid19.service** и помещаем в ```/etc/systemd/system```.

**Запуск:**

```shell
systemctl start covid19
```

**Перезапуск:**

```shell
systemctl restart covid19
```

**Проверка статуса:**

```she
systemctl status covid19
```

Если всё сделано правильно, то должны получить подобное:

```shell
● covid19.service
   Loaded: loaded (/etc/systemd/system/covid19.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2020-04-07 22:16:35 MSK; 10h ago
 Main PID: 3031 (python3)
    Tasks: 8 (limit: 1094)
   CGroup: /system.slice/covid19.service
           └─3031 /usr/bin/python3 main.py
```



## Цель проекта

Данный проект сделан исключительно в образовательных целях, как способ изучения языка **Python** на реальной задаче.

### Контакты

Если у вас есть вопросы или идеи, что добавить/сделать что-то по другому, буду рад вашему отклику.

Связаться со мной можно по электронной [почте](mailto:admin@armavir.ru) или через [Telegram](https://tele.click/irootpro).

