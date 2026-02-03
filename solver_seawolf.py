#!/usr/bin/env python3
"""
Sea Wolf Game Solver - McKinsey PSG (2025)

Rules:
- Select 3 microbes per site (3 sites total)
- Microbe numerical attributes (1-10) must AVERAGE within site range
- At least one microbe must have each required trait

Usage:
  python solver_seawolf.py [--max-solutions N]
"""

import argparse
from itertools import combinations
from typing import NamedTuple

class Microbe(NamedTuple):
    name: str
    ph: float       # 1-10
    salinity: float # 1-10
    temp: float     # 1-10
    traits: frozenset  # e.g., frozenset({'photosynthetic', 'nitrogen-fixing'})

class Site(NamedTuple):
    name: str
    ph_min: float
    ph_max: float
    salinity_min: float
    salinity_max: float
    temp_min: float
    temp_max: float
    required_traits: frozenset

# Example data (hypothetical — actual game data unknown)
MICROBES = [
    Microbe('Cyanobacteria A', 6.5, 3.0, 7.0, frozenset({'photosynthetic', 'nitrogen-fixing'})),
    Microbe('Cyanobacteria B', 7.0, 2.5, 6.5, frozenset({'photosynthetic'})),
    Microbe('Diatom', 6.0, 5.0, 5.5, frozenset({'photosynthetic', 'silica-shell'})),
    Microbe('Green Algae', 5.5, 4.0, 6.0, frozenset({'photosynthetic'})),
    Microbe('Nitrosomonas', 7.5, 4.5, 7.5, frozenset({'nitrogen-fixing', 'aerobic'})),
    Microbe('Nitrobacter', 7.0, 5.0, 7.0, frozenset({'nitrogen-fixing', 'aerobic'})),
    Microbe('Sulfur Bacteria', 4.0, 6.0, 8.0, frozenset({'anaerobic', 'sulfur-oxidizing'})),
    Microbe('Methanogen', 6.0, 3.5, 8.5, frozenset({'anaerobic', 'methane-producing'})),
    Microbe('Purple Bacteria', 5.0, 4.0, 7.0, frozenset({'photosynthetic', 'anaerobic'})),
    Microbe('Iron Bacteria', 5.5, 5.5, 6.5, frozenset({'aerobic', 'iron-oxidizing'})),
    Microbe('Archaea X', 3.5, 7.0, 9.0, frozenset({'extremophile', 'anaerobic'})),
    Microbe('Archaea Y', 4.0, 8.0, 8.5, frozenset({'extremophile', 'sulfur-oxidizing'})),
]

SITES = [
    Site('Coastal Estuary', 5.5, 7.0, 3.0, 5.0, 6.0, 7.5,
         frozenset({'photosynthetic', 'nitrogen-fixing'})),
    Site('Deep Ocean Vent', 3.5, 5.0, 6.0, 8.0, 7.5, 9.0,
         frozenset({'anaerobic', 'sulfur-oxidizing'})),
    Site('Freshwater Lake', 6.0, 7.5, 2.0, 4.0, 5.5, 7.0,
         frozenset({'photosynthetic'})),
]


def validate_selection(microbes: list[Microbe], site: Site) -> tuple[bool, str]:
    """Check if 3 microbes satisfy site requirements. Returns (valid, reason)."""
    if len(microbes) != 3:
        return False, "Need exactly 3 microbes"

    # Compute averages
    avg_ph = sum(m.ph for m in microbes) / 3
    avg_sal = sum(m.salinity for m in microbes) / 3
    avg_temp = sum(m.temp for m in microbes) / 3

    # Check ranges
    if not (site.ph_min <= avg_ph <= site.ph_max):
        return False, f"pH avg {avg_ph:.1f} outside [{site.ph_min}, {site.ph_max}]"
    if not (site.salinity_min <= avg_sal <= site.salinity_max):
        return False, f"Salinity avg {avg_sal:.1f} outside [{site.salinity_min}, {site.salinity_max}]"
    if not (site.temp_min <= avg_temp <= site.temp_max):
        return False, f"Temp avg {avg_temp:.1f} outside [{site.temp_min}, {site.temp_max}]"

    # Check traits
    all_traits = set()
    for m in microbes:
        all_traits |= m.traits
    missing = site.required_traits - all_traits
    if missing:
        return False, f"Missing traits: {missing}"

    return True, f"pH={avg_ph:.1f}, sal={avg_sal:.1f}, temp={avg_temp:.1f}"


def solve_site(pool: list[Microbe], site: Site, max_sol: int = 5) -> list[tuple[list[Microbe], str]]:
    """Find valid microbe combinations for a single site."""
    solutions = []
    for combo in combinations(pool, 3):
        if len(solutions) >= max_sol:
            break
        ok, info = validate_selection(list(combo), site)
        if ok:
            solutions.append((list(combo), info))
    return solutions


def solve_all_no_reuse(pool: list[Microbe], sites: list[Site],
                       max_sol: int = 5) -> list[dict[str, list[Microbe]]]:
    """Solve all sites without reusing microbes."""
    solutions = []

    def search(idx: int, used: set[str], assignment: dict):
        if len(solutions) >= max_sol:
            return
        if idx == len(sites):
            solutions.append({k: list(v) for k, v in assignment.items()})
            return
        site = sites[idx]
        avail = [m for m in pool if m.name not in used]
        for combo in combinations(avail, 3):
            ok, _ = validate_selection(list(combo), site)
            if ok:
                new_used = used | {m.name for m in combo}
                assignment[site.name] = combo
                search(idx + 1, new_used, assignment)
                del assignment[site.name]

    search(0, set(), {})
    return solutions


def main():
    p = argparse.ArgumentParser(description='Sea Wolf Game Solver')
    p.add_argument('--max-solutions', type=int, default=5)
    p.add_argument('--allow-reuse', action='store_true',
                   help='Allow same microbe at multiple sites')
    args = p.parse_args()

    print("Sea Wolf Solver")
    print("="*50)
    print(f"Pool: {len(MICROBES)} microbes, {len(SITES)} sites")
    print(f"Reuse allowed: {args.allow_reuse}\n")

    if args.allow_reuse:
        # Solve each site independently
        for site in SITES:
            print(f"\n{'='*50}")
            print(f"Site: {site.name}")
            print(f"Requirements: pH {site.ph_min}-{site.ph_max}, "
                  f"sal {site.salinity_min}-{site.salinity_max}, "
                  f"temp {site.temp_min}-{site.temp_max}")
            print(f"Required traits: {set(site.required_traits)}")
            print("-"*50)

            sols = solve_site(MICROBES, site, args.max_solutions)
            if not sols:
                print("No valid solutions.")
                continue

            for i, (sel, info) in enumerate(sols, 1):
                names = ', '.join(m.name for m in sel)
                print(f"{i}. {names}")
                print(f"   Averages: {info}")
    else:
        # Solve all sites together without reuse
        sols = solve_all_no_reuse(MICROBES, SITES, args.max_solutions)
        if not sols:
            print("No valid solution covering all sites without reuse.")
            return

        for i, assignment in enumerate(sols, 1):
            print(f"\n{'='*50}")
            print(f"Full Solution {i}")
            print("="*50)
            for site_name, microbes in assignment.items():
                names = ', '.join(m.name for m in microbes)
                site = next(s for s in SITES if s.name == site_name)
                _, info = validate_selection(microbes, site)
                print(f"\n{site_name}:")
                print(f"  Microbes: {names}")
                print(f"  {info}")


if __name__ == '__main__':
    main()
