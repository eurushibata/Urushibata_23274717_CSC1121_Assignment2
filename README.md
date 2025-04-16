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

to stop
```
pkill gunicorn
```

to start service with gunicorn
```
gunicorn -w 1 app:app --daemon --log-file 1.logfile.log --reload
```




sudo systemctl restart gunicorn
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service
sudo nginx -t && sudo systemctl restart nginx