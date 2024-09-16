# Overview
A simple, self-hosted game progress tracker. Heavily inspired by [Backloggery](https://backloggery.com/).

# Features
- Catalog your game collection spanning across various platforms and formats
- Set individual game ownership, completion status, achievements, and more
- Import existing progress from popular digital platforms like Steam and RetroAchievements

# Installation

Clone the repository and install the module
```bash
git clone https://github.com/ccriddler/gameorganize/
cd gameorganize
pip install -e .
```

Alternatively, use pip to install it automatically
```bash
pip install git+https://github.com/ccriddler/gameorganize.git
```

# Running
Once the python module is installed, you can run it in development mode with the command:
```bash
flask run --app gameorganize:app
```

To run as a deployed, persistant webapp, use gunicorn or another WSGI server of your choice
```bash
gunicorn -w 3 --bind 0.0.0.0:5003 gameorganize:app
```
