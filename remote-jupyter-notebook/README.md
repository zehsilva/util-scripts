# Installation

- Copy ``remote-notebook-forward.sh`` to your local bin folder. Copy ``notebook_serve.sh`` to your remote user home folder (or the default folder when login with ssh)
- Make sure you ``chmod a+x`` both of them. 
- Make sure you have installed in the remote computer the folloing packages: ``tmux``, ``jupyter-notebook`` and ``conda`` (only in case you use the option of setting a conda environment).

# Usage
- There are three options of usage now:
  1) run remote default jupyter-notebook installation using ``remote-notebook-forward.sh port user@remote`` and copy the generated url to your local browser
  2) run remote jupyter-notebook in pre-existing conda environment (called ``env_name`` here) using ``remote-notebook-forward.sh port user@remote conda env_name`` and copy the generated url to your local browser
  3) To stop the server first close the script doing ``ctrl+c`` to kill the port forwarding, then run to clean to remote server ``remote-notebook-forward.sh port user@remote k`` (noticed ``k`` in the end)
