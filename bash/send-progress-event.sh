#!/bin/bash

source ./request-jwt-token.sh

token=`cat /etc/subutai/jwttoken`

array1=(`echo $token | sed 's/\./\n/g'`)
array2=(`echo ${array1[1]} | base64 --decode | sed 's/,/\n/g'`)
array3=(`echo ${array2[0]} | sed 's/["{]//g' | sed 's/:/\n/'`)
subutaiOrigin=${array3[1]}

`cat progress-event.json | sed s/\$\{subutaiOrigin\}/${subutaiOrigin}/g > temp-event.json`

curl -vvv -X POST http://10.10.10.1:8080/rest/v1/metadata/event -d @temp-event.json -H "Content-type: application/json" -H "Authorization: Bearer $token"