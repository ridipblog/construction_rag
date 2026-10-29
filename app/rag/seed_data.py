"""
Curated Indian Construction Standards, MoRTH Specifications, and Schedule of Rates
Reference collection for Bridge and Infrastructure Estimation in India.
"""

INDIAN_CONSTRUCTION_DOCUMENTS = [
    {
        "source": "IRC: 112-2020 Code of Practice for Concrete Road Bridges",
        "category": "standards",
        "metadata": {
            "code": "IRC:112-2020",
            "section": "Structural Concrete & Reinforcement",
            "jurisdiction": "India - Ministry of Road Transport & Highways"
        },
        "content": (
            "IRC:112-2020 stipulates structural concrete design guidelines for road bridges in India. "
            "For bridge superstructures (deck slabs, longitudinal T-beams, and box girders), the minimum concrete grade "
            "specified for severe/moderate exposure is M35. High Yield Strength Deformed (HYSD) bars conforming to "
            "IS 1786 Grade Fe 500D (high ductility) are mandatory for seismic zones IV and V (including Assam and Northeast India). "
            "Reinforcement steel consumption standards for preliminary bridge estimation: "
            "Superstructure RCC deck slab & girders: 120 to 140 kg per cubic metre of concrete. "
            "Substructure RCC piers and abutments: 90 to 110 kg per cubic metre of concrete. "
            "Foundation piles and pile caps: 80 to 95 kg per cubic metre of concrete. "
            "Clear concrete cover for bridge decks is 40mm to 50mm to prevent chloride/carbonation corrosion."
        )
    },
    {
        "source": "MoRTH Section 1500 - Formwork and Staging for Bridges",
        "category": "specifications",
        "metadata": {
            "code": "MoRTH 5th Revision",
            "section": "1500 Formwork",
            "jurisdiction": "National Highways Authority of India (NHAI)"
        },
        "content": (
            "MoRTH Section 1500 specifies requirements for bridge shuttering, centering, and staging. "
            "All exposed concrete surfaces of deck slabs, girders, pier shafts, and pier caps must use steel formwork "
            "or high-density film-faced polymer coated plywood (minimum 12mm thick) to achieve uniform finish and tight joints. "
            "Staging across riverbeds must be designed to withstand water velocity, scour, and wind pressure. "
            "Standard formwork surface area allowances for highway bridges: "
            "Superstructure T-beam and deck slab: ~2.8 to 3.2 m² of formwork per m³ of finished concrete. "
            "Substructure circular and wall piers: ~2.2 to 2.6 m² per m³ of concrete. "
            "Striking time: Soffit of girders requires minimum 14 to 21 days curing before formwork removal."
        )
    },
    {
        "source": "MoRTH Section 1700 - Structural Concrete for Bridges",
        "category": "specifications",
        "metadata": {
            "code": "MoRTH 5th Revision",
            "section": "1700 Structural Concrete",
            "jurisdiction": "India"
        },
        "content": (
            "MoRTH Section 1700 governs structural concrete for highway bridges. "
            "All concrete grades M30 and above must be designed as per IS 10262 using automated computerized weigh batching plants. "
            "For M35 grade bridge concrete: "
            "Minimum cement content is 380 kg/m³ with maximum water-cement ratio of 0.40. "
            "Typical mix proportion yields 8.0 bags of 50kg cement, 0.44 m³ of graded Zone-II river sand, "
            "and 0.78 m³ of 20mm down and 10mm crushed aggregate per cubic metre. "
            "Mandatory inclusion of polycarboxylate ether (PCE) based superplasticizers to achieve 120-150mm slump for pumping. "
            "Steam or continuous water curing is required for at least 14 days."
        )
    },
    {
        "source": "MoRTH Section 2100 & 2200 - Substructure and Pile Foundations",
        "category": "specifications",
        "metadata": {
            "code": "MoRTH 5th Revision",
            "section": "2100 & 2200 Substructure & Foundations",
            "jurisdiction": "National Bridges & Highways"
        },
        "content": (
            "MoRTH Section 2100 & 2200 covers bridge piers, abutments, and deep foundations. "
            "In perennial rivers with alluvial soil beds (such as the Brahmaputra River Basin in Assam), "
            "bored cast-in-situ reinforced concrete piles of diameter 1000mm to 1200mm are standard. "
            "Pile depth must penetrate below maximum scour depth calculated using Lacey's Regime formula plus 1/3 embedment. "
            "Typical pile lengths in Assam alluvial floodplains range from 22m to 30m below riverbed. "
            "Piers are provided with elastomeric neoprene bearing pedestals conforming to IRC:83 Part II. "
            "Abutments must incorporate drainage weep holes and non-woven geotextile filter fabric behind dirt and wing walls."
        )
    },
    {
        "source": "Assam PWD Schedule of Rates (Bridge & Road Works 2023-2024)",
        "category": "schedule_of_rates",
        "metadata": {
            "code": "Assam PWD SOR 2023-24",
            "section": "RCC Bridge Works Items",
            "jurisdiction": "Assam, Northeast India"
        },
        "content": (
            "Assam PWD Schedule of Rates (Bridge Works 2023-2024) item benchmarks for Guwahati, Dibrugarh, and Silchar circles: "
            "1. RCC M35 grade concrete in bridge superstructure (deck, girders, diaphragms) including mechanical batching, "
            "transit mixer carriage, concrete pump, and curing: Rs 8,000 to Rs 8,600 per m³. "
            "2. Thermo-Mechanically Treated (TMT) Fe 500D rebar in bridge elements including decoiling, cutting, bending, "
            "binding wire, and hoisting into place: Rs 82,000 to Rs 87,000 per metric tonne. "
            "3. Centering and shuttering with steel plates/waterproof ply for bridge superstructure and substructure: Rs 750 to Rs 880 per m². "
            "4. Bored cast-in-situ piling (1000mm dia) boring in riverbed alluvial strata: Rs 3,900 to Rs 4,600 per linear metre. "
            "5. Strip seal type expansion joints: Rs 12,000 to Rs 14,000 per linear metre of deck width."
        )
    },
    {
        "source": "CPWD Delhi Schedule of Rates (DSR 2023) - Materials & Analysis of Rates",
        "category": "schedule_of_rates",
        "metadata": {
            "code": "CPWD DSR 2023",
            "section": "Concrete Works & Material Breakdown",
            "jurisdiction": "Central Public Works Department, India"
        },
        "content": (
            "CPWD DSR 2023 gives material consumption factors per 1.0 m³ of finished compacted concrete: "
            "For M35 structural concrete: 400 kg cement (8.0 bags of 50 kg), 0.44 m³ coarse sand (Zone II), "
            "0.52 m³ coarse aggregate (20mm nominal) and 0.26 m³ coarse aggregate (10mm nominal). Total coarse aggregate = 0.78 m³. "
            "Standard cost composition on CPWD infrastructure projects: "
            "Materials = 56% to 62% of direct cost. "
            "Direct Labour = 16% to 20%. "
            "Machinery, Fuel & Plant Operations = 12% to 15%. "
            "Contractor profit and overheads standard provision = 10% profit + 5% overheads (15% total)."
        )
    },
    {
        "source": "IRC: 6-2017 Bridge Design Loads and Seismic Zone V Guidelines",
        "category": "standards",
        "metadata": {
            "code": "IRC:6-2017",
            "section": "Loads & Seismic Provisions",
            "jurisdiction": "India"
        },
        "content": (
            "IRC:6-2017 prescribes live load and seismic standards for Indian highway bridges. "
            "Highway bridges on National & State Highways must be designed for IRC Class 70R tracked/wheeled vehicle loading "
            "or two lanes of IRC Class A wheeled loading, whichever produces maximum governing bending moment and shear. "
            "Seismic considerations: The State of Assam lies entirely in Seismic Zone V (Zone factor Z = 0.36), "
            "which represents the highest earthquake risk classification in India. "
            "In Zone V, ductile detailing per IRC:112 is mandatory, including closely spaced helical/circular stirrup ties in pier shafts, "
            "seismic arrestors on pier caps to prevent deck unseating, and elastomeric bearings with shear keys."
        )
    },
    {
        "source": "MoRTH Section 2700 - Wearing Coat and Deck Appurtenances",
        "category": "specifications",
        "metadata": {
            "code": "MoRTH 5th Revision",
            "section": "2700 Wearing Coat",
            "jurisdiction": "India"
        },
        "content": (
            "MoRTH Section 2700 requires a two-layer composite bituminous wearing coat on concrete bridge decks: "
            "Lower layer: 12mm to 40mm mastic asphalt waterproofing layer conforming to IS 5317. "
            "Upper layer: 25mm to 40mm dense bituminous concrete (BC) / bituminous mastic as riding surface. "
            "Combined thickness = 65mm. Estimated rate = Rs 1,800 to Rs 2,200 per m² of carriageway deck area. "
            "Reinforced concrete crash barriers (MoRTH Cl 803.4) along both sides: Height 900mm to 1000mm, "
            "tested for 400kN containment capability."
        )
    }
]
