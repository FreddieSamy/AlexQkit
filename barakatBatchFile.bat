@echo off
CD C:\Users\MBarakat\Desktop\my-project\client
START npm run serve
@echo on
call C:\ProgramData\Anaconda3\Scripts\activate.bat
CD C:\Users\MBarakat\Desktop\my-project\server
flask run