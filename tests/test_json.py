import json

def json_test(class_, obj):
    print(f'{obj.__dict__}')
    json_obj = obj.to_json()
    json_data = json.dumps(json_obj)
    print(f'{json_data}')
    fjson_data = json.loads(json_data)
    print(f'{fjson_data}')
    new_obj = class_.from_json(fjson_data)
    print(f'{new_obj.__dict__}')
    assert obj.to_json() == new_obj.to_json()
    return new_obj

def json_test_treasure(obj):
    from treasures import take_treasure_item
    print(f'{obj.__dict__}')
    json_obj = obj.to_json()
    json_data = json.dumps(json_obj)
    print(f'{json_data}')
    fjson_data = json.loads(json_data)
    print(f'{fjson_data}')
    new_class_obj = take_treasure_item(fjson_data)
    print(f'{new_class_obj.__dict__}')
    assert obj.to_json() == new_class_obj.to_json()

def take_treasure():
    from map_builder import WorldBuilder
    return WorldBuilder.get_random_treasure()

def take_box():
    from boxes import LootBox
    return LootBox(take_treasure())

def take_quest():
    from quests import QuestObject
    import uuid
    sign = 'test'
    id_ = str(uuid.uuid4())
    return QuestObject(sign, id_)

def take_monster():
    import random
    from map_builder import WorldBuilder
    loot = None
    if random.randint(1,2) == 1:
        loot = take_treasure()
    return WorldBuilder.get_random_monster(loot)

def test_box():
    from boxes import LootBox
    obj = take_box()
    json_test(LootBox, obj)

def test_after_death():
    from creatures import ExplosionMod
    obj = ExplosionMod()
    json_test(ExplosionMod, obj)

def test_treasures():
    from treasures import (LittleMedicine, MediumMedicine, LargeMedicine, ImproveAttack,
                           ImproveShield, FakePowerBook, SacrificeAmulet, ResilienceMutagen, Bomb,
                           PhoenixAmulet, TrueBookOfPower
                           )

    treasures_list = [LittleMedicine, MediumMedicine, LargeMedicine, ImproveAttack,
                      ImproveShield, FakePowerBook, SacrificeAmulet, ResilienceMutagen, Bomb,
                      PhoenixAmulet, TrueBookOfPower
                      ]

    for treasure in treasures_list:
        obj = treasure()
        json_test_treasure(obj)

def test_quest_test_treasures():
    from treasures import Key, ImmortalAmulet
    import uuid
    treasures_list = [Key, ImmortalAmulet]
    for treasure in treasures_list:
        id_ = str(uuid.uuid4())
        obj = treasure(id_)
        json_test_treasure(obj)

def test_player():
    from creatures import Player
    obj = Player('test')
    obj.back_pack = [take_treasure() for _ in range(10)]
    json_test(Player, obj)

def test_monster():
    from creatures import Monster
    for obj in (take_monster() for _ in range(100)):
        json_test(Monster, obj)

def test_quest_obj():
    from quests import QuestObject
    obj = take_quest()
    json_test(QuestObject, obj)

def test_room1():
    from room import Room
    room = Room((3,4))
    room.doors = [(1,1),(1,2),(2,3)]
    room.monster = take_monster()
    room.loot = [take_treasure()]
    room.box = take_box()
    room.quest = take_quest()
    new_room = json_test(Room, room)
    assert isinstance(new_room.name, tuple)
    assert isinstance(new_room.doors, list)
    assert isinstance(new_room.doors[0], tuple)


def test_room2():
    from room import Room
    room = Room((3, 4))
    room.doors = [(1, 1), (1, 2), (2, 3)]
    new_room = json_test(Room, room)
    assert isinstance(new_room.name, tuple)
    assert isinstance(new_room.doors, list)
    assert isinstance(new_room.doors[0], tuple)


def test_world():
    from map_builder import World, WorldBuilder
    from quests import MainQuest, ImmortalAmuletQuest
    world = World(WorldBuilder.give_world(10, 10))
    world = MainQuest.add_quest(world)
    world = ImmortalAmuletQuest.add_quest(world)
    json_test(World, world)


def test_game_state():
    from creatures import Player
    from room import name_convert
    from ui_terminal import UI
    from map_builder import World, WorldBuilder
    from game_states import GameState
    from quests import MainQuest, ImmortalAmuletQuest

    master = UI()
    player = Player('test')
    world = World(WorldBuilder.give_world(10, 10))
    world = MainQuest.add_quest(world)
    world = ImmortalAmuletQuest.add_quest(world)
    curr_room = world.rooms_dict[name_convert('A1')]
    game_state = GameState(master, world, player, curr_room)

    json_obj = game_state.to_json()
    json_data = json.dumps(json_obj)
    print(f'{json_data}')
    fjson_data = json.loads(json_data)
    print(f'{fjson_data}')
    new_game_state = GameState.from_json(fjson_data, master)
    print(f'{new_game_state.__dict__}')
    assert game_state.to_json() == new_game_state.to_json()

