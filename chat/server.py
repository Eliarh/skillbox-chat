from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import datetime


class Client(Protocol):
    ip: str = None
    port: int = None
    login: str = None
    factory: 'Chat'

    def __init__(self, factory):
        """
        Инициализация фабрики клиента
        :param factory:
        """
        self.factory = factory

    def connectionMade(self):
        """
        Обработчик подключения нового клиента
        """
        self.ip = self.transport.getPeer().host
        self.port = self.transport.getPeer().port
        self.factory.clients.append(self)

        print(f"{self.factory.get_current_time()} Client connected: {self.ip}:{self.port}")

        self.transport.write("Welcome to the chat v0.1\n".encode())

    def dataReceived(self, data: bytes):
        """
        Обработчик нового сообщения от клиента
        :param data:
        """
        message = data.decode().replace('\n', '')

        if self.login is not None:
            server_message = f"{self.login}: {message}"
            self.factory.notify_all_users(server_message)

            print(f"{self.factory.get_current_time()} {server_message}")
        else:
            if message.startswith("login:"):
                self.login = message.replace("login:", "", 1)  # А вдруг я захочу логин с login:
                notification = f"{self.factory.get_current_time()} New user connected: {self.login}"
                if not self.factory.can_use_login(self):
                    self.transport.write("Login already used\r\n".encode())
                    self.transport.loseConnection()
                    #reactor.callLater(.1, self.transport.loseConnection)
                else:
                    if len(self.factory.log_entries):
                        for entry in self.factory.log_entries:
                            self.transport.write(entry)
                    self.factory.notify_all_users(notification)
                    print(notification)
            else:
                print("Error: Invalid client login")

    def connectionLost(self, reason=None):
        """
        Обработчик отключения клиента
        :param reason:
        """
        self.factory.clients.remove(self)
        print(f"{self.factory.get_current_time()} Client disconnected: {self.login} ({self.ip}:{self.port})")
        # if reason:
        #    print(f"Reason {reason}")


class Chat(Factory):
    clients: list
    log_entries: list

    def __init__(self):
        """
        Инициализация сервера
        """
        self.clients = []
        self.log_entries = []
        print("*" * 10, "\nStart сервер \nCompleted [OK]")

    def startFactory(self):
        """
        Запуск процесса ожидания новых клиентов
        :return:
        """
        print("\n\nStart listening for the clients...")

    def buildProtocol(self, addr):
        """
        Инициализация нового клиента
        :param addr:
        :return:
        """
        return Client(self)

    def notify_all_users(self, data: str):
        """
        Отправка сообщений всем текущим пользователям
        :param data:
        :return:
        """
        for user in self.clients:
            message=f"{self.get_current_time()} {data}\n".encode()
            user.transport.write(message)
            self.log_entries.append(message)

    def get_current_time(self):
        return datetime.datetime.now().time().strftime("%H:%M:%S")

    def can_use_login(self, current_client: Client):
        result = True
        for client in self.clients:
            if client.login == current_client.login and client != current_client:
                result = False
                break

        return result


if __name__ == '__main__':
    reactor.listenTCP(7410, Chat())
    reactor.run()
