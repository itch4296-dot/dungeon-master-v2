from game import Paladin, Boss, loot_generator

def main():
    print("--- ДОМАШНЕЕ ЗАДАНИЕ: DUNGEON CODE v1.0 ---")

    loot_gen = loot_generator()
    
    hero = Paladin(name="Артур")
    print(f"Создан герой: {hero.name} | Класс: Паладин | ХП: {hero.health} | Атака: {hero.attack_power}")

    boss = Boss(name="Дракон Опустошитель", health=250, attack_power=22)
    print(f"⚠️ Появился босс: {boss.name} (Здоровье: {boss.health}, Атака: {boss.attack_power})")
    
    print("\n--- НАЧАЛО БИТВЫ С БОССОМ ---")

    round_counter = 1

    while hero.is_alive() and boss.is_alive():
        print(f"\n=================== РАУНД {round_counter} ===================")
        
        new_item = next(loot_gen)
        hero.inventory.append(new_item)
        print(f"🎁 На поле боя найден предмет: {new_item.name} ({new_item.rarity})! Паладин кладет его в рюкзак.")
        
        hero.show_inventory()
        
        print(f"🤖 Авто-использование предмета:")
        hero.use_item(new_item.name)
        
        print(f"\n⚔️ ХОД ГЕРОЯ:")
        if round_counter % 2 != 0:
            hero.special(boss)
            boss.take_damage(hero.attack_power)
        else:
            hero.attack(boss)

        if not boss.is_alive():
            break

        # Шаг Д: Ход босса
        print(f"\n👹 ХОД БОССА:")
        boss.attack(hero)
        
        round_counter += 1

    print("\n==============================================")
    print("--- ИГРА ЗАВЕРШЕНА ---")
    if hero.is_alive():
        print(f"🏆 ПОБЕДА! {hero.name} одолел {boss.name} за {round_counter} раундов!")
    else:
        print(f"💀 ПОРАЖЕНИЕ! {hero.name} пал жертвой {boss.name}...")

if __name__ == "__main__":
    main()