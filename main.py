import os, sys, math
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

BASE = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE, "logo.png")

def num(v, default=0.0):
    try:
        s = v.get() if hasattr(v, "get") else v
        s = str(s).strip()
        if s == "":
            return default
        return float(s)
    except Exception:
        return default

def fmt(x, nd=2):
    try:
        if isinstance(x, float):
            if math.isnan(x) or math.isinf(x):
                return "n/a"
            return f"{x:.{nd}f}"
        return str(x)
    except Exception:
        return str(x)

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.vsb.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_wheel)
    def _on_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def add_calc(parent, title, fields, compute):
    lf = ttk.LabelFrame(parent, text=title, padding=10)
    lf.pack(fill="x", padx=8, pady=6)
    vars_ = {}
    row = 0
    for label, default in fields:
        ttk.Label(lf, text=label).grid(row=row, column=0, sticky="w", pady=2, padx=(0, 6))
        v = tk.StringVar(value=str(default))
        e = ttk.Entry(lf, textvariable=v, width=16)
        e.grid(row=row, column=1, sticky="w", pady=2)
        vars_[label] = v
        row += 1
    res_var = tk.StringVar(value="")
    def run():
        try:
            res_var.set(compute(vars_))
        except Exception as ex:
            res_var.set(f"Error: {ex}")
    ttk.Button(lf, text="Calculate", command=run).grid(row=row, column=0, columnspan=2, pady=6, sticky="w")
    row += 1
    ttk.Label(lf, textvariable=res_var, foreground="#1a3a6b", font=("Segoe UI", 10, "bold"), wraplength=420, justify="left").grid(row=row, column=0, columnspan=2, sticky="w")
    return lf

def r(v): return num(v)
# ---------------- SCORES TAB ----------------
def build_scores(parent):
    sf = ScrollableFrame(parent)
    sf.pack(fill="both", expand=True)
    p = sf.inner

    add_calc(p, "Glasgow Coma Scale (GCS)", [
        ("Eye opening (1-4)", 4),
        ("Verbal (1-5)", 5),
        ("Motor (1-6)", 6),
    ], lambda v: (lambda s: f"GCS = {s}  |  " + ("Severe (<=8)" if s<=8 else "Moderate (9-12)" if s<=12 else "Mild (13-15)"))(int(r(v['Eye opening (1-4)']))+int(r(v['Verbal (1-5)']))+int(r(v['Motor (1-6)']))))

    add_calc(p, "SOFA Score", [
        ("Resp PaO2/FiO2 score 0-4", 0),
        ("Coag platelets score 0-4", 0),
        ("Liver bilirubin score 0-4", 0),
        ("Cardiovascular score 0-4", 0),
        ("CNS GCS score 0-4", 0),
        ("Renal score 0-4", 0),
    ], lambda v: (lambda s: f"SOFA = {s}  |  Mortality est: " + ("~33%" if s>=11 else "~20%" if s>=9 else "~10%" if s>=7 else "<10%"))(sum(int(r(v[k])) for k in v)))

    add_calc(p, "qSOFA", [
        ("Respiratory rate >=22 (1/0)", 0),
        ("Altered mentation (1/0)", 0),
        ("SBP <=100 (1/0)", 0),
    ], lambda v: (lambda s: f"qSOFA = {s}  |  " + ("High risk (>=2)" if s>=2 else "Low risk"))(sum(int(r(v[k])) for k in v)))

    add_calc(p, "CURB-65", [
        ("Confusion (1/0)", 0),
        ("Urea >19 mg/dL (BUN>20) (1/0)", 0),
        ("RR >=30 (1/0)", 0),
        ("SBP<90 or DBP<=60 (1/0)", 0),
        ("Age >=65 (1/0)", 0),
    ], lambda v: (lambda s: f"CURB-65 = {s}  |  Mortality: " + ("1.5%" if s<=1 else "9.2%" if s==2 else "14.5%" if s==3 else "40%+"))(sum(int(r(v[k])) for k in v)))

    add_calc(p, "Wells Score (PE)", [
        ("Clinical signs DVT (3)", 0),
        ("PE most likely (3)", 0),
        ("HR >100 (1.5)", 0),
        ("Immobilization/surgery 4wk (1.5)", 0),
        ("Prev PE/DVT (1.5)", 0),
        ("Hemoptysis (1)", 0),
        ("Malignancy (1)", 0),
    ], lambda v: (lambda s: f"Wells = {s:.1f}  |  " + ("PE likely (>4)" if s>4 else "PE unlikely (<=4)"))(sum(r(v[k]) for k in v)))

    add_calc(p, "CHA2DS2-VASc", [
        ("CHF/LV dysfunction (1)", 0),
        ("Hypertension (1)", 0),
        ("Age >=75 (2)", 0),
        ("Diabetes (1)", 0),
        ("Stroke/TIA/thromboembolism (2)", 0),
        ("Vascular disease (1)", 0),
        ("Age 65-74 (1)", 0),
        ("Female sex (1)", 0),
    ], lambda v: (lambda s: f"CHA2DS2-VASc = {int(s)}")(sum(int(r(v[k])) for k in v)))

    add_calc(p, "HAS-BLED", [
        ("Hypertension (1)", 0),
        ("Abnormal renal (1)", 0),
        ("Abnormal liver (1)", 0),
        ("Stroke (1)", 0),
        ("Bleeding history (1)", 0),
        ("Labile INR (1)", 0),
        ("Elderly >65 (1)", 0),
        ("Drugs/alcohol (1-2)", 0),
    ], lambda v: (lambda s: f"HAS-BLED = {int(s)}  |  " + ("High bleed risk (>=3)" if s>=3 else "Low-moderate"))(sum(int(r(v[k])) for k in v)))

    add_calc(p, "NIHSS (total)", [
        ("Total NIHSS score", 0),
    ], lambda v: (lambda s: f"NIHSS = {int(s)}  |  " + ("Minor 1-4" if s<=4 else "Moderate 5-15" if s<=15 else "Moderate-severe 16-20" if s<=20 else "Severe 21-42"))(r(v['Total NIHSS score'])))

    add_calc(p, "RASS", [
        ("RASS score (-5 to +4)", 0),
    ], lambda v: (lambda s: f"RASS = {int(s)}  |  " + ("Unarousable" if s<=-5 else "Deep sedation" if s<=-4 else "Moderate sedation" if s<=-3 else "Light sedation" if s<=-2 else "Drowsy" if s==-1 else "Alert & calm" if s==0 else "Restless" if s==1 else "Agitated" if s==2 else "Very agitated" if s==3 else "Combative"))(r(v['RASS score (-5 to +4)'])))

    add_calc(p, "Braden Scale", [
        ("Sensory (1-4)", 4),
        ("Moisture (1-4)", 4),
        ("Activity (1-4)", 4),
        ("Mobility (1-4)", 4),
        ("Nutrition (1-4)", 4),
        ("Friction (1-3)", 3),
    ], lambda v: (lambda s: f"Braden = {int(s)}  |  " + ("Very high risk (<=9)" if s<=9 else "High risk (10-12)" if s<=12 else "Moderate (13-14)" if s<=14 else "Mild (15-18)" if s<=18 else "No risk"))(sum(int(r(v[k])) for k in v)))

    add_calc(p, "APACHE II (APS + age + chronic)", [
        ("Temperature C", 37.0),
        ("MAP mmHg", 80),
        ("Heart rate", 80),
        ("Respiratory rate", 16),
        ("FiO2 (fraction)", 0.21),
        ("PaO2 mmHg", 90),
        ("A-a gradient (if FiO2>=0.5)", 0),
        ("Arterial pH", 7.40),
        ("Sodium", 140),
        ("Potassium", 4.0),
        ("Creatinine mg/dL", 1.0),
        ("Acute renal failure (1/0)", 0),
        ("Hematocrit %", 40),
        ("WBC x1000", 8),
        ("GCS", 15),
        ("Age", 50),
        ("Chronic health points (0/2/5)", 0),
    ], lambda v: _apache(v))

def _apache(v):
    t = r(v['Temperature C'])
    if t >= 41: aps = 4
    elif t >= 39: aps = 3
    elif t >= 38.5: aps = 1
    elif t >= 36: aps = 0
    elif t >= 34: aps = 1
    elif t >= 32: aps = 2
    elif t >= 30: aps = 3
    else: aps = 4
    m = r(v['MAP mmHg'])
    if m >= 160: aps += 4
    elif m >= 130: aps += 3
    elif m >= 110: aps += 2
    elif m >= 70: aps += 0
    elif m >= 50: aps += 2
    else: aps += 4
    hr = r(v['Heart rate'])
    if hr >= 180: aps += 4
    elif hr >= 140: aps += 3
    elif hr >= 110: aps += 2
    elif hr >= 70: aps += 0
    elif hr >= 55: aps += 2
    elif hr >= 40: aps += 3
    else: aps += 4
    rr = r(v['Respiratory rate'])
    if rr >= 50: aps += 4
    elif rr >= 35: aps += 3
    elif rr >= 25: aps += 2
    elif rr >= 12: aps += 0
    elif rr >= 10: aps += 1
    elif rr >= 6: aps += 2
    else: aps += 4
    fio2 = r(v['FiO2 (fraction)'])
    pao2 = r(v['PaO2 mmHg'])
    aag = r(v['A-a gradient (if FiO2>=0.5)'])
    if fio2 >= 0.5:
        if aag >= 500: aps += 4
        elif aag >= 350: aps += 3
        elif aag >= 200: aps += 2
        else: aps += 0
    else:
        if pao2 > 70: aps += 0
        elif pao2 >= 61: aps += 1
        elif pao2 >= 55: aps += 3
        else: aps += 4
    ph = r(v['Arterial pH'])
    if ph >= 7.7: aps += 4
    elif ph >= 7.6: aps += 3
    elif ph >= 7.5: aps += 1
    elif ph >= 7.33: aps += 0
    elif ph >= 7.25: aps += 2
    elif ph >= 7.15: aps += 3
    else: aps += 4
    na = r(v['Sodium'])
    if na >= 180: aps += 4
    elif na >= 160: aps += 3
    elif na >= 155: aps += 2
    elif na >= 150: aps += 1
    elif na >= 130: aps += 0
    elif na >= 120: aps += 2
    elif na >= 111: aps += 3
    else: aps += 4
    k = r(v['Potassium'])
    if k >= 7: aps += 4
    elif k >= 6: aps += 3
    elif k >= 5.5: aps += 1
    elif k >= 3.5: aps += 0
    elif k >= 3: aps += 1
    elif k >= 2.5: aps += 2
    else: aps += 4
    cr = r(v['Creatinine mg/dL'])
    arf = int(r(v['Acute renal failure (1/0)']))
    if cr >= 3.5: sc = 4
    elif cr >= 2: sc = 3
    elif cr >= 1.5: sc = 2
    elif cr >= 0.6: sc = 0
    else: sc = 2
    if arf and cr >= 1.5:
        sc *= 2
    aps += sc
    hct = r(v['Hematocrit %'])
    if hct >= 60: aps += 4
    elif hct >= 50: aps += 2
    elif hct >= 46: aps += 1
    elif hct >= 30: aps += 0
    elif hct >= 20: aps += 2
    else: aps += 4
    wbc = r(v['WBC x1000'])
    if wbc >= 40: aps += 4
    elif wbc >= 20: aps += 2
    elif wbc >= 15: aps += 1
    elif wbc >= 3: aps += 0
    elif wbc >= 1: aps += 2
    else: aps += 4
    gcs = r(v['GCS'])
    aps += (15 - gcs)
    age = r(v['Age'])
    if age < 45: ap = 0
    elif age <= 54: ap = 2
    elif age <= 64: ap = 3
    elif age <= 74: ap = 5
    else: ap = 6
    chronic = int(r(v['Chronic health points (0/2/5)']))
    total = int(round(aps + ap + chronic))
    return f"APACHE II = {total}  (APS={int(aps)}, age={ap}, chronic={chronic})"

# ---------------- HEMODYNAMICS TAB ----------------
def build_hemo(parent):
    sf = ScrollableFrame(parent); sf.pack(fill="both", expand=True); p = sf.inner
    add_calc(p, "MAP", [("SBP", 120), ("DBP", 80)], lambda v: f"MAP = {fmt((r(v['SBP'])+2*r(v['DBP']))/3)} mmHg")
    add_calc(p, "CPP", [("MAP", 80), ("ICP", 10)], lambda v: f"CPP = {fmt(r(v['MAP'])-r(v['ICP']))} mmHg")
    add_calc(p, "Shock Index", [("HR", 100), ("SBP", 100)], lambda v: f"SI = {fmt(r(v['HR'])/r(v['SBP']))}  |  " + ("Shock if >0.7" if r(v['HR'])/r(v['SBP'])>0.7 else "Normal"))
    add_calc(p, "Cardiac Output", [("HR", 80), ("Stroke volume mL", 70)], lambda v: f"CO = {fmt(r(v['HR'])*r(v['Stroke volume mL'])/1000)} L/min")
    add_calc(p, "SVR", [("MAP", 80), ("CVP", 8), ("CO L/min", 5)], lambda v: f"SVR = {fmt((r(v['MAP'])-r(v['CVP']))/r(v['CO L/min'])*80)} dyn·s/cm5")
    add_calc(p, "PVR", [("MPAP", 20), ("PAWP", 10), ("CO L/min", 5)], lambda v: f"PVR = {fmt((r(v['MPAP'])-r(v['PAWP']))/r(v['CO L/min'])*80)} dyn·s/cm5")
    add_calc(p, "Oxygen Delivery (DO2)", [("CO L/min", 5), ("Hb g/dL", 10), ("SaO2 %", 95), ("PaO2 mmHg", 80)], lambda v: (lambda cao2, do2: f"CaO2={fmt(cao2,3)} mL/dL  DO2={fmt(do2)} mL/min")(1.34*r(v['Hb g/dL'])*r(v['SaO2 %'])/100 + 0.003*r(v['PaO2 mmHg']), (1.34*r(v['Hb g/dL'])*r(v['SaO2 %'])/100 + 0.003*r(v['PaO2 mmHg']))*r(v['CO L/min'])*10))
    add_calc(p, "O2 Extraction Ratio", [("DO2", 1000), ("VO2", 250)], lambda v: f"O2ER = {fmt(r(v['VO2'])/r(v['DO2'])*100)} %")
    add_calc(p, "SVV", [("SVmax", 70), ("SVmin", 50)], lambda v: (lambda m: f"SVV = {fmt((r(v['SVmax'])-r(v['SVmin']))/m*100)} %")( (r(v['SVmax'])+r(v['SVmin']))/2 ))

# ---------------- VENTILATION TAB ----------------
def build_vent(parent):
    sf = ScrollableFrame(parent); sf.pack(fill="both", expand=True); p = sf.inner
    add_calc(p, "P/F Ratio", [("PaO2 mmHg", 80), ("FiO2 (fraction)", 0.4)], lambda v: f"P/F = {fmt(r(v['PaO2 mmHg'])/r(v['FiO2 (fraction)']))}  |  " + ("Normal" if r(v['PaO2 mmHg'])/r(v['FiO2 (fraction)'])>=400 else "Mild ARDS" if r(v['PaO2 mmHg'])/r(v['FiO2 (fraction)'])>=200 else "Moderate" if r(v['PaO2 mmHg'])/r(v['FiO2 (fraction)'])>=100 else "Severe"))
    add_calc(p, "A-a Gradient", [("FiO2", 0.21), ("PaO2", 90), ("PaCO2", 40), ("Pb", 760), ("PH2O", 47)], lambda v: (lambda pao2: f"A-a = {fmt(pao2 - r(v['PaO2']))} mmHg")(r(v['FiO2'])*(r(v['Pb'])-r(v['PH2O'])) - r(v['PaCO2'])/0.8))
    add_calc(p, "RSBI", [("RR", 20), ("Vt L", 0.5)], lambda v: f"RSBI = {fmt(r(v['RR'])/r(v['Vt L']))}  |  " + ("Likely wean" if r(v['RR'])/r(v['Vt L'])<105 else "Not ready"))
    add_calc(p, "Static Compliance", [("Vt mL", 500), ("Pplat cmH2O", 20), ("PEEP cmH2O", 5)], lambda v: f"Cstat = {fmt(r(v['Vt mL'])/(r(v['Pplat cmH2O'])-r(v['PEEP cmH2O'])))} mL/cmH2O")
    add_calc(p, "Driving Pressure", [("Pplat", 20), ("PEEP", 5)], lambda v: f"DP = {fmt(r(v['Pplat'])-r(v['PEEP']))} cmH2O")
    add_calc(p, "Minute Ventilation", [("RR", 16), ("Vt L", 0.5)], lambda v: f"MV = {fmt(r(v['RR'])*r(v['Vt L']))} L/min")
    add_calc(p, "IBW (ARDSnet)", [("Height cm", 170), ("Sex (M=1/F=0)", 1)], lambda v: (lambda ibw: f"IBW = {fmt(ibw)} kg  |  Vt 6mL/kg = {fmt(ibw*6)} mL")(50 + 0.91*(r(v['Height cm'])-152.4) if r(v['Sex (M=1/F=0)'])==1 else 45.5 + 0.91*(r(v['Height cm'])-152.4)))
    add_calc(p, "Dead Space Ratio", [("PaCO2", 40), ("PETCO2", 30)], lambda v: f"VD/VT = {fmt((r(v['PaCO2'])-r(v['PETCO2']))/r(v['PaCO2']))}")

# ---------------- RENAL TAB ----------------
def build_renal(parent):
    sf = ScrollableFrame(parent); sf.pack(fill="both", expand=True); p = sf.inner
    add_calc(p, "CrCl (Cockcroft-Gault)", [("Age", 50), ("Weight kg", 70), ("Scr mg/dL", 1.0), ("Female (1/0)", 0)], lambda v: (lambda crcl: f"CrCl = {fmt(crcl)} mL/min")( (140-r(v['Age']))*r(v['Weight kg'])/(72*r(v['Scr mg/dL'])) * (0.85 if r(v['Female (1/0)'])==1 else 1.0) ))
    add_calc(p, "eGFR (CKD-EPI 2021)", [("Scr mg/dL", 1.0), ("Age", 50), ("Female (1/0)", 0)], lambda v: (lambda kappa, alpha, cr: f"eGFR = {fmt(142 * min(cr/kappa,1)**alpha * max(cr/kappa,1)**(-1.200) * 0.9938**r(v['Age']) * (1.012 if r(v['Female (1/0)'])==1 else 1.0))} mL/min/1.73m2")(0.7 if r(v['Female (1/0)'])==1 else 0.9, -0.241 if r(v['Female (1/0)'])==1 else -0.302, r(v['Scr mg/dL'])))
    add_calc(p, "Free Water Deficit", [("Weight kg", 70), ("Na mEq/L", 150), ("Male(1)/Female(0)", 1)], lambda v: (lambda tbw: f"TBW={fmt(tbw)} L  FWD={fmt(tbw*(r(v['Na mEq/L'])/140-1))} L")(r(v['Weight kg'])*(0.6 if r(v['Male(1)/Female(0)'])==1 else 0.5)))
    add_calc(p, "Sodium Correction (hypernatremia rate)", [("Current Na", 150), ("Target Na", 140), ("TBW L", 42)], lambda v: f"Water needed = {fmt(r(v['TBW L'])*(r(v['Current Na'])/r(v['Target Na'])-1))} L")

# ---------------- ACID-BASE TAB ----------------
def build_acid(parent):
    sf = ScrollableFrame(parent); sf.pack(fill="both", expand=True); p = sf.inner
    add_calc(p, "Anion Gap", [("Na", 140), ("Cl", 100), ("HCO3", 24)], lambda v: f"AG = {fmt(r(v['Na'])-(r(v['Cl'])+r(v['HCO3'])))}  |  Delta gap = {fmt(r(v['Na'])-(r(v['Cl'])+r(v['HCO3']))-12)}")
    add_calc(p, "Delta Ratio", [("Na", 140), ("Cl", 100), ("HCO3", 24)], lambda v: (lambda ag: f"Delta ratio = {fmt((ag-12)/(24-r(v['HCO3'])))}")(r(v['Na'])-(r(v['Cl'])+r(v['HCO3']))) if r(v['HCO3'])!=24 else "n/a")
    add_calc(p, "SID (Strong Ion Difference)", [("Na", 140), ("K", 4.0), ("Cl", 100)], lambda v: f"SID = {fmt(r(v['Na'])+r(v['K'])-r(v['Cl']))} mEq/L")
    add_calc(p, "Base Excess", [("HCO3", 24), ("pH", 7.40), ("Hb", 10)], lambda v: f"BE = {fmt(r(v['HCO3'])-24.4 + (2.3*r(v['Hb'])+7.7)*(r(v['pH'])-7.4))} mEq/L")
    add_calc(p, "Osmolar Gap", [("Measured osm", 290), ("Na", 140), ("Glucose mg/dL", 100), ("BUN mg/dL", 14)], lambda v: f"Calc osm = {fmt(2*r(v['Na']) + r(v['Glucose mg/dL'])/18 + r(v['BUN mg/dL'])/2.8)}  |  Gap = {fmt(r(v['Measured osm']) - (2*r(v['Na']) + r(v['Glucose mg/dL'])/18 + r(v['BUN mg/dL'])/2.8))}")

# ---------------- DOSING TAB ----------------
def build_dose(parent):
    sf = ScrollableFrame(parent); sf.pack(fill="both", expand=True); p = sf.inner
    add_calc(p, "Norepinephrine (mcg/min)", [("Dose mcg/kg/min", 0.1), ("Weight kg", 70)], lambda v: f"Rate = {fmt(r(v['Dose mcg/kg/min'])*r(v['Weight kg']))} mcg/min")
    add_calc(p, "Norepi mL/h (conc mcg/mL)", [("mcg/min", 7), ("Conc mcg/mL", 16)], lambda v: f"= {fmt(r(v['mcg/min'])*60/r(v['Conc mcg/mL']))} mL/h")
    add_calc(p, "Vasopressin (units/h)", [("units/min", 0.03)], lambda v: f"= {fmt(r(v['units/min'])*60)} units/h")
    add_calc(p, "Propofol (mg/h)", [("mcg/kg/min", 25), ("Weight kg", 70)], lambda v: f"= {fmt(r(v['mcg/kg/min'])*r(v['Weight kg'])*60/1000)} mg/h")
    add_calc(p, "Fentanyl (mcg/h)", [("mcg/kg/h", 1), ("Weight kg", 70)], lambda v: f"= {fmt(r(v['mcg/kg/h'])*r(v['Weight kg']))} mcg/h")
    add_calc(p, "Midazolam (mg/h)", [("mg/kg/h", 0.05), ("Weight kg", 70)], lambda v: f"= {fmt(r(v['mg/kg/h'])*r(v['Weight kg']))} mg/h")
    add_calc(p, "Insulin infusion (units/h)", [("units/kg/h", 0.1), ("Weight kg", 70)], lambda v: f"= {fmt(r(v['units/kg/h'])*r(v['Weight kg']))} units/h")
    add_calc(p, "Heparin (units/h)", [("units/kg/h", 18), ("Weight kg", 70)], lambda v: f"= {fmt(r(v['units/kg/h'])*r(v['Weight kg']))} units/h")
    add_calc(p, "Vancomycin AUC24", [("Daily dose mg", 2000), ("CrCl mL/min", 80)], lambda v: (lambda cl: f"CL={fmt(cl)} L/h  AUC24={fmt(r(v['Daily dose mg'])/cl)} mg·h/L  (target 400-600)")(r(v['CrCl mL/min'])*0.06))
    add_calc(p, "Aminoglycoside once-daily dose", [("Weight kg", 70), ("Dose mg/kg", 7)], lambda v: f"Dose = {fmt(r(v['Weight kg'])*r(v['Dose mg/kg']))} mg")

# ---------------- FLUIDS / NUTRITION TAB ----------------
def build_fluid(parent):
    sf = ScrollableFrame(parent); sf.pack(fill="both", expand=True); p = sf.inner
    add_calc(p, "Maintenance Fluids (Holliday-Segar, mL/day)", [("Weight kg", 70)], lambda v: (lambda w: f"= {fmt((100*min(w,10)+50*max(0,min(w-10,10))+20*max(0,w-20)))} mL/day  ({fmt((100*min(w,10)+50*max(0,min(w-10,10))+20*max(0,w-20))/24)} mL/h)")(r(v['Weight kg'])))
    add_calc(p, "Fluid Deficit", [("Maintenance mL/h", 100), ("Hours missed", 8)], lambda v: f"Deficit = {fmt(r(v['Maintenance mL/h'])*r(v['Hours missed']))} mL")
    add_calc(p, "BMI", [("Weight kg", 70), ("Height m", 1.75)], lambda v: f"BMI = {fmt(r(v['Weight kg'])/(r(v['Height m'])**2))} kg/m2")
    add_calc(p, "BSA (DuBois)", [("Weight kg", 70), ("Height cm", 170)], lambda v: f"BSA = {fmt(0.007184*r(v['Weight kg'])**0.425*r(v['Height cm'])**0.725)} m2")
    add_calc(p, "IBW (Devine)", [("Height in", 68), ("Male(1)/Female(0)", 1)], lambda v: f"IBW = {fmt((50 if r(v['Male(1)/Female(0)'])==1 else 45.5) + 2.3*(r(v['Height in'])-60))} kg")
    add_calc(p, "BMR (Harris-Benedict)", [("Weight kg", 70), ("Height cm", 170), ("Age", 50), ("Male(1)/Female(0)", 1)], lambda v: (lambda bmr: f"BMR = {fmt(bmr)} kcal/day  (x1.2-1.5 stress)")(66.5+13.75*r(v['Weight kg'])+5.003*r(v['Height cm'])-6.75*r(v['Age']) if r(v['Male(1)/Female(0)'])==1 else 655.1+9.563*r(v['Weight kg'])+1.85*r(v['Height cm'])-4.676*r(v['Age'])))
    add_calc(p, "Protein needs", [("Weight kg", 70), ("g/kg", 1.5)], lambda v: f"Protein = {fmt(r(v['Weight kg'])*r(v['g/kg']))} g/day")

# ---------------- CONVERSIONS TAB ----------------
def build_conv(parent):
    sf = ScrollableFrame(parent); sf.pack(fill="both", expand=True); p = sf.inner
    add_calc(p, "C to F", [("Celsius", 37)], lambda v: f"= {fmt(r(v['Celsius'])*9/5+32)} F")
    add_calc(p, "F to C", [("Fahrenheit", 98.6)], lambda v: f"= {fmt((r(v['Fahrenheit'])-32)*5/9)} C")
    add_calc(p, "lb to kg", [("lb", 154)], lambda v: f"= {fmt(r(v['lb'])*0.453592)} kg")
    add_calc(p, "kg to lb", [("kg", 70)], lambda v: f"= {fmt(r(v['kg'])/0.453592)} lb")
    add_calc(p, "in to cm", [("inches", 68)], lambda v: f"= {fmt(r(v['inches'])*2.54)} cm")
    add_calc(p, "cm to in", [("cm", 170)], lambda v: f"= {fmt(r(v['cm'])/2.54)} in")
    add_calc(p, "mmHg to cmH2O", [("mmHg", 10)], lambda v: f"= {fmt(r(v['mmHg'])*1.36)} cmH2O")
    add_calc(p, "cmH2O to mmHg", [("cmH2O", 13.6)], lambda v: f"= {fmt(r(v['cmH2O'])/1.36)} mmHg")

# ---------------- MAIN ----------------
def main():
    root = tk.Tk()
    root.title("ICU-Critical Care Software | Developed by Dr Sumaiya Mohammad, SMRR Team, Bangladesh")
    try:
        ico = os.path.join(BASE, "logo.ico")
        if os.path.exists(ico):
            root.iconbitmap(ico)
    except Exception:
        pass
    root.geometry("520x720")
    root.minsize(480, 600)

    # header
    hdr = ttk.Frame(root, padding=8)
    hdr.pack(fill="x")
    try:
        img = Image.open(LOGO_PATH).resize((48, 48))
        logo_img = ImageTk.PhotoImage(img)
        lbl = ttk.Label(hdr, image=logo_img)
        lbl.image = logo_img
        lbl.pack(side="left", padx=(0, 10))
    except Exception:
        pass
    ttk.Label(hdr, text="ICU-Critical Care Software", font=("Segoe UI", 16, "bold")).pack(side="left")
    ttk.Label(hdr, text="Developed by Dr Sumaiya Mohammad, SMRR Team, Bangladesh", font=("Segoe UI", 9)).pack(side="left", padx=8)

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=6, pady=6)

    tabs = [
        ("Scores", build_scores),
        ("Hemo", build_hemo),
        ("Vent", build_vent),
        ("Renal", build_renal),
        ("Acid-Base", build_acid),
        ("Dosing", build_dose),
        ("Fluids/Nut", build_fluid),
        ("Convert", build_conv),
    ]
    for name, builder in tabs:
        frame = ttk.Frame(nb)
        nb.add(frame, text=name)
        builder(frame)

    root.mainloop()

if __name__ == "__main__":
    main()

