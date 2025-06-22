from fastapi import APIRouter

router = APIRouter(prefix="/treatment", tags=["Treatment"])

@router.get("/estimate")
def estimate_treatment_cost():
    return {
        "message": "Estimated treatment cost ranges.",
        "estimates": {
            "Low risk": "$50 - $100",
            "Moderate risk": "$150 - $300",
            "High risk": "$400+"
        },
        "note": "Exact cost depends on location and institution. Please contact a provider."
    }
