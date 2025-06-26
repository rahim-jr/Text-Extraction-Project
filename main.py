import os
import json
from pathlib import Path
import fitz

# Input and output paths
INPUT_PATH = Path("./input_pdfs/Form ADT-1-29092023_signed.pdf")
OUTPUT_PATH = Path("./output_json/output.json")

# Make sure output folder exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# === Load Form Fields using PyMuPDF ===
def load_pdf_fields(pdf_path):
    doc = fitz.open(pdf_path)
    fields = {}
    for page in doc:
        widgets = page.widgets()
        if not widgets:
            continue
        for widget in widgets:
            key = widget.field_name
            value = widget.field_value
            if key:
                fields[key] = value
    return fields

def extract_structured_data(fields):
    # Mapping PDF form fields to structured JSON
    data = {
        "company": {
            "cin": fields.get("CIN_C", {}).get("/V", ""),
            "name": fields.get("CompanyName_C", {}).get("/V", ""),
            "address": fields.get("CompanyAdd_C", {}).get("/V", ""),
            "email": fields.get("EmailId_C", {}).get("/V", "")
        },
        "auditor_info": {
            "name": fields.get("NameAuditorFirm_C", {}).get("/V", ""),
            "pan": fields.get("PAN_C", {}).get("/V", ""),
            "membership_no": fields.get("MemberShNum", {}).get("/V", ""),
            "address": f"{fields.get('permaddress2a_C', {}).get('/V', '')} {fields.get('permaddress2b_C', {}).get('/V', '')}".strip(),
            "email": fields.get("email", {}).get("/V", ""),
            "appointment_period": {
                "to": fields.get("DateOfAccAuditedTo_D", {}).get("/V", "")
            },
            "years_applicable": fields.get("NumOfFinanYearApp", {}).get("/V", "")
        },
        "joint_auditor": fields.get("DropDownList1", {}).get("/V", "").lower() == "yes",
        "within_limit_20": fields.get("SEC8", {}).get("/V", "").lower() == "yes",
        "appointment_in_agm_date": fields.get("DateAnnualGenMeet_D", {}).get("/V", ""),
        "date_of_appointment": fields.get("DateReceipt_D", {}).get("/V", ""),
        "previous_appointments": [],
        "declaration": {
            "din_or_pan": fields.get("DINOfDir_C", {}).get("/V", ""),
            "designation": fields.get("DesigD_C", {}).get("/V", ""),
            "resolution_no": fields.get("ResoNum", {}).get("/V", ""),
            "date": fields.get("DateOfAppSect_D", {}).get("/V", "")
        },
        "attachments": [
            "Consent signed.pdf",
            "Resolution for appointment of Auditor Signed.pdf",
            "Intimation Letter Signed.pdf",
            "Acceptance signed.pdf"
        ]
    }

    # Extract previous appointments
    for i in range(1, 11):
        auditor = fields.get(f"TextField5_{i}", {}).get("/V", "")
        year = fields.get(f"TextField7_{i}", {}).get("/V", "")
        if auditor or year:
            data["previous_appointments"].append({
                "auditor": auditor,
                "year": year
            })

    return data

def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON saved to {output_path}")

def main():
    if not INPUT_PATH.exists():
        print(f"❌ PDF not found at: {INPUT_PATH}")
        return

    print("🔍 Loading PDF fields...")
    fields = load_pdf_fields(INPUT_PATH)

    print("📦 Structuring extracted data...")
    structured_data = extract_structured_data(fields)

    print("💾 Saving JSON output...")
    save_json(structured_data, OUTPUT_PATH)

if __name__ == "__main__":
    main()
