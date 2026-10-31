import random
import time
from functools import wraps

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # args[0] — это self (объект персонажа)
        hero_name = args[0].name if args and hasattr(args[0], 'name') else "Персонаж"
        print(f"🎬 [ЛОГ ИГРЫ] {hero_name} вызывает действие: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"⏱️ [ТАЙМЕР] Действие {func.__name__} выполнилось за {end_time - start_time:.6f} сек.")
        return result
    return wrapper

class Item:
    def __init__(self, name, attack_bonus=0, heal_bonus=0, rarity="common", power=0):
        self.name = name
        self.attack_bonus = attack_bonus
        self.heal_bonus = heal_bonus
        self.rarity = rarity
        self.power = power 

    def __str__(self):
        return f"{self.name} ({self.rarity}, Сила: {self.power})"


class Hero:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack_power = attack_power
        self.inventory = []  

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        print(f"💥 {self.name} получает {damage} урона. Осталось здоровья: {self.health}")

    @log_action  
    @timer       
    def attack(self, target):
        damage = self.attack_power
        print(f"⚔️ {self.name} атакует {target.name} на {damage} урона!")
        target.take_damage(damage)

    def show_inventory(self):
        if not self.inventory:
            print(f"🎒 Инвентарь {self.name} сейчас пуст.")
        else:
            items_str = ", ".join([item.name for item in self.inventory])
            print(f"🎒 В инвентаре {self.name} сейчас лежит: [{items_str}]")

    def use_item(self, item_name):
        for item in self.inventory:
            if item.name == item_name:
                if item.attack_bonus > 0:
                    self.attack_power += item.attack_bonus
                    print(f"🗡️ {self.name} экипирует {item.name}! Бонус к атаке +{item.attack_bonus} (Итого: {self.attack_power})")
                if item.heal_bonus > 0:
                    self.health = min(self.max_health, self.health + item.heal_bonus)
                    print(f"🧪 {self.name} использует {item.name}! Здоровье восстановлено до {self.health}")
                
                self.inventory.remove(item)
                return
        print(f"❌ Предмет {item_name} не найден в инвентаре.")


class Paladin(Hero):
    def __init__(self, name, health=140, attack_power=20):
        super().__init__(name, health, attack_power)
        self.shield_charges = 2

    @log_action
    @timer
    def special(self, target):
        if self.shield_charges > 0:
            self.health = min(self.max_health, self.health + 30)
            self.attack_power += 5
            self.shield_charges -= 1
            print(f"✨ {self.name} использует SPECIAL() 'Святой Щит'! Здоровье +30, Атака +5! (Зарядов: {self.shield_charges})")
        else:
            print(f"💨 Щит разряжен! {self.name} бьет обычной атакой.")
            self.attack(target)


class Boss:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        print(f"👹 {self.name} ранен! Осталось здоровья: {self.health}")

    def attack(self, target):
        print(f"🔥 {self.name} наносит сокрушительный удар по {target.name}!")
        target.take_damage(self.attack_power)

ITEMS_DATABASE = [
    Item("Ржавый кинжал", attack_bonus=2, rarity="common", power=5),
    Item("Меч правосудия", attack_bonus=15, rarity="rare", power=45),
    Item("Посох Архимага", attack_bonus=25, rarity="legendary", power=70),
    Item("Кожаный жилет", heal_bonus=10, rarity="common", power=12),
    Item("Щит Иджис", heal_bonus=45, rarity="legendary", power=50),
    Item("Кольцо регенерации", heal_bonus=20, rarity="rare", power=25),
    Item("Деревянный лук", attack_bonus=5, rarity="common", power=15),
    Item("Топор Кровавой Луны", attack_bonus=22, rarity="legendary", power=65),
    Item("Стальные сапоги", attack_bonus=4, rarity="uncommon", power=20),
]
def loot_generator():
    """Бесконечно возвращает случайный предмет из базы данных"""
    while True:
        yield random.choice(ITEMS_DATABASE)