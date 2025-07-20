from treasures import Medicine, ImproveAttack, ImproveShield
import random

class LootBox():
    def __init__(self):
        self.loot = [self.add_loot(Medicine, ImproveAttack, ImproveShield)]

    @staticmethod
    def add_loot(med, imp_attack, imp_shield):
        luck = random.randint(1, 100)
        if 1 <= luck < 35:
            return med(10)
        if 35 <= luck < 55:
            return med(15)
        if 55 <= luck < 70:
            return med(25)
        if 70 <= luck < 85:
            return imp_attack()
        if 85 <= luck <= 100:
            return imp_shield()
        return None

    def __repr__(self):
        return 'open the box'