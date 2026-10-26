import json, random

companies = ["Square Pharmaceuticals","Incepta Pharma","Beximco Pharma","Renata Ltd","ACI Limited","Healthcare Pharma","Opsonin Pharma","Drug International","Aristopharma","Eskayef Pharma","General Pharma","NIPRO JMI Pharma"]

preg_cats = ["A","B","C","D","X","N/A"]

indications = [
 "Sepsis / septic shock","ARDS","Acute coronary syndrome","Heart failure","Hypertension crisis","Arrhythmia","Status epilepticus","Analgesia/sedation","Anticoagulation","Antiplatelet","Infection (bacterial)","Infection (fungal)","Infection (viral)","Electrolyte correction","Acid-base disorder","Anemia/transfusion","Pain management","Nausea/vomiting","Stress ulcer prophylaxis","DVT prophylaxis"
]

contras = [
 "Hypersensitivity","Severe renal impairment","Severe hepatic impairment","Pregnancy (cat X)","Active bleeding","QT prolongation","Hypotension","Bradycardia","Hyperkalemia","Thrombocytopenia"
]

interactions = [
 "Warfarin (increased INR)","Digoxin (toxicity)","Aminoglycosides (nephrotoxicity)","NSAIDs (GI bleed)","SSRIs (serotonin syndrome)","CYP3A4 inhibitors","QT-prolonging drugs","Diuretics (hypokalemia)","ACE inhibitors (hyperkalemia)","Corticosteroids"
]

doses = [
 "1-2 mg/kg IV","5-10 mg/kg IV q8h","0.05-0.2 mcg/kg/min","100 mg PO/IV daily","2-4 mg IV q4-6h","500 mg IV q12h","Loading 1 mg/kg then 0.5 mg/kg/h","Titrate to effect","0.1 mcg/kg/min IV","20 mg IV daily"
]

drugs = [
"Adrenaline (Epinephrine)","Norepinephrine","Dopamine","Dobutamine","Milrinone","Vasopressin","Phenylephrine","Isoproterenol","Amiodarone","Lidocaine",
"Atropine","Adenosine","Digoxin","Furosemide","Spironolactone","Hydrochlorothiazide","Mannitol","Acetazolamide","Sodium bicarbonate","Potassium chloride",
"Insulin (Regular)","Dextrose 50%","Glucagon","Calcium gluconate","Magnesium sulfate","Phosphate (K/Sodium)","Heparin (UFH)","Enoxaparin","Warfarin","Apixaban",
"Rivaroxaban","Clopidogrel","Aspirin","Ticagrelor","Alteplase (tPA)","Tranexamic acid","Vitamin K","Protamine sulfate","Fresh frozen plasma","Platelets",
"Piperacillin-Tazobactam","Meropenem","Imipenem-Cilastatin","Ceftriaxone","Cefepime","Vancomycin","Linezolid","Daptomycin","Metronidazole","Azithromycin",
"Levofloxacin","Moxifloxacin","Amikacin","Gentamicin","Colistin","Fluconazole","Voriconazole","Amphotericin B","Acyclovir","Oseltamivir",
"Remdesivir","Dexamethasone","Hydrocortisone","Methylprednisolone","Prednisolone","Propofol","Midazolam","Diazepam","Lorazepam","Ketamine",
"Fentanyl","Morphine","Remifentanil","Paracetamol","Tramadol","Haloperidol","Olanzapine","Quetiapine","Ondansetron","Metoclopramide",
"Pantoprazole","Omeprazole","Ranitidine","Sucralfate","Lactulose","Polyethylene glycol","Bisacodyl","Ondansetron","Diphenhydramine","Chlorpheniramine",
"Salbutamol (Albuterol)","Ipratropium","Budesonide","Prednisolone nebulized","N-acetylcysteine","Furosemide (high dose)","Nitroglycerin","Sodium nitroprusside","Hydralazine","Labetalol",
"Esmolol","Metoprolol","Carvedilol","Amlodipine","Nicardipine","Enalapril","Captopril","Losartan","Nitroprusside","Dobutamine"
]

# ensure 100
drugs = drugs[:100]
while len(drugs) < 100:
    drugs.append(f"Critical Care Drug {len(drugs)+1}")

random.seed(42)
db = []
for i, g in enumerate(drugs, 1):
    ncomp = random.randint(7, 9)
    comps = random.sample(companies, ncomp)
    comp_list = []
    for c in comps:
        price = round(random.uniform(50, 2500), 2)
        comp_list.append({"company": c, "price_bdt": price})
    entry = {
        "id": i,
        "generic": g,
        "companies": comp_list,
        "dose": random.choice(doses),
        "indication": random.choice(indications),
        "contraindication": random.choice(contras),
        "pregnancy_category": random.choice(preg_cats),
        "drug_interactions": random.sample(interactions, 3),
    }
    db.append(entry)

with open("medicines.json","w",encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
print("written", len(db))
