import binascii
import datetime
import socket
import time
import threading
import hashlib
import hmac
import logging

from PyQt5.QtCore import pyqtSignal, QObject
from client_part.client_packages.common.utils import *
from client_part.client_packages.common.variables import *

# Логер и объект блокировки для работы с сокетом.
CLIENT_LOGGER = logging.getLogger('client')
socket_lock = threading.Lock()


class ClientTransport(threading.Thread, QObject):
    """
        Класс реализующий транспортную подсистему клиентского
        модуля. Отвечает за взаимодействие с сервером.
    """
    # Сигналы новое сообщение и потеря соединения
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username, passwd, keys):
        # Вызываем конструктор предка
        threading.Thread.__init__(self)
        QObject.__init__(self)

        # Класс База данных - работа с базой
        self.database = database
        # Имя пользователя
        self.username = username
        # Пароль
        self.password = passwd
        # Сокет для работы с сервером
        self.transport = None
        # Набор ключей для шифрования
        self.keys = keys
        # Устанавливаем соединение:
        self.connection_init(port, ip_address)
        # Обновляем таблицы известных пользователей и контактов
        try:
            self.user_list_update()
            self.contacts_list_update()
        except OSError as err:
            if err.errno:
                CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
                raise ValueError('Потеряно соединение с сервером!')
            CLIENT_LOGGER.error('Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
            raise ValueError('Потеряно соединение с сервером!')
            # Флаг продолжения работы транспорта.
        self.running = True

    def connection_init(self, port, ip):
        """Метод отвечающий за устанновку соединения с сервером."""
        # Инициализация сокета и сообщение серверу о нашем появлении
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Таймаут необходим для освобождения сокета.
        self.transport.settimeout(5)

        # Соединяемся, 5 попыток соединения, флаг успеха ставим в True если удалось
        connected = False
        for i in range(5):
            CLIENT_LOGGER.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((ip, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        # Если соединится не удалось - исключение
        if not connected:
            CLIENT_LOGGER.critical('Не удалось установить соединение с сервером')
            raise ValueError('Не удалось установить соединение с сервером')

        CLIENT_LOGGER.debug('Starting auth dialog.')
        # Запускаем процедуру авторизации
        # Получаем хэш пароля
        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        CLIENT_LOGGER.debug(f'Passwd hash ready: {passwd_hash_string}')

        # Получаем публичный ключ и декодируем его из байтов
        pubkey = self.keys.publickey().export_key().decode('ascii')

        # Авторизируемся на сервере
        with socket_lock:
            client_presence = {
                ACTION: PRESENCE,
                TIME: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                USER: {
                    ACCOUNT_NAME: self.username,
                    PUBLIC_KEY: pubkey
                }
            }
            CLIENT_LOGGER.debug(f"Presence message = {client_presence}")
            # Отправляем серверу приветственное сообщение.
            try:
                send_message(self.transport, client_presence)
                ans = get_message(self.transport)
                CLIENT_LOGGER.debug(f'Server response = {ans}.')
                # Если сервер вернул ошибку, бросаем исключение.
                if RESPONSE in ans:
                    if ans[RESPONSE] == 400:
                        raise ValueError(ans[ERROR])
                    elif ans[RESPONSE] == 511:
                        # Если всё нормально, то продолжаем процедуру
                        # авторизации.
                        ans_data = ans[DATA]
                        hash = hmac.new(passwd_hash_string, ans_data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        my_ans = RESPONSE_511
                        my_ans[DATA] = binascii.b2a_base64(
                            digest).decode('ascii')
                        send_message(self.transport, my_ans)
                        self.process_answer(get_message(self.transport))
            except (OSError, json.JSONDecodeError) as err:
                CLIENT_LOGGER.debug(f'Connection error.', exc_info=err)
                raise ValueError('Сбой соединения в процессе авторизации.')

        CLIENT_LOGGER.debug('Установлено соединение с сервером')

    def process_answer(self, message):
        """Метод обработчик поступающих сообщений с сервера."""
        CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
        # Если это подтверждение чего-либо
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ValueError(f'{message[ERROR]}')
            elif message[RESPONSE] == 205:
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                CLIENT_LOGGER.debug(f'Принят неизвестный код подтверждения {message[RESPONSE]}')

        # Если это сообщение от пользователя добавляем в базу, даём сигнал о новом сообщении
        elif ACTION in message and message[
            ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                and MESSAGE_TEXT in message and message[DESTINATION] == self.username:
            CLIENT_LOGGER.debug(f'Получено сообщение от пользователя {message[SENDER]}'
                                f':{message[MESSAGE_TEXT]}')
            self.new_message.emit(message)

    def contacts_list_update(self):
        """Метод обновляющий с сервера список контактов."""
        CLIENT_LOGGER.debug(f'Запрос контакт листа для пользователся {self.name}')
        req = {
            ACTION: GET_CONTACTS,
            TIME: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            USER: self.username
        }
        CLIENT_LOGGER.debug(f'Сформирован запрос {req}')
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        CLIENT_LOGGER.debug(f'Получен ответ {ans}')
        if RESPONSE in ans and ans[RESPONSE] == 202:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            CLIENT_LOGGER.error('Не удалось обновить список контактов.')

    def user_list_update(self):
        """Метод обновления таблицы известных пользователей"""
        CLIENT_LOGGER.debug(f'Запрос списка известных пользователей {self.username}')
        req = {
            ACTION: USERS_REQUEST,
            TIME: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            self.database.add_users(ans[LIST_INFO])
        else:
            CLIENT_LOGGER.error('Не удалось обновить список известных пользователей.')

    def key_request(self, user):
        """Метод запрашивающий с сервера публичный ключ пользователя."""
        CLIENT_LOGGER.debug(f'Запрос публичного ключа для {user}')
        req = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            ACCOUNT_NAME: user
        }
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 511:
            return ans[DATA]
        else:
            CLIENT_LOGGER.error(f'Не удалось получить ключ собеседника{user}.')

    def add_contact(self, contact):
        """Метод, сообщающий на сервер о добавлении нового контакта"""
        CLIENT_LOGGER.debug(f'Создание контакта {contact}')
        req = {
            ACTION: ADD_CONTACT,
            TIME: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_message(self.transport, req)
            self.process_answer(get_message(self.transport))

    def remove_contact(self, contact):
        """Метод удаления клиента на сервере"""
        CLIENT_LOGGER.debug(f'Удаление контакта {contact}')
        req = {
            ACTION: REMOVE_CONTACT,
            TIME: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_message(self.transport, req)
            self.process_answer(get_message(self.transport))

    def transport_shutdown(self):
        """
            Метод закрытия соединения, отправляет сообщение
             о выходе.
        """
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            try:
                send_message(self.transport, message)
            except OSError:
                pass
        CLIENT_LOGGER.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    def send_message(self, to, message):
        """Метод отправки сообщения на сервер"""
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: to,
            TIME: datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')

        # Необходимо дождаться освобождения сокета для отправки сообщения
        with socket_lock:
            send_message(self.transport, message_dict)
            self.process_answer(get_message(self.transport))
            CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {to}')

    def run(self):
        """
            Метод содержащий основной цикл работы транспортного
            потока.
        """
        CLIENT_LOGGER.debug('Запущен процесс - приёмник собщений с сервера.')
        while self.running:
            # Отдыхаем секунду и снова пробуем захватить сокет.
            # если не сделать тут задержку, то отправка может достаточно долго ждать освобождения
            # сокета.
            time.sleep(1)
            message = None
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_message(self.transport)
                except OSError as err:
                    if err.errno:
                        CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                # Проблемы с соединением
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError,
                        json.JSONDecodeError, TypeError):
                    CLIENT_LOGGER.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.transport.settimeout(5)
            # Если сообщение получено, то вызываем функцию обработчик:
            if message:
                CLIENT_LOGGER.debug(f'Принято сообщение с сервера: {message}')
                self.process_answer(message)
