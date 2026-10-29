"""
Civil Engineering Calculation Engine for RCC Highway & River Bridges
Formulated based on:
- IRC: 112-2020 (Code of Practice for Concrete Road Bridges)
- IRC: 6-2017 (Standard Specifications and Code of Practice for Road Bridges - Loads & Stresses)
- MoRTH Specifications for Road and Bridge Works (5th Revision, Sections 1500, 1600, 1700, 2100, 2200)
- IS: 456-2000 & IS: 10262-2019 (Concrete Mix Proportioning)
"""
import math
from typing import Dict, Any, List
from app.schemas.estimate import StructuralComponent, MaterialItem

def calculate_bridge_quantities(
    length_m: float,
    width_m: float,
    height_m: float,
    bridge_type: str = "RCC",
    span_length_m: float | None = None,
    concrete_grade: str = "M35",
    foundation_type: str | None = None
) -> Dict[str, Any]:
    """
    Computes deterministic structural concrete volumes, formwork areas,
    and steel reinforcement weights for an RCC girder bridge.
    """
    # 1. Span Determination
    # Economical span for RCC T-beam bridge in India is ~18m to 25m.
    if span_length_m and span_length_m > 0:
        spans_count = max(1, round(length_m / span_length_m))
        actual_span = length_m / spans_count
    else:
        # Standard economical span default: ~20m
        spans_count = max(1, round(length_m / 20.0))
        actual_span = length_m / spans_count

    piers_count = max(0, spans_count - 1)
    abutments_count = 2

    # Foundation selection: In Assam riverbeds / alluvial terrain, pile foundation is standard
    if not foundation_type:
        foundation_type = "Bored Cast-in-Situ RCC Piles (MoRTH Cl 2200)"

    # ----------------------------------------------------
    # 2. Superstructure Calculations
    # Deck Slab + Longitudinal Girders + Cross Diaphragms + Kerbs & Railing
    # ----------------------------------------------------
    # Deck slab: typical thickness 0.22m
    deck_area = length_m * width_m
    deck_slab_volume = deck_area * 0.22  # m³
    deck_slab_formwork = deck_area * 1.15  # m² (including cantilever sides & edges)

    # Longitudinal Girders & Cross Diaphragms:
    # Typically 3 to 4 T-girders per span for 10m-12m width. Depth ~ Span/10 = actual_span * 0.09
    girder_depth = max(1.5, actual_span * 0.085)
    girder_web_thickness = 0.35  # 350mm web
    girders_per_span = 3 if width_m <= 8.5 else (4 if width_m <= 12.0 else 5)
    
    # Net volume of girders (length * web_thickness * (depth - slab_thickness))
    girder_net_depth = max(1.0, girder_depth - 0.22)
    girders_volume = length_m * girders_per_span * girder_web_thickness * girder_net_depth
    
    # Cross diaphragms (at ends and intermediate per span)
    diaphragms_per_span = 3
    diaphragm_volume = (
        spans_count * diaphragms_per_span * (width_m * 0.30 * girder_net_depth * 0.8)
    )
    
    # Crash barriers, kerbs, and wearing coat base:
    crash_barriers_volume = 2 * length_m * 0.45 * 0.85  # 2 sides RCC crash barriers (IRC 5)
    
    total_superstructure_concrete = (
        deck_slab_volume + girders_volume + diaphragm_volume + crash_barriers_volume
    )
    superstructure_formwork = (
        deck_slab_formwork + (girders_volume * 4.8) + (crash_barriers_volume * 2.2)
    )

    # ----------------------------------------------------
    # 3. Substructure Calculations
    # Pier Caps + Pier Columns/Shafts + Abutments + Wing Walls
    # ----------------------------------------------------
    if piers_count > 0:
        # Pier Cap: Length = width_m, width = 1.6m, avg depth = 1.3m (flared)
        single_pier_cap_vol = width_m * 1.6 * 1.3
        # Pier Shafts: 2 circular columns of dia 1.2m or 1 solid wall pier
        # Assam/Brahmaputra standard: twin circular RCC columns with tie beam
        pier_col_radius = 0.7  # 1.4m diameter
        pier_col_area = 2 * (math.pi * (pier_col_radius ** 2))
        single_pier_shaft_vol = pier_col_area * height_m
        
        piers_concrete = piers_count * (single_pier_cap_vol + single_pier_shaft_vol)
        piers_formwork = piers_count * (
            (width_m * 1.6 * 2 + 1.6 * 1.3 * 2) + (2 * (2 * math.pi * pier_col_radius * height_m))
        )
    else:
        piers_concrete = 0.0
        piers_formwork = 0.0

    # Abutments (2 nos): Counterfort / Cantilever RCC abutments with dirt wall and return walls
    # Base slab, breast wall, dirt wall, ballast wall, return walls
    single_abutment_vol = (width_m * 1.8 * (height_m * 0.65)) + (2 * 12.0)  # breast wall + return walls
    abutments_concrete = abutments_count * single_abutment_vol
    abutments_formwork = abutments_count * (single_abutment_vol * 2.4)

    total_substructure_concrete = piers_concrete + abutments_concrete
    total_substructure_formwork = piers_formwork + abutments_formwork

    # ----------------------------------------------------
    # 4. Foundation Calculations (Pile Foundation)
    # Pile Caps + Bored Cast-in-Situ Piles
    # ----------------------------------------------------
    # For each pier: 4 to 6 piles of 1.0m to 1.2m dia, 25m depth in riverbed
    # For each abutment: 6 to 8 piles
    piles_per_pier = 6 if width_m >= 9.0 else 4
    piles_per_abutment = 8 if width_m >= 9.0 else 6
    total_piles_count = (piers_count * piles_per_pier) + (abutments_count * piles_per_abutment)
    
    # Pile depth into alluvial bed (typical Assam MoRTH scour depth guideline: 22m to 28m)
    avg_pile_depth_m = max(20.0, height_m * 2.2)
    pile_dia_m = 1.0
    single_pile_vol = math.pi * ((pile_dia_m / 2) ** 2) * avg_pile_depth_m
    total_piles_concrete = total_piles_count * single_pile_vol

    # Pile caps (1.5m thick RCC slab over pile cluster)
    pile_cap_vol_per_pier = (width_m + 1.0) * 4.5 * 1.5
    pile_cap_vol_per_abutment = (width_m + 1.5) * 4.0 * 1.5
    total_pile_caps_concrete = (piers_count * pile_cap_vol_per_pier) + (abutments_count * pile_cap_vol_per_abutment)

    total_foundation_concrete = total_piles_concrete + total_pile_caps_concrete
    total_foundation_formwork = (piers_count * 28.0) + (abutments_count * 35.0)  # pile cap shuttering

    # ----------------------------------------------------
    # 5. Reinforcement Steel (Fe500D) Consumption Ratios
    # Based on IRC:112 and Indian MoRTH Highway Bridge standards:
    # - Superstructure: 130 kg / m³
    # - Substructure (Piers/Abutments): 100 kg / m³
    # - Foundation (Piles & Pile caps): 85 kg / m³
    # ----------------------------------------------------
    superstructure_steel_kg = total_superstructure_concrete * 130.0
    substructure_steel_kg = total_substructure_concrete * 100.0
    foundation_steel_kg = total_foundation_concrete * 85.0

    total_steel_kg = superstructure_steel_kg + substructure_steel_kg + foundation_steel_kg
    total_steel_tonnes = total_steel_kg / 1000.0

    total_concrete_m3 = (
        total_superstructure_concrete + total_substructure_concrete + total_foundation_concrete
    )
    total_formwork_m2 = (
        superstructure_formwork + total_substructure_formwork + total_foundation_formwork
    )

    # ----------------------------------------------------
    # 6. Basic Material Breakdown (Cement, Sand, Aggregates)
    # Per IS 10262:2019 for M35 grade bridge concrete:
    # Cement: 400 kg/m³ (8 bags of 50kg per m³)
    # Fine Aggregate (Sand / River Sand): 0.44 m³ per m³
    # Coarse Aggregate (10mm + 20mm graded): 0.78 m³ per m³
    # Water: 165 Litres per m³
    # ----------------------------------------------------
    cement_bags = round(total_concrete_m3 * 8.0)
    sand_m3 = round(total_concrete_m3 * 0.44, 2)
    aggregate_m3 = round(total_concrete_m3 * 0.78, 2)
    water_kl = round((total_concrete_m3 * 165.0) / 1000.0, 1)

    components = [
        StructuralComponent(
            component_name="Superstructure (Deck Slab, T-Girders, Cross Diaphragms, Crash Barriers)",
            concrete_volume_m3=round(total_superstructure_concrete, 2),
            formwork_area_m2=round(superstructure_formwork, 2),
            steel_weight_tonnes=round(superstructure_steel_kg / 1000.0, 2),
            description=f"Includes {spans_count} spans of {actual_span:.1f}m each with {girders_per_span} longitudinal RCC T-girders per span."
        ),
        StructuralComponent(
            component_name="Substructure (Pier Caps, Twin Circular Pier Shafts, Abutments, Wing Walls)",
            concrete_volume_m3=round(total_substructure_concrete, 2),
            formwork_area_m2=round(total_substructure_formwork, 2),
            steel_weight_tonnes=round(substructure_steel_kg / 1000.0, 2),
            description=f"{piers_count} Intermediate Piers (H={height_m}m) + 2 RCC Abutments with cantilever return walls."
        ),
        StructuralComponent(
            component_name=f"Foundation ({foundation_type})",
            concrete_volume_m3=round(total_foundation_concrete, 2),
            formwork_area_m2=round(total_foundation_formwork, 2),
            steel_weight_tonnes=round(foundation_steel_kg / 1000.0, 2),
            description=f"{total_piles_count} Bored RCC Piles (Dia {pile_dia_m*1000:.0f}mm, Avg L={avg_pile_depth_m:.1f}m) + RCC Pile Caps."
        )
    ]

    return {
        "spans_count": spans_count,
        "span_length_m": round(actual_span, 2),
        "piers_count": piers_count,
        "abutments_count": abutments_count,
        "total_piles_count": total_piles_count,
        "avg_pile_depth_m": round(avg_pile_depth_m, 2),
        "foundation_type": foundation_type,
        "concrete_grade": concrete_grade,
        "total_concrete_m3": round(total_concrete_m3, 2),
        "total_formwork_m2": round(total_formwork_m2, 2),
        "total_steel_tonnes": round(total_steel_tonnes, 2),
        "cement_bags": cement_bags,
        "sand_m3": sand_m3,
        "aggregate_m3": aggregate_m3,
        "water_kl": water_kl,
        "components": components,
        "deck_area_m2": round(deck_area, 2)
    }
