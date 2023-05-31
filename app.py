from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from BestNPCFinder import BestNPCFinder
from TimeEstimator import TimeEstimator

app = FastAPI()

# Crea una instancia de BestNPCFinder.
finder = BestNPCFinder(filename='npcs.dat', max_damage=300)

# Crea una instancia de TimeEstimator.
time_estimator = TimeEstimator('npcs.dat', 'Niveles.dat', 300, 5)  # Replace 'npcs.dat' and 'levels.dat' with your actual filenames

class NPCModel(BaseModel):
    code: str
    name: str
    exp: int
    gold: int
    min_hp: int
    max_hp: int
    damage: int
    min_hit: int
    max_hit: int
    def_: int
    attack_power: int
    evasion_power: int
    level: int
    respawn_time: int
    quantity: int

class TimeToLevelUpModel(BaseModel):
    time: float
    best_npc: Optional[NPCModel]
    total_gold: int

@app.get("/npcs/best_for_exp", response_model=List[NPCModel])
def get_best_for_exp(num: int = 1):
    npcs = finder.best_for_exp(num)
    return [npc.as_dict() for npc in npcs]

@app.get("/npcs/best_for_gold", response_model=List[NPCModel])
def get_best_for_gold(num: int = 1):
    npcs = finder.best_for_gold(num)
    return [npc.as_dict() for npc in npcs]

@app.get("/npcs/best_for_total", response_model=List[NPCModel])
def get_best_for_total(num: int = 1):
    npcs = finder.best_for_total(num)
    return [npc.as_dict() for npc in npcs]

@app.get("/npcs/best_for_damage", response_model=List[NPCModel])
def get_best_for_damage(num: int = 1):
    npcs = finder.best_for_damage(num)
    return [npc.as_dict() for npc in npcs]

@app.get("/time_to_level_up/{current_level}", response_model=TimeToLevelUpModel)
def time_to_level_up(current_level: int):
    time, best_npc, total_gold = time_estimator.time_to_level_up(current_level)
    return {"time": time, "best_npc": best_npc.as_dict() if best_npc else None, "total_gold": total_gold}

@app.get("/best_npc_to_kill/{player_damage}", response_model=Optional[NPCModel])
def get_best_npc_to_kill(player_damage: int, party_members: int = 1):
    npc = finder.best_npc_to_kill(player_damage, party_members)
    if npc is None:
        raise HTTPException(status_code=404, detail="No se encontro NPC")
    return npc.as_dict()

