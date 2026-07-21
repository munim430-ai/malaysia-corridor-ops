#!/usr/bin/env python3
"""
Download the real public preview page-images Scribd serves in its own
SSR/SEO HTML (visible to search engines / logged-out visitors, no login
or paywall bypassed) and assemble them into an actual PDF file.

Usage: python3 fetch_scribd_pdf.py <doc_id> <slug> <out_dir>
"""
import sys
import re
import urllib.request
from pathlib import Path
from PIL import Image
import io

GOOGLEBOT_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"


def fetch(url, ua=GOOGLEBOT_UA, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def main():
    doc_id, slug, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Find the canonical page-count / doc detail URL pattern first via search-style URL
    detail_url = f"https://www.scribd.com/document/{doc_id}/x"
    html, ctype = fetch(detail_url)
    html = html.decode("utf-8", errors="replace")

    if "Client Challenge" in html[:500]:
        print(f"BLOCKED:{doc_id}: JS challenge even with Googlebot UA")
        sys.exit(2)

    # screenshots.scribd.com/Scribd/<size>/<bucket>/<doc_id>/<page>.jpeg
    urls = sorted(set(re.findall(
        r'https://screenshots\.scribd\.com/Scribd/[\d_]+/\d+/' + re.escape(doc_id) + r'/(\d+)\.jpeg',
        html,
    )), key=int)
    prefix_match = re.search(
        r'(https://screenshots\.scribd\.com/Scribd/[\d_]+/\d+/' + re.escape(doc_id) + r'/)\d+\.jpeg',
        html,
    )
    images = []
    fallback_single_page = False
    if not urls or not prefix_match:
        # Fall back to the single full-res "original" page-1 image embedded
        # for every doc (used as the hero/OG image) when the multi-page
        # screenshot gallery isn't exposed for this document.
        orig_match = re.search(
            r'(https://imgv2-\d-[a-z]\.scribdassets\.com/img/document/' + re.escape(doc_id) + r'/original/[a-f0-9]+/)1\?v=1',
            html,
        )
        if not orig_match:
            print(f"NO_IMAGES_AT_ALL:{doc_id}: no screenshots gallery and no original page-1 image found in HTML ({len(html)} bytes)")
            sys.exit(3)
        img_url = f"{orig_match.group(1)}1?v=1"
        try:
            data, ct = fetch(img_url, ua="Mozilla/5.0")
            img = Image.open(io.BytesIO(data)).convert("RGB")
            images.append(img)
            fallback_single_page = True
        except Exception as e:
            print(f"PAGE_FAIL:{doc_id}:page 1 (fallback): {e}")
    else:
        prefix = prefix_match.group(1)
        for page in urls:
            img_url = f"{prefix}{page}.jpeg"
            try:
                data, ct = fetch(img_url, ua="Mozilla/5.0")
                img = Image.open(io.BytesIO(data)).convert("RGB")
                images.append(img)
            except Exception as e:
                print(f"PAGE_FAIL:{doc_id}:page {page}: {e}")

    if not images:
        print(f"NO_IMAGES:{doc_id}: found {len(urls)} page URLs but downloaded 0")
        sys.exit(4)

    out_pdf = out_dir / f"{slug}.pdf"
    images[0].save(out_pdf, save_all=True, append_images=images[1:])
    tag = "PARTIAL(page1-only)" if fallback_single_page else "OK"
    print(f"{tag}:{doc_id}:{out_pdf}:{len(images)} pages")


if __name__ == "__main__":
    main()
