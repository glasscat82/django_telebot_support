# тг. бот службы технической поддержки
```
(или прокси бот)
в файле .env  токен и chat_id администратора-менеджера
пользователи пишут боту он отправляет сообщение админам [chat_id]
чтобы узнать chat_id набрать /getchatid
(или добавить бот в чат узнать id чата, и добавить в [chat_id, -chat_id])
```

## Django + Webhook + pyTelegramBotAPI

```
$ cp .env.example .env
```

```
$ pip install -r requirements.txt
```

## Сервис для проброса тунеля https://serveo.net/
позволяет тестировать bot на setWebhook
```
ssh -R 80:127.0.0.1:8000 serveo.net
```

## api на Django для bota
serveo - возвращает url который будит вашим api для телеграм бота
```
toket_you_bot = ''
api_from_telegram = https://ebdca775c7494a7816d05534479b1d93.serveo.net/bots/{toket_you_bot}/
```

## установить setWebhook для бота
```
https://api.telegram.org/bot{toket_you_bot}/setWebhook?url=https://ebdca775c7494a7816d05534479b1d93.serveo.net/bots/{toket_you_bot}/
```