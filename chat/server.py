from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor


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

        print(f"Client connected: {self.ip}:{self.port}")

        self.transport.write("Welcome to the chat v0.1\n".encode())
        if len(self.factory.log_entries):
            for entry in self.factory.log_entries:
                self.transport.write(entry)

    def dataReceived(self, data: bytes):
        """
        Обработчик нового сообщения от клиента
        :param data:
        """
        message = data.decode().replace('\n', '')

        if self.login is not None:
            server_message = f"{self.login}: {message}"
            self.factory.notify_all_users(server_message)

            print(server_message)
        else:
            if message.startswith("login:"):
                self.login = message.replace("login:", "", 1)  # А вдруг я захочу логин с login:
                notification = f"New user connected: {self.login}"
                if not self.factory.can_use_login(self):
                    self.transport.loseConnection()
                else:
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
        print(f"Client disconnected: {self.login} ({self.ip}:{self.port})")


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
            user.transport.write(f"{data}\n".encode())
            self.log_entries.append(f"{data}\n".encode())

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
