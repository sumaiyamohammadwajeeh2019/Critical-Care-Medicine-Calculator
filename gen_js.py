import json
db = json.load(open("medicines.json", encoding="utf-8"))
js = "window.MEDS = " + json.dumps(db, ensure_ascii=False) + ";"
open("medicines.js","w",encoding="utf-8").write(js)
print("ok", len(db))
