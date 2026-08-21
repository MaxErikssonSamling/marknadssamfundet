# Marknadssamfundet – v4 + Pages CMS

Detta paket behåller den visuella v4-designen men ersätter exempelmaterialet med ett riktigt, formulärbaserat publiceringsflöde via Pages CMS.

## Vid lansering

`content/articles/` är tom. Därför visar startsidan **Inga publiceringar ännu**. Exempelartiklarna och deras exempelbilder är borttagna.

## När första riktiga texten publiceras

Pages CMS sparar en JSON-fil i `content/articles/` och bilder i `assets/uploads/`. GitHub Actions kör `tools/build_site.py`, som automatiskt:

- skapar artikelsidan,
- gör senaste texten till huvudartikel,
- fyller Senaste,
- fyller arkivet och sökningen,
- fyller Rapporter när rapporter finns,
- fyller Analys & opinion när sådana texter finns,
- använder skribentens huvudbild, inlinebilder, rapportomslag och PDF.

## Första tekniska installationen

1. Ladda upp alla filer till GitHub-lagringsplatsen.
2. Ändra GitHub Pages Source till **GitHub Actions**.
3. Vänta på workflowet **Bygg och publicera Marknadssamfundet**.
4. Självhosta Pages CMS enligt `docs/SELFHOST-PAGES-CMS.md`.
5. Pages CMS hittar `.pages.yml` i lagringsplatsens rot och visar formuläret **Publiceringar**.
