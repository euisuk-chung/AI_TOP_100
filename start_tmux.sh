#!/bin/bash

# Session Name
SESSION="ai_top_100"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)

# Only create session if it doesn't exist
if [ "$SESSIONEXISTS" = "" ]
then
    # Start New Session with our name
    tmux new-session -d -s $SESSION

    # Name the first window 'Services'
    tmux rename-window -t $SESSION:0 'Services'

    # Pane 0: Backend
    # Send keys to start backend
    tmux send-keys -t $SESSION:0 'cd platform/backend' C-m
    tmux send-keys -t $SESSION:0 'uv run python main.py' C-m

    # Split window horizontally
    tmux split-window -h -t $SESSION:0

    # Pane 1: Frontend
    # Send keys to start frontend
    tmux send-keys -t $SESSION:0.1 'cd platform/frontend' C-m
    tmux send-keys -t $SESSION:0.1 'npm run dev -- --host' C-m

    # Select pane 0
    tmux select-pane -t $SESSION:0.0
fi

# Attach to session
echo "Tmux session '$SESSION' created."
echo "Attach using: tmux attach -t $SESSION"
