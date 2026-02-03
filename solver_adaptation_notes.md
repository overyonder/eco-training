# Solver Adaptation: Ecosystem → Redrock / Sea Wolf

## Current Ecosystem Solver

**Core algorithm:**
1. Generate all C(n, 8) combinations of species
2. Filter: habitat window intersection valid (dim + temp overlap)
3. Filter: all consumers have at least one food source in selection
4. Simulate: sort by Calories Provided desc, sequential eating
5. Validate: all species survive (Needed met AND Provided > 0)

**Key data structures:**
- Species: name, type, provided, needed, dim_min/max, temp_min/max, eats[]

---

## Redrock Island (2025)

**PARTIALLY ADAPTABLE** — workflow assistant rather than combinatorial solver.

**Data Types:**
- **Studies**: Extended research task with 3 stages
- **Cases**: Short independent questions on different research topics

**Three Stages (for Studies):**
1. **Investigation**: Collect observations, review relevant datapoints
2. **Analysis**: Evaluate data, perform calculations based on study questions
3. **Report**: Compose and submit written/visual reports

**Exercise Structure:**
- 1 Study (multi-stage) + 3 Cases (independent short questions)

**Why traditional solver doesn't apply:**
- No combinatorial selection (unlike Ecosystem's 8-of-39)
- Success depends on data interpretation and calculation accuracy
- Workflow is sequential, not optimization-based

**What a helper tool CAN do:**
- Track progress through stages
- Organize collected datapoints during Investigation
- Provide calculation templates for Analysis
- Structure report output for Report stage
- Timer/pacing for the exercise

---

## Sea Wolf (2025)

**ADAPTABLE** — similar selection mechanics, simpler validation.

### Game Mechanics

**Task:** Select 3 microbes per site × 3 sites = 9 microbes total (30 min)

**Microbe attributes:**
- Numerical (1-10 scale): e.g., pH tolerance, salinity tolerance, temperature range
- Binary traits: e.g., "photosynthetic", "nitrogen-fixing", "anaerobic"

**Site requirements:**
- Numerical ranges: "pH must be 4-6", "salinity 2-5"
- Required traits: "must include nitrogen-fixing microbe"
- The AVERAGE of selected microbes' attributes must fall within site range

### Required Changes to Solver

```python
# NEW: Microbe data structure
class Microbe(NamedTuple):
    name: str
    # Numerical attributes (1-10 scale)
    ph: float
    salinity: float
    temp: float
    # Binary traits
    traits: set[str]  # e.g., {'photosynthetic', 'nitrogen-fixing'}

# NEW: Site requirements
class Site(NamedTuple):
    name: str
    ph_min: float
    ph_max: float
    salinity_min: float
    salinity_max: float
    temp_min: float
    temp_max: float
    required_traits: set[str]  # at least one microbe must have each

# CHANGE: Validation logic (replaces simulate())
def validate_site(microbes: list[Microbe], site: Site) -> bool:
    if len(microbes) != 3:
        return False

    # Check averages within range
    avg_ph = sum(m.ph for m in microbes) / 3
    avg_sal = sum(m.salinity for m in microbes) / 3
    avg_temp = sum(m.temp for m in microbes) / 3

    if not (site.ph_min <= avg_ph <= site.ph_max):
        return False
    if not (site.salinity_min <= avg_sal <= site.salinity_max):
        return False
    if not (site.temp_min <= avg_temp <= site.temp_max):
        return False

    # Check all required traits are covered
    all_traits = set()
    for m in microbes:
        all_traits |= m.traits
    if not site.required_traits.issubset(all_traits):
        return False

    return True

# CHANGE: Solver (simpler — C(n,3) per site, no simulation)
def solve_site(pool: list[Microbe], site: Site) -> list[list[Microbe]]:
    solutions = []
    for combo in combinations(pool, 3):
        if validate_site(combo, site):
            solutions.append(list(combo))
    return solutions

# NEW: Multi-site solver (if microbes can't be reused)
def solve_all_sites(pool: list[Microbe], sites: list[Site],
                    reuse: bool = True) -> list[dict[str, list[Microbe]]]:
    """
    If reuse=True: same microbe can appear at multiple sites
    If reuse=False: each microbe used at most once across all sites
    """
    if reuse:
        # Simple: solve each site independently
        return [{s.name: solve_site(pool, s) for s in sites}]

    # Complex: backtracking search
    solutions = []
    def search(site_idx: int, used: set[str], assignment: dict):
        if site_idx == len(sites):
            solutions.append(assignment.copy())
            return
        site = sites[site_idx]
        available = [m for m in pool if m.name not in used]
        for combo in combinations(available, 3):
            if validate_site(combo, site):
                new_used = used | {m.name for m in combo}
                assignment[site.name] = list(combo)
                search(site_idx + 1, new_used, assignment)
                del assignment[site.name]
    search(0, set(), {})
    return solutions
```

### Key Differences Summary

| Aspect | Ecosystem | Sea Wolf |
|--------|-----------|----------|
| Selection size | 8 species | 3 microbes × 3 sites |
| Validation | Sequential simulation | Average within range |
| Complexity | State mutation, order matters | Stateless, order irrelevant |
| Constraints | Habitat overlap + food chain | Attribute averages + traits |
| Failure mode | Starvation / consumption | Average out of range |

### Implementation Priority

1. **Data entry UI** — microbe cards with sliders (1-10) and trait checkboxes
2. **Site config** — range inputs and required trait selection
3. **Solver** — straightforward enumeration (C(n,3) small)
4. **Visualization** — show averages vs requirements

---

## File Structure Recommendation

```
eco-training/
├── index.html           # Ecosystem trainer (existing)
├── seawolf.html         # Sea Wolf trainer (new)
├── solver_ecosystem.py  # CLI solver for ecosystem
├── solver_seawolf.py    # CLI solver for sea wolf
└── redrock.html         # Redrock prep (practice problems, no solver)
```
