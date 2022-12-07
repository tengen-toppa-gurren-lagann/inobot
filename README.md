# inobot

## Описание
Телеграм-бот для чата, поддерживающий классовое неравенство.

## Возможности
- **Добавляет метку пользователю и выводит соответствующий ответ в зависимости от неё** - основной функционал проекта
- **Команда ```/start```** - старт и регистрация в базе данных бота. Если пользователь не был зарегистрирован, выдастся приветственное сообщение, иначе - уведомление, что пользователь в базе уже присутствует.
- **Команда ```/help```** - получение информации о командах бота.
- **Команда ```/Хто_я```** - информирует пользователя о его статусе и правах (является ли он администратором).
- **Команда ```/Госуслуги```** - вызывает меню с кнопками для контроля бота.
  - **Меню** содержит в себе 4 кнопки с различным функционалом.
    - **Кнопка ```Список иноагентов```** - осуществляет обращение к базе данных и выводит списком всех, кто отмечен как иноагент.
- - Функционал всех кнопок ниже доступен только обладателю статуса администратора.
    - **Кнопка ```Оповестить```** - аналогична предыдущей функции, но вместо списка выдаёт сообщение, в котором происходит упоминание всех отмеченных лиц.
    - **Кнопка ```Добавить иноагента```** - меняет в базе данных метку регалии "иноагент" на положительную для конкретного пользователя.
      - Для всех пользователей с такой меткой каждое их сообщение, не являющееся командой или вызовом кнопки помечается соответствующей плашкой.
    - **Кнопка ```Амнистировать иноагента```** - меняет в базе данных метку регалии "иноагент" на отрицательную для конкретного пользователя.
- ## Запуск проекта
- Для начала требуется склонировать репозиторий:

```git clone https://github.com/tengen-toppa-gurren-lagann/inobot.git```

- Потом следует выбрать один из видов запуска проекта, которые разобраны в главах ниже.
- После успешного запуска следует перейти в Telegram ```https://web-telegram.ru/```
- Создадим новый чат с нашим ботом, для этого найдите его по тегу ```@inoagentsbot```

![Find bot ](examples/2.PNG)

- Нажимаем на кнопку ```start``` или вводим аналогичную команду и можем начинать пользоваться ботом. Весь функционал описан в разделе ```Возможности```

### Обычный запуск проекта
Запустите проект в среде PyCharm путем выбора необходимой папки (см. рис ниже):

![Open Project](examples/3.PNG)

Затем настройте интерпретатор Python, для этого перейдите ```File->Settings->Project:inobot->Python Interpreter``` и выполните следующую настройку:

![Open Project](examples/4.PNG)

Теперь следует добавить все необходимые библиотеки в проект, для этого следует в консоли ввести следующую команду:
```pip install -r requirements.txt```
Можно использовать консоль прямо из Pycharm, как показано ниже

![Open Project](examples/5.PNG)

Или же перейти в папку проекта и добавить их через обычную консоль, как показано ниже

![Open Project](examples/6.PNG)

Теперь откройте файл ```main.py``` и на строке 15 запустите бота:

![Start Bot](examples/7.PNG)

Если при запуске возникли какие-то сбои, то для проверки перейдите в окно подключенных модулей и проверьте их в соответствии со следующим фото:

```File->Settings->Project:inobot->Python Interpreter```

![Packages](examples/8.PNG)

### Запуск проекта при помощи Docker
При помощи командной строки перейдите в папку проекта и проверьте наличие всех файлов:
```cd PyCharmProjects/inobot```

![Docker Check Files](examples/9.PNG)

Теперь создайте образ при помощи следующей команды:
```sudo docker build -t dockerfile .```

![Docker Build Image](examples/10.PNG)

После создания образа его можно запустить в Docker Desktop:

![Docker Run Image](examples/11.PNG)

## Пример работы проекта

Теперь перейдем в Telegram и найдем нашего бота:

![Usage 1](examples/2.PNG)

Начнем работу:

![Usage 2](examples/bot-1.PNG)

Введём ```/help```:

![Usage 3](examples/1.PNG)

Введём ```/Хто_я```:

![Usage 4](examples/bot-2.PNG)

Введём ```/Госуслуги```:

![Usage 5](examples/bot-3.PNG)

Если была нажата кнопка ```Список иноагентов```:

![Usage 6](examples/bot-4.PNG)

Если была нажата кнопка ```Оповестить```:

![Usage 7](examples/bot-5.PNG)

Если была нажата кнопка ```Добавить иноагента```:

![Usage 8](examples/bot-6.PNG)

Если была нажата кнопка ```Список иноагентов``` после этого:

![Usage 9](examples/bot-7.PNG)

Если была нажата кнопка ```Амнистировать иноагента```:

![Usage 10](examples/bot-8.PNG)

Если была нажата кнопка ```Список иноагентов``` после этого:

![Usage 11](examples/bot-9.PNG)

Сообщение, которое прикрепляет бот к пользователю, имеющему статус иноагента:  

![Usage 12](examples/bot-10.PNG)
