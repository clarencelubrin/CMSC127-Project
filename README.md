# How to run the application

## Download dependencies

Create the .venv environment
```
python -m venv .venv
```

Activate the python virtual environment
```
source .venv/bin/activate
```

Download the dependencies
```
pip install -r requirements.txt
```

## How to initialize the MariaDB Database

Give the script run permissions
```
chmod +x init.sh
```

Run the init script
```
sudo ./init.sh
```
or
```
sudo bash <ROOT_LOCATION_OF_REPOSITORY>/init.sh
```

## Run the server

Start the server
```
uvicorn app:app --reload
```