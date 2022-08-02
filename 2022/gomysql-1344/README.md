https://github.com/go-sql-driver/mysql/issues/1344

```
$ docker pull mariadb:10.7
$ docker run -e MYSQL_ROOT_PASSWORD=Asd123dsa -p 3306:3306 --rm --name maria mariadb:10.7
$ mysql -uroot -pAsd123dsa -h127.0.0.1 -e 'create database nahry'
$ mysql -uroot -pAsd123dsa -h127.0.0.1 nahry < db.sql
```
