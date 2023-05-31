from typing import Union
import re
from NPC import NPC

SPECIAL_EVENT_NPCS = ['NPC607', 'Otro NPC de evento especial']


class BestNPCFinder:
    def __init__(self, filename, max_damage, party_members=1):
        self.filename = filename
        self.max_damage = max_damage
        self.npcs = []
        self.load_npcs()
        self.party_members = party_members

    def load_npcs(self):
        with open(self.filename, 'r') as file:
            data = file.read()

        start = data.find('#######################NPCS HOSTILES##########################')
        if start == -1:
            print("No se encontraron NPC hostiles en el archivo.")
            return

        data = data[start:]
        npc_sections = re.findall(r'\[NPC\d+\][\s\S]*?(?=\[NPC\d+\]|\Z)', data)

        for npc in npc_sections:
            try:
                code = re.search(r'\[(NPC\d+)\]', npc).group(1)
                min_hp = int(re.search(r'MinHP=(\d+)', npc).group(1))
                max_hp = int(re.search(r'MaxHP=(\d+)', npc).group(1))
                name = re.search(r'Name=(.+?)\n', npc).group(1)  # change here
                give_exp = int(re.search(r'GiveEXP=(\d+)', npc).group(1))
                give_gld = int(re.search(r'GiveGLD=(\d+)', npc).group(1))
                level = int(re.search(r'Nivel=(\d+)', npc).group(1))
                max_hit = int(re.search(r'MaxHIT=(\d+)', npc).group(1))
                min_hit = int(re.search(r'MinHIT=(\d+)', npc).group(1))
                defence = int(re.search(r'DEF=(\d+)', npc).group(1))
                respawn_time = int(re.search(r'IntervaloRespawn=(\d+)', npc).group(1))
                attack_power = (min_hit + max_hit) / 2
                evasion_power = 0  # This value is unknown.

                if code not in SPECIAL_EVENT_NPCS:
                    self.npcs.append(
                        NPC(code, name, give_exp, give_gld, min_hp, max_hp, attack_power, min_hit, max_hit, defence,
                            attack_power, evasion_power, level, respawn_time))
            except AttributeError:
                print(f"Failed to parse NPC: {npc}")

    def best_for_exp(self, num=1):
        sorted_npcs = sorted(self.npcs, key=lambda npc: npc.exp_ratio(), reverse=True)[:num]
        return sorted_npcs

    def best_for_gold(self, num=1):
        sorted_npcs = sorted(self.npcs, key=lambda npc: npc.gold_ratio(), reverse=True)[:num]
        return sorted_npcs

    def best_for_total(self, num=1):
        sorted_npcs = sorted(self.npcs, key=lambda npc: npc.total_ratio(), reverse=True)[:num]
        return sorted_npcs

    def best_for_damage(self, num=1):
        damage_npcs = [npc for npc in self.npcs if npc.max_hp <= self.max_damage]
        sorted_npcs = sorted(damage_npcs, key=lambda npc: npc.total_ratio(), reverse=True)[:num]
        return sorted_npcs

    def best_npc_to_kill(self, player_damage: int = 300, party_members: int = 1) -> Union[NPC, None]:
        npcs_efficiency = []
        party_members = min(party_members, 5)

        for npc in self.npcs:
            hits_to_kill = npc.max_hp / player_damage
            exp_per_hit = npc.exp / hits_to_kill
            gold_per_hit = npc.gold / hits_to_kill
            total_group_exp = npc.exp / party_members
            total_group_gold = npc.gold / party_members

            efficiency = (exp_per_hit + gold_per_hit + total_group_exp + total_group_gold) / 4
            efficiency_per_second = efficiency / npc.respawn_time  # Calculate efficiency per second

            npcs_efficiency.append((npc, efficiency_per_second))

        npcs_efficiency.sort(key=lambda x: x[1], reverse=True)
        best_npc, _ = npcs_efficiency[0] if npcs_efficiency else (None, None)
        return best_npc
