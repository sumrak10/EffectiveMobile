class ObjList:
    def __init__(self, data: str = None) -> None:
        self.__next = None
        self.__prev = None
        self.__data = data
    
    def set_next(self, obj: 'ObjList') -> None:
        self.__next = obj
    def set_prev(self, obj: 'ObjList') -> None: 
        self.__prev = obj

    def get_next(self) -> 'ObjList': 
        return self.__next
    def get_prev(self) -> 'ObjList':
        return self.__prev

    def set_data(self, data: str) -> None:
        self.__data = data
    def get_data(self) -> str:
        return self.__data

    def __str__(self) -> str:
        return f"Linked list object {self.__data}"


class LinkedList:
    def __init__(self) -> None:
        self.head: ObjList = None
        self.tail: ObjList = None
    
    def add_obj(self, obj: ObjList):
        if self.head is None:
            self.head = obj
        if self.tail is None:
            self.tail = obj
        else:
            obj.set_prev(self.tail)
            self.tail.set_next(obj)
            self.tail = obj

    def remove_obj(self) -> None:
        if self.tail is not None:
            self.tail = self.tail.get_prev()
            if self.tail is not None:
                self.tail.set_next(None)
            else:
                self.head = None

    def get_data(self) -> list[str]:
        elem = self.head
        data = []
        while elem is not None:
            data.append(elem.get_data())
            elem = elem.get_next()
        return data

if __name__ == '__main__':
    lst = LinkedList()
    lst.add_obj(ObjList('1'))
    lst.add_obj(ObjList('2'))
    lst.add_obj(ObjList('3'))
    print(lst.get_data())