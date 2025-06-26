import os
import json
from pathlib import Path
import fitz

#input and output path
INPUT_PATH = Path("./input_pdfs/Form ADT-1-29092023_signed.pdf")
OUTPUT_PATH = Path("./output_json/output.json")

#make sure output folder exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# === Load PDF Form Fields ===
def load_pdf_fields(pdf_path):
    doc = fitz.open(pdf_path)
    fields = {}
    for page in doc:
        if not page.widgets():
            continue
        for widget in page.widgets():
            if widget.field_name:
                fields[widget.field_name] = widget.field_value
    return fields

# === Extract Structured Data ===
def extract_structured_data(fields):
    def f(key): return fields.get(key, "")

    def full_address():
        a = f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].permaddress2a_C[0]")
        b = f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].permaddress2b_C[0]")
        return f"{a} {b}".strip()

    data = {
        "company": {
            "cin": f("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].CIN_C[0]"),
            "name": f("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].CompanyName_C[0]"),
            "address": f("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].CompanyAdd_C[0]"),
            "email": f("data[0].FormADT1_Dtls[0].Page1[0].Subform1[0].EmailId_C[0]")
        },
        "auditor_info": {
            "name": f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].NameAuditorFirm_C[0]"),
            "pan": f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].PAN_C[0]"),
            "membership_no": f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].MemberShNum[0]"),
            "address": full_address(),
            "email": f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].email[0]"),
            "appointment_period": {
                "from": f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].DateOfAccAuditedFrom_D[0]"),
                "to": f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].DateOfAccAuditedTo_D[0]")
            },
            "years_applicable": f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].NumOfFinanYearApp[0]")
        },
        "joint_auditor": f("data[0].FormADT1_Dtls[0].Page1[0].Subform2[0].WhtrJointAudAppoint[0]").lower() == "yes",
        "within_limit_20": f("data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4aTo4h[0].WhrtInLimit[0]").lower() == "yes",
        "appointment_in_agm_date": f("data[0].FormADT1_Dtls[0].Page1[0].Subform6[0].DateAnnualGenMeet_D[0]"),
        "date_of_appointment": f("data[0].FormADT1_Dtls[0].Page1[0].Subform6[0].DateReceipt_D[0]"),
        "previous_appointments": [],
        "declaration": {
            "din_or_pan": f("data[0].FormADT1_Dtls[0].Page1[0].Subform6[0].DINOfDir_C[0]"),
            "designation": f("data[0].FormADT1_Dtls[0].Page1[0].Subform6[0].DesigD_C[0]"),
            "resolution_no": f("data[0].FormADT1_Dtls[0].Page1[0].Subform6[0].ResoNum[0]"),
            "date": f("data[0].FormADT1_Dtls[0].Page1[0].Subform6[0].DateOfAppSect_D[0]")
        },
        "attachments": []
    }

    for i in range(1, 11):
        auditor = f(f"data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4i[0].TextField5_{i}[0]")
        start = f(f"data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4i[0].TextField6_{i}[0]")
        end = f(f"data[0].FormADT1_Dtls[0].Page1[0].Subform3[0].Subform_4i[0].TextField7_{i}[0]")
        if auditor or start or end:
            data["previous_appointments"].append({
                "auditor": auditor,
                "start_date": start,
                "end_date": end
            })

    # Attachments (clean from Hidden_L)
    raw = f("data[0].FormADT1_Dtls[0].Page1[0].Subform6[0].Hidden_L[0]")
    if raw:
        parts = raw.split(":")
        data["attachments"] = [parts[i] for i in range(0, len(parts), 2) if parts[i].strip()]

    return data

def save_json(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"JSON saved to {output_path}")

def main():
    if not INPUT_PATH.exists():
        print(f"PDF not found at: {INPUT_PATH}")
        return

    print("Loading PDF fields...")
    fields = load_pdf_fields(INPUT_PATH)

    print(f"Found {len(fields)} fields:")
    for k, v in fields.items():
        print(f"  {k}: {v}")

    if not fields:
        print("No fields found. Possible reasons:")
        print("- PDF might not have AcroForm widgets.")
        print("- PDF may be flattened or XFA-based.")
        print("- Try opening the file in Adobe Reader and check if fields are fillable.")

    print("Structuring extracted data...")
    structured_data = extract_structured_data(fields)

    print("Saving JSON output...")
    save_json(structured_data, OUTPUT_PATH)


if __name__ == "__main__":
    main()
    