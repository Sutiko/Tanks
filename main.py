import random
import enum


class Gun:
    """Класс Gun - класс ПУШКИ, который описывает характеристики орудия танка

    Attributes
    __________
    caliber - калибр орудия
    length_gun - длинна орудия

    Methods
    _______
    dice_rand() - статический метод, иммитирующий бросок кубика
    is_on_target() - определяет попадание пушки в цель"""

    @staticmethod
    def dice_rand():
        return random.randint(1, 6)

    def __init__(self, caliber: float, length_gun: float) -> None:
        self.caliber = caliber
        self.length_gun = length_gun
        self.dice = self.dice_rand()

    def is_on_target(self) -> bool:
        return True if self.length_gun * self.dice > 100 else False


class Ammo:
    """Класс Ammo - класс СНАРЯДОВ, который описывает типы и характеристики снаряда

    Attributes
    __________
    projectle_type - константа, определяющая тип снаряда
    gun - параметры орудия
    caliber - калибр орудия

    Methods
    _______
    get_damage() - возможный урон от снаряда
    get_penetration() - возвращает калибр орудия """

    PROJECTLE_TYPE = enum.Enum(
        value='PROJECTLE_TYPE',
        names=[
            ('TYPE_1', 1.2),
            ('TYPE_2', 1),
            ('TYPE_3', 0.7),
        ],
    )

    def __init__(self, projectle_type: PROJECTLE_TYPE, gun: Gun, caliber) -> None:
        self.projectle_type = projectle_type
        self.gun = gun
        self.caliber = caliber

    def get_damage(self) -> int:
        return self.caliber * 3

    def get_penetration(self):
        return self.caliber


class HECartridge(Ammo):
    """ Класс HECartridge - класс фугасных снарядов"""
    pass


class HEATCartridge(Ammo):
    """Класс HEATCartridge - класс кумулятивных снарядов,
     переопределяет метод get_damage() """

    def get_damage(self):
        return self.caliber * 3 * 0.6


class APCartridge(Ammo):
    """Класс APCartridge - класс класс подкалиберных снарядов,
 переопределяет метод get_damage() """

    def get_damage(self):
        return self.caliber * 3 * 0.3


class Armour:
    """Класс Armour - класс БРОНЯ, который описывает
    характеристики брони танка

    Attributes
    __________
    armour_type - тип брони
    projectle_type - тип снаряда
    thikness - толщина брони
    caliber - калибр орудия

    Methods
    _______
    projectle_types() - определяет урон в зависимости от типа снаряда
    is_penetrated() - определяет наличие пробития

    """
    # Я так понимаю что тип брони будет не один,для дальнейших махинаций
    ARMOUR_TYPE = enum.Enum(
        value='ARMOUR_TYPES',
        names=[
            ('A1', 1),
            ('A2', 1),
            ('A3', 1),
        ],
    )

    def __init__(self, armour_type: ARMOUR_TYPE, projectle_type: Ammo, caliber: Ammo, thickness: float) -> None:
        self.thickness = thickness
        self.armour_type = armour_type
        self.projectle_type = projectle_type
        self.caliber = caliber

    def projectle_types(self):
        if self.projectle_type.name == 'TYPE_1':
            return HECartridge.get_damage(self)
        elif self.projectle_type.name == 'TYPE_2':
            return HEATCartridge.get_damage(self)
        elif self.projectle_type == 'TYPE_3':
            return APCartridge.get_damage(self)

    def is_penetrated(self):
        return True if Armour.projectle_types(self) > self.thickness else False


class HArmour(Armour):
    """Класс HArmour - класс , который описывает
    характеристики гомогенной брони танка и переопределяет
    метод is_penetrated() """

    def is_penetrated(self):
        if self.projectle_type.name == 'TYPE_1':
            return True if Armour.projectle_types(self) > self.thickness * 1.2 else False
        elif self.projectle_type.name == 'TYPE_2':
            return True if Armour.projectle_types(self) > self.thickness * 1 else False
        elif self.projectle_type == 'TYPE_3':
            return True if Armour.projectle_types(self) > self.thickness * 0.7 else False


if __name__ == '__main__':
    gun = Gun(10, 100)
    ammo = Ammo(Ammo.PROJECTLE_TYPE.TYPE_1, gun, gun.caliber)
    armour = Armour(Armour.ARMOUR_TYPE.A1, ammo.projectle_type, ammo.caliber, 25)
    print(ammo.projectle_type.value)
    print(Gun.is_on_target(gun))
    print(HEATCartridge.get_damage(ammo))
    print(Armour.projectle_types(ammo))
    print(Armour.is_penetrated(armour))
    print(HArmour.is_penetrated(armour))
