@echo off
CD /home/mario/Desktop/AlexQkit/client
START npm run serve
@echo on
call /home/mario/anaconda3/bin/activate.bat
CD /home/mario/Desktop/AlexQkit/server
flask run