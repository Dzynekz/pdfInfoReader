# Skrypt do Wydobywania Informacji z Plików PDF
Ten skrypt pozwala na wydobycie informacji z plików PDF, których nazwy znajdują się w wybranym pliku CSV.

## Wydobywane Informacje
Skrypt wydobywa następujące informacje z każdego pliku PDF:

- UUID: Nazwa pliku
- LiczbaStron: Liczba stron
- OrientacjaV: Orientacje pliku (pozioma/pionowa)
- CzyFormularz: Czy jest to formularz
- StatusFormularza: Status formularza (zablokowany/otwarty)
- Podpis: czy jest podpis
- TypPodpisu: Typ podpisu (profil zaufany/certyfikowany)
- Błąd: Wystąpił błąd (jeżeli jakiś wystąpi np. jeżeli plik jest chroniony hasłem)

Wydobyte informacje są następnie zapisywane do wybranego pliku CSV.

## Uwagi
Skrypt został przetestowany w różnych scenariuszach, aby zapewnić poprawne działanie.
Istnieje możliwość napotkania nieprzewidzianych sytuacji, które mogą spowodować niepoprawną kategoryzację.

## Użycie
- Przygotuj plik CSV zawierający nazwy plików PDF, które chcesz przetworzyć.
- Na początku kodu podaj ścieżkę do pliku csv, ścieżkę do folderu z plikami pdf i ścieżkę do pliku wynikowego
- Wynikiem będzie plik CSV zawierający wydobyte informacje dla każdego pliku PDF.

### Upewnij się, że zweryfikujesz wyniki, ponieważ skrypt może nie obsługiwać perfekcyjnie niektórych przypadków brzegowych.
