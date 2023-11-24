# Файловое хранилище




Для начала работы:
В терминале:
1) cd dev-compose
2) docker compose up --build -d
3) docker compose -it app /bin/bash
4) composer update
5) mv .env.example .env
6) php artisan cache:clear
7) composer dump-autoload
8) php artisan key:generate
9) php artisan storage:link

Для включения:

1) cd dev-compose
2) docker compose up  -d

Для Re:Build :
В файловом хранилище:
1) В app/public удалить все символьные ссылки( по умолч: storage)
В терминале:
1) cd dev-compose
2) docker compose up --build -d
3) docker compose -it app /bin/bash
4)  php artisan storage:link
