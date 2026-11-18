import json
import math
import os
import subprocess
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import project as P

UA = "pdawgy-property-map/1.0"
OUT = os.path.join(P.WORK, "map", "nominatim.json")
SPAN = 0.024


def q(params):
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(params)
    out = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url], capture_output=True, text=True).stdout
    time.sleep(1.1)
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return []


def dist(la, lo):
    return 6371000 * math.hypot(math.radians(la - P.SITE[0]),
                                math.radians(lo - P.SITE[1]) * math.cos(math.radians(P.SITE[0])))


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    la, lo = P.SITE
    vb = f"{lo - SPAN},{la + SPAN},{lo + SPAN},{la - SPAN}"
    site = q({"q": P.MAP_SITE_QUERY, "format": "json", "limit": 5})
    print("site candidates (check P.SITE matches the plans' key plan):")
    for r in site:
        print(f"   {r['lat']}, {r['lon']}  {r['display_name'][:90]}  ({r.get('class')}/{r.get('type')})")
    data = {"pois": {}, "roads": {}}
    for kind, term in [("school", "school"), ("park", "park")]:
        rows = q({"q": term, "format": "json", "viewbox": vb, "bounded": 1, "limit": 40})
        data["pois"][kind] = [(r["display_name"].split(",")[0], float(r["lat"]), float(r["lon"]), r.get("type"))
                              for r in rows]
    mrt = []
    for name in P.MRT_STATION_QUERIES:
        rows = [r for r in q({"q": name, "format": "json", "limit": 4, "countrycodes": "sg"})
                if r.get("class") == "railway" and r.get("type") == "station"]
        if rows:
            mrt.append((name.replace(" station", "") + " MRT", float(rows[0]["lat"]), float(rows[0]["lon"]), "station"))
    data["pois"]["mrt"] = mrt
    for road in P.MAP_ROADS:
        rows = q({"street": road, "city": "Singapore", "format": "json", "limit": 40, "polygon_geojson": 1,
                  "polygon_threshold": 0.00003, "viewbox": vb, "bounded": 1})
        data["roads"][road] = [x["geojson"] for x in rows if x.get("class") == "highway" and "geojson" in x]
    with open(OUT, "w") as fh:
        json.dump(data, fh)
    print(f"\nroads: {sum(len(v) for v in data['roads'].values())} segments; "
          f"empty: {[k for k, v in data['roads'].items() if not v]}")
    for kind in ("mrt", "school", "park"):
        print(f"\nnearest {kind} (straight-line from the pin):")
        for n, a, b, t in sorted(data["pois"][kind], key=lambda x: dist(x[1], x[2]))[:8]:
            print(f"   {int(dist(a, b)):5d} m  {n}  ({t})  {a:.7f}, {b:.7f}")
    print(f"\nwrote {OUT} — copy the real, near POIs into project.POIS")


if __name__ == "__main__":
    main()
