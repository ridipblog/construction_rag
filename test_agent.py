import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from app.schemas.estimate import BridgeEstimateRequest
from app.rag.agent import construction_agent

def main():
    print("=" * 70)
    print("TESTING CONSTRUCTION RAG AGENT (RCC BRIDGE IN ASSAM, INDIA)")
    print("=" * 70)

    # User input scenario
    req = BridgeEstimateRequest(
        project_type="bridge",
        bridge_type="RCC",
        length_m=100.0,
        width_m=10.0,
        height_m=8.0,
        location="Assam, India",
        currency="INR"
    )

    print(f"Request: {req.model_dump_json(indent=2)}")
    print("\nRunning RAG Retrieval, Civil Engineering Calculations & LLM Review...")
    
    response = construction_agent.process_estimate(req)
    
    print("\n" + "=" * 70)
    print("AGENT ESTIMATION REPORT RESULT:")
    print("=" * 70)
    print(f"Project: {response.project.type} ({response.project.bridge_type}) - {response.project.location}")
    print(f"Dimensions: {response.project.length_m}m L x {response.project.width_m}m W x {response.project.height_m}m H")
    print(f"Spans: {response.project.spans_count} spans of {response.project.span_length_m}m")
    print(f"Foundation: {response.project.foundation_type}")
    print(f"Total Estimated Cost: Rs. {response.estimation.total_estimated_cost:,.2f} {response.estimation.currency}")
    print(f"Cost per Linear Metre: Rs. {response.estimation.cost_per_linear_metre:,.2f} / m")
    
    print("\n--- Structural Components Breakdown ---")
    for comp in response.components:
        print(f"* {comp.component_name}: Concrete={comp.concrete_volume_m3} m3, Steel={comp.steel_weight_tonnes} T, Shuttering={comp.formwork_area_m2} m2")

    print("\n--- Key Material Quantities ---")
    for mat in response.materials[:6]:
        print(f"* {mat.name}: {mat.quantity:,.1f} {mat.unit} @ Rs. {mat.rate:,.2f} = Rs. {mat.amount:,.2f}")

    print("\n--- RAG Retrieved Indian Standards ---")
    for ref in response.source_references:
        print(f"* [{ref.code_reference}] (Score: {ref.relevance_score}): {ref.title}")

    print("\n--- AI Civil Engineer Technical Analysis ---")
    print(response.ai_engineer_analysis)

    print("\n--- Missing Inputs Identified by Agent ---")
    for mi in response.missing_inputs:
        print(f"- [WARNING] {mi}")

    # Output full JSON to a file so user can review the exact API payload
    with open("sample_estimate_response.json", "w", encoding="utf-8") as f:
        f.write(response.model_dump_json(indent=2))
    print("\nFull JSON saved to sample_estimate_response.json")

if __name__ == "__main__":
    main()
