import dataclasses
import json
from extract import get_paragraphs
from utils import write_to_file_utf8
from extract import remove_pages_boilerplate, get_text_pages, get_paragraphs


SHOULD_FIX_TEXT = True

if __name__ == "__main__":
    print("Reading pdf")
    full_text = "".join(list(get_text_pages("kodeks.pdf")))

    print("Removing headers and footers")
    full_text = remove_pages_boilerplate(full_text)

    print("Splitting articles")
    paragraphs = get_paragraphs(full_text)

    if SHOULD_FIX_TEXT:
        print("Creating polish dictionary")
        from fix import fix_text

        print("Fixing paragraphs")
        for paragraph in paragraphs:
            paragraph.content = fix_text(paragraph.content)

    print("Saving to json")
    json_data = json.dumps(
        [dataclasses.asdict(p) for p in paragraphs], indent=4, ensure_ascii=False
    )
    write_to_file_utf8("kodeks.json", json_data)
