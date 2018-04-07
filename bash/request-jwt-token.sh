#!/bin/sh

ip=`hostname --ip-address`
echo $ip
curl -vvv -X GET http://10.10.10.1:8080/rest/v1/metadata/token/$ip
#cat /etc/subutai/jwttoken