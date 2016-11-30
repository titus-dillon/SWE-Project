# SWE-Project
For linux
    1) Must have Python 3.5 and pip for python 3.5
        - pip may need to be manually installed by downloading get-pip.py from https://pip.pypa.io/en/stable/installing/
        - once downloaded, use "python3 get-pip.py" to install pip
        - pip --version returns "pip 9.0.1 from /usr/lib/python3.5/site-packages (python 3.5)" or similar
    2) pip install Cython
    3) pip install xlrd
    4) pip install gzip
    5) pip install datetime
    6) pip install pandas
    7) pip install ggplot
        - if problems installing statsmodels for ggplot:
            - install development tools (Fedora command:  dnf install @development-tools)
            - install python3-dev (Fedora command:  dnf install python3.devel.x86_64)
            ** There should be something very similar to these commands for Debian-based distributions **
    8) pip install tkinter
    9) pip install sip
    10) pip install pyqt5
    11) install mallet
        - use this guide http://programminghistorian.org/lessons/topic-modeling-and-mallet
    12) python3 ntm.py
        - use shell to run
For Windows
    1) Install Anaconda 4.2.0 for python 3.5
        - Can be installed from https://www.continuum.io/downloads
    2) pip install ggplot
        - Make sure you are using anaconda pip script
        - pip script if not in the environment path is located in Anaconda3\Scripts
    3) install mallet
        - use this guide http://programminghistorian.org/lessons/topic-modeling-and-mallet
    12) python3 ntm.py
        - use cmd terminal to run
        - make sure to use the anaconda python 3.5 interpreter