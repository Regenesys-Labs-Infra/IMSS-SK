#!/bin/bash
# UC-04: AI-generated restart script with planted SAFETY defects. Find at least 3 before fixing.
SERVICE=$1
echo "Restarting $SERVICE"
sudo systemctl restart $SERVICE
if [ $? = 0 ]; then echo "done"; fi
rm -rf /var/log/$SERVICE/*.log
echo "$(date) restarted $SERVICE" >> /tmp/restart.log
