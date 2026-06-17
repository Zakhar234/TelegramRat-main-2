@echo off

pip install --upgrade pip
pip install pyinstaller
pip install aiogram==2.25.1
pip install aiohttp==3.9.0
pip install Babel==2.9.1
pip install requests
pip install opencv-python
pip install psutil
pip install GPUtil
pip install tabulate
pip install pycryptodome
pip install comtypes
pip install PyAutoGUI
pip install pycaw
pip install cryptography
pip install Pillow
pip install keyboard
pip install pyperclip
pip install pypiwin32
pip install wave
pip install pyttsx3
pip install pywin32
pip install pyuac

pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" --version-file "version.py" --add-data "logs;logs/" --add-data "keyboards;keyboards/" --add-data "functions;functions/" --add-data "videoplayback.mp4;." --hidden-import=aiogram.types --hidden-import=aiogram.dispatcher --hidden-import=aiogram.dispatcher.filters --hidden-import=aiogram.dispatcher.middlewares --hidden-import=aiogram.utils --collect-all aiogram --collect-all aiohttp "main.py"


rmdir /s /q __pycache__
rmdir /s /q build

:cmd
pause null
