export APP_ENV=local FLASK_APP=$(pwd)/mini_wallet/app/api/app.py FLASK_ENV=local
sudo /home/robertojulianto/.local/share/virtualenvs/SimpleMiniWallet-MNsmNGH4/bin/python -m flask run --reload -p 80