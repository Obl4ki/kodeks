import re
from typing import Iterator

from pypdf import PdfReader
from utils import tuple_windows

from dataclasses import dataclass


@dataclass
class Paragraph:
    name: int
    article_name: int
    content: str
    declined: bool


@dataclass
class Article:
    name: int
    content: str
    declined: bool


def remove_pages_boilerplate(text: str) -> str:
    s = r"\s+"  # whitespace
    date = r"\d{4}\s?-\d{2}-\d{2}"  # date in yyyy-mm-dd format
    page_number = r"\d*\/\d*"  # page number (ex. 71/142)

    header_footer_regex = f"©Kancelaria Sejmu{s}s.{s}{page_number}{s}{date}{s}"
    spans = [m.span() for m in re.finditer(header_footer_regex, text)]
    spans.reverse()

    for start, stop in spans:
        text = text[:start] + text[stop:]

    return text


def get_articles(text: str) -> list[Article]:
    delim_regex = r"Art. \d+\w?\."

    spans = [m.span() for m in re.finditer(delim_regex, text)]
    spans.append((len(text), len(text)))

    for span_idx, (start, stop) in enumerate(spans):
        if text[start:stop] != f"Art. {span_idx+1}.":
            f"Article span should be {span_idx} and is {text[start:stop]}"

    articles = []

    for (start1, stop1), (start2, _) in tuple_windows(spans, n=2):
        content = text[stop1:start2].strip()
        article_name = text[start1 + 5 : stop1 - 1]

        articles.append(
            Article(article_name, content, declined="(uchylony)" in content)
        )

    return articles


def get_paragraphs(text: str) -> list[Paragraph]:
    articles = get_articles(text)

    paragraph_delim = r"§ \d+\w?\."

    paragraphs = []
    for article in articles:
        spans = [m.span() for m in re.finditer(paragraph_delim, article.content)]
        spans.append((len(article.content), len(article.content)))

        if len(spans) == 1:
            paragraphs.append(
                Paragraph(
                    article_name=article.name,
                    name="",
                    content=article.content,
                    declined="(uchylony)" in article.content,
                )
            )
            continue

        for (start1, stop1), (start2, _) in tuple_windows(spans, n=2):
            content = article.content[stop1:start2].strip()
            paragraph_name = article.content[start1 + 2 : stop1 - 1]

            paragraphs.append(
                Paragraph(
                    article_name=article.name,
                    name=paragraph_name,
                    content=content,
                    declined="(uchylony)" in content,
                )
            )

    return paragraphs


def get_text_pages(pdf_name: str) -> Iterator[str]:
    reader = PdfReader(pdf_name)
    for page in reader.pages:
        yield page.extract_text()
