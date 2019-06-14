"""
Примеры базового синтаксиса и работа с типами данных
Числа, строки, списки, булево значение
"""
a = 1 + 1  # integer
b = 1.0 + 1.0  # float
string = "John"  # string
string = "John" * 2  # JohnJohn
string = "John" + str(2)  # Error -> OK
users = ["John", "Artur", "Kate"]  # list
users[0]  # John
users[1]  # Artur
users[-2]  # Artur

true_test = 10 > 5  # True
false_test = 10 == 5  # False

len(users)  # 3
print(users.count("John"))  # 1