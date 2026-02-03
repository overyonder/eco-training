#!/usr/bin/env python3
"""
Ecosystem Game Solver - McKinsey PSG (Coral Reef / Mountain)

Rules:
- Select 8 species from available pool
- All species must share overlapping habitat window (depth/elevation + temp)
- Sequential eating simulation: highest Calories Provided eats first
- Eater consumes from food source with highest CURRENT Calories Provided
- Survival: Calories Needed met AND Calories Provided > 0

Usage:
  python solver_ecosystem.py [--scenario reef|mountain] [--max-solutions N]
"""

import argparse
from itertools import combinations
from typing import NamedTuple, Optional

class Species(NamedTuple):
    name: str
    type: str  # 'producer' or 'consumer'
    provided: int
    needed: int
    dim_min: int  # depth or elevation min
    dim_max: int  # depth or elevation max
    temp_min: int
    temp_max: int
    eats: list[str]  # names of food sources

# Example data
REEF_DATA = [
    Species('Giant Kelp', 'producer', 4000, 0, 5, 30, 12, 20, []),
    Species('Sea Grass', 'producer', 2500, 0, 0, 25, 15, 24, []),
    Species('Coral', 'producer', 1800, 0, 5, 20, 18, 26, []),
    Species('Sea Urchin', 'consumer', 800, 600, 5, 25, 14, 22, ['Giant Kelp', 'Sea Grass']),
    Species('Small Fish', 'consumer', 500, 350, 0, 30, 12, 24, ['Sea Grass', 'Coral']),
    Species('Crab', 'consumer', 700, 450, 5, 20, 14, 20, ['Giant Kelp', 'Coral']),
    Species('Lobster', 'consumer', 600, 400, 10, 30, 12, 18, ['Sea Urchin', 'Small Fish']),
    Species('Octopus', 'consumer', 750, 500, 5, 35, 14, 22, ['Crab', 'Lobster']),
    Species('Sea Bass', 'consumer', 650, 450, 10, 40, 12, 20, ['Small Fish', 'Crab']),
    Species('Barracuda', 'consumer', 550, 600, 5, 30, 16, 24, ['Sea Bass', 'Small Fish']),
    Species('Shark', 'consumer', 700, 800, 10, 50, 14, 22, ['Sea Bass', 'Octopus', 'Barracuda']),
]

MOUNTAIN_DATA = [
    Species('Alpine Grass', 'producer', 3500, 0, 1500, 3000, 5, 18, []),
    Species('Mountain Shrub', 'producer', 2800, 0, 1200, 2500, 8, 20, []),
    Species('Pine Tree', 'producer', 2000, 0, 1000, 2200, 5, 15, []),
    Species('Mountain Hare', 'consumer', 700, 500, 1500, 2800, 4, 16, ['Alpine Grass', 'Mountain Shrub']),
    Species('Marmot', 'consumer', 600, 400, 1800, 3000, 2, 14, ['Alpine Grass']),
    Species('Mountain Goat', 'consumer', 800, 650, 2000, 3500, 0, 12, ['Alpine Grass', 'Mountain Shrub']),
    Species('Red Fox', 'consumer', 550, 450, 1200, 2600, 5, 18, ['Mountain Hare', 'Marmot']),
    Species('Golden Eagle', 'consumer', 650, 500, 1500, 3500, 2, 16, ['Mountain Hare', 'Marmot']),
    Species('Snow Leopard', 'consumer', 750, 700, 2000, 3500, -5, 10, ['Mountain Goat', 'Mountain Hare']),
    Species('Wolf', 'consumer', 850, 750, 1500, 3000, 0, 15, ['Mountain Goat', 'Red Fox', 'Marmot']),
]


def habitat_window(sel: list[Species]) -> tuple[int, int, int, int]:
    """Return (dim_min, dim_max, temp_min, temp_max) intersection."""
    return (
        max(s.dim_min for s in sel),
        min(s.dim_max for s in sel),
        max(s.temp_min for s in sel),
        min(s.temp_max for s in sel),
    )


def is_valid_window(w: tuple[int, int, int, int]) -> bool:
    return w[0] <= w[1] and w[2] <= w[3]


def can_eat(c: Species, sel: list[Species]) -> bool:
    if c.type == 'producer':
        return True
    names = {s.name.lower() for s in sel}
    return any(f.lower() in names for f in c.eats)


def simulate(sel: list[Species]) -> tuple[bool, list[str], dict]:
    """
    Run eating simulation.
    Returns (success, log, final_state).
    """
    state = {s.name: {'provided': s.provided, 'needed': s.needed,
                      'eats': s.eats, 'type': s.type, 'met': s.type == 'producer'}
             for s in sel}
    log = []
    order = sorted(sel, key=lambda x: -x.provided)

    for s in order:
        n = s.name
        if s.type == 'producer':
            log.append(f"{n} ({s.provided}) — producer")
            continue
        need = s.needed
        foods = [(f, state[f]['provided']) for f in s.eats
                 if f in state and state[f]['provided'] > 0]
        foods.sort(key=lambda x: -x[1])
        for fn, _ in foods:
            if need <= 0:
                break
            eat = min(need, state[fn]['provided'])
            state[fn]['provided'] -= eat
            need -= eat
            log.append(f"{n} eats {fn}: {state[fn]['provided']+eat}−{eat}={state[fn]['provided']}")
        state[n]['met'] = need <= 0
        if need > 0:
            log.append(f"{n} STARVES (short {need})")
            return False, log, state

    dead = [n for n, d in state.items() if d['provided'] <= 0]
    if dead:
        log.append(f"CONSUMED TO 0: {', '.join(dead)}")
        return False, log, state

    log.append("All 8 survive ✓")
    return True, log, state


def solve(pool: list[Species], max_sol: int = 5) -> list[tuple[list[Species], tuple, list[str]]]:
    solutions = []
    # Sort by provided desc for earlier pruning
    pool = sorted(pool, key=lambda x: -x.provided)

    for combo in combinations(pool, 8):
        if len(solutions) >= max_sol:
            break
        w = habitat_window(combo)
        if not is_valid_window(w):
            continue
        if not all(can_eat(c, combo) for c in combo):
            continue
        ok, log, _ = simulate(combo)
        if ok:
            solutions.append((list(combo), w, log))

    return solutions


def main():
    p = argparse.ArgumentParser(description='Ecosystem Game Solver')
    p.add_argument('--scenario', choices=['reef', 'mountain'], default='reef')
    p.add_argument('--max-solutions', type=int, default=5)
    args = p.parse_args()

    data = REEF_DATA if args.scenario == 'reef' else MOUNTAIN_DATA
    dim_name = 'Depth' if args.scenario == 'reef' else 'Elevation'

    print(f"Solving {args.scenario} scenario...")
    sols = solve(data, args.max_solutions)

    if not sols:
        print("No valid solutions found.")
        return

    for i, (sel, w, log) in enumerate(sols, 1):
        print(f"\n{'='*50}")
        print(f"Solution {i}")
        print(f"{'='*50}")
        print(f"Species: {', '.join(s.name for s in sel)}")
        print(f"Habitat: {dim_name} {w[0]}-{w[1]}m, Temp {w[2]}-{w[3]}°C")
        print(f"\nSimulation:")
        for line in log:
            print(f"  {line}")


if __name__ == '__main__':
    main()
