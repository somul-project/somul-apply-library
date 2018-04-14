!/bin/bash

CONTAINER_ID=`sudo docker ps | grep somul-stage | grep -v 'grep' | awk '{ print $1 }'`
if [ -n $CONTAINER_ID ]
then
    echo "killing $CONTAINER_ID"
    sudo docker kill $CONTAINER_ID
else
    echo "container not found"
fi
