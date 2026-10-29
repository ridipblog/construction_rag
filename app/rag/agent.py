import logging
from typing import Dict, Any, List
from app.schemas.estimate import (
    BridgeEstimateRequest,
    EstimateResponse,
    ProjectDetails,
    SourceReference
)
from app.calculations.bridge_calculator import calculate_bridge_quantities
from app.calculations.cost_calculator import calculate_bridge_costs
from app.rag.ollama_client import ollama_client
from app.rag.vector_store import search_similar_documents

logger = logging.getLogger(__name__)

class ConstructionRAGAgent:
    """
    Hybrid AI Agent combining deterministic Indian civil engineering calculations
    with vector retrieval of IRC/MoRTH standards and LLM technical review.
    """

    def __init__(self):
        self.ollama = ollama_client

    def process_estimate(self, request: BridgeEstimateRequest) -> EstimateResponse:
        logger.info(f"Processing estimate for {request.project_type}: L={request.length_m}m, W={request.width_m}m, H={request.height_m}m in {request.location}")

        # 1. Retrieve Applicable Indian Standards & Rates via RAG
        search_query = (
            f"RCC road bridge {request.location} length {request.length_m}m width {request.width_m}m "
            f"height {request.height_m}m MoRTH IRC 112 pile foundation schedule of rates concrete steel"
        )
        
        query_embedding = self.ollama.get_embedding(search_query)
        matching_docs = search_similar_documents(query_embedding=query_embedding, limit=4)

        source_refs: List[SourceReference] = []
        context_snippets = []
        for doc in matching_docs:
            code_ref = doc.get("metadata", {}).get("code", doc.get("source", "Standard Reference"))
            excerpt = doc["content"][:240] + "..." if len(doc["content"]) > 240 else doc["content"]
            source_refs.append(SourceReference(
                title=doc.get("source", "Indian Construction Reference"),
                code_reference=str(code_ref),
                excerpt=excerpt,
                relevance_score=doc.get("similarity", 0.0)
            ))
            context_snippets.append(f"[{code_ref}] {doc['content']}")

        rag_context_text = "\n\n".join(context_snippets)

        # 2. Run Deterministic Civil Engineering Calculations
        quantities = calculate_bridge_quantities(
            length_m=request.length_m,
            width_m=request.width_m,
            height_m=request.height_m,
            bridge_type=request.bridge_type,
            span_length_m=request.span_length_m,
            concrete_grade=request.concrete_grade or "M35",
            foundation_type=request.foundation_type
        )

        cost_results = calculate_bridge_costs(
            quantities=quantities,
            length_m=request.length_m,
            width_m=request.width_m,
            location=request.location,
            custom_rates=request.custom_rates
        )

        # 3. Document Engineering Assumptions
        is_assam = "assam" in request.location.lower() or "northeast" in request.location.lower()
        assumptions = [
            f"Economical span configuration: {quantities['spans_count']} spans @ {quantities['span_length_m']}m each (RCC T-Beam Deck & Girder system).",
            f"Design Concrete: Grade {quantities['concrete_grade']} design mix per IS 10262 & MoRTH Section 1700 (400 kg cement/m³, W/C ratio 0.40).",
            f"Reinforcement Steel: Grade {request.steel_grade or 'Fe500D'} high ductility TMT rebars conforming to IS 1786.",
            f"Substructure: {quantities['piers_count']} intermediate piers with pier caps + 2 cantilever RCC abutments.",
            f"Foundation: {quantities['foundation_type']} ({quantities['total_piles_count']} piles @ avg {quantities['avg_pile_depth_m']}m depth).",
            f"Design Live Loading: IRC Class 70R Tracked / 2-Lane Class A loading per IRC:6-2017."
        ]
        if is_assam:
            assumptions.append(
                "Seismic Zone V (Highest hazard, Z=0.36): Special ductile detailing per IRC:112 and seismic arrestor brackets included."
            )

        # 4. Enumerate Critical Missing Inputs Required Before Construction
        missing_inputs = [
            "Approved General Arrangement Drawing (GAD) & structural drawings from certified civil structural engineer",
            "Geotechnical Borelog Investigation Report (Soil bearing capacity, N-values, and depth to bedrock/firm strata)",
            "Hydrological & Hydraulic Survey (High Flood Level - HFL, design discharge Q, and riverbed scour depth Lacey formula)",
            "Local District Schedule of Rates (SOR) verification for active site district and quarry lead distances",
            "Environmental Clearance (MoEFCC) and River Inland Waterways navigation clearance if applicable"
        ]

        # 5. Invoke Ollama LLM for Engineering Review Commentary
        llm_prompt = f"""
You are a Senior Indian Chartered Civil Structural Engineer reviewing a preliminary bridge estimate.
Project:
- Type: {request.bridge_type} Highway Bridge in {request.location}
- Dimensions: Length = {request.length_m} m, Width = {request.width_m} m, Pier Height = {request.height_m} m
- Calculated Total Concrete: {quantities['total_concrete_m3']} m³
- Calculated Rebar Steel: {quantities['total_steel_tonnes']} Tonnes
- Calculated Cement: {quantities['cement_bags']} Bags (50kg)
- Calculated Estimated Cost: ₹{cost_results['estimation_summary'].total_estimated_cost:,.2f} INR

Relevant Indian Standards retrieved:
{rag_context_text}

Provide a concise, professional engineering evaluation (3-4 concise paragraphs) covering:
1. Soundness of span configuration and M35 concrete / Fe500D steel consumption ratios against IRC:112.
2. Geotechnical and seismic precautions for {request.location} (e.g. Brahmaputra alluvial scour, Seismic Zone V ductility).
3. Recommendation for the project manager before submitting this estimate to Laravel construction management.
Write professionally, objectively, and concisely.
"""
        system_prompt = (
            "You are a strict, authoritative Indian Bridge & Highway Civil Engineer following IRC:112, "
            "MoRTH specifications, and CPWD standards. Provide precise technical engineering analysis without fluff."
        )

        ai_analysis = self.ollama.generate_response(prompt=llm_prompt, system_prompt=system_prompt)

        # 6. Assemble Project Details
        project_details = ProjectDetails(
            type="Bridge Construction",
            bridge_type=request.bridge_type,
            location=request.location,
            length_m=request.length_m,
            width_m=request.width_m,
            height_m=request.height_m,
            spans_count=quantities["spans_count"],
            span_length_m=quantities["span_length_m"],
            concrete_grade=quantities["concrete_grade"],
            steel_grade=request.steel_grade or "Fe500D",
            foundation_type=quantities["foundation_type"]
        )

        # 7. Construct Final Estimate Response
        response = EstimateResponse(
            success=True,
            project=project_details,
            estimation=cost_results["estimation_summary"],
            components=quantities["components"],
            materials=cost_results["materials"],
            cost_breakdown=cost_results["cost_breakdown"],
            civil_engineering_assumptions=assumptions,
            source_references=source_refs,
            missing_inputs=missing_inputs,
            requires_engineer_review=True,
            ai_engineer_analysis=ai_analysis
        )

        return response

construction_agent = ConstructionRAGAgent()
