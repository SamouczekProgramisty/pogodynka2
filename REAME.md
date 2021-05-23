# Pogodynka w chmurze

Pogodynka wysyłająca dane do chmury. Uruchamiana jako demon na Raspberry PI. Obsługuje dwa czujniki:

* czujnik temperatury
* czujnik stężenia pyłów PM2.5/PM10

## Środowisko developerskie

Żeby uniknąć kompilowania/instalacji specyficznej wersji Python'a na Rasberry PI użyłem domyślnej wersji, która jest
aktualnie dosępna. W trakcie pracy nad kodem zainstalowałem dokładnie taką samą wersję lokalnie używając narzędzia
pyenv.

    pyenv install 3.7.10
    pip install poetry
    poetry install
    poetry run pre-commit install
    poetry run pytest
