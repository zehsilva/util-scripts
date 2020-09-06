#!/bin/bash
if [ "$3" = "k" ] 
then
	echo "killing remote notebook server"
	ssh $2 './notebook_serve.sh '"$1"' kill'
else
	echo "creating notebook server and forwarind port"
	ssh $2 './notebook_serve.sh '"$1"''
	echo "finishing port-forwarding copy the above link in the browser"
	ssh -N -L localhost:$1:localhost:$1 $2
fi
