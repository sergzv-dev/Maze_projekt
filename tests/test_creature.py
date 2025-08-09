from creatures import Player, Monster

def test_heal_hp():
    test_player = Player('test', hp = 50)
    chek = 0
    while chek < 15:
        test_hp = test_player.hp + 7
        test_player.heal_hp(7)
        player_hp = test_player.hp
        assert  player_hp == test_hp or player_hp == test_player.max_hp
        chek += 1

def test_get_damage():
    test_player = Player('test', hp=50)
    chek = 0
    while chek < 15:
        test_hp = test_player.hp - 7
        test_player.get_damage(7)
        player_hp = test_player.hp
        assert player_hp == test_hp or player_hp == -1
        chek += 1

    test_player = Player('test', hp=5)
    test_player.get_damage(7, death=False)
    assert test_player.hp == 1
    test_player.get_damage(7, death=False)
    assert test_player.hp == -1

    test_monster = Monster('monster', 15, 15, 50, 10)
    chek = 0
    while chek < 15:
        test_hp = test_monster.hp - 7
        test_monster.get_damage(7)
        monster_hp = test_monster.hp
        assert monster_hp == test_hp or monster_hp == -1
        chek += 1


def test_increase_spec():
    test_player = Player('test')
    chek = 0
    while chek < 15:
        test_spec = test_player.attack + 3
        test_player.increase_spec('attack', 3)
        player_spec = test_player.attack
        assert player_spec == test_spec
        chek += 1

    chek = 0
    while chek < 15:
        test_spec = test_player.shield + 3
        test_player.increase_spec('shield', 3)
        player_spec = test_player.shield
        assert player_spec == test_spec or player_spec == test_player.max_shield
        assert test_player.max_shield == 25
        chek += 1

    chek = 0
    while chek < 15:
        test_spec = test_player.max_hp + 3
        test_player.increase_spec('max_hp', 3)
        player_spec = test_player.max_hp
        assert player_spec == test_spec
        chek += 1

    chek = 0
    while chek < 15:
        test_spec = test_player.agility + 3
        test_player.increase_spec('agility', 3)
        player_spec = test_player.agility
        assert player_spec == test_spec
        chek += 1

def test_reduce_spec():
    test_player = Player('test')
    chek = 0
    while chek < 15:
        test_spec = test_player.attack - 3
        test_player.reduce_spec('attack', 3)
        player_spec = test_player.attack
        assert player_spec == test_spec or  player_spec == 1
        chek += 1

    chek = 0
    while chek < 15:
        test_spec = test_player.shield - 3
        test_player.reduce_spec('shield', 3)
        player_spec = test_player.shield
        assert player_spec == test_spec or player_spec == 1
        chek += 1

    chek = 0
    while chek < 15:
        test_spec = test_player.max_hp - 3
        test_player.reduce_spec('max_hp', 3)
        player_spec = test_player.max_hp
        assert player_spec == test_spec or player_spec == 1
        chek += 1

    chek = 0
    while chek < 15:
        test_spec = test_player.agility - 3
        test_player.reduce_spec('agility', 3)
        player_spec = test_player.agility
        assert player_spec == test_spec or player_spec == 1
        chek += 1

