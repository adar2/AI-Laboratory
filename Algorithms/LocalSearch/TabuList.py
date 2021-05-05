class TabuList:
    def __init__(self, initial_capacity, tenure) -> None:
        self._list = {}
        self.capacity = initial_capacity
        self.tenure = tenure

    def add(self, item):
        self._list[item] = 0
        self.update_tenure()
        if len(self._list) > self.capacity:
            self.__balance()

    def get_size(self):
        return len(self._list)

    def update(self):
        for key in self._list.keys():
            if self._list[key] > self.tenure:
                del self._list[key]

    def __balance(self):
        while len(self._list) > self.capacity:
            if len(self._list) == 1:
                return
            self.__remove_oldest()

    def __remove_oldest(self):
        del self._list[max(self._list, key=self._list.get)]

    def __contains__(self, item):
        return item in self._list

    def __getitem__(self, item):
        return self._list[item]

    def update_tenure(self):
        for item in self._list:
            self._list[item] = self._list[item]+1
