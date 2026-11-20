#!/usr/bin/env python3
"""Split the JD Hardware pages export into the storefront JSON files.

Source: content/sheets/jd-hardware-pages.txt (exported from the Pages and Policies doc).
Each page's `lines` array is the tab text, one string per paragraph or bullet.
`sections` are rebuilt from those same lines.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content" / "sheets" / "jd-hardware-pages.txt"

PAGE_TITLES = [
    "About Us",
    "Our Commitment",
    "Contact Us",
    "Frequently Asked Questions",
    "Shipping & Delivery Policy",
    "Return Policy",
    "Refund Policy",
    "Order Cancellation Policy",
    "Payment Options",
    "Warranty & Product Support",
    "Order Help Centre",
    "Privacy Policy",
    "Terms & Conditions",
    "Cookie Policy",
    "Legal Notice",
    "Accessibility Statement",
    "Your Privacy Choices",
]

SLUGS = {
    "About Us": "about-us",
    "Our Commitment": "our-commitment",
    "Contact Us": "contact-us",
    "Frequently Asked Questions": "faqs",
    "Shipping & Delivery Policy": "shipping-policy",
    "Return Policy": "return-and-refund-policy",
    "Order Cancellation Policy": "cancellation-policy",
    "Payment Options": "payment-policy",
    "Warranty & Product Support": "warranty",
    "Order Help Centre": "order-help-center",
    "Privacy Policy": "privacy-policy",
    "Terms & Conditions": "terms-of-service",
    "Cookie Policy": "cookie-policy",
    "Legal Notice": "legal-notice",
    "Accessibility Statement": "accessibility-statement",
    "Your Privacy Choices": "your-privacy-choices",
}

DISCOVER = ["about-us", "contact-us", "faqs", "our-commitment"]
CARE = [
    "shipping-policy",
    "return-and-refund-policy",
    "cancellation-policy",
    "payment-policy",
    "warranty",
    "order-help-center",
]
TRUST = [
    "privacy-policy",
    "terms-of-service",
    "cookie-policy",
    "legal-notice",
    "accessibility-statement",
    "your-privacy-choices",
]

SMALL_WORDS = {"and", "to", "for", "of", "a", "the", "your", "with", "in", "on", "or"}


def clean_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if set(line) <= {"_", "-"}:
            continue
        lines.append(line)
    return lines


def split_pages(lines: list[str]) -> dict[str, list[str]]:
    titles = set(PAGE_TITLES)
    pages: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        if line in titles and line not in pages:
            current = line
            pages[current] = [line]
            continue
        if current is None:
            continue
        pages[current].append(line)
    missing = [title for title in PAGE_TITLES if title not in pages]
    if missing:
        raise SystemExit(f"Missing pages in the export: {missing}")
    return pages


def is_bullet(line: str) -> bool:
    return line.startswith("* ")


def is_meta(line: str) -> bool:
    return bool(re.match(r"^(Effective Date|Last Updated):", line, re.I))


def is_question(line: str) -> bool:
    return line.endswith("?") and len(line) < 160


def is_numbered(line: str) -> bool:
    return bool(re.match(r"^\d+\.\s+\S", line)) and len(line) < 120 and not re.search(r"[.!;]$", line)


def is_title_heading(line: str) -> bool:
    if line in {"United Kingdom", "United States"}:
        return False
    if len(line) < 8 or len(line) > 72:
        return False
    if re.search(r"[.!?;:]$", line):
        return False
    if ": " in line or "@" in line or re.search(r"https?:", line, re.I):
        return False
    if re.search(r"\d", line):
        return False
    words = line.strip().split()
    if len(words) < 2 or len(words) > 10:
        return False

    def ok(word: str) -> bool:
        trimmed = re.sub(r"^[^A-Za-z&]+", "", word)
        core = re.sub(r"[^A-Za-z]", "", trimmed).lower()
        return bool(re.match(r"^[&A-Z]", trimmed)) or core in SMALL_WORDS

    return all(ok(word) for word in words)


def is_heading(line: str) -> bool:
    if is_bullet(line) or is_meta(line) or is_question(line):
        return False
    return is_numbered(line) or is_title_heading(line)


def slugify(text: str) -> str:
    text = re.sub(r"^\d+\.\s+", "", text)
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return text.strip("-") or "section"


def body_start(lines: list[str]) -> int:
    if len(lines) > 1 and is_heading(lines[1]) and not is_numbered(lines[1]):
        return 2
    return 1


def first_sentence(lines: list[str]) -> str:
    for line in lines[body_start(lines) :]:
        if is_meta(line) or is_bullet(line) or is_heading(line) or is_question(line):
            continue
        if len(line) >= 40:
            return line
    for line in lines[1:]:
        if not is_meta(line):
            return line
    return lines[0]


def effective_date(lines: list[str]) -> str:
    for line in lines:
        match = re.match(r"^(?:Last Updated|Effective Date):\s*(.+)$", line, re.I)
        if match:
            return match.group(1).strip()
    return ""


def intro_lines(lines: list[str]) -> list[str]:
    intro: list[str] = []
    for line in lines[body_start(lines) :]:
        if is_heading(line) or is_question(line):
            break
        if is_meta(line) or is_bullet(line):
            continue
        intro.append(line)
    return intro or [first_sentence(lines)]


def tagline_for(lines: list[str], description: str) -> str:
    if len(lines) > 1 and not is_meta(lines[1]) and not is_bullet(lines[1]) and len(lines[1]) <= 90:
        return lines[1]
    return description


def sections_from(lines: list[str]) -> list[dict]:
    sections: list[dict] = []
    current: dict = {"id": "overview", "title": lines[0], "blocks": []}
    seen: dict[str, int] = {}

    def close() -> None:
        if current["blocks"]:
            sections.append(current)

    def push_paragraph(text: str) -> None:
        current["blocks"].append({"type": "paragraph", "text": text})

    def push_bullet(text: str) -> None:
        if current["blocks"] and current["blocks"][-1]["type"] == "bullets":
            current["blocks"][-1]["items"].append(text)
        else:
            current["blocks"].append({"type": "bullets", "items": [text]})

    body = lines[1:]
    index = 0
    while index < len(body):
        line = body[index]
        if is_heading(line):
            close()
            base = slugify(line)
            seen[base] = seen.get(base, 0) + 1
            section_id = base if seen[base] == 1 else f"{base}-{seen[base]}"
            current = {"id": section_id, "title": line, "blocks": []}
            index += 1
            continue
        if is_question(line):
            answer: list[str] = []
            index += 1
            while index < len(body) and not is_heading(body[index]) and not is_question(body[index]):
                part = body[index][2:] if is_bullet(body[index]) else body[index]
                if not is_meta(part):
                    answer.append(part)
                index += 1
            current["blocks"].append(
                {"type": "faq", "question": line, "answer": " ".join(answer).strip()}
            )
            continue
        if is_bullet(line):
            push_bullet(line[2:])
        elif not is_meta(line):
            push_paragraph(line)
        index += 1
    close()
    return sections


def page_record(title: str, lines: list[str]) -> dict:
    description = first_sentence(lines)
    return {
        "slug": SLUGS[title],
        "title": title,
        "effectiveDate": effective_date(lines),
        "tagline": tagline_for(lines, description),
        "intro": intro_lines(lines),
        "description": description,
        "sections": sections_from(lines),
        "lines": lines,
    }


def write_json(path: Path, pages: list[dict]) -> None:
    path.write_text(json.dumps({"pages": pages}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def paragraphs_until_heading(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        if is_heading(line) or is_bullet(line) or is_question(line):
            break
        if is_meta(line):
            continue
        out.append(line)
    return out


def blocks_after(lines: list[str], heading: str) -> list[str]:
    start = None
    for index, line in enumerate(lines):
        if line == heading:
            start = index + 1
            break
    if start is None:
        return []
    out = []
    for line in lines[start:]:
        if is_heading(line):
            break
        out.append(line)
    return out


def build_site_pages(pages: dict[str, list[str]]) -> dict:
    about = pages["About Us"]
    commitment = pages["Our Commitment"]
    contact = pages["Contact Us"]
    faqs = pages["Frequently Asked Questions"]

    why_start = about.index("Why Shop at JD Hardware?") + 1
    why_end = about.index("Our Commitment to Customers")
    why = about[why_start:why_end]
    values = []
    index = 0
    while index < len(why) - 1:
        title = why[index]
        text = why[index + 1]
        if (
            not title.endswith(".")
            and not title.startswith("* ")
            and len(title) < 48
            and text.endswith(".")
        ):
            values.append({"title": title, "text": text})
            index += 2
            continue
        index += 1

    about_sections = []
    for heading in [
        "Who We Are",
        "Explore Our Product Categories",
        "Our Mission",
        "Our Commitment to Customers",
        "Contact JD Hardware",
    ]:
        chunk = blocks_after(about, heading)
        if not chunk:
            continue
        section = {"title": heading, "paragraphs": [line for line in chunk if not is_bullet(line)]}
        bullets = [line[2:] for line in chunk if is_bullet(line)]
        if bullets:
            section["bullets"] = bullets
        about_sections.append(section)

    commitment_sections = []
    for line in commitment:
        if is_numbered(line):
            chunk = blocks_after(commitment, line)
            section = {
                "title": line,
                "paragraphs": [item for item in chunk if not is_bullet(item)],
            }
            bullets = [item[2:] for item in chunk if is_bullet(item)]
            if bullets:
                section["bullets"] = bullets
            commitment_sections.append(section)

    contact_intro = [line for line in contact[2:4] if line]
    topic_labels = [
        "Product Enquiries",
        "Order Assistance",
        "Shipping and Delivery",
        "Returns",
        "Refunds",
        "Damaged or Incorrect Products",
    ]
    topics = []
    for index, heading in enumerate(topic_labels):
        start = contact.index(heading) + 1
        end = contact.index(topic_labels[index + 1]) if index + 1 < len(topic_labels) else contact.index("Contact Form")
        chunk = [line for line in contact[start:end] if not is_bullet(line) and not is_heading(line)]
        if chunk:
            topics.append({"title": heading, "text": " ".join(chunk)})

    groups = []
    current = None
    for line in faqs[1:]:
        if is_heading(line) and not is_question(line):
            current = {"title": line, "items": []}
            groups.append(current)
            continue
        if is_question(line) and current is not None:
            current["items"].append({"question": line, "answer": ""})
    # Fill answers from the care-style sections so they match the lines.
    for section in sections_from(faqs):
        for group in groups:
            if group["title"] != section["title"]:
                continue
            answers = {
                block["question"]: block["answer"]
                for block in section["blocks"]
                if block["type"] == "faq"
            }
            for item in group["items"]:
                item["answer"] = answers.get(item["question"], "")
    groups = [group for group in groups if group["items"]]

    contact_faqs = []
    for group in groups:
        if group["title"] == "General Questions":
            contact_faqs = group["items"][:4]
            break

    return {
        "about": {
            "eyebrow": "About JD Hardware",
            "title": "Welcome to JD Hardware",
            "intro": about[2] if len(about) > 2 else first_sentence(about),
            "body": about[3] if len(about) > 3 else "",
            "image": "/brand/home-hero.jpg",
            "values": values,
            "sections": about_sections,
            "ctaTitle": "Contact JD Hardware",
            "ctaBody": " ".join(
                line
                for line in blocks_after(about, "Contact JD Hardware")
                if not line.endswith(":")
            ),
        },
        "contact": {
            "eyebrow": "Contact us",
            "title": contact[1] if len(contact) > 1 else "Contact Us",
            "intro": " ".join(contact_intro[:2]),
            "channels": [
                {
                    "title": "Email",
                    "detail": "info@jdhardware.shop",
                    "text": "Whether you need product information, assistance with an order, delivery updates or help with a return or refund, our customer support channels are available to assist you.",
                },
                {
                    "title": "Telephone",
                    "detail": "020 7606 3333",
                    "text": "Time Zone: UK local time (GMT/BST depending on the season).",
                },
                {
                    "title": "Live chat",
                    "detail": "Available 24/7",
                    "text": "Live Chat: Available 24/7",
                },
            ],
            "businessNote": "JD Hardware Co., 280A Norwood Road, Norwood, London SE27 9AJ, United Kingdom. Website: https://jdhardware.shop.",
            "helpTopics": topics,
            "formNote": "You may also contact us through the website contact form.",
            "securityNote": "Please do not provide passwords or complete payment card information.",
            "hours": [
                {"channel": "Live chat", "availability": "24/7"},
                {"channel": "Email", "availability": "info@jdhardware.shop"},
                {"channel": "Telephone", "availability": "020 7606 3333"},
                {"channel": "Time zone", "availability": "UK local time (GMT/BST)"},
            ],
            "faqs": contact_faqs,
        },
        "commitment": {
            "eyebrow": "Our commitment",
            "title": commitment[1] if len(commitment) > 1 else "Our Commitment",
            "intro": commitment[2] if len(commitment) > 2 else first_sentence(commitment),
            "body": commitment[3] if len(commitment) > 3 else "",
            "sections": commitment_sections,
            "ctaTitle": "Contact Information",
            "ctaBody": "JD Hardware Co., 280A Norwood Road, Norwood, London SE27 9AJ, United Kingdom. Email info@jdhardware.shop or telephone 020 7606 3333. Live chat is available 24/7.",
        },
        "faq": {
            "eyebrow": "FAQs",
            "title": "Frequently Asked Questions",
            "intro": " ".join(paragraphs_until_heading(faqs[1:])[:2]),
            "groups": groups,
        },
    }


def write_sources(pages: dict[str, list[str]]) -> None:
    def dump(titles: list[str]) -> str:
        chunks = []
        for title in titles:
            chunks.append("\n".join(pages[title]))
        return "\n\n".join(chunks) + "\n"

    (ROOT / "data" / "discover" / "_source.txt").write_text(
        dump(["About Us", "Our Commitment", "Contact Us", "Frequently Asked Questions"]),
        encoding="utf-8",
    )
    (ROOT / "data" / "customer-care" / "_source.txt").write_text(
        dump(
            [
                "Shipping & Delivery Policy",
                "Return Policy",
                "Refund Policy",
                "Order Cancellation Policy",
                "Payment Options",
                "Warranty & Product Support",
                "Order Help Centre",
            ]
        ),
        encoding="utf-8",
    )
    (ROOT / "data" / "trust" / "_source.txt").write_text(
        dump(
            [
                "Privacy Policy",
                "Terms & Conditions",
                "Cookie Policy",
                "Legal Notice",
                "Accessibility Statement",
                "Your Privacy Choices",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8").lstrip("\ufeff")
    pages = split_pages(clean_lines(text))
    returns = pages["Return Policy"] + pages["Refund Policy"]
    records = []
    for title in PAGE_TITLES:
        if title == "Refund Policy":
            continue
        lines = returns if title == "Return Policy" else pages[title]
        records.append(page_record(title if title != "Return Policy" else "Return Policy", lines))

    by_slug = {record["slug"]: record for record in records}
    write_json(ROOT / "data" / "discover" / "pages.json", [by_slug[slug] for slug in DISCOVER])
    write_json(ROOT / "data" / "customer-care" / "pages.json", [by_slug[slug] for slug in CARE])
    write_json(ROOT / "data" / "trust" / "pages.json", [by_slug[slug] for slug in TRUST])
    site_pages = build_site_pages(pages)
    (ROOT / "data" / "pages.json").write_text(
        json.dumps(site_pages, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_sources(pages)
    print("pages", ", ".join(f"{record['slug']}({len(record['lines'])})" for record in records))
    print("faq groups", [group["title"] for group in site_pages["faq"]["groups"]])
    print("about values", len(site_pages["about"]["values"]))


if __name__ == "__main__":
    main()
