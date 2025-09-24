from typing import override


class Example():
    def method(self):
        pass

    def another_method(self):
        pass

    def yet_another_method(self):
        pass


class AnotherExample(Example):
    @override
    def methodd(self):
        pass

    @override
    def another_methodd(self):
        pass

    @override
    def yet_another_methodd(self):
        pass