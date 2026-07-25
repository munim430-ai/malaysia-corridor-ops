import fitz
from PIL import Image, ImageDraw, ImageFont
import os, io

pdf_dir = r'reports/sample_work_orders/pdfs'

def save_images_to_pdf(img_list, output_path):
    doc = fitz.open()
    for img in img_list:
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        img_doc = fitz.open("png", buf.getvalue())
        pdf_bytes = img_doc.convert_to_pdf()
        pdf_img_doc = fitz.open("pdf", pdf_bytes)
        doc.insert_pdf(pdf_img_doc)
        img_doc.close()
        pdf_img_doc.close()
    doc.save(output_path)
    doc.close()

print("Starting precision PDF date updates to 2026...")

# 1. Eng Leong Tin Can Manufacturing
path_eng = os.path.join(pdf_dir, 'eng_leong_tin_can_manufacturing_poa.pdf')
doc_eng = fitz.open(path_eng)
img_pages_eng = []
for pno, page in enumerate(doc_eng):
    pix = page.get_pixmap(dpi=150)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if pno == 0:
        draw = ImageDraw.Draw(img)
        font_bold = ImageFont.truetype('C:/Windows/Fonts/timesbd.ttf', 7)
        font_regular = ImageFont.truetype('C:/Windows/Fonts/times.ttf', 7)

        # Ref line: KSM/100/2022/001502 -> 2026
        draw.rectangle([112, 149, 126, 157], fill=(255, 255, 255))
        draw.text((112, 149), '2026', fill=(0, 0, 0), font=font_bold)

        # Date line: 29th July 2022 -> 2026
        draw.rectangle([124, 160, 138, 168], fill=(255, 255, 255))
        draw.text((124, 160), '2026', fill=(0, 0, 0), font=font_regular)
    img_pages_eng.append(img)
doc_eng.close()
save_images_to_pdf(img_pages_eng, path_eng)
print("Updated eng_leong_tin_can_manufacturing_poa.pdf")


# 2. CCK Farm Demand Letter
path_cck = os.path.join(pdf_dir, 'cck_farm_demand_letter.pdf')
doc_cck = fitz.open(path_cck)
img_pages_cck = []
for pno, page in enumerate(doc_cck):
    pix = page.get_pixmap(dpi=150)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if pno == 0:
        draw = ImageDraw.Draw(img)
        font_regular = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 7)
        # Date: 5 February 2023 -> 2026
        draw.rectangle([70, 135, 100, 145], fill=(255, 255, 255))
        draw.text((70, 135), '2026', fill=(0, 0, 0), font=font_regular)
    img_pages_cck.append(img)
doc_cck.close()
save_images_to_pdf(img_pages_cck, path_cck)
print("Updated cck_farm_demand_letter.pdf")


# 3. CCK Farm BL2 Companion
path_cck_bl2 = os.path.join(pdf_dir, 'cck_farm_bl2_companion.pdf')
doc_cck_bl2 = fitz.open(path_cck_bl2)
pix = doc_cck_bl2[0].get_pixmap(dpi=150)
img_cck_bl2 = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
doc_cck_bl2.close()
draw = ImageDraw.Draw(img_cck_bl2)
font_regular = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
draw.rectangle([210, 420, 310, 455], fill=(255, 255, 255))
draw.text((210, 420), '2026', fill=(0, 0, 0), font=font_regular)
save_images_to_pdf([img_cck_bl2], path_cck_bl2)
print("Updated cck_farm_bl2_companion.pdf")


# 4. Sampan Maju Enterprise Demand Letter
path_sampan = os.path.join(pdf_dir, 'sampan_maju_enterprise_demand_letter.pdf')
doc_sampan = fitz.open(path_sampan)
img_pages_sampan = []
for pno, page in enumerate(doc_sampan):
    pix = page.get_pixmap(dpi=150)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if pno == 0:
        draw = ImageDraw.Draw(img)
        font_regular = ImageFont.truetype('C:/Windows/Fonts/times.ttf', 7)
        # Date : 29 May 2023 -> 2026
        draw.rectangle([360, 160, 400, 172], fill=(255, 255, 255))
        draw.text((360, 160), '2026', fill=(0, 0, 0), font=font_regular)
    img_pages_sampan.append(img)
doc_sampan.close()
save_images_to_pdf(img_pages_sampan, path_sampan)
print("Updated sampan_maju_enterprise_demand_letter.pdf")


# 5. Al-Rabeta / Potential Region
path_alrabeta = os.path.join(pdf_dir, 'al_rabeta_potential_region_demand_letter.pdf')
doc_alrabeta = fitz.open(path_alrabeta)
pix = doc_alrabeta[0].get_pixmap(dpi=150)
img_alrabeta = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
doc_alrabeta.close()
draw = ImageDraw.Draw(img_alrabeta)
font_regular = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
draw.rectangle([830, 310, 875, 345], fill=(255, 255, 255))
draw.text((830, 310), '26', fill=(0, 0, 0), font=font_regular)

draw.rectangle([540, 350, 620, 390], fill=(255, 255, 255))
draw.text((540, 350), '2026', fill=(0, 0, 0), font=font_regular)

draw.rectangle([690, 915, 770, 955], fill=(255, 255, 255))
draw.text((690, 915), '2026', fill=(0, 0, 0), font=font_regular)

save_images_to_pdf([img_alrabeta], path_alrabeta)
print("Updated al_rabeta_potential_region_demand_letter.pdf")


# 6. Exelite Resources Demand Employment Letter
path_exelite = os.path.join(pdf_dir, 'exelite_resources_demand_employment_letter.pdf')
doc_exelite = fitz.open(path_exelite)
pix = doc_exelite[0].get_pixmap(dpi=150)
img_exelite = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
doc_exelite.close()
draw = ImageDraw.Draw(img_exelite)
font_regular = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 20)
draw.text((320, 320), '15 May 2026', fill=(0, 0, 0), font=font_regular)
save_images_to_pdf([img_exelite], path_exelite)
print("Updated exelite_resources_demand_employment_letter.pdf")


# 7. Agensi Pekerjaan OSM Template
path_osm = os.path.join(pdf_dir, 'agensi_pekerjaan_osm_demand_letter_template.pdf')
doc_osm = fitz.open(path_osm)
img_pages_osm = []
for pno, page in enumerate(doc_osm):
    pix = page.get_pixmap(dpi=150)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if pno == 0:
        draw = ImageDraw.Draw(img)
        font_regular = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 8)
        draw.rectangle([85, 145, 145, 155], fill=(255, 255, 255))
        draw.text((85, 145), '15/05/2026', fill=(0, 0, 0), font=font_regular)
    img_pages_osm.append(img)
doc_osm.close()
save_images_to_pdf(img_pages_osm, path_osm)
print("Updated agensi_pekerjaan_osm_demand_letter_template.pdf")

print("All 7 PDFs updated successfully to 2026!")
