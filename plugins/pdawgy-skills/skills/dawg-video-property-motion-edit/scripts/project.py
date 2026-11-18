import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
WORK = os.path.join(ROOT, "work")
NAME = os.path.basename(ROOT)
RAW = os.path.join(ROOT, "..", "..", "raw", NAME)
PROXY = os.path.join(WORK, "proxy")
PROXY_BROLL = os.path.join(WORK, "proxy4")
FPS = 30
SPEED = float(os.environ.get("SPEED", "0.8"))
PROXY_PLAY = PROXY if SPEED == 1 else os.path.join(WORK, f"proxy_x{round(SPEED * 100)}")

AGENT_NAME = os.environ.get("AGENT_NAME", "Ivan Heng")
AGENT_PHONE = os.environ.get("AGENT_PHONE", "+65 9201 2029")
AGENT_CEA = os.environ.get("AGENT_CEA", "R074539F")
AGENCY = os.environ.get("AGENCY", "PropNex Realty Pte Ltd")
AGENCY_LICENCE = os.environ.get("AGENCY_LICENCE", "L3008022J")

PROJECT_NAME = "Amberwood"
HIDE_PROJECT_NAME = True
CTA_TEXT = "Text me for the project name" if HIDE_PROJECT_NAME else "Book a private viewing"
MAP_PIN_LABEL = "New launch" if HIDE_PROJECT_NAME else PROJECT_NAME
MAP_PIN_SUB = "Holland Link"
COMPARABLE = os.environ.get("COMPARABLE", "Thomson Reserve")

TAKES = {
    "20261116151818": 3.8,
    "20261116151450": 4.6,
    "20261116151903": 2.56,
    "20261116152344": 8.633,
    "20261116153111": 4.333,
    "20261116153824": 7.8,
}

SKIP_CLIPS = {"20261116151903"}
CAPTION_FIXES = {
    "Thompson Resort": COMPARABLE,
    "top school": "top schools",
    "Development comes": "The development comes",
    "5 bedrooms": "5-bedrooms",
}
WORD_FIXES = {
    "20261116153111": {0: "At", 1: "such a", 2: "price,"},
}
CHUNKS = {
    "20261116151450": [5, 4, 3, 3, 4],
    "20261116151818": [3, 4, 3, 4],
    "20261116152344": [3, 2, 3, 2, 4, 2, 4, 2, 2],
    "20261116153111": [3, 4, 2, 3, 4],
    "20261116153824": [3, 2, 3, 4, 2, 3, 4, 4],
}
KEYWORDS = ["such a price", "958", "square feet", "flexi", "bomb shelter", "value buy",
            "core central region", "$3.5 million", "CCR", "$2.54 million", "top schools", "MRT",
            "full-fledged facilities", "3,", "4,", "5", "contact me"]
WHISPER_PROMPT = ("Singapore condo showflat tour. 3-bedders, flexi room, bomb shelter, value buy, "
                  "core central region, CCR, MRT, top schools, full-fledged facilities, square feet, "
                  "million dollars.")

SITE = (1.3279031, 103.7876972)
MAP_SITE_QUERY = "Amberwood, Singapore"
MAP_ROADS = ["Holland Road", "Bukit Timah Road", "Dunearn Road", "Farrer Road", "Pan-Island Expressway",
             "Holland Link", "Holland Plain", "Holland Grove Road", "Holland Grove Drive",
             "Holland Grove Terrace", "Holland Grove View", "Holland Green", "Holland Hill", "Holland Close",
             "Holland Avenue", "Sixth Avenue", "Fifth Avenue", "Fourth Avenue", "Third Avenue",
             "Second Avenue", "First Avenue", "Queensway", "Adam Road", "Ewart Park",
             "Jalan Kampong Chantek", "Victoria Park Road", "Coronation Road", "Coronation Road West",
             "Duchess Road", "Duchess Avenue", "Taman Warna", "Blackmore Drive", "King Albert Park",
             "Clementi Road", "Toh Tuck Road", "Jalan Jurong Kechil", "Binjai Park", "Maple Avenue",
             "Ford Avenue", "Jalan Haji Alias", "Ulu Pandan Road", "Namly Avenue", "Namly Place",
             "Greenleaf Avenue", "Greenwood Avenue", "Hillcrest Road", "Mount Sinai Road", "Leedon Road",
             "Leedon Heights", "Jalan Kebaya", "Cluny Park Road", "Swiss Club Road", "Eng Neo Avenue",
             "Shelford Road", "Watten Estate Road", "Jalan Jelita", "Holland Village Way", "Lorong Liput",
             "Ghim Moh Road", "Bukit Tinggi Road", "Lasia Avenue", "Belmont Road", "Gallop Road",
             "Woollerton Park", "Sian Tuan Avenue"]
MAJOR_ROADS = {"Pan-Island Expressway", "Bukit Timah Road", "Dunearn Road", "Farrer Road", "Holland Road",
               "Adam Road", "Queensway", "Sixth Avenue"}
POIS = {
    "mrt": [("King Albert Park MRT", 1.3339975, 103.7823196),
            ("Sixth Avenue MRT", 1.3308546, 103.7973004)],
    "school": [("Methodist Girls' School", None, None),
               ("Henry Park Primary School", None, None)],
}
MRT_STATION_QUERIES = ["King Albert Park", "Sixth Avenue station", "Beauty World", "Holland Village station",
                       "Farrer Road station", "Tan Kah Kee"]

FLOOR_PLANS = [
    ("WhatsApp Image 2026-11-18 at 11.41.51.jpeg", "485x450+912+203", "3 Bed", "872 sqft"),
    ("WhatsApp Image 2026-11-18 at 11.41.52.jpeg", "490x515+892+92", "4 Bed", "1,076 sqft"),
    ("WhatsApp Image 2026-11-18 at 11.41.52 (1).jpeg", "645x450+838+112", "5 Bed Premium", "1,324 sqft"),
]

BG = "#0D0B09"
AMBER = "#E8A85C"
FONT_BOLD = "/usr/share/fonts/noto/NotoSans-Bold.ttf"
FONT_MED = "/usr/share/fonts/noto/NotoSans-Medium.ttf"
OUT = os.path.join(ROOT, f"{NAME}-property-motion.mp4")
