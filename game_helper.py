import json
from BestNPCFinder import BestNPCFinder

if __name__ == "__main__":
    npc_finder = BestNPCFinder('npcs.dat', 300, 1)

    best_exp_npcs = npc_finder.best_for_exp(20)
    best_gold_npcs = npc_finder.best_for_gold(3)
    best_total_npc = npc_finder.best_for_total(3)
    best_damage_npcs = npc_finder.best_for_damage(5)

    report = {
        'best_exp_npcs': [npc.as_dict() for npc in best_exp_npcs],
        'best_gold_npcs': [npc.as_dict() for npc in best_gold_npcs],
        'best_total_npc': best_total_npc[0].as_dict(),
        'best_damage_npcs': [npc.as_dict() for npc in best_damage_npcs],
    }

    report_json = json.dumps(report, indent=4)

    # Imprime el informe en formato JSON.
    print(report_json)

    # También puedes guardar el informe en un archivo
    with open('npc_report.json', 'w') as f:
        f.write(report_json)
