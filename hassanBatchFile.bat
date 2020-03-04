@echo off
CD C:\Users\HP\Desktop\AlexQkit-master\client
START npm run serve
@echo on
call C:\ProgramData\Anaconda3\Scripts\activate.bat
CD C:\Users\HP\Desktop\AlexQkit-master\server
flask run