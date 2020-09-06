# Usage

- Copy ``remote-notebook-forward.sh`` to your local bin folder. Copy ``notebook_serve.sh`` to your remote user home folder (or the default folder when login with ssh)
- Make sure you ``chmod a+x`` both of them. 
- Make sure you have jupyter-notebook installed in the remote computer, as well as ``tmux``
- Now run ``remote-notebook-forward.sh port user@remote`` and copy the generated url to your local browser
- To stop the server first close the script doing ``ctrl+c`` to kill the port forwarding, then run to clean to remote server ``remote-notebook-forward.sh port user@remote k`` (noticed ``k`` in the end)
