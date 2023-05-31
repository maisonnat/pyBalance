import re


class NPC:

    def __init__(self, code: str, name: str, exp: int, gold: int, min_hp: int, max_hp: int, damage: int, min_hit: int,
                 max_hit: int, def_: int, attack_power: int, evasion_power: int, level: int, respawn_time: int,
                 immunity: int = 0, quantity: int = 1, group_members: int = 1):
        self.code = code
        self.name = name
        self.exp = exp
        self.gold = gold
        self.min_hp = min_hp
        self.max_hp = max_hp
        self.damage = damage
        self.min_hit = min_hit
        self.max_hit = max_hit
        self.def_ = def_
        self.attack_power = attack_power
        self.evasion_power = evasion_power
        self.level = level
        self.difficulty = self._difficulty()
        self.respawn_time = respawn_time
        self.immunity = immunity
        self.quantity = quantity
        self.group_members = group_members

    def __str__(self):
        return f"{self.name} (Code: {self.code}, Exp: {self.exp}, Gold: {self.gold})"
    # Calcula la dificultad del NPC basándose en sus estadísticas.

    def _difficulty(self):
        total_damage = self.group_members * 300  # 300 es el daño que hace cada miembro del grupo
        hp_diff = self.max_hp - self.min_hp
        return hp_diff / 2 + self.damage - total_damage

    # Calcula el ratio de recompensa a dificultad para la experiencia y el oro.
    def exp_ratio(self):
        return self.exp / self.difficulty

    def gold_ratio(self):
        return self.gold / self.difficulty

    def total_ratio(self):
        return self.exp_ratio() + self.gold_ratio()

    def as_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "exp": self.exp,
            "gold": self.gold,
            "min_hp": self.min_hp,
            "max_hp": self.max_hp,
            "damage": self.damage,
            "min_hit": self.min_hit,
            "max_hit": self.max_hit,
            "def_": self.def_,
            "attack_power": self.attack_power,
            "evasion_power": self.evasion_power,
            "level": self.level,
            "respawn_time": self.respawn_time,
            "immunity": self.immunity,
            "quantity": self.quantity
        }

    @staticmethod
    def from_string(npc_string: str) -> 'NPC':
        """Crea una instancia de NPC a partir de un string que define a un NPC."""
        try:
            code = re.search(r'\[(NPC\d+)\]', npc_string).group(1)
            name = re.search(r'Name=(\w+)', npc_string).group(1)
            min_hp = int(re.search(r'MinHP=(\d+)', npc_string).group(1))
            max_hp = int(re.search(r'MaxHP=(\d+)', npc_string).group(1))
            give_exp = int(re.search(r'GiveEXP=(\d+)', npc_string).group(1))
            give_gld = int(re.search(r'GiveGLD=(\d+)', npc_string).group(1))
            level = int(re.search(r'Nivel=(\d+)', npc_string).group(1))
            min_hit = int(re.search(r'MinHIT=(\d+)', npc_string).group(1))
            max_hit = int(re.search(r'MaxHIT=(\d+)', npc_string).group(1))
            def_ = int(re.search(r'DEF=(\d+)', npc_string).group(1))
            respawn_time = int(re.search(r'IntervaloRespawn=(\d+)', npc_string).group(1))
            attack_power = (min_hit + max_hit) / 2
            damage = attack_power  # Let's suppose the damage is the attack power
            evasion_power = 0  # Let's suppose the evasion power is 0
            immunity = 0  # Default immunity is 0
            quantity = 1  # Default quantity is 1

            # If the NPC string has an Immunity attribute, override the default
            immunity_match = re.search(r'Inmunidad=(\d+)', npc_string)
            if immunity_match:
                immunity = int(immunity_match.group(1))

            return NPC(code, name, give_exp, give_gld, min_hp, max_hp, damage, min_hit, max_hit, def_, attack_power,
                       evasion_power, level, respawn_time, immunity, quantity)
        except AttributeError:
            print(f"Failed to parse NPC: {npc_string}")
            return None
