from typing import List
from pydantic import BaseModel


class FarmerProfile(BaseModel):
    state: str
    land_acres: float
    category: str         # General / SC / ST / OBC
    annual_income: float
    crop_type: str
    has_bank_account: bool
    has_aadhaar: bool


SCHEMES = [
    {
        "id": "pm_kisan",
        "name": "PM-KISAN",
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "benefit": "₹6,000/year in 3 installments directly to bank account",
        "ministry": "Ministry of Agriculture",
        "documents": ["Aadhaar Card", "Land record (Khatauni)",
                      "Bank passbook", "Mobile linked to Aadhaar"],
        "apply_at": "pmkisan.gov.in or nearest CSC centre",
        "check": lambda p: p.has_aadhaar and p.has_bank_account and p.land_acres > 0
    },
    {
        "id": "pmfby",
        "name": "PMFBY",
        "full_name": "Pradhan Mantri Fasal Bima Yojana",
        "benefit": "Crop insurance against drought, flood & pest. Premium only 2% for Kharif crops",
        "ministry": "Ministry of Agriculture",
        "documents": ["Aadhaar Card", "Land record / Khasra",
                      "Bank passbook", "Sowing certificate"],
        "apply_at": "pmfby.gov.in or your bank branch",
        "check": lambda p: p.has_aadhaar and p.land_acres > 0
    },
    {
        "id": "kcc",
        "name": "Kisan Credit Card",
        "full_name": "Kisan Credit Card Scheme",
        "benefit": "Credit up to ₹3 lakh at 4% interest for farming expenses",
        "ministry": "RBI / NABARD",
        "documents": ["Aadhaar Card", "Land ownership proof",
                      "Passport size photo", "Bank account details"],
        "apply_at": "Any nationalized bank or cooperative bank",
        "check": lambda p: p.has_aadhaar and p.land_acres >= 0.5 and p.has_bank_account
    },
    {
        "id": "smam",
        "name": "SMAM Subsidy",
        "full_name": "Sub-Mission on Agricultural Mechanisation",
        "benefit": "Up to 50% subsidy on farm machinery for small & marginal farmers",
        "ministry": "Ministry of Agriculture",
        "documents": ["Aadhaar Card", "Land record",
                      "Caste certificate (SC/ST)", "Bank passbook"],
        "apply_at": "agrimachinery.nic.in",
        "check": lambda p: p.land_acres <= 10 and p.has_aadhaar
    },
    {
        "id": "soil_health",
        "name": "Soil Health Card",
        "full_name": "Soil Health Card Scheme",
        "benefit": "Free soil testing + personalised fertilizer recommendation",
        "ministry": "Ministry of Agriculture",
        "documents": ["Aadhaar Card", "Land details"],
        "apply_at": "soilhealth.dac.gov.in or nearest agriculture office",
        "check": lambda p: p.land_acres > 0
    },
    {
        "id": "enam",
        "name": "eNAM",
        "full_name": "National Agriculture Market",
        "benefit": "Sell crops online at best price across India, transparent bidding",
        "ministry": "Ministry of Agriculture",
        "documents": ["Aadhaar Card", "Bank passbook", "Mobile number"],
        "apply_at": "enam.gov.in or nearest APMC mandi",
        "check": lambda p: p.has_aadhaar and p.has_bank_account
    },
]


def check_eligibility(profile: FarmerProfile) -> List[dict]:
    results = []
    for scheme in SCHEMES:
        try:
            is_eligible = scheme["check"](profile)
        except Exception:
            is_eligible = False

        results.append({
            "id":        scheme["id"],
            "name":      scheme["name"],
            "full_name": scheme["full_name"],
            "benefit":   scheme["benefit"],
            "ministry":  scheme["ministry"],
            "documents": scheme["documents"],
            "apply_at":  scheme["apply_at"],
            "eligible":  is_eligible,
        })

    results.sort(key=lambda x: x["eligible"], reverse=True)
    return results