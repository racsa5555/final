## Для начала работы с программой необходимо выполнить в терминале следующие действия

> [!IMPORTANT]
> У вас должен быть установлен **Python** и **Visual Studio Code**.


- [ ] Необходимо скопировать файлы с **Github**.

```
cd Desktop/
git clone {ssh ссылка репозитория}

```
далее переходим в папку проекта

```
cd final/
```
- [ ] Необходимо создать файл **.env**.

Открываем файл ```env.txt``` и меняем его название на ```.env```.

## Приступаем к работе с приложением 

> [!NOTE]
> Если у вас запущен **postgresql** и **redis**, то необходимо остановить их процесс.
>```
>sudo service posgresql stop
>sudo servise redis stop
>```

- [ ] Запуск Docker-compose

```
sudo apt update
sudo apt install docker.io
sudo apt install docker-compose
sudo chown $USER /var/run/docker.sock
docker-compose up --build

```

> [!TIP]
> Для полной информации о запросах перейдите по [ссылке](http://34.16.110.19//api/swagger/).
