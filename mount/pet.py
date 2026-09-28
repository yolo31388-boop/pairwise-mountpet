
class Mount:
    def __init__(self, speed_bonus=20, stamina=100):
        self.speed_bonus = speed_bonus
        self.stamina = stamina
        self.max_stamina = stamina
        self.active = False

    def apply_bonus(self, player):
        # BUG: 直接加到基础速度，下马不移除
        player.base_speed += self.speed_bonus
        self.active = True

    def remove_bonus(self, player):
        # BUG: 没有实现移除
        self.active = False

    def consume_stamina(self, dt, mode="run"):
        # BUG: 飞行和奔跑同速率
        self.stamina -= 5 * dt


class Pet:
    def __init__(self):
        self.loyalty = 100
        self.exp = 0
        self.level = 1
        self.skill_cd = 0
        self.auto_loot = True

    def pickup(self, item, inventory):
        # BUG: 不检查背包空间
        inventory.append(item)
        return True

    def gain_exp(self, amount):
        # BUG: 绝对值而非等级曲线
        self.exp += amount
        if self.exp >= 100:
            self.level += 1
            self.exp -= 100

    def decay_loyalty(self, dt, online=True):
        # BUG: 下线也掉忠诚
        self.loyalty -= 1 * dt


class Player:
    def __init__(self):
        self.base_speed = 10
        self.inventory = []
        self.skill_cd = 0
        self.region = "indoor"
