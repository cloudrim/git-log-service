# cloc-service

it is a api service(producer) to get "GET/POST/DELETE/PUT" method from front end.

it send them to rabbitmq and there has many "worker" to solve them to data and call the api to send the data to database.

## init 

### create db

before you run the app, you should add one database in your mysql named "cloc_db" uses utf-8 format. then other things will be handled by
this app via flask-sqlalchemy.

### create user

```shell
CREATE USER 'gitlog_user'@'%' IDENTIFIED BY 'gitlog=123';
```

### create database

```shell
CREATE SCHEMA `gitlog` DEFAULT CHARACTER SET utf8mb4 ;
```