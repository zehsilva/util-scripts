#!/bin/bash

SESSION='guild_'"$4"'_server'"$1" 
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
       tmux send-keys -t $SESSION 'guild '"$4"' --no-open --port='"$1"' '"${@:5}" Enter
       echo "Loading Tensor board"
       sleep 5
    fi
fi

