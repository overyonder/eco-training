#!/usr/bin/env python3
"""
Redrock Island Helper - McKinsey PSG (2025)

Workflow assistant for the 3-stage research game.
Not a solver — helps organize data and track progress.

Structure:
- 1 Study (Investigation → Analysis → Report)
- 3 Cases (independent short questions)

Usage:
  python helper_redrock.py
"""

from dataclasses import dataclass, field
from typing import Optional
import json
import sys

@dataclass
class Observation:
    """A datapoint collected during Investigation."""
    source: str      # Where it came from (e.g., "Table 2", "Chart A")
    label: str       # What it represents
    value: str       # The actual value (kept as string for flexibility)
    notes: str = ""  # Additional context

@dataclass
class Calculation:
    """A calculation performed during Analysis."""
    question: str    # What we're trying to answer
    formula: str     # How we're calculating it
    inputs: list[str] = field(default_factory=list)  # Which observations used
    result: str = ""
    notes: str = ""

@dataclass
class Study:
    """The main study with 3 stages."""
    topic: str = ""
    # Investigation
    observations: list[Observation] = field(default_factory=list)
    # Analysis
    calculations: list[Calculation] = field(default_factory=list)
    # Report
    report_summary: str = ""
    report_findings: list[str] = field(default_factory=list)
    report_visuals: list[str] = field(default_factory=list)  # descriptions

@dataclass
class Case:
    """An independent short question."""
    topic: str = ""
    question: str = ""
    relevant_data: list[str] = field(default_factory=list)
    answer: str = ""
    reasoning: str = ""

@dataclass
class Exercise:
    """Complete exercise: 1 study + 3 cases."""
    study: Study = field(default_factory=Study)
    cases: list[Case] = field(default_factory=lambda: [Case(), Case(), Case()])


def print_stage_guide():
    """Print the 3-stage workflow guide."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    REDROCK ISLAND WORKFLOW                       ║
╠══════════════════════════════════════════════════════════════════╣
║  STAGE 1: INVESTIGATION                                          ║
║  ─────────────────────────────────────────────────────────────── ║
║  • Collect observations from provided materials                  ║
║  • Note source (table/chart/text) for each datapoint             ║
║  • Look for: trends, outliers, relationships                     ║
║  • Don't calculate yet — just gather                             ║
╠══════════════════════════════════════════════════════════════════╣
║  STAGE 2: ANALYSIS                                               ║
║  ─────────────────────────────────────────────────────────────── ║
║  • Answer specific questions from the study                      ║
║  • Use observations from Stage 1                                 ║
║  • Show calculations clearly                                     ║
║  • Common operations: %, change, average, ratio, comparison      ║
╠══════════════════════════════════════════════════════════════════╣
║  STAGE 3: REPORT                                                 ║
║  ─────────────────────────────────────────────────────────────── ║
║  • Synthesize findings into written summary                      ║
║  • Create/select appropriate visuals                             ║
║  • Answer the research question clearly                          ║
║  • Support conclusions with data from Analysis                   ║
╚══════════════════════════════════════════════════════════════════╝
""")


def print_checklist():
    """Print a quick checklist for the exercise."""
    print("""
REDROCK EXERCISE CHECKLIST
══════════════════════════

STUDY
  □ Investigation
      □ Identify all data sources (tables, charts, text)
      □ Extract key datapoints
      □ Note units and time periods
      □ Flag any anomalies or gaps

  □ Analysis
      □ Read each question carefully
      □ Identify which observations needed
      □ Perform calculations (show work)
      □ Verify results make sense

  □ Report
      □ State main finding clearly
      □ Support with 2-3 key data points
      □ Choose appropriate visual type
      □ Check for consistency with analysis

CASES (x3)
  □ Case 1: _______________
      □ Understand the question
      □ Find relevant data
      □ Calculate/reason
      □ State answer clearly

  □ Case 2: _______________
      □ Understand the question
      □ Find relevant data
      □ Calculate/reason
      □ State answer clearly

  □ Case 3: _______________
      □ Understand the question
      □ Find relevant data
      □ Calculate/reason
      □ State answer clearly
""")


def print_calculation_templates():
    """Print common calculation patterns."""
    print("""
COMMON CALCULATIONS
═══════════════════

PERCENTAGE OF TOTAL
  (part / whole) × 100
  Example: 25 of 100 = 25%

PERCENTAGE CHANGE
  ((new - old) / old) × 100
  Example: 80 → 100 = +25%

RATIO
  A : B  or  A/B
  Example: 300:100 = 3:1

AVERAGE
  sum / count
  Example: (10+20+30)/3 = 20

WEIGHTED AVERAGE
  Σ(value × weight) / Σ(weights)
  Example: (10×2 + 20×3) / 5 = 16

GROWTH RATE (CAGR)
  ((end/start)^(1/years) - 1) × 100
  Example: 100→200 over 5yr = 14.9%/yr

DIFFERENCE
  new - old
  Example: 150 - 100 = +50

CONTRIBUTION
  (segment change / total change) × 100
  Example: segment +30 of total +50 = 60% contribution
""")


def interactive_mode():
    """Run interactive workflow tracker."""
    ex = Exercise()

    print("\n" + "="*60)
    print("REDROCK ISLAND - Interactive Tracker")
    print("="*60)

    while True:
        print("\nOptions:")
        print("  1. View workflow guide")
        print("  2. View checklist")
        print("  3. View calculation templates")
        print("  4. Record observation (Investigation)")
        print("  5. Record calculation (Analysis)")
        print("  6. View collected data")
        print("  7. Export to JSON")
        print("  q. Quit")

        choice = input("\nChoice: ").strip().lower()

        if choice == '1':
            print_stage_guide()
        elif choice == '2':
            print_checklist()
        elif choice == '3':
            print_calculation_templates()
        elif choice == '4':
            print("\n-- Record Observation --")
            obs = Observation(
                source=input("Source (e.g., Table 2): "),
                label=input("Label (what it represents): "),
                value=input("Value: "),
                notes=input("Notes (optional): ")
            )
            ex.study.observations.append(obs)
            print(f"✓ Recorded: {obs.label} = {obs.value}")
        elif choice == '5':
            print("\n-- Record Calculation --")
            calc = Calculation(
                question=input("Question being answered: "),
                formula=input("Formula/method: "),
                result=input("Result: "),
                notes=input("Notes (optional): ")
            )
            ex.study.calculations.append(calc)
            print(f"✓ Recorded: {calc.question} → {calc.result}")
        elif choice == '6':
            print("\n-- Collected Data --")
            print(f"\nObservations ({len(ex.study.observations)}):")
            for i, obs in enumerate(ex.study.observations, 1):
                print(f"  {i}. [{obs.source}] {obs.label}: {obs.value}")
            print(f"\nCalculations ({len(ex.study.calculations)}):")
            for i, calc in enumerate(ex.study.calculations, 1):
                print(f"  {i}. {calc.question}")
                print(f"     Formula: {calc.formula}")
                print(f"     Result: {calc.result}")
        elif choice == '7':
            filename = input("Filename (default: redrock_data.json): ").strip()
            if not filename:
                filename = "redrock_data.json"
            data = {
                'study': {
                    'observations': [vars(o) for o in ex.study.observations],
                    'calculations': [vars(c) for c in ex.study.calculations],
                },
                'cases': [vars(c) for c in ex.cases]
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Exported to {filename}")
        elif choice == 'q':
            break
        else:
            print("Invalid choice")


def main():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == '--guide':
            print_stage_guide()
        elif cmd == '--checklist':
            print_checklist()
        elif cmd == '--calc':
            print_calculation_templates()
        elif cmd == '--interactive':
            interactive_mode()
        else:
            print("Usage: python helper_redrock.py [--guide|--checklist|--calc|--interactive]")
    else:
        print_stage_guide()
        print("\nRun with --interactive for workflow tracker")
        print("Run with --checklist for quick reference")
        print("Run with --calc for calculation templates")


if __name__ == '__main__':
    main()
