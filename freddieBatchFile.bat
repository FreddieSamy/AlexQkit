@echo off
CD C:\Users\asuss\Desktop\AlexQkit\client
START npm run serve
@echo on
call C:\ProgramData\Anaconda3\Scripts\activate.bat
CD C:\Users\asuss\Desktop\AlexQkit\server
flask run