# Фигуры на плоскости 
#Название проекта: 3_figures
#Рассмотрим пример из лекций с наследованием класса "квадрат" от класса "прямоугольник".
#Этот пример нарушает принцип подстановки Барбары Лисков.
#Как исправить код (подсказка: с помощью свойств), чтобы принцип не нарушался?

# !!! Вся информация в READ.ME (в этой папке) !!!

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Ошибка !")
        self._width = value
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Ошибка !")
        self._height = value
    @property
    def area(self):
        return self.width * self.height

class Square:
    def __init__(self, side):
        self.side = side
    @property
    def side(self):
        return self._side
    @side.setter
    def side(self, value):
        if value <= 0:
            raise ValueError("Ошибка !")
        self._side = value
    @property
    def width(self):
        return self.side
    @property
    def height(self):
        return self.side
    @property
    def area(self):
        return self.side ** 2

def main():
    rect = Rectangle(10, 20)
    print(f"Площадь прямоугольника: {rect.area}")
    square = Square(5)
    print(f"Площадь квадрата: {square.area}")
main()
