import sys
sys.stdout.reconfigure(encoding='utf-8')
from fastapi.testclient import TestClient
from app.main import app

def test_api():
    client = TestClient(app)

    print("=" * 60)
    print("1. Testing Health Endpoint (GET /api/construction/health)")
    print("=" * 60)
    resp = client.get("/api/construction/health")
    print("Status:", resp.status_code)
    print("Response:", resp.json())
    assert resp.status_code == 200

    print("\n" + "=" * 60)
    print("2. Testing Estimate Endpoint (POST /api/construction/estimate)")
    print("=" * 60)
    payload = {
        "project_type": "bridge",
        "bridge_type": "RCC",
        "length_m": 100.0,
        "width_m": 10.0,
        "height_m": 8.0,
        "location": "Assam, India"
    }
    resp = client.post("/api/construction/estimate", json=payload)
    print("Status:", resp.status_code)
    data = resp.json()
    print("Success:", data.get("success"))
    print("Total Cost:", f"Rs. {data['estimation']['total_estimated_cost']:,.2f}")
    print("Concrete m3:", f"{data['materials'][0]['quantity']:,.1f} m3")
    print("Steel tonnes:", f"{data['materials'][1]['quantity']:,.1f} tonnes")
    print("Cement bags:", f"{data['materials'][3]['quantity']:,.0f} bags")
    print("Matching standards count:", len(data.get("source_references", [])))
    print("Missing inputs count:", len(data.get("missing_inputs", [])))
    assert resp.status_code == 200

    print("\nAll API tests passed successfully!")

if __name__ == "__main__":
    test_api()
