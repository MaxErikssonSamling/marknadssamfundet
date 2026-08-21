from pathlib import Path
import json, subprocess, sys, shutil
root=Path(__file__).resolve().parents[1]
content=root/'content'/'articles'
test=content/'2099-01-01-lokalt-test.json'
data={
  "published": True,
  "title": "Lokalt test av publiceringssystemet",
  "publish_date": "2099-01-01",
  "type": "Analys",
  "topic": "Ekonomi",
  "author": "Marknadssamfundet",
  "excerpt": "Denna fil skapas bara under det lokala testet och tas bort direkt efteråt.",
  "hero_image": "/assets/mark-icon.png",
  "hero_alt": "Marknadssamfundets symbol.",
  "tags": ["test"],
  "body": "<p>Detta är en lokal kontroll av byggsystemet.</p><h2>Mellanrubrik</h2><p>Om denna sida byggs fungerar flödet.</p>"
}
try:
    test.write_text(json.dumps(data, ensure_ascii=False, indent=2),encoding='utf-8')
    subprocess.check_call([sys.executable,str(root/'tools'/'build_site.py')])
    expected=root/'_site'/'artikel-lokalt-test.html'
    if not expected.exists():
        raise SystemExit('Testet misslyckades: artikelsidan skapades inte.')
    print('OK: publiceringssystemet byggde en testartikel korrekt.')
finally:
    if test.exists(): test.unlink()
    subprocess.check_call([sys.executable,str(root/'tools'/'build_site.py')])
