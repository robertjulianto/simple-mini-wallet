#!/usr/bin/env bash

usage () {
  echo "Mini Wallet Liquibase";
  echo "===============================================================================";
  echo "usage: liquibase [-e] [-h]";
  echo "[mandatory] -e --env     <value>    Environment [unittest|local]";
  echo "[optional]  -h --help      -- Help";
}

for arg in "$@"; do
  shift
  case "$arg" in
    "--env"       ) set -- "$@" "-e";;
    "--help"      ) set -- "$@" "-h";;
    *             ) set -- "$@" "$arg"
  esac
done

changelog="mini_wallet"
env="local"

while getopts e:h option; do
  case $option in
    (e)
      env=$OPTARG;;
    (h)
      usage;
      exit;;
    (*)
      echo "unknown option: "$option;
      usage;
      exit;;
  esac
done

docker run --rm -v $(pwd)/migrations/changelog:/liquibase/changelog -v $(pwd)/migrations/config:/liquibase/config \
  --link=postgres --entrypoint=/liquibase/liquibase liquibase/liquibase --logLevel=debug \
  --changeLogFile=changelog/"$changelog".postgres.sql --defaultsFile=/liquibase/config/"$env" \
  --defaultSchemaName="$changelog" update
