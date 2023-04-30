FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Actualiza los repositorios y paquetes existentes
RUN apt-get update && apt-get -y upgrade

# Instala Apache, PHP y MySQL
RUN apt-get -y install apache2 php mysql-server

# Instala phpMyAdmin
RUN apt-get -y install phpmyadmin

# Configura el servidor de Apache para que pueda servir archivos de phpMyAdmin
RUN ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin

# Crea el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos
COPY requirements.txt /app
# Copia la aplicación
COPY . /app

# Configura las variables de entorno para phpMyAdmin
ENV PMA_HOST=db
ENV PMA_PORT=3306
ENV PMA_ARBITRARY=1
RUN sed -i "s/\$dbserver='localhost';/\$dbserver='127.0.0.1';/" /etc/phpmyadmin/config-db.php

# Configura la contraseña para el usuario root de MySQL
#RUN service mysql start && mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234';"


RUN service mysql start && \
    mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234';" && \
    mysql -u root -p1234 -e "CREATE DATABASE idrink_db;" && \
    mysql -u root -p1234 idrink_db < idrink_db.sql


# Habilita el módulo PHP de Apache
RUN phpenmod mysqli


ENV TZ=UTC
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1






# Instala dependencias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip python3-setuptools python3-wheel \
    default-libmysqlclient-dev gcc mysql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala los requerimientos
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt


RUN phpenmod mysqli

# Configura el servidor de Apache para que pueda servir archivos de phpMyAdmin
RUN ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin

# Configura las variables de entorno para phpMyAdmin
ENV PMA_HOST=db
ENV PMA_PORT=3306
ENV PMA_ARBITRARY=1
RUN sed -i "s/\$dbserver='localhost';/\$dbserver='127.0.0.1';/" /etc/phpmyadmin/config-db.php
EXPOSE 80
EXPOSE 3306
EXPOSE 8000
# Inicia Apache y MySQL en primer plano
CMD service mysql start && service apache2 start && cd /app && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload



