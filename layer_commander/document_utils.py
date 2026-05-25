from krita import Document, Krita


def get_active_document() -> Document | None:
    out = Krita.instance().activeDocument()
    if out is None:
        print("BUG IN LAYER COMMANDER, NO DOCUMENT")
        print("REPORT TO Ben-Collett github.com")
    return out


def refresh_projection(document: Document):
    document.refreshProjection()


def get_document_size(document: Document) -> tuple[int, int]:
    return document.width(), document.height()
