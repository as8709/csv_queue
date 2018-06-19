FROM postgres:10

ENV POSTGRES_USER root
ENV POSTGRES_PASSWORD rootroot
COPY csv.sql /docker-entrypoint-initdb.d/
COPY postgresql.conf /etc/postgresql/postgresql.conf

EXPOSE 5432

