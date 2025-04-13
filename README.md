# Urushibata_23274717_CSC1121_Assignment2

## requirements

Install requirements using
```
pip install -r requirements.txt
```


## Run server

```
flask run
```


on 
```
/home/urushibata.com.br/dcu
```

needs to run the bellow before running pip install -r requirements

```
source myenv/bin/activate
```


to start service with gunicorn
```
gunicorn -w 1 app:app
```