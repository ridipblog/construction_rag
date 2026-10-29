"""
Cost Estimation and Rate Analysis Engine for Indian Construction Projects
Standardized against CPWD DSR (Delhi Schedule of Rates) & Assam PWD SOR (Bridge Works).
"""
from typing import Dict, Any, List
from app.schemas.estimate import MaterialItem, CostBreakdown, EstimationSummary

# Default Indian Schedule of Rates (INR) for Bridge Construction
DEFAULT_RATES = {
    # Finished Works Rates (Including materials & basic processing)
    "concrete_m35_per_m3": 8200.0,      # CPWD DSR item 5.33 / MoRTH Section 1700
    "steel_fe500d_per_tonne": 84000.0,  # CPWD DSR item 5.22 / MoRTH Section 1600 (includes cutting & binding)
    "formwork_bridge_per_m2": 780.0,    # MoRTH Section 1500 (Steel/Plywood staging & shuttering)
    "pile_boring_per_m": 4200.0,        # MoRTH Section 2200 (Boring 1000mm dia in alluvial soil)
    "wearing_coat_per_m2": 1950.0,      # MoRTH Section 2700 (40mm Mastic asphalt + 25mm BC)
    "elastomeric_bearings_each": 45000.0, # MoRTH Section 2000 (per bearing pedestal)
    "expansion_joints_per_m": 12500.0,  # MoRTH Section 2600 (Strip seal expansion joints)

    # Raw Material Component Rates (For Bill of Quantities breakdown)
    "cement_per_bag": 420.0,            # 50 kg bag (Ultratech/Dalmia/Star Cement Assam)
    "sand_per_m3": 1650.0,              # Coarse river sand per m³
    "aggregate_per_m3": 2100.0,         # 20mm & 10mm crushed aggregate per m³
    "rebar_raw_per_tonne": 68000.0,     # Raw Fe500D TMT rebar (without binding/labour)
    "binding_wire_per_kg": 95.0
}

def calculate_bridge_costs(
    quantities: Dict[str, Any],
    length_m: float,
    width_m: float,
    location: str = "Assam, India",
    custom_rates: Dict[str, float] | None = None
) -> Dict[str, Any]:
    """
    Applies itemized rates, computes labour, equipment, overheads,
    and returns a structured financial estimate.
    """
    rates = DEFAULT_RATES.copy()
    if custom_rates:
        rates.update(custom_rates)

    total_concrete_m3 = quantities["total_concrete_m3"]
    total_steel_tonnes = quantities["total_steel_tonnes"]
    total_formwork_m2 = quantities["total_formwork_m2"]
    total_piles_count = quantities["total_piles_count"]
    avg_pile_depth_m = quantities["avg_pile_depth_m"]
    spans_count = quantities["spans_count"]
    deck_area_m2 = quantities["deck_area_m2"]

    # 1. Structural Works Costing
    concrete_cost = total_concrete_m3 * rates["concrete_m35_per_m3"]
    steel_cost = total_steel_tonnes * rates["steel_fe500d_per_tonne"]
    formwork_cost = total_formwork_m2 * rates["formwork_bridge_per_m2"]
    
    # Pile boring and installation
    total_piling_linear_m = total_piles_count * avg_pile_depth_m
    piling_boring_cost = total_piling_linear_m * rates["pile_boring_per_m"]

    # Bridge Appurtenances (Bearings, Expansion Joints, Wearing Coat)
    # Girders * (Piers + 2) bearings
    bearings_count = spans_count * 4 * 2
    bearings_cost = bearings_count * rates["elastomeric_bearings_each"]
    expansion_joints_cost = (spans_count + 1) * width_m * rates["expansion_joints_per_m"]
    wearing_coat_cost = deck_area_m2 * rates["wearing_coat_per_m2"]

    subtotal_direct_works = (
        concrete_cost + steel_cost + formwork_cost + 
        piling_boring_cost + bearings_cost + expansion_joints_cost + wearing_coat_cost
    )

    # 2. Financial Breakdown (Standard CPWD / MoRTH Proportions)
    # Materials comprise ~58% of direct works
    materials_cost = round(subtotal_direct_works * 0.58, 2)
    # Labour component ~18% (Carpenters, bar benders, masons, crane operators)
    labour_cost = round(subtotal_direct_works * 0.18, 2)
    # Machinery & Equipment ~14% (Piling rig, transit mixers, batching plant, vibrators)
    machinery_equipment_cost = round(subtotal_direct_works * 0.14, 2)
    # Contractor Profit & Overheads ~10% (CPWD standard: 10% CP + Overhead)
    contractor_profit_and_overhead = round(subtotal_direct_works * 0.10, 2)

    total_cost = round(
        materials_cost + labour_cost + machinery_equipment_cost + contractor_profit_and_overhead, 2
    )

    cost_per_linear_m = round(total_cost / max(1.0, length_m), 2)
    cost_per_sqm_deck = round(total_cost / max(1.0, deck_area_m2), 2)

    # 3. Itemized Materials Table for Laravel UI
    materials_items = [
        MaterialItem(
            name="Structural Concrete (M35 Grade)",
            category="Concrete Works",
            quantity=total_concrete_m3,
            unit="m³",
            rate=rates["concrete_m35_per_m3"],
            amount=round(concrete_cost, 2),
            formula_basis="IS 10262 Design Mix (Cement, Aggregates, Sand, Admixtures, Batching & Pumping)"
        ),
        MaterialItem(
            name="Reinforcement Steel (Fe500D TMT)",
            category="Steel Works",
            quantity=total_steel_tonnes,
            unit="tonne",
            rate=rates["steel_fe500d_per_tonne"],
            amount=round(steel_cost, 2),
            formula_basis="MoRTH Sec 1600 / IRC 112: 130 kg/m³ (Superstructure), 100 kg/m³ (Substructure), 85 kg/m³ (Piles)"
        ),
        MaterialItem(
            name="Steel / Plywood Shuttering & Staging",
            category="Formwork",
            quantity=total_formwork_m2,
            unit="m²",
            rate=rates["formwork_bridge_per_m2"],
            amount=round(formwork_cost, 2),
            formula_basis="MoRTH Sec 1500: Deck soffit, girder sides, pier columns & pile caps"
        ),
        MaterialItem(
            name="Ordinary Portland Cement (50kg bags)",
            category="Constituent Materials",
            quantity=float(quantities["cement_bags"]),
            unit="bags",
            rate=rates["cement_per_bag"],
            amount=round(quantities["cement_bags"] * rates["cement_per_bag"], 2),
            formula_basis="8.0 bags / m³ for M35 grade concrete (IS 456 / IS 10262)"
        ),
        MaterialItem(
            name="Coarse River Sand / Fine Aggregate",
            category="Constituent Materials",
            quantity=quantities["sand_m3"],
            unit="m³",
            rate=rates["sand_per_m3"],
            amount=round(quantities["sand_m3"] * rates["sand_per_m3"], 2),
            formula_basis="0.44 m³ per m³ concrete (Zone-II graded river sand)"
        ),
        MaterialItem(
            name="Crushed Coarse Aggregate (10mm + 20mm)",
            category="Constituent Materials",
            quantity=quantities["aggregate_m3"],
            unit="m³",
            rate=rates["aggregate_per_m3"],
            amount=round(quantities["aggregate_m3"] * rates["aggregate_per_m3"], 2),
            formula_basis="0.78 m³ per m³ concrete (Hard granite/basalt broken stone)"
        ),
        MaterialItem(
            name="Bored Piling Rig Boring & Casing",
            category="Foundation Specialized Works",
            quantity=round(total_piling_linear_m, 2),
            unit="metre",
            rate=rates["pile_boring_per_m"],
            amount=round(piling_boring_cost, 2),
            formula_basis=f"{total_piles_count} piles @ avg depth {avg_pile_depth_m}m in alluvial riverbed"
        ),
        MaterialItem(
            name="Elastomeric Bridge Bearings (Neoprene/Pot)",
            category="Bridge Appurtenances",
            quantity=float(bearings_count),
            unit="nos",
            rate=rates["elastomeric_bearings_each"],
            amount=round(bearings_cost, 2),
            formula_basis="MoRTH Sec 2000 / IRC 83: Bearings under each girder at pier caps and abutments"
        ),
        MaterialItem(
            name="Strip Seal Expansion Joints & Wearing Coat",
            category="Bridge Deck Finishes",
            quantity=round(deck_area_m2, 2),
            unit="m²",
            rate=rates["wearing_coat_per_m2"],
            amount=round(wearing_coat_cost + expansion_joints_cost, 2),
            formula_basis="MoRTH Sec 2600 & 2700: 65mm bituminous wearing course + movement joint seals"
        )
    ]

    cost_breakdown = CostBreakdown(
        materials_cost=materials_cost,
        labour_cost=labour_cost,
        machinery_equipment_cost=machinery_equipment_cost,
        contractor_profit_and_overhead=contractor_profit_and_overhead,
        total_cost=total_cost,
        currency="INR"
    )

    estimation_summary = EstimationSummary(
        status="preliminary",
        total_estimated_cost=total_cost,
        currency="INR",
        cost_per_linear_metre=cost_per_linear_m,
        cost_per_sqm_deck=cost_per_sqm_deck
    )

    return {
        "cost_breakdown": cost_breakdown,
        "estimation_summary": estimation_summary,
        "materials": materials_items
    }
