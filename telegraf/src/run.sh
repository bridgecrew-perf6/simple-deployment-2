#!/bin/bash
# Copyright (C) 2021 Scalers.ai

grafana_ip=grafana

# wait until grafana is running and healthy
while [ $(curl -LI http://$grafana_ip:3000/api/health -o /dev/null -w '%{http_code}\n' -s) != "200" ]
do
    echo "Waiting for grafana to start"
    sleep 10
done

# removing the existing grafana auth keys
while [ $(curl -X GET -H "Content-Type: application/json" http://admin:admin@$grafana_ip:3000/api/auth/keys) != "[]" ]
do
    KEY_ID=$(curl -X GET -H "Content-Type: application/json" http://admin:admin@$grafana_ip:3000/api/auth/keys |  cut -d':' -f 2 | cut -d',' -f 1 | sed 's/\}//g')
    curl -X DELETE -H "Content-Type: application/json" http://admin:admin@$grafana_ip:3000/api/auth/keys/$KEY_ID
done

# get Authentication key for telegraf for dashboard creation
AUTH_KEY=$(curl -X POST -H "Content-Type: application/json" -d '{"name":"telegraf", "role": "Admin"}' http://admin:admin@$grafana_ip:3000/api/auth/keys |  cut -d':' -f 4 | sed 's/\}//g')

if [ -z $AUTH_KEY ]
then
    echo "Authenticaion key with name telegraf and role Admin already exists."
    exit 1
fi

# create grafana dashboard with crowd_dashboard.json
curl -X POST --insecure -H "Authorization: Bearer ${AUTH_KEY:1:-1}" -H "Content-Type: application/json"  --data-binary @./crowd_dashboard.json http://$grafana_ip:3000/api/dashboards/db

if [ $?  -ne 0 ]
then
    echo "Dashboard creation failed. Try manual creation of the dashboard"
fi

# update http output plugin in telegraf.conf
sed -i "s/GRAFANA/$grafana_ip/g" /etc/telegraf/telegraf.conf
sed -i "s/Authorization.*/Authorization = \"Bearer ${AUTH_KEY:1:-1}\"/g" /etc/telegraf/telegraf.conf
# start telegraf process
/bin/bash /entrypoint.sh telegraf