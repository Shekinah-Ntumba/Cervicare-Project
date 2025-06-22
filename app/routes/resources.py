from fastapi import APIRouter

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.get("/")
def get_resource_links():
    return {
        "book_screening": "/screening/book",
        "estimate_treatment": "/treatment/estimate",
        "healthcare_institutions": "/resources/healthcare",
        "financial_support": "/resources/financial"
    }

@router.get("/healthcare")
def list_healthcare_providers():
    return [
        {"name": "Kinshasa General Hospital", "location": "Kinshasa", "contact": "+243 123456789"},
        {"name": "Lubumbashi Medical Center", "location": "Lubumbashi", "contact": "+243 987654321"}
    ]

@router.get("/financial")
def list_financial_resources():
    return [
        {"name": "Health Access Fund", "type": "NGO", "website": "https://example.com"},
        {"name": "Ministry of Health Subsidy Program", "type": "Govt", "contact": "+243 1122334455"}
    ]
