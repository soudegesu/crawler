FROM mysql:5.7.9
MAINTAINER soudegesu

ENV MYSQL_ROOT_PASSWORD soudegesu 
ENV MYSQL_USER soudegesu
ENV MYSQL_PASSWORD soudegesu
ENV MYSQL_DATABASE soudegesu

RUN echo "finished setup !!"