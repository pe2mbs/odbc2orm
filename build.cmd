@echo off
@echo Removing old distributions
del /F /Q dist\*.*
@echo Activating viritual environment
call venv\Scripts\activate.bat
@echo Setting company proxy
set HTTPS_PROXY=ssoproxy.internal.zone:8080
@echo Building distribution package
python -m build
@echo Upload package to PyPi
python -m twine upload --verbose dist/*
