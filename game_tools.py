from numpy import isin
import pygame as pg
import math as m

class Vector:
    def __init__(self, x, y, is_unitary=True):
        self.__x = x
        self.__y = y

        if is_unitary:
            self._normalize()

        self._slope()

    def magnitude(self):
        return m.sqrt(self.__x**2 + self.__y**2)

    def turn_vert(self):
        self.__y = -self.__y
        self._slope()

    def get(self):
        return (self.__x, self.__y)

    def _normalize(self):
        mag = self.magnitude()
        if mag - 1 > 1e-6:
            self.__x /= mag
            self.__y /= mag

    def _slope(self):
        self.__slope = self.__y / self.__x
        if self.__x > 0:
            self.__way = "R"
        else:
            self.__way = "L"

    @property
    def Slope(self):
        return self.__slope

    @property
    def Way(self):
        return self.__way

    def __str__(self):
        return f'({self.__x}, {self.__y})'

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(self.__x * other, self.__y * other, False)
        elif isinstance(other, Vector):
            return self.__x * other.__x + self.__y * other.__y
        else:
            raise ValueError('Multiplying only by int or float or Vector.')

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.__x + other.__x, self.__y + other.__y, True)
        else:
            raise ValueError('Other must be instance of Vector.')

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def X(self):
        return self._x

    @X.setter
    def X(self, value):
        self._x = value

    @property
    def Y(self):
        return self._y

    @Y.setter
    def Y(self, value):
        self._y = value

    def __str__(self):
        return f'({self._x}, {self._y})'

    def __sub__(self, other):
        if isinstance(other, Point):
            return Vector(self.X - other.X, self.Y - other.Y)
        else:
            raise ValueError('Other must be instance of Point.')


class GameObject:
    default_velocity = 5

    def __init__(self, color=(255,255,255), position=None, velocity=default_velocity):
        if not(isinstance(color, tuple)):
            raise TypeError('Color must be a tuple (r, g ,b).')
        elif (position is not None and not isinstance(position, tuple)):
            raise TypeError('Position must be a tuple (x, y) or None.')
        # elif not(isinstance(size, tuple)):
        #     raise TypeError('Size must be a tuple (width, height).')
        elif not isinstance(velocity, int):
            raise TypeError('Velocity must be an int.')

        self.find_window_size()

        self._color = color
        self._velocity = velocity

        if position is None:
            self._center = Point(Paddle.window_width/2, Paddle.window_height/2)
        else:
            self._center = Point(*position)

    @classmethod
    def find_window_size(cls):
        cls.window_width = pg.display.Info().current_w
        cls.window_height = pg.display.Info().current_h

    @property
    def Color(self):
        return self._color
    
    @property
    def Position(self):
        return self._center

    @property
    def Velocity(self):
        return self._velocity

    def _move(self, x, y):
        self._center.X += x
        self._center.Y += y

class Paddle(GameObject):
    default_size = (20, 100)

    def __init__(self, size=default_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._size = size

    @property
    def Size(self):
        return self._size

    @property
    def Rect_properties(self):
        return (*self.upper_left_coords(), *self._size)

    def move_up(self):
        if (self._center.Y > 0):
            self._move(0, -self._velocity)

    def move_down(self):
        if (self._center.Y ) < Paddle.window_height:
            self._move(0, self._velocity)

    def upper_left_coords(self):
        return (self._center.X - self._size[0]/2, self._center.Y - self._size[1]/2)

    def offset_vect(self):
        return Vector(self._size[0]/2, 0)

class Ball(GameObject):
    default_radius = 10

    def __init__(self, radius=default_radius, direction=(-1, 0), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._radius = radius
        self._direction = Vector(*direction)
        print('mag',(self._direction).magnitude())
        self.last_bump = None # 0 up, 1 down, None didnt bump

    @property
    def Radius(self):
        return self._radius

    @property
    def Circle_properties(self):
        return (self._color, (self.Position.X, self.Position.Y), self._radius)

    @property
    def Direction(self):
        return self._direction

    def make_move(self):
        self._move(*(self._direction*self._velocity).get())

    def swap_direct_v(self):
        if (self._direction.Way == 'R' and self._direction.Slope > 0) or (self._direction.Way == 'L' and self._direction.Slope <= 0):
            self.last_bump = 1
        elif (self._direction.Way == 'L' and self._direction.Slope > 0) or (self._direction.Way == 'R' and self._direction.Slope <= 0):
            self.last_bump = 0
        self._direction.turn_vert()

    def change_direction(self, new_direct):
        self._direction = new_direct
