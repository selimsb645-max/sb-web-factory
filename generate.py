#!/usr/bin/env python3
"""SB AI Studio — Website Factory.
Reads specs/*.json, renders a complete premium website per spec into sites/<slug>/index.html
Deterministic, dependency-free, runs locally (Solas pushes rendered output).
Usage: python3 generate.py [specs_dir] [out_dir]"""
import json, os, re, sys, html

SPEC_DIR = sys.argv[1] if len(sys.argv) > 1 else "specs"
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else "sites"

def esc(s):
    return html.escape(str(s), quote=True)

def hours_table(hours):
    if not hours:
        return ""
    rows = "".join(f"<tr><td>{esc(d)}</td><td>{esc(h)}</td></tr>" for d, h in hours)
    return f'<table class="hours">{rows}</table>'

def menu_or_services(spec):
    items = spec.get("sections", {}).get("items", [])
    if not items:
        return ""
    label = "Menu" if spec.get("kind", "services") == "restaurant" else "Our Services"
    cards = "".join(
        f'<div class="item"><div class="ic">{esc(i.get("icon","•"))}</div>'
        f'<h3>{esc(i["name"])}</h3><p>{esc(i.get("desc",""))}</p>'
        f'<div class="price">{esc(i.get("price",""))}</div></div>'
        for i in items)
    return f'<section id="items"><div class="wrap"><div class="stitle">{label}</div><div class="grid">{cards}</div></section>'

def gallery(spec):
    shots = spec.get("sections", {}).get("gallery", [])
    if not shots:
        return ""
    tiles = "".join(f'<div class="shot">{esc(s)}</div>' for s in shots)
    return f'<section id="gallery"><div class="wrap"><div class="stitle">Gallery</div><div class="gallery">{tiles}</div></section>'

def booking_form(spec):
    bk = spec.get("sections", {}).get("booking", {})
    if not bk.get("enabled"):
        return ""
    kind = bk.get("type", "appointment")
    if kind == "order":
        title, action = "Order Online", "Place Order"
        field = '<label>What would you like?</label><textarea name="order" rows="3" required placeholder="e.g. 2 croissants, 1 birthday cake..."></textarea>'
    else:
        title, action = "Book an Appointment", "Request Appointment"
        opts = "".join(f'<option>{esc(s)}</option>' for s in bk.get("options", ["General appointment"]))
        field = f'<label>Service</label><select name="service">{opts}</select>'
    return f'''<section id="booking"><div class="wrap"><div class="stitle">{title}</div>
<div class="bform">
<label>Your name</label><input name="name" required placeholder="Your name">
<label>Phone / Email</label><input name="contact" required placeholder="How do we reach you?">
{field}
<label>Preferred date &amp; time</label><input name="when" placeholder="e.g. Saturday morning">
<button type="button" onclick="sendForm()">{action}</button>
<p class="note">We confirm every request personally — usually within a few hours.</p>
</div></section>'''

def render(spec):
    b = spec["business"]
    sec = spec.get("sections", {})
    t = spec.get("theme", {})
    primary = t.get("primary", "#8b7cff")
    accent = t.get("accent", "#2dd4bf")
    base = t.get("base", "dark")
    bg = "#0b0d17" if base == "dark" else "#faf7f2"
    fg = "#eef1fa" if base == "dark" else "#1c1a17"
    mut = "#9aa3c0" if base == "dark" else "#6b655c"
    card = "rgba(255,255,255,.045)" if base == "dark" else "#ffffff"
    line = "rgba(255,255,255,.1)" if base == "dark" else "rgba(0,0,0,.08)"
    font = t.get("font", "'Inter',system-ui,sans-serif")
    bk = sec.get("booking", {})
    bk_word = "order" if bk.get("type") == "order" else "booking"
    wa_num = re.sub(r'[^0-9]', '', bk.get("notify_whatsapp", "")) or "0000000000"
    nav_links = [("Home","top"),("About","about")]
    if sec.get("items"): nav_links.append(("Menu" if spec.get("kind")=="restaurant" else "Services","items"))
    if sec.get("gallery"): nav_links.append(("Gallery","gallery"))
    if bk.get("enabled"): nav_links.append(("Book","booking"))
    nav_links.append(("Contact","contact"))
    nav = "".join(f'<a href="#{h[1]}">{h[0]}</a>' for h in nav_links)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(b["name"])} — {esc(b.get("tagline",""))}</title>
<meta name="description" content="{esc(spec.get("seo",{}).get("description", b.get("tagline","")))}">
<meta name="keywords" content="{esc(", ".join(spec.get("seo",{}).get("keywords",[])))}">
<style>
:root{{--primary:{primary};--accent:{accent};--bg:{bg};--fg:{fg};--mut:{mut};--card:{card};--line:{line}}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:{font};background:var(--bg);color:var(--fg);line-height:1.65}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 22px}}
nav{{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 85%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}}
.nav-in{{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;max-width:1100px;margin:0 auto;flex-wrap:wrap;gap:8px}}
.brand{{font-weight:800;font-size:1.15rem;background:linear-gradient(135deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;color:transparent}}
.nav-in div a{{color:var(--mut);text-decoration:none;margin-left:18px;font-size:.93rem}}
.nav-in div a:hover{{color:var(--fg)}}
header{{padding:110px 0 90px;text-align:center;background:radial-gradient(ellipse 60% 55% at 50% -10%,color-mix(in srgb,var(--primary) 24%,transparent),transparent)}}
h1{{font-size:clamp(2.1rem,5vw,3.4rem);line-height:1.15;letter-spacing:-.02em}}
h1 span{{background:linear-gradient(135deg,var(--primary),var(--accent));-webkit-background-clip:text;background-clip:text;color:transparent}}
.sub{{color:var(--mut);max-width:600px;margin:20px auto 34px;font-size:1.1rem}}
.btn{{display:inline-block;padding:14px 30px;border-radius:12px;font-weight:600;text-decoration:none;transition:.25s;cursor:pointer;border:none;font-size:1rem}}
.btn-p{{background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;box-shadow:0 6px 24px color-mix(in srgb,var(--primary) 40%,transparent)}}
.btn-p:hover{{transform:translateY(-3px)}}
.btn-o{{border:1px solid var(--line);color:var(--fg);background:var(--card)}}
.btn-o:hover{{border-color:var(--accent)}}
section{{padding:70px 0}}
.stitle{{text-align:center;font-size:1.9rem;font-weight:800;letter-spacing:-.02em;margin-bottom:40px}}
.about-box{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;align-items:center}}
.about-box p{{color:var(--mut)}}
.about-box .logo-big{{text-align:center;font-size:4rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px}}
.item{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:24px;transition:.25s}}
.item:hover{{transform:translateY(-5px);border-color:var(--primary)}}
.item .ic{{font-size:1.6rem;margin-bottom:8px}}
.item h3{{font-size:1.05rem;margin-bottom:6px}}
.item p{{color:var(--mut);font-size:.9rem}}
.item .price{{color:var(--accent);font-weight:700;margin-top:8px}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}}
.shot{{background:var(--card);border:1px solid var(--line);border-radius:14px;height:130px;display:flex;align-items:center;justify-content:center;font-size:2.4rem}}
.hours{{width:100%;max-width:420px;border-collapse:collapse;margin:14px auto 0}}
.hours td{{padding:9px 14px;border-bottom:1px dashed var(--line);color:var(--mut)}}
.hours td:first-child{{color:var(--fg);font-weight:600}}
.bform{{max-width:480px;margin:0 auto;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:28px}}
.bform label{{display:block;font-weight:600;margin:13px 0 6px;font-size:.9rem}}
.bform input,.bform select,.bform textarea{{width:100%;padding:12px;border:1px solid var(--line);border-radius:9px;background:transparent;color:var(--fg);font-size:.95rem;font-family:inherit}}
.bform button{{width:100%;margin-top:18px}}
.note{{color:var(--mut);font-size:.85rem;text-align:center;margin-top:12px}}
.cgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}}
.ccard{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:26px;text-align:center;text-decoration:none;color:var(--fg)}}
.ccard:hover{{border-color:var(--accent)}}
.ccard p{{color:var(--mut);font-size:.9rem}}
footer{{border-top:1px solid var(--line);padding:30px 0;text-align:center;color:var(--mut);font-size:.85rem}}
@media(max-width:640px){{.nav-in div{{display:none}}}}
</style></head>
<body id="top">
<nav><div class="nav-in"><div class="brand">{esc(b["name"])}</div><div>{nav}</div></div></nav>
<header><div class="wrap">
<h1>{esc(sec.get("hero",{}).get("headline", b.get("tagline","")))}<br><span>{esc(sec.get("hero",{}).get("subline",""))}</span></h1>
<p class="sub">{esc(sec.get("hero",{}).get("text", b.get("about","")))}</p>
<a class="btn btn-p" href="{('#booking' if bk.get('enabled') else '#contact')}">{esc(sec.get("hero",{}).get("cta","Contact Us"))}</a>
<a class="btn btn-o" href="tel:{esc(re.sub(r'[^+0-9]','',b.get("phone","")))}" style="margin-left:10px">Call Now</a>
</div></header>
<section id="about"><div class="wrap"><div class="stitle">About Us</div><div class="about-box">
<div class="logo-big">{esc(sec.get("hero",{}).get("icon","✨"))}</div>
<div><p>{esc(b.get("about",""))}</p>{hours_table(b.get("hours"))}</div>
</div></div></section>
{menu_or_services(spec)}
{gallery(spec)}
{booking_form(spec)}
<section id="contact"><div class="wrap"><div class="stitle">Contact</div><div class="cgrid">
<div class="ccard"><b>📍 Address</b><p>{esc(b.get("address",""))}</p></div>
<div class="ccard"><b>📞 Phone</b><p>{esc(b.get("phone",""))}</p></div>
<div class="ccard"><b>✉️ Email</b><p>{esc(b.get("email",""))}</p></div>
</div></div></section>
<footer><div class="wrap">© {esc(b.get("year","2026"))} {esc(b["name"])} — {esc(b.get("tagline",""))}</div></footer>
<script>
function sendForm(){{
  var f=document.querySelector('.bform');
  var msg='New {bk_word} request for {esc(b["name"])}: '+f.querySelector('[name=name]').value+', '+f.querySelector('[name=contact]').value+', '+f.querySelector('[name=when]').value;
  var ta=f.querySelector('[name=order]')||f.querySelector('[name=service]');
  if(ta)msg+=', details: '+ta.value;
  window.open('https://wa.me/{wa_num}?text='+encodeURIComponent(msg),'_blank');
}}
</script>
</body></html>'''

def validate(spec, out):
    errs = []
    if not spec.get("business", {}).get("name"):
        errs.append("business.name missing")
    if not re.fullmatch(r"[a-z0-9-]+", spec.get("slug", "")):
        errs.append("slug must be lowercase letters/digits/hyphens")
    if "{{" in out:
        errs.append("unrendered template braces left in output")
    if len(out) < 3000:
        errs.append("output suspiciously small")
    return errs

def main():
    built = failed = 0
    os.makedirs(OUT_DIR, exist_ok=True)
    for fn in sorted(os.listdir(SPEC_DIR)):
        if not fn.endswith(".json"):
            continue
        name = fn[:-5]
        try:
            spec = json.load(open(os.path.join(SPEC_DIR, fn)))
            out = render(spec)
            errs = validate(spec, out)
            if errs:
                print(f"QA_FAIL {name}: {errs}"); failed += 1; continue
            d = os.path.join(OUT_DIR, name)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "index.html"), "w").write(out)
            print(f"OK {name} -> {d}/index.html ({len(out)} bytes)")
            built += 1
        except Exception as e:
            print(f"FAIL {name}: {e}"); failed += 1
    print(f"SUMMARY built={built} failed={failed}")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
