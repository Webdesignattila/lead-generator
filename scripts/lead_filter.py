"""
lead_filter.py: Grote Ketens & Rommel-Filter voor Webdesign Attila.

Blokkeert leads die nooit klant worden:
  * grote autodealers, dealergroepen en importeurs (Toyota, Louwman, Pon, Stern, ...)
  * landelijke ketens (KwikFit, Profile Tyrecenter, Albert Heijn, ...)
  * gemeenten en overheid, stichtingen en verenigingen
  * rommel: pagina's met "Contactinformatie", lege of generieke namen, nep-e-mails

Gebruik als module (in echte_scraper.py / mijnhost_jager.py):
    from lead_filter import is_geblokkeerd, reden_blokkade, rij_geblokkeerd
    if is_geblokkeerd(naam=naam, website=url, email=mail): continue

Of automatisch voor alle csv-schrijfacties (wordt toegevoegd door koppel_lead_filter.py):
    import lead_filter; lead_filter.activeer_csv_bewaker()

Gebruik vanaf de command line:
    python scripts/lead_filter.py schoon echte_leads.csv
    python scripts/lead_filter.py test "Toyota Louwman Den Haag" --website https://www.louwman.nl
"""

from __future__ import annotations

import argparse
import csv
import io
import os
import re
import shutil
import sys
import unicodedata
from datetime import datetime
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Blokkeerlijsten. Alles in kleine letters, zonder accenten.
# Elke term wordt als heel woord gezocht ("pon" blokkeert niet "ponyclub").
# ---------------------------------------------------------------------------

AUTO_MERKEN = [
    "toyota", "lexus", "volkswagen", "vw", "audi", "seat", "cupra", "skoda", "porsche",
    "bmw", "mercedes", "mercedes-benz", "ford", "opel", "peugeot",
    "citroen", "ds automobiles", "renault", "dacia", "nissan", "kia", "hyundai", "mazda",
    "honda", "suzuki", "mitsubishi", "subaru", "volvo", "polestar", "fiat", "alfa romeo",
    "jeep", "lancia", "abarth", "tesla", "jaguar", "land rover", "range rover", "byd",
    "mg motor", "lynk & co", "lynk co", "leapmotor", "xpeng", "nio",
]

# Dealergroepen, importeurs en landelijke auto-/bandenketens.
AUTO_GROEPEN = [
    "louwman", "pon", "pon automotive", "stern", "stern groep", "hedin", "hedin automotive",
    "van mossel", "broekhuis", "bochane", "wittebrug", "hessing", "munsterhuis", "kroymans",
    "ardea", "dealergroep", "autogroep", "importeur", "kwikfit", "kwik-fit", "kwik fit",
    "profile tyrecenter", "profile car", "profile car & tyreservice", "euromaster",
    "carglass", "halfords", "autotaalglas", "point s", "first stop",
    "anwb",
]

# Landelijke ketens buiten de autobranche.
LANDELIJKE_KETENS = [
    "albert heijn", "jumbo", "lidl", "aldi", "plus supermarkt", "dirk van den broek",
    "coop supermarkt", "hema", "action nederland", "kruidvat", "etos", "trekpleister",
    "gamma", "praxis", "karwei", "hornbach", "intratuin", "welkoop", "pets place",
    "mediamarkt", "media markt", "coolblue", "bol.com", "blokker", "xenos", "zeeman",
    "primark", "ikea", "leen bakker", "kwantum", "jysk", "decathlon", "intersport",
    "rabobank", "ing bank", "abn amro", "sns bank", "asn bank", "kpn", "vodafone",
    "ziggo", "odido", "t-mobile", "tele2", "shell", "esso", "texaco", "tango",
    "tinq", "totalenergies", "postnl", "dhl", "dpd", "ns stations", "hertz", "europcar", "sixt",
    "avis", "mcdonald's", "mcdonalds", "burger king", "kfc", "domino's", "dominos",
    "new york pizza", "subway", "starbucks", "van der valk", "fletcher", "bilderberg",
    "specsavers", "pearle", "hans anders", "makro", "sligro", "hanos", "basic-fit",
    "basic fit", "sportcity", "anytime fitness", "randstad", "tempo-team", "adecco",
    "remax", "re/max", "era makelaars", "hypotheker", "de hypotheker", "makelaarsland",
]

OVERHEID = [
    "gemeente", "provincie", "waterschap", "hoogheemraadschap", "rijkswaterstaat",
    "rijksoverheid", "overheid", "ministerie", "politie", "brandweer", "ggd",
    "omgevingsdienst", "veiligheidsregio", "belastingdienst", "uwv",
    "kadaster", "rechtbank",
]

NON_PROFIT = [
    "stichting", "vereniging", "ver.", "coöperatie", "cooperatie", "kerk", "parochie",
    "moskee", "sportvereniging", "voetbalvereniging", "fanfare", "scouting",
]

# Rommel: scraperesultaten die geen bedrijf zijn.
# ROMMEL_OVERAL wordt in de naam én in alle andere kolommen gezocht,
# ROMMEL_NAAM alleen in de naam (een "404" of "in aanbouw" in een statuskolom is juist een goede lead).
ROMMEL_OVERAL = ["contactinformatie", "contact informatie", "contact-informatie"]
ROMMEL_NAAM = [
    "contactgegevens", "pagina niet gevonden", "page not found", "404", "403 forbidden",
    "access denied", "cookiebeleid", "cookie instellingen", "privacyverklaring",
    "privacy policy", "algemene voorwaarden", "just a moment", "attention required",
    "index of", "error",
]
ROMMEL_EXACT = {
    "", "contact", "home", "homepage", "welkom", "start", "over ons", "nieuws", "menu",
    "untitled", "naamloos", "n/a", "na", "none", "null", "-", "onbekend", "test",
}

# Domeinen die altijd geblokkeerd worden (ook subdomeinen).
DOMEIN_BLOK = [
    "overheid.nl", "rijksoverheid.nl", "politie.nl", "louwman.nl", "pon.com", "pon.nl",
    "sterngroep.nl", "stern.nl", "kwik-fit.nl", "kwikfit.nl", "profile.nl",
    "profiletyrecenter.nl", "euromaster.nl", "carglass.nl", "toyota.nl", "volkswagen.nl",
    "bmw.nl", "mercedes-benz.nl", "ford.nl", "opel.nl", "peugeot.nl", "renault.nl",
    "kia.com", "hyundai.nl", "nissan.nl", "hedin.nl", "vanmossel.nl", "broekhuis.nl",
    # Let op: facebook.com/instagram.com staan hier bewust NIET in: een bedrijf met alleen een
    # Facebookpagina als "website" is juist een goede webdesign-lead.
]
DOMEIN_PATRONEN = [
    re.compile(r"(^|\.)gemeente[a-z0-9-]*\.nl$"),
    re.compile(r"(^|\.)[a-z0-9-]*\.gemeente\.nl$"),
    re.compile(r"(^|\.)provincie[a-z0-9-]*\.nl$"),
    re.compile(r"(^|\.)waterschap[a-z0-9-]*\.nl$"),
    re.compile(r"(^|\.)stichting[a-z0-9-]*\.nl$"),
]

EMAIL_ROMMEL = [
    re.compile(r"\.(png|jpe?g|gif|webp|svg)$"),
    re.compile(r"@(example|domain|email|test|sentry|wixpress|sentry-next)\."),
    re.compile(r"^(noreply|no-reply|donotreply|do-not-reply|mailer-daemon|postmaster|abuse)@"),
    re.compile(r"@.*\.(gemeente|overheid)\.nl$|@gemeente[a-z0-9-]*\.nl$|@overheid\.nl$"),
]

# Kolomnamen die als naam / website / e-mail worden herkend (kleine letters).
NAAM_KOLOMMEN = ("bedrijfsnaam", "bedrijf", "naam", "name", "company", "titel", "title", "business")
WEBSITE_KOLOMMEN = ("website", "url", "site", "domein", "domain", "web", "link")
EMAIL_KOLOMMEN = ("email", "e-mail", "mail", "emailadres", "e-mailadres")


def _normaal(tekst: object) -> str:
    """Kleine letters, accenten weg, witruimte samengevoegd."""
    t = "" if tekst is None else str(tekst)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t.lower()).strip()


def _woord_regex(termen: list[str]) -> re.Pattern:
    delen = sorted({re.escape(_normaal(t)) for t in termen}, key=len, reverse=True)
    return re.compile(r"(?<![a-z0-9])(" + "|".join(delen) + r")(?![a-z0-9])")


_RX = {
    "autodealer/merk": _woord_regex(AUTO_MERKEN),
    "dealergroep/keten (auto)": _woord_regex(AUTO_GROEPEN),
    "landelijke keten": _woord_regex(LANDELIJKE_KETENS),
    "overheid/gemeente": _woord_regex(OVERHEID),
    "stichting/vereniging": _woord_regex(NON_PROFIT),
}
_RX_ROMMEL_OVERAL = _woord_regex(ROMMEL_OVERAL)
_RX_ROMMEL_NAAM = _woord_regex(ROMMEL_OVERAL + ROMMEL_NAAM)


def domein_van(website: object) -> str:
    """'https://www.Garage-Jansen.nl/contact' -> 'garage-jansen.nl'."""
    w = _normaal(website)
    if not w:
        return ""
    if "@" in w and "/" not in w:
        w = w.split("@", 1)[1]
    if "://" not in w:
        w = "http://" + w
    try:
        host = urlparse(w).hostname or ""
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def _domein_reden(domein: str) -> str | None:
    if not domein:
        return None
    for d in DOMEIN_BLOK:
        if domein == d or domein.endswith("." + d):
            return f"geblokkeerd domein ({d})"
    for p in DOMEIN_PATRONEN:
        if p.search(domein):
            return f"overheid/stichting-domein ({domein})"
    # Merk- of groepsnaam als los deel van het domein: toyota-vandermeer.nl, louwman-dealer.nl
    delen = " ".join(re.split(r"[.\-_]", domein.rsplit(".", 1)[0]))
    for label in ("autodealer/merk", "dealergroep/keten (auto)", "landelijke keten"):
        m = _RX[label].search(delen)
        if m:
            return f"{label} in domein ({m.group(1)})"
    return None


def reden_blokkade(naam: object = "", website: object = "", email: object = "",
                   tekst: object = "") -> str | None:
    """Geeft de reden waarom een lead geblokkeerd wordt, of None als hij door mag."""
    n = _normaal(naam)
    t = _normaal(tekst)

    if n and n in ROMMEL_EXACT:
        return f"rommel: generieke naam ('{n}')"
    m = _RX_ROMMEL_NAAM.search(n) if n else None
    if not m and t:
        m = _RX_ROMMEL_OVERAL.search(t)
    if m:
        return f"rommel: '{m.group(1)}'"

    for label, rx in _RX.items():
        m = rx.search(n)
        if m:
            return f"{label} ({m.group(1)})"

    r = _domein_reden(domein_van(website))
    if r:
        return r

    e = _normaal(email)
    if e:
        for p in EMAIL_ROMMEL:
            if p.search(e):
                return f"rommel/overheid e-mail ({e})"
        r = _domein_reden(domein_van(e))
        if r:
            return r.replace("domein", "e-maildomein", 1)
    return None


def is_geblokkeerd(naam: object = "", website: object = "", email: object = "",
                   tekst: object = "") -> bool:
    return reden_blokkade(naam, website, email, tekst) is not None


def _kies(rij: dict, kandidaten: tuple[str, ...]) -> str:
    sleutels = {str(k).strip().lower(): k for k in rij.keys() if k is not None}
    for k in kandidaten:
        if k in sleutels and rij[sleutels[k]] not in (None, ""):
            return str(rij[sleutels[k]])
    for k_norm, k in sleutels.items():  # deelmatch: "bedrijfsnaam_google", "website_url"
        if any(c in k_norm for c in kandidaten) and rij[k] not in (None, ""):
            return str(rij[k])
    return ""


def rij_geblokkeerd(rij: dict) -> str | None:
    """Controleert een csv-rij (dict). Herkent zelf de kolommen naam/website/e-mail."""
    naam = _kies(rij, NAAM_KOLOMMEN)
    website = _kies(rij, WEBSITE_KOLOMMEN)
    email = _kies(rij, EMAIL_KOLOMMEN)
    overig = " | ".join(str(v) for k, v in rij.items()
                        if v not in (None, "") and str(v) not in (naam, website, email))
    if not (naam or website or email or overig.strip()):
        return "rommel: lege rij"
    # Een rij zonder naamkolom: de naamcheck op de eerste tekstwaarde doen.
    if not naam:
        naam = next((str(v) for v in rij.values() if v and not str(v).startswith("http")), "")
    return reden_blokkade(naam=naam, website=website, email=email, tekst=overig)


# ---------------------------------------------------------------------------
# CSV opschonen
# ---------------------------------------------------------------------------

def _lees_csv(pad: str) -> tuple[list[str], list[dict], str, str]:
    ruw = open(pad, "rb").read()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            tekst = ruw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    try:
        dialect = csv.Sniffer().sniff(tekst[:20000], delimiters=",;\t|")
        scheiding = dialect.delimiter
    except csv.Error:
        scheiding = ";" if tekst.split("\n", 1)[0].count(";") > tekst.split("\n", 1)[0].count(",") else ","
    lezer = csv.DictReader(io.StringIO(tekst, newline=""), delimiter=scheiding)
    rijen = list(lezer)
    return list(lezer.fieldnames or []), rijen, scheiding, enc


def _schrijf_csv(pad: str, kolommen: list[str], rijen: list[dict], scheiding: str,
                 enc: str, extra_kolom: str | None = None) -> None:
    velden = kolommen + ([extra_kolom] if extra_kolom else [])
    tmp = pad + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8-sig" if enc.startswith("utf") else enc) as f:
        w = csv.DictWriter(f, fieldnames=velden, delimiter=scheiding, extrasaction="ignore")
        w.writeheader()
        w.writerows(rijen)
    os.replace(tmp, pad)


def schoon_csv(pad: str = "echte_leads.csv", backup_pad: str | None = None,
               dedup: bool = True, voortgang=None) -> dict:
    """Maakt eerst een backup, verwijdert dan geblokkeerde rijen en dubbelen.

    Geblokkeerde rijen gaan met hun reden naar <naam>_verwijderd.csv, zodat niets verloren gaat.
    De eerste keer heet de backup <naam>_backup.csv; die wordt nooit overschreven
    (latere backups krijgen een tijdstempel).
    """
    if not os.path.isfile(pad):
        raise FileNotFoundError(f"Bestand niet gevonden: {pad}")
    basis, ext = os.path.splitext(pad)
    if backup_pad is None:
        backup_pad = f"{basis}_backup{ext}"
        if os.path.exists(backup_pad):
            backup_pad = f"{basis}_backup_{datetime.now():%Y%m%d_%H%M%S}{ext}"
    shutil.copy2(pad, backup_pad)

    kolommen, rijen, scheiding, enc = _lees_csv(pad)
    houden, weg, redenen = [], [], {}
    gezien: set[str] = set()
    for i, rij in enumerate(rijen, 1):
        reden = rij_geblokkeerd(rij)
        if not reden and dedup:
            sleutel = (_normaal(_kies(rij, EMAIL_KOLOMMEN))
                       or domein_van(_kies(rij, WEBSITE_KOLOMMEN))
                       or _normaal(_kies(rij, NAAM_KOLOMMEN)))
            if sleutel:
                if sleutel in gezien:
                    reden = "dubbel"
                gezien.add(sleutel)
        if reden:
            rij = dict(rij)
            rij["reden_verwijderd"] = reden
            weg.append(rij)
            soort = reden.split(" (")[0].split(":")[0]
            redenen[soort] = redenen.get(soort, 0) + 1
        else:
            houden.append(rij)
        if voortgang and (i % 50 == 0 or i == len(rijen)):
            voortgang(i, len(rijen))

    _schrijf_csv(pad, kolommen, houden, scheiding, enc)
    verwijderd_pad = f"{basis}_verwijderd{ext}"
    if weg:
        if os.path.exists(verwijderd_pad):  # aanvullen, niet overschrijven
            k2, oud, _, _ = _lees_csv(verwijderd_pad)
            weg = oud + weg
        _schrijf_csv(verwijderd_pad, kolommen, weg, scheiding, enc, extra_kolom="reden_verwijderd")

    return {
        "bestand": pad, "backup": backup_pad, "verwijderd_bestand": verwijderd_pad if weg else None,
        "totaal": len(rijen), "behouden": len(houden), "verwijderd": len(rijen) - len(houden),
        "redenen": redenen,
    }


# ---------------------------------------------------------------------------
# CSV-bewaker: filtert automatisch alles wat scrapers naar *leads*.csv schrijven
# ---------------------------------------------------------------------------

_BEWAKER_ACTIEF = False
GEBLOKKEERD_TELLER = {"aantal": 0}


def _is_leadbestand(f, patroon: re.Pattern) -> bool:
    naam = getattr(f, "name", "")
    return isinstance(naam, str) and bool(patroon.search(os.path.basename(naam).lower()))


def activeer_csv_bewaker(patroon: str = r"leads.*\.csv$", stil: bool = False) -> None:
    """Patcht csv.writer, csv.DictWriter en (indien aanwezig) pandas.DataFrame.to_csv zodat
    geblokkeerde leads nooit in een leadbestand (standaard: naam bevat 'leads', eindigt op .csv)
    terechtkomen. Veilig om meerdere keren aan te roepen."""
    global _BEWAKER_ACTIEF
    if _BEWAKER_ACTIEF:
        return
    _BEWAKER_ACTIEF = True
    rx = re.compile(patroon)
    orig_writer = csv.writer
    orig_dictwriter = csv.DictWriter

    def meld(reden, waarde):
        GEBLOKKEERD_TELLER["aantal"] += 1
        if not stil:
            print(f"[lead_filter] overgeslagen: {str(waarde)[:70]}  →  {reden}")

    class _BewaakteWriter:
        def __init__(self, f, *a, **kw):
            self._w = orig_writer(f, *a, **kw)
            self._kop: list[str] | None = None

        def writerow(self, rij):
            rij_l = list(rij)
            if self._kop is None:
                laag = [str(c).strip().lower() for c in rij_l]
                if any(any(k in c for k in NAAM_KOLOMMEN + WEBSITE_KOLOMMEN + EMAIL_KOLOMMEN)
                       for c in laag):
                    self._kop = [str(c) for c in rij_l]
                    return self._w.writerow(rij_l)
                self._kop = []
            if self._kop:
                reden = rij_geblokkeerd(dict(zip(self._kop, rij_l)))
            else:
                reden = rij_geblokkeerd({f"kolom{i}": v for i, v in enumerate(rij_l)})
            if reden:
                meld(reden, rij_l[:2])
                return 0
            return self._w.writerow(rij_l)

        def writerows(self, rijen):
            for r in rijen:
                self.writerow(r)

        def __getattr__(self, item):
            return getattr(self._w, item)

    def bewaakte_writer(f, *a, **kw):
        if _is_leadbestand(f, rx):
            return _BewaakteWriter(f, *a, **kw)
        return orig_writer(f, *a, **kw)

    class BewaakteDictWriter(orig_dictwriter):
        def __init__(self, f, fieldnames, restval="", extrasaction="raise",
                     dialect="excel", *a, **kw):
            super().__init__(f, fieldnames, restval, extrasaction, dialect, *a, **kw)
            # De interne writer moet de originele zijn, anders wordt elke rij dubbel gecontroleerd.
            self.writer = orig_writer(f, dialect, *a, **kw)
            self._bewaakt = _is_leadbestand(f, rx)

        def writerow(self, rowdict):
            if self._bewaakt:
                reden = rij_geblokkeerd(rowdict)
                if reden:
                    meld(reden, list(rowdict.values())[:2])
                    return 0
            return super().writerow(rowdict)

        def writerows(self, rowdicts):
            for r in rowdicts:
                self.writerow(r)

    csv.writer = bewaakte_writer
    csv.DictWriter = BewaakteDictWriter

    if "pandas" in sys.modules:
        _patch_pandas(rx, meld)
    else:  # pandas pas patchen als het script het importeert
        import builtins
        orig_import = builtins.__import__

        def import_haak(name, *a, **kw):
            mod = orig_import(name, *a, **kw)
            if name.split(".")[0] == "pandas" and "pandas" in sys.modules \
                    and not getattr(sys.modules["pandas"], "_lead_filter_gepatcht", False):
                try:
                    _patch_pandas(rx, meld)
                except Exception:
                    pass
            return mod

        builtins.__import__ = import_haak


def _patch_pandas(rx: re.Pattern, meld) -> None:
    pd = sys.modules.get("pandas")
    if pd is None or getattr(pd, "_lead_filter_gepatcht", False) or not hasattr(pd, "DataFrame"):
        return
    pd._lead_filter_gepatcht = True
    orig_to_csv = pd.DataFrame.to_csv

    def to_csv(self, path_or_buf=None, *a, **kw):
        naam = path_or_buf if isinstance(path_or_buf, str) else getattr(path_or_buf, "name", "")
        if isinstance(naam, (str, os.PathLike)) and rx.search(os.path.basename(str(naam)).lower()):
            houden = []
            for _, r in self.iterrows():
                reden = rij_geblokkeerd({str(k): ("" if v is None else v) for k, v in r.items()})
                if reden:
                    meld(reden, list(r.values)[:2])
                houden.append(reden is None)
            self = self[houden]
        return orig_to_csv(self, path_or_buf, *a, **kw)

    pd.DataFrame.to_csv = to_csv


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Grote Ketens & Rommel-Filter")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("schoon", help="CSV opschonen (met backup)")
    s.add_argument("csv", nargs="?", default="echte_leads.csv")
    s.add_argument("--backup", default=None)
    s.add_argument("--geen-dedup", action="store_true")
    t = sub.add_parser("test", help="Eén lead testen")
    t.add_argument("naam")
    t.add_argument("--website", default="")
    t.add_argument("--email", default="")
    a = p.parse_args(argv)

    if a.cmd == "schoon":
        r = schoon_csv(a.csv, a.backup, dedup=not a.geen_dedup)
        print(f"Backup:      {r['backup']}")
        print(f"Totaal:      {r['totaal']}")
        print(f"Behouden:    {r['behouden']}")
        print(f"Verwijderd:  {r['verwijderd']}" +
              (f"  (zie {r['verwijderd_bestand']})" if r["verwijderd_bestand"] else ""))
        for k, v in sorted(r["redenen"].items(), key=lambda x: -x[1]):
            print(f"  - {k}: {v}")
        return 0
    reden = reden_blokkade(a.naam, a.website, a.email)
    print(f"GEBLOKKEERD: {reden}" if reden else "OK: lead mag door")
    return 1 if reden else 0


if __name__ == "__main__":
    sys.exit(main())
