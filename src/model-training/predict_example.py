from pathlib import Path

import spacy

REPO_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = REPO_ROOT / "data" / "model" / "model-best"

SAMPLE_TEXTS = [
"""Inclusion Criteria:
Patients must meet all the following criteria to be eligible for enrollment in the study:
1. Be age ≥ 18 years on the day of signing informed consent.
2. Be able and willing to voluntarily complete the informed consent process.
3. Have a predicted life expectancy of ≥ 3 months.
4. Have an ECOG PS ≤ 2.
5. Have the following disease characteristics:
Have a histologically or cytologically-confirmed advanced selected solid tumor or DLBCL for which there are no further standard therapeutic options available, or patient is not a candidate for standard treatment:
• MRT-2359 monotherapy
• Phase 1:
    − NSCLC
    − SCLC
    − High-grade neuroendocrine cancer (or small cell carcinoma) of any primary site
    − Any solid tumors with L-MYC or N-MYC amplification*
    − DLBCL
• Phase 2:
    − Any solid tumors with L-MYC or N-MYC known amplification* (excluding patients with breast or prostate cancer eligible for disease-specific cohorts)
    − NSCLC with known L-MYC or N-MYC expression status** (excluding patients with breast or prostate cancer eligible for disease-specific cohorts)
    − SCLC
• MRT-2359 in combination with fulvestrant
• Phase 2:
    − HR-positive, HER2-negative breast cancer
• MRT-2359 in combination with enzalutamide
• Phase 2:
    − Non-neuroendocrine prostate cancer including at least 7 patients who have received prior abiraterone but not prior enzalutamide, darolutamide, apalutamide, or similar experimental therapy such as AR inhibitors and degraders and 7 patients who have ligand‑binding domain mutations such as AR L702H, AR T878X (e.g., T878A or T878S), AR H875Y, or similar pathogenic mutations (if approved by the Sponsor) detected by the clinical molecular testing of tumor tissue or circulating tumor DNA. Patients meeting both criteria will count towards both subgroups.
* L-MYC and N-MYC amplification status will be available from local site assessment (as part of patient’s standard of care treatment)
** L-MYC and N-MYC expression status is planned to be analyzed with investigational clinical trial assay in the College of American Pathologists-accredited and Clinical Laboratory Improvement Amendmentscertified central laboratory provided by the Sponsor.
6. Have measurable disease by RECIST 1.1 (Eisenhauer, et al. 2009) in case of solid tumors or Revised Response Criteria for Malignant Lymphoma (Phase 1only) (Cheson, et al. 2014) in case of DLBCL
7. Be able to provide tumor biopsies for biomarker analysis during the screening period, on treatment, and at progression/EOT (optional).
• Patients for whom a biopsy is contraindicated may opt out of providing tumor biopsies after Investigator discussion with, and approval from, the Sponsor.
8. Have adequate organ function, defined as follows:
System Laboratory Value
Hematologic
ANC ≥ 1,000/µL
Platelets ≥ 75,000/µL
Hemoglobin ≥ 8.0 g/dL
Renal
Creatinine clearance ≥ 60 mL/min measured via 24-hour urine collection or calculated creatinine clearance using Cockcroft-Gault formula (Appendix 10.1)
Hepatic
Total bilirubin ≤ 1.5 × ULN OR direct bilirubin ≤ ULN for participants with total bilirubin levels > 1.5 × ULN
AST and ALT ≤ 3 × ULN (≤ 5 × ULN for participants with tumor liver involvement)
Coagulation
INR or PT aPTT ≤ 1.5 × ULN unless participant is receiving anticoagulant therapy as long as PT or aPTT is within therapeutic range of intended use of anticoagulants
Abbreviations: ALT = alanine aminotransferase; ANC = absolute neutrophil count; aPTT = activated partial thromboplastin time; AST = aspartate aminotransferase; INR = international normalized ratio; PT = prothrombin time; ULN = upper limit of normal.
Note: This table includes eligibility-defining laboratory value requirements for treatment; laboratory value requirements should be adapted according to local regulations and guidelines for the administration of specific chemotherapies. 
Patients may be retested more than once during the screening period.
9. Have serum calcium and phosphate levels within normal limits, no worse than Grade 1 if abnormal, or correctable with supplements or other therapies. Hypercalcemia with serum calcium corrected for albumin ≤ 13.5 mg/dL is allowed.
10. Have vitamin D levels of ≥ 12 ng/mL, confirmed using a serum 25-hydroxy vitamin D test.
11. Have magnesium levels of Grade ≤ 1.
12. If female of childbearing potential, patient must avoid becoming pregnant and agree to use acceptable method of contraception after signing informed consent, throughout the study, and for 90 days after the last dose of MRT-2359. Acceptable methods of contraception include any of the following:
• Total abstinence (if it is their preferred and usual lifestyle) OR 2 of the following:
• Double-barrier contraception (e.g., a combination of condom or diaphragm with spermicidal gel)
• Hormonal contraception (birth control pills, injections, hormonal patches, vaginal rings, or implants)
• An intrauterine device
• Have a vasectomized partner with confirmed azoospermia
Note: All females will be considered of childbearing potential unless they are post-menopausal (has amenorrhea for at least 12 consecutive months, in the appropriate age group, and without other known or suspected cause) or have been sterilized surgically (i.e., bilateral tubal ligation, total hysterectomy, or bilateral oophorectomy, all with surgery at least 1 month before dosing).
13. Male of reproductive potential, agree, in collaboration with their female partners, to use 2 approved methods of contraception (listed above), or total abstinence (if it is their preferred and usual lifestyle), from informed consent until 90 days after study discharge. Sperm donation is not allowed during the study period and for 90 days after last dose of MRT-2359. 
14. Be willing and able to check her/his blood pressure daily and before each dose of MRT-2359 during C1 (first 28 days). If clinically appropriate, blood pressure may be checked daily during subsequent treatment using the provided device.

Exclusion Criteria:
Patients meeting any of the following criteria will not be enrolled in the study:
1. Have received prior chemotherapy, definitive radiation, or biological cancer therapy within 21 days before the first dose of study treatment or have any AEs that have failed to recover to baseline or Common Terminology Criteria for Adverse Events (CTCAE) Grade 1, except for any grade of alopecia or hearing loss from AEs caused by cancer therapeutics administered > 21 days earlier. In addition, Grade ≤ 2 endocrinopathies compensated with medication are eligible for enrollment. In patients with prostate cancer, continuation of systemic therapies such as luteinizing hormone-releasing hormone analogues to achieve and maintain castration levels of testosterone is allowed. Also, pre-menopausal patients with hormone-dependent breast cancer can continue on therapies used for suppression of ovarian function, such as luteinizing hormone-releasing hormone analogues.
2. Have received bisphosphonates or denosumab within 14 days before the first administration of the study drug unless they were given for acute hypercalcemia.
3. Be unable to swallow PO medication.
4. Be unable to take PO calcium and calcitriol.
5. Have received prior therapy with a GSPT1 degrader that was discontinued due to an AE.
6. Have systolic blood pressure < 100 mmHg.
7. Have received prior auto-HCT and not fully recovered from effects of the last transplant.
8. Have received allogeneic hematopoietic stem cell transplantation within past 6 months and/or have symptoms of graft-versus-host disease. Patients requiring minimal intervention such as topical steroids are eligible.
9. Have received a live vaccine within 90 days before the first dose of study treatment. Examples of live vaccines include, but are not limited to, the following: measles, mumps, rubella, varicella/zoster (chicken pox), yellow fever, rabies, Bacillus Calmette-Guérin, and typhoid vaccine. Seasonal influenza vaccines for injection are generally killed virus vaccines and are allowed; however, intranasal influenza vaccines (e.g., FluMist®) are live attenuated vaccines and are not allowed.
10. Have received Coronavirus disease 2019 immunization within 14 days of receiving the first dose of MRT-2359.
11. Have participated in a study of an investigational agent and received study therapy or used an investigational device within 21 days before the first dose of study treatment.
12. Current use of chronic systemic steroid therapy in excess of replacement doses (prednisone ≤ 10 mg/day is acceptable).
13. Have clinically significant active malabsorption syndrome or other condition likely to affect gastrointestinal absorption of the study drug.
14. Have anticipated requirement of any other form of antineoplastic therapy while on study.
15. Have a history of a second malignancy, unless controlled not requiring therapy.
16. Have clinically active CNS involvement and/or carcinomatous meningitis. Patients with treated and stable brain metastases (not progressing for at least 4 weeks prior to enrollment) not requiring steroids are eligible.
17. Have a confirmed history of (non-infectious) pneumonitis that required steroids.
18. Have known human immunodeficiency virus unless the patient is on antiviral therapy with undetectable human immunodeficiency virus ribonucleic acid (RNA) levels.
19. Have known hepatitis B or C infection(s) unless treated with undetectable hepatitis B deoxyribonucleic acid (DNA) or hepatitis C RNA levels.
20. Have active infection requiring systemic intravenous therapy.
21. Have significant detectable infection or failure to fully recover from the effects of major surgery. Surgeries that required general anesthesia must be completed > 28 days before the first dose of study drug. Surgery requiring regional/epidural anesthesia must be completed > 7 days before the first dose of study treatment and participants should be recovered.
22. Have active cardiac disease or a history of cardiac dysfunction, including any of the following:
• History of angina pectoris, symptomatic pericarditis, or myocardial infarction within 6 months before study entry.
• Congestive heart failure (New York Heart Association functional classification III or IV).
• Documented restrictive cardiomyopathy.
• Have an LVEF < 50% as determined by MUGA scan or ECHO.
• Have a history of any cardiac arrhythmias, e.g., ventricular, supraventricular, nodal arrhythmias, or conduction abnormality, in the previous 12 months. Rate controlled and hemodynamically stable atrial fibrillation is allowed.
• Have a prolonged corrected QT interval (QTc) interval of > 470 ms as demonstrated by the QTc corrected by Fridericia’s formula or history of long QTc syndrome. The eligibility of patients with ventricular pacemakers for whom the QT interval may not be accurately measurable will be determined on a case by case basis by the Sponsor in consultation with the Medical Monitor.
23. Have a history or current evidence of any other condition, therapy, or laboratory abnormality that might confound the results of the study, interfere with the participant’s participation for the full duration of the study, or not be in the best interest of the participant to participate, in the opinion of the treating Investigator.
24. Be pregnant or breastfeeding or anticipate conception or fathering of children within the projected duration of the study and for 90 days after the last dose of MRT-2359."""]


def main() -> None:
    nlp = spacy.load(MODEL_DIR)

    for text in SAMPLE_TEXTS:
        doc = nlp(text)
        print(f"\nText: {text}")
        scores = doc.spans["sc"].attrs["scores"]
        for span, score in zip(doc.spans["sc"], scores):
            print(f"  {span.label_:<12} {span.text!r:<30} confidence={score:.4f}")


if __name__ == "__main__":
    main()
