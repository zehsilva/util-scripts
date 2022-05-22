#!/bin/bash
if [ "$3" = "kill" ]
then
        echo "killing remote tensorboard server"
        ssh $2 ./guildview_serve.sh $1 kill $4 "${@:5}"
else
        if [ "$3" = "conda" ]
        then
                echo "creating guild "$5" server and port-forwarding"
                ssh $2 ./guildview_serve.sh $1 $3 $4 "${@:5}"
        else
                echo "creating guild "$4" server and port-forwarding"
                ssh $2 ./guildview_serve.sh $1 conda base $3 "${@:4}"
        fi
        echo "finishing guild port-forwarding. copy the above link in the browser"
        ssh -N -L localhost:$1:localhost:$1 $2
fi

