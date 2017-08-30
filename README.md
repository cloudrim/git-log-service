# cloc-service

it is a api service to get "GET/POST/DELETE/PUT" method from front end.

it send them to rabbitmq and there has many "worker" to solve them to data.

## init 

### create db

before you run the app, you should add one database in your mysql named "cloc_db" uses utf-8 format. then other things will be handled by
this app via flask-sqlalchemy.

### create user

```shell
CREATE USER 'cloc_user'@'%' IDENTIFIED BY 'cloc=123';
```

### create database

```shell
CREATE SCHEMA `cloc` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci
```