#!/bin/bash

SESSION='notebook_server'"$1" 
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)
# Only create tmux session if it doesn't already exist

if [ "$2" = "kill" ]
then
    if [ "$SESSIONEXISTS" != "" ] 
    then
        tmux send-keys -t $SESSION C-c "y" Enter
        tmux kill-session -t $SESSION 
    fi
else
    if [ "$SESSIONEXISTS" = "" ] 
    then
       # Start New Session with our name
       tmux new-session -d -s $SESSION
       if [ "$2" = "conda" ]
       then
           tmux send-keys -t $SESSION 'conda activate '"$3" Enter
       fi
       tmux send-keys -t $SESSION 'jupyter-notebook --no-browser --port='"$1" Enter
       echo "Loading jupyter-notebook remote server"
       sleep 5
       list_runtime=$(ls ~/.local/share/jupyter/runtime/nbserver*.json)
       for x in $list_runtime
       do 
          nb_port=$(cat $x | python3 -c "import sys, json; json_in=json.load(sys.stdin); print(str(json_in['url']).split(':')[2].split('/')[0])")
          if [ "$1" == "$nb_port" ]
          then
              cat $x | python3 -c "import sys, json; json_in=json.load(sys.stdin); print(json_in['url']+'tree?token='+json_in['token'])" ; 
          fi
       done
    fi
fi

