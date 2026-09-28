class Mount:
    # 不同移动模式下的耐力消耗速率（每秒）
    STAMINA_RATES = {"run": 5, "fly": 10, "swim": 3}
    # 允许骑乘的区域
    RIDABLE_REGIONS = ("outdoor", "field")

    def __init__(self, speed_bonus=20, stamina=100):
        self.speed_bonus = speed_bonus
        self.stamina = stamina
        self.max_stamina = stamina
        self.active = False

    def apply_bonus(self, player):
        # 修饰器模式：上马时挂载速度修饰器
        if self.active:
            return
        player.base_speed += self.speed_bonus
        self.active = True

    def remove_bonus(self, player):
        # 下马时精确卸载同一个修饰器
        if not self.active:
            return
        player.base_speed -= self.speed_bonus
        self.active = False

    def consume_stamina(self, dt, mode="run"):
        rate = self.STAMINA_RATES.get(mode, self.STAMINA_RATES["run"])
        self.stamina = max(0, self.stamina - rate * dt)

    def can_summon(self, player):
        return getattr(player, "region", None) in self.RIDABLE_REGIONS


class Pet:
    DEFAULT_INVENTORY_CAP = 10
    SKILL_COOLDOWN = 5
    LOYALTY_DECAY_RATE = 1

    def __init__(self):
        self.loyalty = 100
        self.exp = 0
        self.level = 1
        # 宠物自己的冷却计时器，与主人完全独立
        self.skill_cd = 0
        self.auto_loot = True
        self.fed = False
        self.message = ""

    def pickup(self, item, inventory, cap=DEFAULT_INVENTORY_CAP):
        # 拾取前先检查背包剩余空间
        if len(inventory) >= cap:
            self.message = "背包空间不足，无法拾取"
            return False
        inventory.append(item)
        return True

    def cast_skill(self):
        # 只写入宠物自身的冷却，不触碰主人的计时器
        if self.skill_cd > 0:
            return False
        self.skill_cd = self.SKILL_COOLDOWN
        return True

    def tick_cooldown(self, dt):
        self.skill_cd = max(0, self.skill_cd - dt)

    def exp_to_next_level(self):
        # 等级曲线：升到下一级所需经验随当前等级递增
        return 100 * self.level

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next_level():
            self.exp -= self.exp_to_next_level()
            self.level += 1

    def feed(self):
        self.fed = True
        self.loyalty = min(100, self.loyalty + 10)

    def decay_loyalty(self, dt, online=True):
        # 下线冻结忠诚度；已喂食期间也不下降
        if not online or self.fed:
            return
        self.loyalty = max(0, self.loyalty - self.LOYALTY_DECAY_RATE * dt)
        if self.loyalty == 0:
            self.message = "忠诚度耗尽，宠物离开了"


class Player:
    def __init__(self):
        self.base_speed = 10
        self.inventory = []
        self.inventory_cap = 10
        self.skill_cd = 0
        self.region = "indoor"
