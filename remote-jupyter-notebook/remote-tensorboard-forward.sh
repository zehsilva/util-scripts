#!/bin/bash
if [ "$3" = "kill" ]
then
        echo "killing remote tensorboard server"
        ssh $2 ./tensorboard_serve.sh $1 kill
else
        echo "creating tensorboard server and port-forwarding"
        if [ "$3" = "conda" ]
        then
                ssh $2 ./tensorboard_serve.sh $1 $3 $4
        else
                ssh $2 ./tensorboard_serve.sh $1
        fi
        echo "finishing port-forwarding. copy the above link in the browser"
        ssh -N -L localhost:$1:localhost:$1 $2
fi



