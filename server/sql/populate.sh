#!/bin/bash

if [ $# -ne 1 ]
then
	echo "USAGE $0 <db_file>"
	exit 1
fi

SQL_PATH=.
DB_PATH="$1"

cat ${SQL_PATH}/{clients.sql,accounts.sql} | sqlite3 "${DB_PATH}"
