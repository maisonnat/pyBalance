from NPC import NPC
import math
import re
import json
from datetime import datetime
from pathlib import Path


def copy(self, target):
    import shutil
    shutil.copy2(self, target)


# Añade el método a la clase Path
Path.copy = copy


class NPCBalancer:
    def __init__(self, filename, exp_multiplier=1, gold_multiplier=1, level_multiplier=1):
        self.filename = Path(filename)
        self.exp_multiplier = exp_multiplier
        self.gold_multiplier = gold_multiplier
        self.level_multiplier = level_multiplier
        self.change_report = []

    def backup_file(self):
        backup_filename = f"{self.filename.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{self.filename.suffix}"
        self.filename.copy(backup_filename)  # Utilizando pathlib para copiar el archivo.

    def balance(self):
        # Crea una copia de seguridad del archivo original.
        self.backup_file()

        output_filename = f"{self.filename}_balanced"
        with self.filename.open('r') as file, Path(output_filename).open('w') as output_file:
            # Utilizando pathlib para abrir los archivos.
            npc_data = ""
            for line in file:
                if line.startswith("[NPC"):
                    if npc_data:  # if there is any NPC data accumulated, process it
                        output_file.write(self.process_npc(npc_data))
                        npc_data = ""  # clear the accumulated data
                    npc_data += line  # start accumulating data for the new NPC
                else:
                    if npc_data:  # if we are inside an NPC block, accumulate the data
                        npc_data += line
                    else:  # otherwise, write the line to the output file directly
                        output_file.write(line)

            # process the last NPC
            if npc_data:
                output_file.write(self.process_npc(npc_data))

        # Replace the original file with the balanced file
        Path(output_filename).rename(self.filename)  # Utilizando pathlib para mover el archivo.

    def process_npc(self, npc):
        try:
            # Extract the old values of the NPC
            code = re.search(r'\[(NPC\d+)\]', npc).group(1)
            min_hp = int(re.search(r'MinHP=(\d+)', npc).group(1))
            max_hp = int(re.search(r'MaxHP=(\d+)', npc).group(1))
            name = re.search(r'Name=(\w+)', npc).group(1)
            give_exp = int(re.search(r'GiveEXP=(\d+)', npc).group(1))
            give_gld = int(re.search(r'GiveGLD=(\d+)', npc).group(1))
            level = int(re.search(r'Nivel=(\d+)', npc).group(1))
            max_hit = int(re.search(r'MaxHIT=(\d+)', npc).group(1))
            min_hit = int(re.search(r'MinHIT=(\d+)', npc).group(1))
            def_ = int(re.search(r'DEF=(\d+)', npc).group(1))
            attack_power = (min_hit + max_hit) / 2
            damage = attack_power  # Let's suppose the damage is the attack power
            evasion_power = 0  # Let's suppose the evasion power is 0

            old_npc = NPC(code, name, give_exp, give_gld, min_hp, max_hp, damage, min_hit, max_hit, def_, attack_power,
                          evasion_power, level)

            # Calculate the new values of GiveEXP, GiveGLD, MinHP, and MaxHP based on multipliers and level
            give_exp *= self.exp_multiplier
            give_gld *= self.gold_multiplier
            min_hp *= self.level_multiplier
            max_hp *= self.level_multiplier

            new_npc = NPC(code, name, math.ceil(give_exp), math.ceil(give_gld), min_hp, max_hp, damage, min_hit,
                          max_hit, def_, attack_power, evasion_power, level)
            self.change_report.append({"old": old_npc.as_dict(), "new": new_npc.as_dict()})

            # Replace the old values in the NPC section
            npc = re.sub(r'GiveEXP=\d+', f'GiveEXP={math.ceil(give_exp)}', npc)
            npc = re.sub(r'GiveGLD=\d+', f'GiveGLD={math.ceil(give_gld)}', npc)
            npc = re.sub(r'MinHP=\d+', f'MinHP={min_hp}', npc)
            npc = re.sub(r'MaxHP=\d+', f'MaxHP={max_hp}', npc)
        except AttributeError:
            print(f"Failed to parse NPC: {npc}")

        return npc

    def save_report(self):
        with Path('npc_change_report.json').open('w') as f:  # Utilizando pathlib para abrir el archivo.
            json.dump(self.change_report, f)
