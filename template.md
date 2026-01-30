---
title: Ecosystem Game Scratch Pad
subtitle: McKinsey Solve - 35 min time limit
geometry: margin=1.5cm
fontsize: 10pt
---

# Key Rules

**Eating Order:** Species with highest Calories Provided eats first. Food source's Provided decreases permanently.

**Survival:** Calories Needed must be met AND Calories Provided must remain > 0.

**Terrain:** Only Depth/Elevation and Temperature typically matter.

---

# Habitat Window

| Dimension | Min | Max |
|-----------|-----|-----|
| Depth (m) | | |
| Temp (C) | | |

---

# Selected Species (sorted by Calories Provided - highest first)

| # | Species Name | Provided | Needed | Eats |
|---|--------------|----------|--------|------|
| 1 | | | (producer) | |
| 2 | | | (producer) | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |

---

# Eating Simulation

Walk through in order of Calories Provided (highest first):

| Eater | Eats | Food's Provided - Needed = Remaining |
|-------|------|--------------------------------------|
| | | - = |
| | | - = |
| | | - = |
| | | - = |
| | | - = |
| | | - = |

---

# Survival Check

- [ ] All consumers' Needed met?
- [ ] All species' Provided > 0?

---

# Dead End Recovery

If simulation fails:

| Problem | Fix |
|---------|-----|
| Predator consumes prey entirely | Swap for predator with lower Needed |
| Producer exhausted | Add second producer or swap herbivore |
| Species eaten before it eats | Needs higher Provided (eats earlier) |
| No 8 species fit window | Try different anchor producer |

---

# Final Habitat Placement

Pick **middle** of each range:

- Depth: _____ m
- Temp: _____ C
