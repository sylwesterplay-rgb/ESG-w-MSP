# ESG360 Academy — system automatyzacji (13.10.2026)

## Cel i granice
- Marka nadrzędna: **ESG360 Academy**. Hasło: **Wiedza. Narzędzia. Wdrożenie.**
- **ESG w MŚP** to nazwa serii publikacji (podręcznik główny, VSME w 30 krokach, przyszłe opracowania EcoVadis).
- Witryna tymczasowa: https://sylwesterplay-rgb.github.io/ESG-w-MSP/ — po migracji domeny wymagane aktualizacje canonical, sitemap, Open Graph, linków LinkedIn oraz przekierowań.
- Strona firmowa LinkedIn: organizacja `145302737`.
- **Nigdy nie mieszać** postów ani grafik ESG360 Academy z marką artystyczną Bazgranie Nocą, mimo że Metricool używa wspólnej marki/obszaru roboczego.

## Komponenty i dostęp
| Komponent | Identyfikator / adres | Rola |
| --- | --- | --- |
| ChatGPT Work | tryb Work, zalogowany LinkedIn po potwierdzeniu użytkownika | przeglądarka do kontroli widoczności i interakcji wymagających UI |
| GitHub | `sylwesterplay-rgb/ESG-w-MSP` | źródło witryny i wersjonowanie |
| GitHub Pages | `https://sylwesterplay-rgb.github.io/ESG-w-MSP/` | tymczasowa witryna |
| LinkedIn | `urn:li:organization:145302737` | oficjalny profil marki |
| Metricool | `blogId=7358175`, `Europe/Warsaw`, `network=linkedin` | planowanie, autopublikacja i kontrola statusu |
| Canva | folder **ESG360 Academy — identyfikacja i publikacje** | katalog grafik w zatwierdzonym brandingu |

## Zasady publikacji
1. Sprawdź kalendarz Metricool na następne 14 dni. Modyfikuj wyłącznie wpisy z `providers[].network=linkedin`, docelowo powiązane z organizacją `145302737`.
2. Każdy post ma mieć aktualną grafikę ESG360 Academy zgodną z tematem, alt text, datę i godzinę w `Europe/Warsaw`, `autoPublish=true`.
3. Aktualizacja istniejącego posta: pobierz **całe** aktualne dane, zachowaj tekst, datę, ustawienia i uuid, modyfikuj jedynie uzgodnione pole. Po aktualizacji ID może ulec zmianie; UUID pozostaje stałe.
4. Sprawdź wynik przez ponowny odczyt listy z Metricool. `PENDING` = zaplanowano, a nie opublikowano. Status publikacji weryfikuj po terminie.
5. Nie uruchamiaj ponownej publikacji / nie twórz duplikatów dla niejednoznacznych błędów.
6. Nie publikuj informacji o cenach i dostępności podręczników ani terminach szkoleń bez ich zatwierdzenia. Nie kopiuj bez weryfikacji zmian regulacyjnych ESG.
7. Zmiany treści, zmiany cen, uruchomienie kampanii reklamowej i publikacje poza ustalonym harmonogramem wymagają akceptacji użytkownika.

## Kontrole operacyjne
- **Codziennie ok. 11:00:** kontrola planu LinkedIn, potwierdzonych statusów i obecności właściwych grafik przez zaplanowane zadanie ChatGPT.
- **Co tydzień:** kontrola dostępności strony, podstawowych linków, spójności nazwy/logo, braków treści, metadanych i przekierowań; zgłoszenie propozycji poprawek. Bez automatycznych zmian na produkcji.
- **Raz w miesiącu:** podsumowanie wyników publikacji i propozycja tematyki na kolejny miesiąc, oddzielając dane potwierdzone od hipotez.

## GitHub — zasada bezpieczeństwa
- Wprowadzaj zmiany na osobnej gałęzi, przez pull request. Nie scalaj do `main` bez zatwierdzenia.
- Przed scaleniem: weryfikacja linków, mobilnego menu, responsywności, dostępności, metadanych SEO i statusu publikacji.
- Nie przechowuj tokenów API, haseł ani danych uwierzytelniania w publicznym repozytorium.
- Wdrożenie formularza zapisu, CRM, automatycznej wysyłki materiałów, płatności lub analityki wymagają odpowiedniej usługi, polityki prywatności i dodatkowej decyzji.

## ChatGPT Work — standardowe polecenie
> Otwórz w przeglądarce Work panel administratora ESG360 Academy na LinkedIn, sprawdź wizualnie logo, baner, opis, przycisk „Odwiedź witrynę” i ostatnie publikacje. Następnie otwórz witrynę GitHub Pages i sprawdź stronę główną oraz menu w wersji desktop i mobile. Przygotuj raport z dowodami i zaleceniami. Nie używaj TinyFish. Nie wprowadzaj zmian i nie publikuj niczego bez mojej akceptacji.

## Stan konfiguracji i ograniczenia
- Metricool: 11 postów LinkedIn 14.10–06.11.2026, grafiki i automatyczna publikacja zapisane.
- Canva: 10 zatwierdzonych grafik zaimportowanych do osobnego folderu. To **nie jest jeszcze Canva Brand Kit**; jego konfiguracja wymaga sprawdzenia możliwości konta.
- ChatGPT Work: użytkownik potwierdził zalogowanie i dostęp do administracji LinkedIn.
- Brak autonomicznej bezobsługowej sesji przeglądarkowej pomiędzy uruchomieniami Work; cykliczne kontrole używają dostępnych integracji i jawnie sygnalizują ograniczenia.
- Komunikaty/automatyzacje mogą wymagać włączenia powiadomień w ustawieniach ChatGPT.
