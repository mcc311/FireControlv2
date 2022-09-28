from inspect import getcallargs
from telnetlib import TM
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from problems.solver import Solver
from .models import Problem
from weapons.models import Weapon
from ships.models import Ship
import numpy as np
from .serializers import ProblemSerializer
import time

@api_view(['GET', 'POST'])
def post_problem(request):
    if request.method == 'POST':
        solve(request.data)
        data = Problem.objects.latest('id')
        serializer = ProblemSerializer(data, context={'id':data.id}, many=False)

        return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'GET':
        data = Problem.objects.all()
        serializer = ProblemSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_result(request, id):
    data = Problem.objects.filter(id=id)
    serializer = ProblemSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

def solve(data):
    markers = data['markers']
    enemy_markers = [marker for marker in markers if marker['ship']['belongsTo'] == 'e']
    ally_markers = [marker for marker in markers if marker['ship']['belongsTo'] == 'a']
    distances = data['distances']
    def get_damage_mtx():
        weapons = []
        for marker in ally_markers:
            weapons += [ (marker['id'], Weapon.objects.filter(id=weapon_id)[0]) 
                        for weapon_id in marker['weapons']]
        
        enemies = []

        for marker in enemy_markers:
            enemies += [(marker['id'], Ship.objects.filter(id=marker['ship']['id'])[0])]
        damage_mtx = np.zeros((len(weapons), len(enemies)))
        for i, (aid, weapon) in enumerate(weapons):
            for j, (eid, ship) in enumerate(enemies):
                from_id, to_id = (str(aid), str(eid)) if int(aid) < int(eid) else (str(eid), str(aid))
                distance = float(distances[from_id][to_id])
                damage_mtx[i][j] = weapon.damage * np.max([0, 1 - distance/(weapon.range+1e-6)])
        return damage_mtx


    def get_threat_matrix():
        weapons = []
        num_w = []
        num_e = 0
        for marker in enemy_markers:
            print(marker['id'])
            current_weapons = [ (marker['id'], Weapon.objects.filter(id=weapon_id)[0]) 
                        for weapon_id in marker['weapons']]
            weapons += current_weapons
            num_e += 1
            num_w += [len(current_weapons)]
        
        allies = []

        for marker in ally_markers:
            print(marker['id'])
            current_weapons = [ (marker['id'], Weapon.objects.filter(id=weapon_id)[0]) 
                        for weapon_id in marker['weapons']]
            allies += current_weapons
        damage_mtx = np.zeros((len(weapons), len(allies)))
        for i, (eid, weapon) in enumerate(weapons):
            for j, (aid, ship) in enumerate(allies):
                from_id, to_id = (str(aid), str(eid)) if int(aid) < int(eid) else (str(eid), str(aid))
                distance = float(distances[from_id][to_id])
                damage_mtx[i][j] = weapon.damage * np.max([0, 1 - distance/(weapon.range+1e-6)])
        counter = 0
        threat_mtx = []
        for n in num_w:
            threat_mtx += [np.max(damage_mtx[counter:counter+n], 0)]
            counter += n
        threat_mtx = np.vstack(threat_mtx).T
        print(threat_mtx.shape)

        return threat_mtx

    def get_cost_mtx():
        weapons = []
        for marker in ally_markers:
            weapons += [ (marker['id'], Weapon.objects.filter(id=weapon_id)[0]) 
                        for weapon_id in marker['weapons']]
        cost_mtx = [weapon.cost for _, weapon in weapons]
        cost_mtx = np.array(cost_mtx).T
        return cost_mtx

    damage_mtx = get_damage_mtx()
    threat_mtx = get_threat_matrix()
    cost_mtx = get_cost_mtx()
    aw_pair = [(marker['id'], weapon)  for marker in ally_markers for weapon in marker['weapons']]
    e_ids = [marker['id'] for marker in enemy_markers]

    # print(damage_mtx.shape, damage_mtx)\
    solver = Solver(d_mtx=damage_mtx, t_mtx=threat_mtx, v_mtx=None, c_mtx=cost_mtx, aw_pair=aw_pair, e_ids=e_ids)
    constraint = data['constraint']
    results = {'timeCost':{}}
    timeCost = {}
    for policy in data['policy']:
        start = time.time()
        result = solver.solve(policy=policy, constraint=constraint)
        end = time.time()
        results[policy] = result
        results['timeCost'][policy] = end - start
        
    Problem(problem_request=data, results=results).save()