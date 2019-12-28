#!/bin/bash

API_URL=https://owqa8nw4t3.execute-api.ap-northeast-1.amazonaws.com/dev/test
IP_ADDR=`curl -s https://api.ipify.org/`
curl ${API_URL} \
    -X POST \
    -H "x-api-key:$R53_DDNS_API_KEY" \
    -H 'Content-Type: application/json' \
    -d "{'ip':'${IP_ADDR}'}"
