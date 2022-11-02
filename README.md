# Rift Server
This is a Rift Server API aimed to collect and distribute English words.

## 1. Installation
## 1.1. Running server
To run the server you can use the **docker-compose.yml** file to deploy the following containers:
1. Nginx server
2. Gunicorn server

If you just want deploy the web server application you can opt for one of the next options:
### 1.1.1. Embeded Django server 
```
python manage.py runserver 0:8080
```
### 1.1.2. Gunicorn 
```
gunicorn rift_server.wsgi -b 0:80
```
## 1.2. Environment Variables

Both manual and Docker deployments need of the next Environment variables:
### 1.2.1. ALLOWED_HOSTS (Required)
```
export ALLOWED_HOSTS='["server", "localhost"]'
```
### 1.2.2. DJANGO_DEBUG (Optional)
If this variable is present the server gonna be able to show you debug errors.
```
export DJANGO_DEBUG="1"
```

## 1.3. Endpoints
### 1.3.1. Single dictionary word
```
http://<SERVER_ADDRESS>/dictionary/<WORD>
```
The response gonna be a single JSON Word
### 1.3.1. Single dictionary word
```
http://<SERVER_ADDRESS>/dictionary/?word[<i>]=<word>&word[<i>]=<word>[...]
```
The response gonna be a Word JSON array
