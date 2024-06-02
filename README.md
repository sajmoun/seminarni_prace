# Knižní databáze

Jednoduchá webová aplikace pro správu osobní knižní databáze. Uživatelé se mohou registrovat, přihlašovat, přidávat knihy, filtrovat knihy podle autora a spravovat svůj účet.

## Popis projektu

Tato aplikace umožňuje:
- Registraci a přihlášení uživatelů
- Přidávání knih do databáze
- Filtrování knih podle autora
- Zobrazení detailů knihy
- Smazání knihy
- Odhlášení uživatele
- Smazání účtu

## Požadavky

- Python 3.8 nebo vyšší
- FastAPI
- Uvicorn
- Jinja2
- SQLite

## Instalace

1. Klonujte tento repozitář do svého lokálního zařízení:
    ```bash
    git clone https://github.com/vase-repozitar/knizni-databaze.git
    cd knizni-databaze
    ```

2. Vytvořte a aktivujte virtuální prostředí:
    ```bash
    python3 -m venv env
    source env/bin/activate  # Na Windows použijte `env\Scripts\activate`
    ```

3. Nainstalujte požadované balíčky:
    ```bash
    pip install fastapi uvicorn jinja2 atd
    ```

## Spuštění

1. Ujistěte se, že jste ve virtuálním prostředí:
    ```bash
    source env/bin/activate  # Na Windows použijte `env\Scripts\activate`
    ```

2. Spusťte aplikaci pomocí Uvicorn:
    ```bash
    uvicorn main:app --reload
    ```

3. Otevřete webový prohlížeč a přejděte na adresu `http://127.0.0.1:8000`.

## Použití

1. Na úvodní stránce se můžete registrovat nebo přihlásit.
2. Po přihlášení budete přesměrováni na stránku pro správu vašich knih.
3. Můžete přidat novou knihu, filtrovat knihy podle autora, zobrazit detaily knihy, smazat knihu nebo svůj účet.


