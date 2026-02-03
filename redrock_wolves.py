#!/usr/bin/env python3
"""Redrock Session: Wolf Predation Analysis"""

# Updated data after +8 days
wind_river = {'days': 20, 'wolves': 10, 'kills': 8, 'prey_pop': 281}
high_peak = {'days': 19, 'wolves': 13, 'kills': 5, 'prey_pop': 400}
illness_rate = 0.18  # 18% annual loss to illness

print("="*60)
print("REDROCK: Wolf Predation Analysis")
print("="*60)

# Q1: New kill rates
print("\nQ1: New Kill Rates")
print("-"*40)
print("Formula: total prey killed / (tracking days × pack size)")
print()

wr_rate = wind_river['kills'] / (wind_river['days'] * wind_river['wolves'])
print("Wind River:")
print(f"  total prey killed = {wind_river['kills']}")
print(f"  tracking days = {wind_river['days']}")
print(f"  pack size = {wind_river['wolves']} wolves")
print(f"  kill rate = {wind_river['kills']} / ({wind_river['days']} × {wind_river['wolves']}) = {wr_rate:.4f}")

hp_rate = high_peak['kills'] / (high_peak['days'] * high_peak['wolves'])
print("\nHigh Peak:")
print(f"  total prey killed = {high_peak['kills']}")
print(f"  tracking days = {high_peak['days']}")
print(f"  pack size = {high_peak['wolves']} wolves")
print(f"  kill rate = {high_peak['kills']} / ({high_peak['days']} × {high_peak['wolves']}) = {hp_rate:.4f}")

print(f"\n>>> Wind River: {wr_rate:.2f} prey/day/wolf")
print(f">>> High Peak:  {hp_rate:.2f} prey/day/wolf")

# Q2: Prey killed per year per pack
print("\n" + "="*60)
print("\nQ2: Prey Killed Per Year")
print("-"*40)
print("Formula: kill rate (rounded) × pack size × days per year")
print()

# Use rounded kill rates for yearly calculation
wr_rate_rounded = round(wr_rate, 2)
hp_rate_rounded = round(hp_rate, 2)

wr_yearly = wr_rate_rounded * wind_river['wolves'] * 365
print("Wind River:")
print(f"  kill rate (rounded) = {wr_rate_rounded:.2f} prey/day/wolf")
print(f"  pack size = {wind_river['wolves']} wolves")
print(f"  days per year = 365")
print(f"  yearly kills = {wr_rate_rounded:.2f} × {wind_river['wolves']} × 365 = {wr_yearly:.2f}")

hp_yearly = hp_rate_rounded * high_peak['wolves'] * 365
print("\nHigh Peak:")
print(f"  kill rate (rounded) = {hp_rate_rounded:.2f} prey/day/wolf")
print(f"  pack size = {high_peak['wolves']} wolves")
print(f"  days per year = 365")
print(f"  yearly kills = {hp_rate_rounded:.2f} × {high_peak['wolves']} × 365 = {hp_yearly:.2f}")

print(f"\n>>> Wind River: {wr_yearly:.2f} prey/year")
print(f">>> High Peak:  {hp_yearly:.2f} prey/year")

# Q3: Percentage of yearly prey loss due to wolves
print("\n" + "="*60)
print("\nQ3: Percentage of Yearly Prey Loss Due to Wolves")
print("-"*40)
print("Formula: (wolf kills / total prey loss) × 100")
print()

# Wind River
wr_illness = illness_rate * wind_river['prey_pop']
wr_total_loss = wr_yearly + wr_illness
wr_wolf_pct = (wr_yearly / wr_total_loss) * 100

print("Wind River:")
print(f"  prey population = {wind_river['prey_pop']}")
print(f"  wolf kills = {wr_yearly:.2f}")
print(f"  illness loss = {illness_rate} × {wind_river['prey_pop']} = {wr_illness:.2f}")
print(f"  total loss = {wr_yearly:.2f} + {wr_illness:.2f} = {wr_total_loss:.2f}")
print(f"  wolf percentage = ({wr_yearly:.2f} / {wr_total_loss:.2f}) × 100 = {wr_wolf_pct:.2f}%")

# High Peak
hp_illness = illness_rate * high_peak['prey_pop']
hp_total_loss = hp_yearly + hp_illness
hp_wolf_pct = (hp_yearly / hp_total_loss) * 100

print("\nHigh Peak:")
print(f"  prey population = {high_peak['prey_pop']}")
print(f"  wolf kills = {hp_yearly:.2f}")
print(f"  illness loss = {illness_rate} × {high_peak['prey_pop']} = {hp_illness:.2f}")
print(f"  total loss = {hp_yearly:.2f} + {hp_illness:.2f} = {hp_total_loss:.2f}")
print(f"  wolf percentage = ({hp_yearly:.2f} / {hp_total_loss:.2f}) × 100 = {hp_wolf_pct:.2f}%")

# Combined
total_prey = wind_river['prey_pop'] + high_peak['prey_pop']
total_wolf_kills = wr_yearly + hp_yearly
illness_loss = wr_illness + hp_illness
total_loss = total_wolf_kills + illness_loss
wolf_pct = (total_wolf_kills / total_loss) * 100

print("\nCombined:")
print(f"  total prey = {wind_river['prey_pop']} + {high_peak['prey_pop']} = {total_prey}")
print(f"  total wolf kills = {wr_yearly:.2f} + {hp_yearly:.2f} = {total_wolf_kills:.2f}")
print(f"  total illness = {wr_illness:.2f} + {hp_illness:.2f} = {illness_loss:.2f}")
print(f"  total loss = {total_wolf_kills:.2f} + {illness_loss:.2f} = {total_loss:.2f}")
print(f"  wolf percentage = ({total_wolf_kills:.2f} / {total_loss:.2f}) × 100 = {wolf_pct:.2f}%")

print(f"\n>>> Wind River: {wr_wolf_pct:.2f}% of prey loss due to wolves")
print(f">>> High Peak:  {hp_wolf_pct:.2f}% of prey loss due to wolves")
print(f">>> Combined:   {wolf_pct:.2f}% of prey loss due to wolves")

# Q4: Prey loss due to illness vs wolves
print("\n" + "="*60)
print("\nQ4: Prey Loss Breakdown")
print("-"*40)
print()

print("Wind River:")
print(f"  illness loss = {illness_rate} × {wind_river['prey_pop']} = {wr_illness:.2f} prey/year")
print(f"  wolf kills = {wr_yearly:.2f} prey/year")
print(f"  total loss = {wr_total_loss:.2f} prey/year")

print("\nHigh Peak:")
print(f"  illness loss = {illness_rate} × {high_peak['prey_pop']} = {hp_illness:.2f} prey/year")
print(f"  wolf kills = {hp_yearly:.2f} prey/year")
print(f"  total loss = {hp_total_loss:.2f} prey/year")

print("\nCombined:")
print(f"  illness loss = {wr_illness:.2f} + {hp_illness:.2f} = {illness_loss:.2f} prey/year")
print(f"  wolf kills = {wr_yearly:.2f} + {hp_yearly:.2f} = {total_wolf_kills:.2f} prey/year")
print(f"  total loss = {total_loss:.2f} prey/year")

print(f"\n>>> Wind River - Illness: {wr_illness:.2f}, Wolves: {wr_yearly:.2f}")
print(f">>> High Peak  - Illness: {hp_illness:.2f}, Wolves: {hp_yearly:.2f}")
print(f">>> Combined   - Illness: {illness_loss:.2f}, Wolves: {total_wolf_kills:.2f}")

print("\n" + "="*60)
print("SUMMARY (rounded to 2 digits)")
print("="*60)
print(f"Q1: Kill rates    - Wind River: {wr_rate:.2f}, High Peak: {hp_rate:.2f}")
print(f"Q2: Yearly kills  - Wind River: {wr_yearly:.2f}, High Peak: {hp_yearly:.2f}")
print(f"Q3: Wolf % of loss")
print(f"      Wind River: {wr_wolf_pct:.2f}%")
print(f"      High Peak:  {hp_wolf_pct:.2f}%")
print(f"      Combined:   {wolf_pct:.2f}%")
print(f"Q4: Prey loss breakdown")
print(f"      Wind River - Illness: {wr_illness:.2f}, Wolves: {wr_yearly:.2f}")
print(f"      High Peak  - Illness: {hp_illness:.2f}, Wolves: {hp_yearly:.2f}")
print(f"      Combined   - Illness: {illness_loss:.2f}, Wolves: {total_wolf_kills:.2f}")
