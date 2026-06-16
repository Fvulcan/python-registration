
from typing import Tuple
from datetime import date


# ========= Pflichtfunktionen (TODO) =========

def normalize_name(name: str) -> str:
    """Nur Buchstaben + Leerzeichen; jedes Wort groß am Anfang. Ungültig -> ValueError."""
    # TODO: trimmen; prüfen: nur .isalpha() bzw. Leerzeichen; Mehrfach-Leerzeichen auf 1 reduzieren;
    # pro Wort: erstes Zeichen groß, Rest klein.

    try:
        name = name.strip()
        if not name:
            raise ValueError("Name darf nicht leer sein")
        for char in name:
            if not (char.isalpha() or char == ' '):
                raise ValueError("Name darf nur Buchstaben und Leerzeichen enthalten")
        words = ' '.join(name.split())
        return ' '.join(word[0].upper() + word[1:].lower() for word in words.split())
    except ValueError as e:
        raise ValueError(f"Ungültiger Name: {e}")



def parse_birth_year(text: str) -> int:
    """Text -> int (Geburtsjahr). Ungültig -> ValueError.
    Hinweis: Überlege sinnvolle Prüfungen für eine Registrierung (z. B. 4-stellig, nicht Zukunft,
    Volljährigkeit, ungewöhnlich hohes Alter…)."""
    # TODO: trimmen; Ganzzahl erzwingen; sinnvolle Grenzen definieren; ValueError bei Verstößen.
    try:
        text = text.strip()
        if not (text.isdigit() and len(text) == 4):
            raise ValueError("Geburtsjahr muss genau 4 Ziffern haben")
        birth_year = int(text)
        current_year = date.today().year
        if birth_year > current_year:
            raise ValueError("Geburtsjahr kann nicht in der Zukunft liegen")
        age = current_year - birth_year
        if age < 18:
            raise ValueError("Mindestalter 18 Jahre")
        if age > 120:
            raise ValueError("Maximalalter 120 Jahre")
        return birth_year
    except ValueError as e:
        raise ValueError(f"Ungültiges Geburtsjahr: {e}")



def format_profile(name: str, birth_year: int) -> str:
    """Formatiert: 'Profil: Name (Geburtsjahr: YYYY)'. Ungültig -> ValueError."""
    # TODO: Name nicht leer; birth_year plausibel (int); String zurückgeben wie oben.

    try:
        normalized_name = normalize_name(name)

        if not isinstance(birth_year, int):
            raise ValueError("Geburtsjahr muss eine ganze Zahl sein")

        current_year = date.today().year
        if birth_year > current_year:
            raise ValueError("Geburtsjahr kann nicht in der Zukunft liegen")

        age = current_year - birth_year
        if age < 18:
            raise ValueError("Mindestalter 18 Jahre")
        if age > 120:
            raise ValueError("Maximalalter 120 Jahre")

        return f"Profil: {normalized_name} (Geburtsjahr: {birth_year})"
    except ValueError as e:
        raise ValueError(f"Ungültiges Profil: {e}")



# ========== Bonus (optional) ==========
def parse_email(text: str) -> str:
    """Sehr einfache E-Mail-Prüfung: genau ein '@', Punkt nach '@', keine Leerzeichen. Ungültig -> ValueError."""
    # TODO (Bonus): einfache Regeln prüfen, ansonsten ValueError.

    try:
        text = text.strip()
        if not text or ' ' in text or text.count('@') != 1:
            raise ValueError("Ungültige E-Mail-Adresse")

        at_index = text.find('@')
        if at_index == 0 or at_index == len(text) - 1:
            raise ValueError("Ungültige E-Mail-Adresse")

        if '.' not in text[at_index + 1:]:
            raise ValueError("Ungültige E-Mail-Adresse")

        return text

    except ValueError as e:
        raise ValueError(f"Ungültige E-Mail-Adresse: {e}")



# ========== Prüfer & Demo (nicht ändern) ==========
class Testfehler(AssertionError):
    pass


class Pruefer:
    def __init__(self):
        self.ok = 0
        self.fail = 0
        self.skip = 0
        self.year = date.today().year

    def _ok(self, msg: str):
        self.ok += 1
        print(f"✔ {msg}")

    def _fail(self, msg: str):
        self.fail += 1
        print(f"✘ {msg}")

    def _skip(self, msg: str):
        self.skip += 1
        print(f"↷ Übersprungen: {msg}")

    def summary(self):
        print("\n=== Zusammenfassung ===")
        print(f"Bestanden: {self.ok} | Fehlgeschlagen: {self.fail} | Übersprungen: {self.skip}")
        if self.fail == 0:
            print("✅ Alle ausgeführten Tests bestanden – sehr gut!")
        else:
            print("ℹ Prüfe die Hinweise oben und korrigiere deine Funktionen.")



    # ---- Pflicht-Tests ------------------------------------------------------
    def test_normalize_name(self):
        try:
            out = normalize_name(" nina max mustermann ")
        except NotImplementedError:
            return self._fail("normalize_name ist nicht implementiert.")
        if out != "Nina Max Mustermann":
            raise Testfehler(f"normalize_name() → '{out}', erwartet 'Nina Max Mustermann'")

        # Unerlaubte Zeichen (Ziffern/Symbole)
        for bad in ["Nina-Max", "Max3", "Nina_Max", "Nina!"]:
            try:
                normalize_name(bad)
                raise Testfehler("normalize_name hätte ValueError werfen müssen.")
            except ValueError:
                pass
        self._ok("normalize_name – Zeichenprüfung & Großschreibung")

    def test_parse_birth_year(self):
        fn = parse_birth_year
        cy = self.year

        # gültige Beispiele (Plausibilität, nicht exakt vorgegeben)
        for s in [str(cy - 30), f" {cy - 18} ", "1990"]:
            try:
                val = fn(s)
                if not isinstance(val, int):
                    raise Testfehler("parse_birth_year muss int liefern.")
            except ValueError:
                raise Testfehler(f"parse_birth_year('{s}') sollte gültig sein.")

        # ungültig: leer/keine Zahl/falsch formatiert
        for bad in ["", "abcd", "19 90", "199", " "]:
            try:
                fn(bad)
                raise Testfehler(f"parse_birth_year('{bad}') hätte ValueError werfen müssen.")
            except ValueError:
                pass

        # ungültig: zu jung (unter 18)
        too_young = str(cy - 10)
        try:
            fn(too_young)
            raise Testfehler("parse_birth_year (unter 18) hätte ValueError werfen müssen.")
        except ValueError:
            pass

        # ungültig: zu alt (>120 Jahre)
        too_old = str(cy - 130)
        try:
            fn(too_old)
            raise Testfehler("parse_birth_year (>120) hätte ValueError werfen müssen.")
        except ValueError:
            pass

        # ungültig: Zukunft
        future = str(cy + 1)
        try:
            fn(future)
            raise Testfehler("parse_birth_year (Zukunft) hätte ValueError werfen müssen.")
        except ValueError:
            pass

        self._ok("parse_birth_year – Plausibilitäten (18+ / <=120 / nicht Zukunft)")

    def test_format_profile(self):
        text = format_profile("Max Mustermann", 1990)
        if text != "Profil: Max Mustermann (Geburtsjahr: 1990)":
            raise Testfehler(f"format_profile → '{text}', erwartet 'Profil: Max Mustermann (Geburtsjahr: 1990)'")
        # Fehlerfälle
        for args in [("", 1990), ("Max Mustermann", "1990"), ]:
            try:
                format_profile(*args)
                raise Testfehler("format_profile hätte ValueError werfen müssen.")
            except ValueError:
                pass
        self._ok("format_profile – Ausgabe & Eingabeprüfung")

    # ---- Bonus-Tests --------------------------------------------------------
    def test_email(self):
        try:
            s = parse_email("max@example.com")
        except NotImplementedError:
            return self._skip("parse_email nicht implementiert (Bonus).")
        if s != "max@example.com":
            raise Testfehler(f"parse_email → '{s}', erwartet 'max@example.com'")
        for bad in ["", "max@", "@example.com", "max example@com", "max@com"]:
            try:
                parse_email(bad)
                raise Testfehler("parse_email hätte ValueError werfen müssen.")
            except ValueError:
                pass
        self._ok("parse_email – einfache Strukturprüfung")

    def run_all(self):
        print("=== Starte Tests ===\n")
        self.test_normalize_name()
        self.test_parse_birth_year()
        self.test_format_profile()
        # Bonus
        self.test_email()
        self.summary()


def demo_cli() -> None:
    """Kurze Demo nach dem Testlauf (bewusst minimal)."""
    print("\n=== Demo: Registrierung – Profil & Prüfungen ===")
    try:
        name_raw = input("Dein Name: ")
        try:
            name = normalize_name(name_raw)
        except Exception:
            name = name_raw.strip()
        birth_year = parse_birth_year(input("Dein Geburtsjahr (YYYY): "))
        print("\n" + format_profile(name, birth_year))
        print("\n(Hinweis: Überlege selbst, welche weiteren Prüfungen/Outputs hier sinnvoll wären.)")
    except Exception as e:
        print(f"Fehler: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        Pruefer().run_all()
    else:
        Pruefer().run_all()
        print("\nJetzt kannst du die Demo ausprobieren…")
        demo_cli()