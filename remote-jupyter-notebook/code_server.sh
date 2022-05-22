#!/bin/bash

SESSION='code_server_'"$1" 
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
       tmux send-keys -t $SESSION 'code-server --bind-addr 127.0.0.1:'"$1" Enter
       echo "Loading code server"
       sleep 2
    fi
fi

