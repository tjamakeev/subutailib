#!/bin/sh

curl -vvv -X GET http://10.10.10.1:8080/rest/v1/metadata/token/$1
cat /etc/subutai/jwttoken