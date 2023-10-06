from abc import ABC, abstractmethod

class AbstractNetworkDevice(ABC):
    @abstractmethod
    def send_data(self):
        raise NotImplementedError
    @abstractmethod
    def receive_data(self):
        raise NotImplementedError


class Data:
    def __init__(self, data: str, destination_ip: int) -> None:
        self.data = data
        self.destination_ip = destination_ip
    def __repr__(self) -> str:
        return f"Data: '{self.data}'"
    def __str__(self) -> str:
        return f"Data: '{self.data}'"

class Server(AbstractNetworkDevice):
    def __init__(self) -> None:
        self.ip = None
        self.__buffer: list[Data] = []
        self.linked_router: 'Router' = None

    def receive_data(self, data: Data) -> None:
        self.__buffer.append(data)

    def send_data(self, data: Data):
        self.linked_router.receive_data(data)

    def get_data(self):
        res = self.__buffer
        self.__buffer = []
        return res

    def get_ip(self) -> int:
        return self.ip

class Router(AbstractNetworkDevice):
    def __init__(self) -> None:
        self.servers: list[Server] = []
        self.__buffer: list[Data] = []
        self.__ip_seq = 0
    
    def receive_data(self, data: Data) -> None:
        '''
        Для реалистичности симуляции можно вызывать метод send_data здесь
        чтобы рассылка данных происходила автоматически
        '''
        self.__buffer.append(data)

    def generate_ip(self) -> int:
        self.__ip_seq += 1
        return self.__ip_seq

    def link(self, server: Server) -> None:
        server.linked_router = self
        server.ip = self.generate_ip()
        self.servers.append(server)

    def unlink(self, server: Server) -> None:
        server = self.servers.pop(self.servers.index(server))
        server.linked_router = None

    def send_data(self):
        for data in self.__buffer:
            for server in self.servers:
                if data.destination_ip == server.get_ip():
                    server.receive_data(data)
        self.__buffer = []



if __name__ == '__main__':
    router = Router()
    server1 = Server()
    server2 = Server()
    server3 = Server()
    router.link(server1)
    router.link(server2)
    router.link(server3)
    server1.send_data(Data('hello from server1 to server2', server2.get_ip()))
    server1.send_data(Data('hello from server1 to server3', server3.get_ip()))
    server3.send_data(Data('hello from server3 to server1', server1.get_ip()))
    router.send_data()
    print("Server1 data:",server1.get_data())
    print("Server2 data:",server2.get_data())
    print("Server3 data:", server3.get_data())