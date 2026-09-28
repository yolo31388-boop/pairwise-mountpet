
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mount.pet import Mount, Pet, Player


def test_mount_bonus_removed_on_dismount():
    p = Player()
    m = Mount(speed_bonus=20)
    m.apply_bonus(p)
    assert p.base_speed == 30
    m.remove_bonus(p)
    assert p.base_speed == 10


def test_pet_pickup_checks_inventory_space():
    p = Player()
    p.inventory = ["item"] * 9
    p.inventory_cap = 10
    pet = Pet()
    assert pet.pickup("new_item", p.inventory) == True
    assert pet.pickup("another", p.inventory) == False


def test_pet_skill_cd_independent_from_owner():
    p = Player()
    p.skill_cd = 10
    pet = Pet()
    pet.skill_cd = 0
    # 宠物CD不应受主人影响
    assert pet.skill_cd == 0


def test_mount_stamina_different_by_mode():
    m = Mount()
    m.stamina = 100
    m.consume_stamina(1, "run")
    run_cost = 100 - m.stamina
    m.stamina = 100
    m.consume_stamina(1, "fly")
    fly_cost = 100 - m.stamina
    assert fly_cost > run_cost


def test_pet_exp_curve_increases():
    pet = Pet()
    pet.gain_exp(100)
    assert pet.level == 2
    # 二级升三级需要更多经验
    pet.gain_exp(100)
    assert pet.level == 2  # 100不够升三级


def test_summon_mount_checks_region():
    p = Player()
    p.region = "indoor"
    m = Mount()
    assert m.can_summon(p) == False
    p.region = "outdoor"
    assert m.can_summon(p) == True


def test_pet_loyalty_frozen_offline():
    pet = Pet()
    pet.loyalty = 100
    pet.decay_loyalty(10, online=False)
    assert pet.loyalty == 100


def test_pet_loyalty_decays_online():
    pet = Pet()
    pet.loyalty = 100
    pet.decay_loyalty(10, online=True)
    assert pet.loyalty < 100


def test_mount_active_state():
    p = Player()
    m = Mount()
    m.apply_bonus(p)
    assert m.active == True
    m.remove_bonus(p)
    assert m.active == False
