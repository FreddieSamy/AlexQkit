@echo off
CD C:\Users\asuss\Desktop\AlexQkit\client
START npm run serve
@echo on
call C:\Users\asuss\Anaconda3\Scripts\activate.bat
CD C:\Users\asuss\Desktop\AlexQkit\server
flask run