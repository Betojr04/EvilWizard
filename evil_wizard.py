import random

"""
Base Character class
"""


class Character:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.max_health = health

    def attack(self, opponent):
        if hasattr(opponent, "evade_active") and opponent.evade_active:
            print(f"{opponent.name} evades the attack!")
            opponent.evade_active = False
            return

        if hasattr(opponent, "shield_active") and opponent.shield_active:
            print(f"{opponent.name}'s Divine Shield blocks the attack!")
            opponent.shield_active = False
            return

        random_damage_power = random.randint(
            self.attack_power - 10, self.attack_power + 10
        )
        opponent.health -= random_damage_power
        print(f"{self.name} attacks {opponent.name} for {random_damage_power} damage!")

        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")

    def display_stats(self):
        print(
            f"{self.name}'s Stats - Health: {self.health}/{self.max_health}"
            f", Attack Power: {self.attack_power}"
        )

    def heal(self):
        if self.health < self.max_health:
            self.health += 15

            if self.health > self.max_health:
                self.health = self.max_health
            print(
                f"{self.name} healed by 15. {self.name} is now at health: {self.health}"
            )
        else:
            print(f"Cannot heal past the max health: {self.max_health}.")


"""
Warrior class (inherits from Character)
"""


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=25)


""" 
Mage class (inherits from Character)
"""


class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)


""" 
EvilWizard class (inherits from Character)
"""


class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=15)

    def regenerate(self):
        self.health += 5
        print(f"{self.name} regenerates 5 health! Current health: {self.health}")


"""
ARCHER CLASS
"""


class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=40)
        self.evade_active = False

    def double_arrow(self, opponent):
        random_damage_power = random.randint(
            max(0, self.attack_power - 10), self.attack_power + 10
        )
        random_damage_power *= 2
        opponent.health -= random_damage_power
        print(
            f"{self.name} attacks {opponent.name} with a double arrow for "
            f"{random_damage_power} damage!"
        )

    def activate_evade(self):
        self.evade_active = True
        print(f"{self.name} activates Evade! They will dodge the next attack.")


"""
PALADIN CLASS
"""


class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=40)
        self.shield_active = False

    def holy_strike(self, opponent):
        if opponent.health < 90:
            bonus_damage = 30
            super().attack(opponent)
            opponent.health -= bonus_damage
            print(
                f"{self.name} uses Holy Strike on {opponent.name}, dealing an additional "
                f"{bonus_damage} bonus damage!"
            )
        else:
            super().attack(opponent)

    def activate_shield(self):
        self.shield_active = True
        print(f"{self.name} activates Divine Shield! They will block the next attack.")


"""
CREATE CHARACTER FUNCTION
"""


def create_character():
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Archer")
    print("4. Paladin")

    class_choice = input("Enter the number of your class choice: ")
    name = input("Enter your character's name: ")

    if class_choice == "1":
        return Warrior(name)
    elif class_choice == "2":
        return Mage(name)
    elif class_choice == "3":
        return Archer(name)
    elif class_choice == "4":
        return Paladin(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)


"""
BATTLE FUNCTION 
"""


def battle(player, wizard):
    while wizard.health > 0 and player.health > 0:
        print("\n--- Your Turn ---")
        print("1. Attack")
        print("2. Use Special Ability")
        print("3. Heal")
        print("4. View Stats")

        choice = input("Choose an action: ")

        if choice == "1":
            player.attack(wizard)
        elif choice == "2":
            if isinstance(player, Archer):
                print("1. Double Arrow")
                print("2. Evade")
                special_choice = input("Choose a special ability: ")
                if special_choice == "1":
                    player.double_arrow(wizard)
                elif special_choice == "2":
                    player.activate_evade()
                else:
                    print("Invalid choice.")
            elif isinstance(player, Paladin):
                print("1. Holy Strike")
                print("2. Divine Shield")
                special_choice = input("Choose a special ability: ")
                if special_choice == "1":
                    player.holy_strike(wizard)
                elif special_choice == "2":
                    player.activate_shield()
                else:
                    print("Invalid choice.")
            else:
                print("Your character has no special offensive abilities.")
        elif choice == "3":
            player.heal()
        elif choice == "4":
            player.display_stats()
        else:
            print("Invalid choice. Try again.")

        if wizard.health > 0:
            wizard.regenerate()
            wizard.attack(player)

        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            break

    if wizard.health <= 0:
        print(f"The wizard {wizard.name} has been defeated by {player.name}!")


def main():
    player = create_character()
    wizard = EvilWizard("The Dark Wizard")
    battle(player, wizard)


if __name__ == "__main__":
    main()
