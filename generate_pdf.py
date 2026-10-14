"""Generate a short, two-page introduction to arrays as a standalone PDF."""

from pathlib import Path
import textwrap


PAGE_WIDTH = 612
PAGE_HEIGHT = 792
NAVY = (0.08, 0.16, 0.28)
BLUE = (0.12, 0.38, 0.68)
PALE = (0.93, 0.96, 0.99)
DARK = (0.16, 0.20, 0.25)
MUTED = (0.36, 0.41, 0.47)


def pdf_string(value):
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def text(x, y, value, size=11, font="F1", color=DARK):
    red, green, blue = color
    return (
        f"{red:.3f} {green:.3f} {blue:.3f} rg\n"
        f"BT /{font} {size} Tf 1 0 0 1 {x} {y} Tm "
        f"({pdf_string(value)}) Tj ET\n"
    )


def rectangle(x, y, width, height, color):
    red, green, blue = color
    return (
        f"{red:.3f} {green:.3f} {blue:.3f} rg\n"
        f"{x} {y} {width} {height} re f\n"
    )


def wrapped_lines(value, width=88):
    return textwrap.wrap(value, width=width, break_long_words=False)


def paragraph(x, y, value, width=88, size=11, leading=16, color=DARK):
    result = ""
    for line in wrapped_lines(value, width):
        result += text(x, y, line, size=size, color=color)
        y -= leading
    return result, y


def heading(x, y, value):
    return text(x, y, value, size=15, font="F2", color=BLUE)


def header(page_number):
    result = rectangle(0, 744, PAGE_WIDTH, 48, NAVY)
    result += text(42, 763, "ARRAYS: A SIMPLE GUIDE", 10, "F2", (1, 1, 1))
    result += text(550, 763, str(page_number), 10, "F1", (1, 1, 1))
    result += rectangle(42, 38, 528, 1, (0.82, 0.86, 0.90))
    result += text(42, 22, "Introduction to arrays | C++ example included", 8, "F1", MUTED)
    return result


def make_page_one():
    result = header(1)
    result += text(42, 706, "What is an array?", 27, "F2", NAVY)
    block, y = paragraph(
        42,
        679,
        "An array is an ordered collection of values stored under one name. "
        "Each value is called an element, and its position is identified by an index.",
        width=84,
        size=12,
        leading=18,
    )
    result += block
    result += text(42, y - 3, "A small C++ example", 13, "F2", NAVY)

    result += rectangle(42, y - 88, 528, 68, PALE)
    result += text(56, y - 45, "int scores[5] = {88, 94, 76, 100, 91};", 11, "F3", NAVY)
    result += text(56, y - 66, "scores[0] is 88; scores[4] is 91. Indexing starts at 0.", 10, "F3", DARK)

    y -= 117
    result += heading(42, y, "Why are arrays needed?")
    y -= 24
    benefits = [
        ("Keep related data together", "One collection is easier to manage than many separate variables."),
        ("Use loops", "A loop can process every element for totals, searches, or reports."),
        ("Access by position", "An index gives direct access to an element when its position is known."),
    ]
    for title, description in benefits:
        result += text(48, y, "- " + title + ":", 11, "F2", NAVY)
        block, y = paragraph(67, y - 17, description, width=77, size=10, leading=14)
        result += block
        y -= 7

    result += heading(42, y, "A couple of things to remember")
    y -= 23
    block, y = paragraph(
        42,
        y,
        "Indexes start at 0, so an array of 5 elements has positions 0 through 4. "
        "Using a position outside that range is an error to avoid.",
        width=87,
        size=10,
        leading=15,
    )
    result += block
    block, y = paragraph(
        42,
        y - 4,
        "A built-in array or C++ std::array has a fixed size. Use std::vector when "
        "the number of items needs to grow or shrink while the program runs.",
        width=87,
        size=10,
        leading=15,
    )
    result += block
    return result


def make_page_two():
    result = header(2)
    result += text(42, 706, "Arrays in everyday software", 25, "F2", NAVY)
    block, y = paragraph(
        42,
        679,
        "Arrays are useful whenever software needs an ordered group of similar "
        "values. Examples include:",
        width=86,
        size=12,
        leading=18,
    )
    result += block

    examples = [
        ("Weather apps", "Keep a day's hourly temperatures together to calculate a daily high or average."),
        ("Music players", "Store an ordered playlist so tracks can be shown and played one after another."),
        ("Games", "Keep player scores together to sort or display a leaderboard."),
        ("Photo software", "Represent image pixels as rows and columns of color values."),
        ("Shop inventory", "Keep product records together to search products and total their stock value."),
    ]
    for title, description in examples:
        result += text(48, y, title, 12, "F2", BLUE)
        block, y = paragraph(48, y - 18, description, width=86, size=10, leading=14)
        result += block
        y -= 8

    result += heading(42, y, "Project: Array Inventory Tracker")
    y -= 23
    block, y = paragraph(
        42,
        y,
        "The companion C++ console app models a small shop. It stores up to 20 "
        "products in std::array<Product, 20>. Each array element is a Product "
        "record with a name, quantity, and unit price.",
        width=86,
        size=10,
        leading=15,
    )
    result += block
    y -= 4

    result += rectangle(42, y - 115, 528, 102, PALE)
    steps = [
        "1. Add: put a new product into the next unused array position.",
        "2. List: loop through stored products and display their details.",
        "3. Find or update: compare product names while looping over the array.",
        "4. Total: multiply each quantity by its price and add the results.",
    ]
    step_y = y - 34
    for line in steps:
        result += text(56, step_y, line, 9, "F3", NAVY)
        step_y -= 19

    y -= 140
    block, y = paragraph(
        42,
        y,
        "A count records how many of the 20 positions are in use. Before adding, "
        "the app checks that there is room; its loops only visit used positions. "
        "Real shops need flexible storage and reliable saving, so production "
        "software commonly uses resizable collections and databases instead.",
        width=86,
        size=10,
        leading=15,
    )
    result += block
    return result


def build_pdf():
    pages = [make_page_one(), make_page_two()]
    objects = [None]

    def add_object(value):
        objects.append(value)
        return len(objects) - 1

    font_regular = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    font_bold = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    font_mono = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

    page_ids = []
    for content in pages:
        stream = content.encode("latin-1")
        stream_id = add_object(
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"\nendstream"
        )
        page_id = add_object(
            f"<< /Type /Page /Parent PAGES_ID 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_regular} 0 R /F2 {font_bold} 0 R "
            f"/F3 {font_mono} 0 R >> >> /Contents {stream_id} 0 R >>"
        )
        page_ids.append(page_id)

    pages_id = add_object(
        "<< /Type /Pages /Kids [" + " ".join(f"{page_id} 0 R" for page_id in page_ids)
        + f"] /Count {len(page_ids)} >>"
    )
    objects[page_ids[0]] = objects[page_ids[0]].replace("PAGES_ID", str(pages_id))
    objects[page_ids[1]] = objects[page_ids[1]].replace("PAGES_ID", str(pages_id))
    catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, value in enumerate(objects[1:], start=1):
        offsets.append(len(output))
        if isinstance(value, str):
            value = value.encode("latin-1")
        output.extend(f"{index} 0 obj\n".encode("ascii"))
        output.extend(value)
        output.extend(b"\nendobj\n")

    xref_offset = len(output)
    output.extend(f"xref\n0 {len(objects)}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(objects)} /Root {catalog_id} 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    destination = Path(__file__).with_name("arrays_explained.pdf")
    destination.write_bytes(output)
    print(f"Created {destination.name} ({len(pages)} pages, {len(output)} bytes)")


if __name__ == "__main__":
    build_pdf()
