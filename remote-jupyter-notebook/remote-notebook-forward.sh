#!/bin/bash
if [ "$3" = "k" ] 
then
	echo "killing remote notebook server"
	ssh $2 './notebook_serve.sh '"$1"' kill'
fi

if [ "$3" = "conda" ] 
then
	echo "creating notebook server and forwarind port"
	ssh $2 './notebook_serve.sh '"$1"' '"$3"' '"$4"
	ssh -N -L localhost:$1:localhost:$1 $2
fi
