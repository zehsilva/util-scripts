#!/bin/bash
if [ "$3" = "kill" ]
then
        echo "killing remote code-server"
        ssh $2 ./code_server.sh $1 kill $4 
else
        if [ "$3" = "conda" ]
        then
                echo "creating code-server on port "$1", conda-env "$4" and port-forwarding"
                ssh $2 ./code_server.sh $1 $3 $4 
        else
                echo "creating code-server on port "$1", conda-env base and port-forwarding"
                ssh $2 ./code_server.sh $1 conda base
        fi
        echo "finishing port-forwarding. copy the above link in the browser"
        ssh -N -L localhost:$1:localhost:$1 $2
fi
