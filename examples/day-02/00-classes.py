"""
Основы ООП - конструктор, наследование, перегрузка, полиморфизм, инкапсуляция
"""


class Human:
    first_name: str
    last_name: str

    def __init__(self, first_name, last_name="Undefined"):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"Human: {self.first_name} {self.last_name}"


class User(Human):
    __passport: str = "1234 123123"

    def hello(self):
        print(f"Hello, {self.first_name}!")


john = User("John", "Doe")
# john.hello()
artur = User("Artur")


# artur.hello()
# print(john)
# print(john._User__passport)
# john._passport = "4312 123123"

class Person:
    def __init__(self, name):
        self.name = name


bob = Person("Bob")
tim = Person("Tim")
sue = Person("Sue")
people = [bob, tim, sue]
print(people)
people.remove(bob)
print(people)
