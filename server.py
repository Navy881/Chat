# -*- coding: utf-8 -*-

'''
Импортируем библиотеку socket
Cокет — это программный интерфейс для обеспечения
информационного обмена между процессами.
Существуют клиентские и серверные сокеты.
Серверный сокет прослушивает определенный порт, а
клиентский подключается к серверу.
После того, как было установлено соединение начинается
обмен данными.
'''
import socket
import _thread


'''
Метод для обработки сообщений нового клиента + отправка всем
'''
def communication(conn):
    while True:
        try:
            # Получение сообщение из сокета клиента  + удалене проблелов в начале и конце строки (strip())
            data = conn.recv(DATASIZE).decode().strip()
            if not data:
                break
            # Формирование сообщеня для отправки
            data_message = clients.get(conn) + ": " + str(data)
            # Цикл по всем записанным совектам клиентов
            for client_socket in conns.keys():
                try:
                    # Отправляем на каждый сокет полученное сообщение
                    client_socket.send(bytes(data_message, "utf8"))
                except Exception as e:
                    print("Warning!", e)
                    '''
                    # Удаление сокета из списка
                    del conns[client_socket]
                    print("Client {} disconnect. {}".format(conn, e))
                    '''
                    break
            print('{} send: {}'.format(clients.get(conn), data))
        except Exception as e:
            print("\nClient {} disconnect. {}".format(clients.get(conn), e))
            remove_client(conn, conns, clients)
            break


'''
Метод удаления из списков отключившегося клиента
'''
def remove_client(conn, conns, clients):
    # Формирование сообщение о покидании чата килентов до удаления списков
    leave_client_message = ">>> Server: %s leave chat" % clients.get(conn)

    # Удаление сокета из списков адресов и имен клиетов
    del conns[conn]
    del clients[conn]

    # Отправка всем сообщения об отключении клиента
    for client_socket in conns.keys():
        # Отправляем на каждый сокет полученное сообщение
        client_socket.send(bytes(leave_client_message, "utf8"))


'''
Метод добавления нового клиента из списка
'''
def add_new_client(conn, addr, i):
    # Отправка запроса имени клиента
    conn.send(bytes(">>> Server: Hello! What is your name?", "utf8"))
    # Получение имени + удалене проблелов в начале и конце строки (strip())
    client_name = conn.recv(DATASIZE).decode().strip()
    # Проверка занятости имени
    nickname = False
    while nickname is False:
        # Если список имент не пустой
        if len(clients) != 0:
            for client_name_in_mem in clients.values():
                # Сравнение полученного имени со список в нижнем регистре
                if client_name.lower() == client_name_in_mem.lower():
                    conn.send(bytes(">>> Server: Sorry, this name is already use. Try again.", "utf8"))
                    client_name = conn.recv(DATASIZE).decode().strip()
                else:
                    nickname = True
        else:
            nickname = True
    # Запоминаем имя клиента
    clients[conn] = client_name
    # Запоминаем адрес и сокет клиента
    conns[conn] = addr

    # Отпрвка сообщения приветствия клиенту
    welcome_message = ">>> Server: Welcome %s " % client_name
    conn.send(bytes(welcome_message, "utf8"))

    # Вывод информации о подключении
    print('\nNew connection:\n    '
          'client name: {}\n    '
          'client address: {}\n    '
          'client socket: {}'.format(client_name, addr, conn))
    print('------------\nClients online {}:'.format(len(clients)))
    for cl in clients.values():
        print("    {} client - {}".format(i, cl))
        i += 1
    print('------------')

    # Отправка всем сообщеия о подключении новго клиента
    new_client_message = ">>> Server: %s join to chat" % client_name
    for client_socket in conns.keys():
        # Отправляем на каждый сокет полученное сообщение
        client_socket.send(bytes(new_client_message, "utf8"))

    # Запуск общения с новым клиентом
    communication(conn)


'''
Основной метод
'''
def main():
    # Создаем сокет
    sock = socket.socket()
    # Определяем хост и порт для сервера
    sock.bind((HOST, PORT))
    # Запуск прослушивания c заданным максимальным количеством подключений в очереди
    sock.listen(QUEUE)
    while True:
        try:
            # Счётчик клиентов
            i = 1
            # Принимаем подключение с помощью accept(), которое возвращает кортеж из двух
            # значений: нового сокета и адреса клиента
            conn, addr = sock.accept()
            # Создание нового потока для добавления и общения с новым клиентом
            _thread.start_new_thread(add_new_client, (conn, addr, i))
        except Exception as e:
            print("Error!", e)      
    conn.close()


if __name__ == "__main__":
    # Параметры
    HOST = "localhost"
    PORT = 9080
    QUEUE = 1
    DATASIZE = 1024

    # Key-value dict для записи сокетов клиентов
    conns = {}
    # Key-value dict для записи имен клиентов
    clients = {}

    # Запуск основного метода
    print("Server running...")
    main()
    print ("Server stoping...")
