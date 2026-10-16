# ESG360 Academy — TikTok Autopilot (pilot)
**Stan:** wdrożenie testowe w gałęzi `automation/esg360-tiktok-autopilot`; strona produkcyjna bez zmian.

System renderuje pionowy film 1080×1920 z pięciu lub siedmiu autorskich plansz tekstowych, wysyła MP4 do Cloudinary i planuje go w Buffer na firmowy TikTok `@esg360.academy`. Dane pochodzą z trzech wcześniej opracowanych tematów ESG360 na LinkedIn (20, 22 i 24 października 2026). Późniejszy automatyczny import nowych postów LinkedIn jeszcze **nie został wdrożony**.

## Jednorazowe ustawienia na GitHub
Otwórz `https://github.com/sylwesterplay-rgb/ESG-w-MSP/settings/secrets/actions` i dodaj dwa **Repository secrets**:
- `BUFFER_API_KEY` — własny Personal Key z ustawień Buffer; nie wklejaj go do rozmowy ani kodu.
- `CLOUDINARY_UPLOAD_PRESET` — tylko nazwa już skonfigurowanego presetu unsigned: `esg360_tiktok` (to nie jest prywatny klucz).

Identyfikatory Buffer kanału i organizacji, cloud name `dvtirowe` oraz nazwy marek są wpisane jawnie w skrypcie (nie są sekretami). Cloudinary używa presetu unsigned, dlatego powinien mieć ograniczenia, aby nie dopuścić do nadużyć.

## Test i włączenie
1. Kod znajduje się na oddzielnej gałęzi. Workflow `.github/workflows/esg360-tiktok-autopilot.yml` działa ręcznie (`workflow_dispatch`) i w harmonogramie **dopiero gdy znajdzie się na gałęzi domyślnej**. <https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows>
2. Po ustawieniu sekretów zaktualizuj/publikuj PR i scal wyłącznie po przeglądzie; następnie otwórz **Actions → ESG360 TikTok Autopilot → Run workflow**.
3. Po starcie szukaj w logu `SCHEDULED_VERIFIED` z ID posta. Niezależnie sprawdź w Buffer kanał TikTok, status scheduled i godzinę 18:00 Europe/Warsaw.
4. Po godzinie publikacji potwierdź status `sent` i widoczność na TikToku. W razie błędów system ma przerwać, nie publikować na innym kanale.
5. Cron 10:20 UTC uruchamia raz dziennie, ze sporym zapasem do 18:00; terminy publikacji rozwiązywane są w strefie Europe/Warsaw także po zmianie czasu.

## Ograniczenia
- Jedynie **3 zdefiniowane odcinki**; nie jest to nieograniczona generacja nowych pomysłów z LinkedIn.
- Film ma plansze i cichą ścieżkę audio, **bez lektora i muzyki komercyjnej**. Wymaga oceny jakości przed szerokim uruchomieniem.
- Weryfikacja schematu API wykonana wobec dostępnego Buffer; pełna integracja Actions–Cloudinary–Buffer nieprzetestowana do czasu dodania sekretów i ręcznego uruchomienia.
- Domyślna blokada: nazwa i ID dokładnie `esg360.academy`; nigdy `bazgranie_noca`. Unikanie duplikatów według opisu i terminu, sprawdzenie kolejki przed publikacją.
- GitHub Actions używa Pythona **na serwerze GitHub, a nie na komputerze użytkownika**.
- Nie dodawaj wideo do publicznego repozytorium; trwały URL dostarcza Cloudinary.
