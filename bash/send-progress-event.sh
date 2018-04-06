#!/bin/sh

token=`cat /etc/subutai/jwttoken`
echo $token
curl -vvv -X POST http://10.10.10.1:8080/rest/v1/metadata/event -d @progress-event.json -H "Content-type: application/json" -H "Authorization: Bearer $token"