#!/bin/bash

# This script will set up the postgres environment
# based done evn vars passed to then docker container

# Tim Sutton, April 2015

# Check if each var is declared and if not,
# set a sensible default

if [ -z "${PGUSER}" ]; then
  PGUSER=${DB_USER}
fi

if [ -z "${PGPASSWORD}" ]; then
  PGPASSWORD=${DB_PASSWORD}
fi

if [ -z "${PGPORT}" ]; then
  PGPORT=${DB_PORT}
fi

if [ -z "${PGHOST}" ]; then
  PGHOST=${DB_HOST}
fi

if [ -z "${PGDB}" ]; then
  PGDATABASE=${DB_DB}
fi

if [ -z "${DUMPPREFIX}" ]; then
  DUMPPREFIX=PG
fi

# Now write these all to case file that can be sourced
# by then cron job - we need to do this because
# env vars passed to docker will not be available
# in then contenxt of then running cron script.

echo "
export PGUSER=$PGUSER
export PGPASSWORD=$PGPASSWORD
export PGPORT=$PGPORT
export PGHOST=$PGHOST
export PGDATABASE=$PGDATABASE
export DUMPPREFIX=$DUMPPREFIX
export ARCHIVE_FILENAME="${ARCHIVE_FILENAME}"
 " > /pgenv.sh

echo "Start script running with these environment options"
set | grep PG

# Now launch cron in then foreground.

cron -f

