# Självhostad redaktion med Pages CMS

Den publika webbplatsen och CMS:et är två separata delar:

- `marknadssamfundet.se` = den publika statiska webbplatsen på GitHub Pages.
- `redaktion.marknadssamfundet.se` = en självhostad Pages CMS-instans där skribenter loggar in och redigerar.

Pages CMS använder en GitHub App för inloggning och åtkomst till lagringsplatsen. Vi bygger därför inget eget lösenordssystem i Marknadssamfundets webbplats.

## Vad som redan är färdigt i detta paket

- `.pages.yml` definierar skribentens formulär.
- `content/articles/` är artikelarkivet.
- `assets/uploads/` är bildbiblioteket.
- `assets/documents/` är PDF-biblioteket.
- `tools/build_site.py` bygger den publika webbplatsen.
- `.github/workflows/pages.yml` bygger och publicerar automatiskt efter varje ändring.

## Självhosta Pages CMS

Enligt Pages CMS nuvarande 2.x-dokumentation behöver en produktionsinstallation:

1. En PostgreSQL-databas och en `DATABASE_URL`.
2. `BETTER_AUTH_SECRET` och `CRYPTO_KEY`.
3. En stabil HTTPS-adress, exempelvis `https://redaktion.marknadssamfundet.se`, som används som `BASE_URL`.
4. En GitHub App. Pages CMS har ett installationskommando som skapar appen och fyller i GitHub App-variablerna.
5. Databasmigrering med `npm run db:migrate`.
6. Bygg/start med `npm run build` och `npm run start`.

### Exempel på miljövariabler

Skapa dem i CMS-hostingen – lägg aldrig riktiga hemligheter i denna webbplatslagringsplats:

```env
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=GENERERA_EN_HEMLIGHET
CRYPTO_KEY=GENERERA_EN_HEMLIGHET
BASE_URL=https://redaktion.marknadssamfundet.se
ADMIN_EMAILS=din-adminadress@example.com
```

Pages CMS rekommenderar `openssl rand -base64 32` för de två hemligheterna.

### GitHub App

I Pages CMS-källkoden körs:

```bash
npm run setup:github-app -- --base-url https://redaktion.marknadssamfundet.se --env .env
```

GitHub Appen installeras sedan på kontot/organisationen som äger `marknadssamfundet`-lagringsplatsen. Endast behöriga redaktörer får åtkomst via GitHub.

## Redaktörens arbetsflöde

1. Logga in på `redaktion.marknadssamfundet.se` med GitHub.
2. Öppna **Publiceringar**.
3. Välj **Ny publicering**.
4. Fyll i rubrik, datum, typ, ämne, författare och ingress.
5. Ladda upp huvudbild. För rapport kan även rapportomslag och PDF laddas upp.
6. Skriv texten i den visuella redigeraren och lägg in bilder direkt i texten.
7. Låt **Publicerad** vara av för att spara ett utkast.
8. Slå på **Publicerad** och spara när texten ska gå live.
9. GitHub Actions bygger automatiskt om webbplatsen.

## Viktigt vid första installationen

GitHub Pages måste ändras från **Deploy from a branch** till **GitHub Actions** under:

`Inställningar → Pages → Build and deployment → Source → GitHub Actions`

Det görs en gång.
