> Автор данного бота не пропагандирует и не одобряет любые действия, которые могут нарушать авторские права. Бот предназначен исключительно для образовательных и информативных целях.
# Зависимости и прочие детали
`pip install -r requirements.txt`

а также (в строках 8-17):

`# Необходимо вставить данные своего сервера`
`connection = mysql.connector.connect(`
`    host="",`
`    user="",`
`    password="",`
`    database=""`
`)`
``
`# Необходимо вставить свой API Telegram Bot`
`bot = telebot.TeleBot('')`
