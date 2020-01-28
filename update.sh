#!/bin/bash

API_URL=https://owqa8nw4t3.execute-api.ap-northeast-1.amazonaws.com/dev/test
IP_ADDR=$(\
  curl -s https://api.ipify.org/ \
    | egrep "^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$" \
) && echo ${IP_ADDR}

if [ ! "${IP_ADDR}" ]; then
  echo [ERROR] !{IP_ADDR} is not IP Address.
  exit 1
fi

curl ${API_URL} \
    -X POST \
    -H "x-api-key:$R53_DDNS_API_KEY" \
    -H 'Content-Type: application/json' \
    -d "{'ip':'${IP_ADDR}'}"

exit 0
