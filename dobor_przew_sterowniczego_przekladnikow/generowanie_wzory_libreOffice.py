import os
from odf.opendocument import OpenDocumentText
from odf.text import P, H
from odf.style import Style, TextProperties, ParagraphProperties


def generate_odt_document(formula_text):
    textdoc = OpenDocumentText()

    # 2. Tworzenie stylu dla wyśrodkowanego wzoru
    formula_style = Style(name="FormulaCenter", family="paragraph")

    # POPRAWKA 1: Używamy argumentu 'textalign' bezpośrednio (sprawdzone)
    formula_style.addElement(ParagraphProperties(
        textalign="center"
    ))

    # POPRAWKA 2: Usuwamy prefiks 'fo:' z atrybutów TextProperties!
    formula_style.addElement(TextProperties(
        attributes={
            "font-size": "20pt",  # Bez "fo:"
            "font-weight": "bold"  # Bez "fo:"
        }
    ))

    textdoc.styles.addElement(formula_style)

    # 3. Dodanie nagłówka
    textdoc.text.addElement(H(outlinelevel=1, stylename='Heading_20_1',
                              text="Automatycznie wygenerowany dokument z formułą"))

    # 4. Dodanie akapitu wstępu
    textdoc.text.addElement(P(text="Poniżej znajduje się wzór wygenerowany programowo za pomocą biblioteki odfpy:"))

    # 5. Dodanie akapitu z wzorem, używając specjalnego stylu
    textdoc.text.addElement(P(
        stylename=formula_style,
        text=formula_text
    ))

    # 6. Zapis pliku
    try:
        desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
    except KeyError:
        desktop_path = os.path.expanduser("~/Desktop")

    file_path = os.path.join(desktop_path, "wzor.odt")

    try:
        textdoc.save(file_path)
        print(f"✅ Sukces! Plik ODT zapisano: {file_path}")
    except Exception as e:
        print(f"❌ Błąd podczas zapisu pliku ODT: {e}")


if __name__ == "__main__":
    formula = "a / b = c"
    generate_odt_document(formula)