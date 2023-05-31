import re
from BestNPCFinder import BestNPCFinder


class TimeEstimator:
    def __init__(self, npc_file, level_file, damage_by_player, time_to_kill):
        self.npc_finder = BestNPCFinder(npc_file, damage_by_player)
        self.time_to_kill = float(time_to_kill)
        self.level_exp = self.load_level_exp(level_file)

    def load_level_exp(self, level_file):
        with open(level_file, 'r') as file:
            data = file.read()

        levels_and_exp = re.findall(r'Nivel(\d+)=(\d+)', data)
        return {int(level): int(exp) for level, exp in levels_and_exp}

    def time_to_level_up(self, current_level):
        if current_level >= len(self.level_exp):
            return 0, None, 0

        needed_exp = self.level_exp[current_level]
        npc_list = self.npc_finder.best_for_exp(needed_exp)
        if not npc_list:  # Check if the list is empty
            return 0, None, 0
        best_npc = npc_list[0]
        npc_qty = needed_exp // best_npc.exp  # This is the quantity of NPC needed
        time_to_level_up = npc_qty * self.time_to_kill
        total_gold = best_npc.gold * npc_qty
        return time_to_level_up, best_npc, total_gold

    def total_time_to_max_level(self, max_level):
        total_time = 0
        best_npcs = []
        total_gold = 0
        for level in range(1, max_level + 1):
            time, best_npc, gold = self.time_to_level_up(level)
            total_time += time
            total_gold += gold
            best_npcs.append((level, best_npc, gold))
        return total_time, best_npcs, total_gold

