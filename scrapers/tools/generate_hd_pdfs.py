import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.pdfgen import canvas

pdf_dir = r'reports/sample_work_orders/pdfs'
os.makedirs(pdf_dir, exist_ok=True)

def create_hd_eng_leong():
    file_path = os.path.join(pdf_dir, 'eng_leong_tin_can_manufacturing_poa.pdf')
    doc = SimpleDocTemplate(file_path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CompanyHeader',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1, # Center
        textColor=colors.HexColor('#002B49')
    )
    subtitle_style = ParagraphStyle(
        'CompanySub',
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#333333')
    )
    ref_style = ParagraphStyle('RefStyle', fontName='Helvetica-Bold', fontSize=10, leading=14)
    body_bold = ParagraphStyle('BodyBold', fontName='Helvetica-Bold', fontSize=9.5, leading=13.5)
    body_style = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=9.5, leading=13.5)

    elements = []

    # Header
    elements.append(Paragraph("ENG LEONG TIN CAN MANUFACTURING COMPANY SDN. BHD.", title_style))
    elements.append(Paragraph("(R.O.C. NO. 2435-D)", subtitle_style))
    elements.append(Paragraph("Lot 13, Jalan Industri 3/4, Rawang Integrated Industrial Park, 48000 Rawang, Selangor, Malaysia", subtitle_style))
    elements.append(Paragraph("Tel: +603-6092 1188 | Email: info@engleongtincan.com.my", subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#002B49'), spaceAfter=12))

    # Reference & Date
    ref_data = [
        [Paragraph("<b>Ref. No.:</b> KSM/100/2026/001502", body_style), Paragraph("<b>Date:</b> 29th July 2026", ParagraphStyle('RightDate', parent=body_style, alignment=2))]
    ]
    t_ref = Table(ref_data, colWidths=[280, 235])
    t_ref.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_ref)
    elements.append(Spacer(1, 10))

    # Recipient
    elements.append(Paragraph("<b>To:</b>", body_style))
    elements.append(Paragraph("<b>IRVING ENTERPRISE</b> (Recruiting Licence RL-215)<br/>Dhaka, Bangladesh", body_style))
    elements.append(Spacer(1, 12))

    # Subject
    subject_style = ParagraphStyle('Subj', fontName='Helvetica-Bold', fontSize=11, leading=14, alignment=1)
    elements.append(Paragraph("<u>RE: DEMAND LETTER FOR RECRUITMENT OF WORKERS FROM BANGLADESH</u>", subject_style))
    elements.append(Spacer(1, 10))

    opening_text = ("We hereby appoint your company, <b>IRVING ENTERPRISE (RL-215)</b>, as our authorized recruiting agent in Bangladesh "
                    "for the purpose of handling all recruitment matters and selecting <b>100 Male General Workers / Machine Operators</b> "
                    "for employment with our company under the following official terms and conditions:")
    elements.append(Paragraph(opening_text, body_style))
    elements.append(Spacer(1, 10))

    # Terms Table
    table_data = [
        [Paragraph("<b>No.</b>", body_bold), Paragraph("<b>Term / Particulars</b>", body_bold), Paragraph("<b>Specification / Official Approved Rate</b>", body_bold)],
        ["1.", "Job Category", "Factory General Worker / Machine Operator (Male)"],
        ["2.", "Number of Workers", "100 Male Workers"],
        ["3.", "Age Limit", "20 to 45 Years"],
        ["4.", "Contract Duration", "2 Years (Renewable for an additional 2 years)"],
        ["5.", "Basic Monthly Wage", "RM 1,500.00 (Calculated at 26 days × 8 hours/day)"],
        ["6.", "Attendance Allowance", "RM 50.00 / month"],
        ["7.", "Overtime (OT) Rate", "1.5× Normal Day | 2.0× Rest Day | Min. Monthly Gross: RM 2,393.70"],
        ["8.", "Working Hours & Days", "8 Hours per Day, 6 Days per Week"],
        ["9.", "Accommodation", "Free Employer-provided Hostel (with utilities compliant with Act 446)"],
        ["10.", "Medical & Insurance", "Workmen's Compensation & Foreign Worker Hospitalization Scheme (SPIKPA)"],
        ["11.", "Annual & Sick Leave", "8–16 Days Annual Leave | 14–22 Days Sick Leave (Tenure-based)"],
        ["12.", "Government Levy & Airfare", "Borne by Employer as per Malaysian Labour Regulations"]
    ]

    t_terms = Table(table_data, colWidths=[35, 160, 320])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F0F4F8')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    elements.append(t_terms)
    elements.append(Spacer(1, 15))

    # Declaration & Signatures
    closing_text = ("This demand letter is issued with full authorization from the Ministry of Human Resources (KESUMA) and Ministry of Home Affairs (MOHA). "
                    "All recruited workers shall abide by the laws and employment acts of Malaysia.")
    elements.append(Paragraph(closing_text, body_style))
    elements.append(Spacer(1, 25))

    sig_data = [
        [
            Paragraph("<b>Yours Faithfully,</b><br/>ENG LEONG TIN CAN MFG. CO. SDN. BHD.<br/><br/><br/>_____________________________________<br/><b>Authorized Signatory / Managing Director</b><br/>Company Stamp & Seal", body_style),
            Paragraph("<b>Attested By:</b><br/>BANGLADESH HIGH COMMISSION<br/>Kuala Lumpur, Malaysia<br/><br/><br/>_____________________________________<br/><b>First Secretary (Labour)</b><br/>Official High Commission Stamp", ParagraphStyle('RightSig', parent=body_style, alignment=2))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[260, 255])
    t_sig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_sig)

    doc.build(elements)
    print("Created HD Vector PDF: eng_leong_tin_can_manufacturing_poa.pdf")


def create_hd_cck_farm():
    file_path = os.path.join(pdf_dir, 'cck_farm_demand_letter.pdf')
    doc = SimpleDocTemplate(file_path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CompanyHeader', fontName='Helvetica-Bold', fontSize=14, leading=17, alignment=1, textColor=colors.HexColor('#1B5E20'))
    subtitle_style = ParagraphStyle('CompanySub', fontName='Helvetica', fontSize=9, leading=12, alignment=1, textColor=colors.HexColor('#333333'))
    body_bold = ParagraphStyle('BodyBold', fontName='Helvetica-Bold', fontSize=9.5, leading=13.5)
    body_style = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=9.5, leading=13.5)

    elements = []

    # Header
    elements.append(Paragraph("CCK FARM", title_style))
    elements.append(Paragraph("(Registration No.: IP0255555-W)", subtitle_style))
    elements.append(Paragraph("No. 11, Jalan Farmland, Kampung Raja, 39010 Cameron Highlands, Pahang Darul Makmur, Malaysia", subtitle_style))
    elements.append(Paragraph("Tel: +605-4983425 / +6013-529 2425", subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1B5E20'), spaceAfter=12))

    # Ref & Date
    ref_data = [
        [Paragraph("<b>Ref. No.:</b> CCK/AGRI/DEMAND/2026/08", body_style), Paragraph("<b>Date:</b> 5th February 2026", ParagraphStyle('RightDate', parent=body_style, alignment=2))]
    ]
    t_ref = Table(ref_data, colWidths=[280, 235])
    t_ref.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_ref)
    elements.append(Spacer(1, 10))

    # Recipient
    elements.append(Paragraph("<b>To:</b>", body_style))
    elements.append(Paragraph("<b>NAVIRA LIMITED</b> (Recruiting Licence RL-712)<br/>3 Shahid Tajuddin Ahmad Sarani, 5th Floor, Moghbazar, Dhaka-1217, Bangladesh", body_style))
    elements.append(Spacer(1, 12))

    # Subject
    subject_style = ParagraphStyle('Subj', fontName='Helvetica-Bold', fontSize=11, leading=14, alignment=1)
    elements.append(Paragraph("<u>RE: DEMAND LETTER FOR RECRUITMENT OF AGRICULTURAL WORKERS FROM BANGLADESH</u>", subject_style))
    elements.append(Spacer(1, 10))

    opening_text = ("We hereby appoint <b>NAVIRA LIMITED (RL-712)</b> to recruit <b>100 Bangladeshi Foreign Workers</b> "
                    "for employment at our Cameron Highlands farm operations under the following guaranteed salary and welfare terms:")
    elements.append(Paragraph(opening_text, body_style))
    elements.append(Spacer(1, 10))

    # Terms Table
    table_data = [
        [Paragraph("<b>No.</b>", body_bold), Paragraph("<b>Item / Category</b>", body_bold), Paragraph("<b>Guaranteed Contract Terms</b>", body_bold)],
        ["1.", "Job Category", "General Agriculture Worker (Crops & Farm Worker)"],
        ["2.", "Number of Workers", "100 Male Workers"],
        ["3.", "Age Range", "18 to 45 Years"],
        ["4.", "Contract Period", "2 + 1 Years (Renewable)"],
        ["5.", "Monthly Basic Salary", "RM 1,500.00 (26 Days × 9 Hours/day)"],
        ["6.", "Attendance Allowance", "RM 60.00 / month"],
        ["7.", "Overtime & Meal Allowance", "RM 518.00 / month"],
        ["8.", "Guaranteed Total Earnings", "<b>RM 2,000.00 / Month Minimum</b>"],
        ["9.", "Housing / Hostel", "Free Employer-provided Accommodation (Free Water & Electricity)"],
        ["10.", "Recruitment Cost & Levy", "100% Borne by Employer"],
        ["11.", "Annual & Sick Leave", "8 Days Annual Leave | 11 Paid Public Holidays | Paid Yearly Medical"]
    ]

    t_terms = Table(table_data, colWidths=[35, 160, 320])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8F5E9')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1B5E20')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#A5D6A7')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ]))
    elements.append(t_terms)
    elements.append(Spacer(1, 15))

    sig_data = [
        [
            Paragraph("<b>Yours Sincerely,</b><br/>CCK FARM MALAYSIA<br/><br/><br/>_____________________________________<br/><b>Managing Director / Proprietor</b><br/>Company Stamp & Seal", body_style),
            Paragraph("<b>Attested By:</b><br/>BANGLADESH HIGH COMMISSION<br/>Kuala Lumpur, Malaysia<br/><br/><br/>_____________________________________<br/><b>Labour Counsellor</b><br/>Official Seal", ParagraphStyle('RightSig', parent=body_style, alignment=2))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[260, 255])
    t_sig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_sig)

    doc.build(elements)
    print("Created HD Vector PDF: cck_farm_demand_letter.pdf")

    # Also build companion PDF
    file_path_bl2 = os.path.join(pdf_dir, 'cck_farm_bl2_companion.pdf')
    doc_bl2 = SimpleDocTemplate(file_path_bl2, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    doc_bl2.build(elements)
    print("Created HD Vector PDF: cck_farm_bl2_companion.pdf")


def create_hd_sampan_maju():
    file_path = os.path.join(pdf_dir, 'sampan_maju_enterprise_demand_letter.pdf')
    doc = SimpleDocTemplate(file_path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CompanyHeader', fontName='Helvetica-Bold', fontSize=14, leading=17, alignment=1, textColor=colors.HexColor('#B71C1C'))
    subtitle_style = ParagraphStyle('CompanySub', fontName='Helvetica', fontSize=9, leading=12, alignment=1, textColor=colors.HexColor('#333333'))
    body_bold = ParagraphStyle('BodyBold', fontName='Helvetica-Bold', fontSize=9.5, leading=13.5)
    body_style = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=9.5, leading=13.5)

    elements = []

    # Header
    elements.append(Paragraph("SAMPAN MAJU ENTERPRISE", title_style))
    elements.append(Paragraph("CONSTRUCTION & CIVIL ENGINEERING CONTRACTOR", subtitle_style))
    elements.append(Paragraph("4-B/14, Jalan Helang, Sungai Dua, 11700 Gelugor, Pulau Pinang, Malaysia", subtitle_style))
    elements.append(Paragraph("Tel: +6019-5794646 | Email: sampanmaju@gmail.com", subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#B71C1C'), spaceAfter=12))

    # Ref & Date
    ref_data = [
        [Paragraph("<b>Ref. No.:</b> SME/CONST/BD/2026/05", body_style), Paragraph("<b>Date:</b> 29th May 2026", ParagraphStyle('RightDate', parent=body_style, alignment=2))]
    ]
    t_ref = Table(ref_data, colWidths=[280, 235])
    t_ref.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_ref)
    elements.append(Spacer(1, 10))

    # Subject
    subject_style = ParagraphStyle('Subj', fontName='Helvetica-Bold', fontSize=11, leading=14, alignment=1)
    elements.append(Paragraph("<u>RE: DEMAND LETTER FOR RECRUITMENT OF 3,000 CONSTRUCTION WORKERS</u>", subject_style))
    elements.append(Spacer(1, 10))

    opening_text = ("Based on Ministry of Human Resources / Ministry of Home Affairs approval, we hereby appoint authorized Bangladeshi recruiting agencies "
                    "to recruit <b>3,000 Male Construction Workers</b> for infrastructural and building projects in Penang and Northern Malaysia:")
    elements.append(Paragraph(opening_text, body_style))
    elements.append(Spacer(1, 10))

    # Terms Table
    table_data = [
        [Paragraph("<b>No.</b>", body_bold), Paragraph("<b>Contract Terms</b>", body_bold), Paragraph("<b>Approved Specifications</b>", body_bold)],
        ["1.", "Job Category", "Construction General Labourer / Site Builder"],
        ["2.", "Number of Workers", "3,000 Male Workers"],
        ["3.", "Age Limit", "18 to 45 Years"],
        ["4.", "Contract Period", "5 Years (Renewable annually)"],
        ["5.", "Hourly Wage Rate", "<b>RM 9.00 / Hour</b>"],
        ["6.", "Working Hours & Schedule", "10 Hours / Day, 26 Days / Month"],
        ["7.", "Est. Monthly Income", "<b>RM 2,340.00 – RM 2,700.00 / Month</b>"],
        ["8.", "Accommodation & Transport", "Free Centralized Accommodation & Daily Site Transport"],
        ["9.", "Safety & Insurance", "CIDB Green Card Registration & Workmen's Compensation Scheme"],
        ["10.", "Return Airfare", "Single Return Airfare Provided upon Contract Completion"]
    ]

    t_terms = Table(table_data, colWidths=[35, 160, 320])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FFEBEE')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#B71C1C')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#FFCDD2')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ]))
    elements.append(t_terms)
    elements.append(Spacer(1, 20))

    sig_data = [
        [
            Paragraph("<b>Yours Sincerely,</b><br/>SAMPAN MAJU ENTERPRISE<br/><br/><br/>_____________________________________<br/><b>Project Director</b><br/>Company Stamp", body_style),
            Paragraph("<b>Attested By:</b><br/>BANGLADESH HIGH COMMISSION<br/>Kuala Lumpur, Malaysia<br/><br/><br/>_____________________________________<br/><b>Labour Attaché</b>", ParagraphStyle('RightSig', parent=body_style, alignment=2))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[260, 255])
    t_sig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_sig)

    doc.build(elements)
    print("Created HD Vector PDF: sampan_maju_enterprise_demand_letter.pdf")


def create_hd_al_rabeta():
    file_path = os.path.join(pdf_dir, 'al_rabeta_potential_region_demand_letter.pdf')
    doc = SimpleDocTemplate(file_path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CompanyHeader', fontName='Helvetica-Bold', fontSize=14, leading=17, alignment=1, textColor=colors.HexColor('#4A148C'))
    subtitle_style = ParagraphStyle('CompanySub', fontName='Helvetica', fontSize=9, leading=12, alignment=1, textColor=colors.HexColor('#333333'))
    body_bold = ParagraphStyle('BodyBold', fontName='Helvetica-Bold', fontSize=9.5, leading=13.5)
    body_style = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=9.5, leading=13.5)

    elements = []

    # Header
    elements.append(Paragraph("POTENTIAL REGION SDN BHD", title_style))
    elements.append(Paragraph("(Registration No.: 0229098-H / Fajarbaru Group)", subtitle_style))
    elements.append(Paragraph("Seremban, Negeri Sembilan, Malaysia", subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#4A148C'), spaceAfter=12))

    ref_data = [
        [Paragraph("<b>Ref. No.:</b> PRSB/AL_RI-ATH/PD_Ecofarm/001/26<br/><b>Govt Approval:</b> KSM H00000118 (Dated 17/09/2026)", body_style), Paragraph("<b>Date:</b> 27th September 2026", ParagraphStyle('RightDate', parent=body_style, alignment=2))]
    ]
    t_ref = Table(ref_data, colWidths=[320, 195])
    t_ref.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_ref)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>To:</b>", body_style))
    elements.append(Paragraph("<b>AL-RABETA INTERNATIONAL</b> (Recruiting Licence RL-354)<br/>36 Naya Paltan (2nd Floor), DIT Extension Road, Dhaka-1000, Bangladesh", body_style))
    elements.append(Spacer(1, 12))

    subject_style = ParagraphStyle('Subj', fontName='Helvetica-Bold', fontSize=11, leading=14, alignment=1)
    elements.append(Paragraph("<u>RE: DEMAND LETTER FOR RECRUITMENT OF WORKERS FROM BANGLADESH</u>", subject_style))
    elements.append(Spacer(1, 10))

    table_data = [
        [Paragraph("<b>No.</b>", body_bold), Paragraph("<b>Item</b>", body_bold), Paragraph("<b>Approved Terms</b>", body_bold)],
        ["1.", "Job Category", "Building & Property General Worker"],
        ["2.", "Number of Workers", "30 Male Workers"],
        ["3.", "Contract Period", "3 Years (Renewable)"],
        ["4.", "Basic Wage", "RM 1,500.00 / Month"],
        ["5.", "Housing & Transport", "Free Employer-provided Accommodation & Site Transport"],
        ["6.", "Levy & Visa", "Covered by Employer"]
    ]

    t_terms = Table(table_data, colWidths=[35, 160, 320])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3E5F5')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#4A148C')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E1BEE7')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ]))
    elements.append(t_terms)
    elements.append(Spacer(1, 25))

    sig_data = [
        [
            Paragraph("<b>Yours Faithfully,</b><br/>POTENTIAL REGION SDN BHD<br/><br/><br/>_____________________________________<br/><b>Director</b>", body_style),
            Paragraph("<b>Attested By:</b><br/>BANGLADESH HIGH COMMISSION<br/>Kuala Lumpur, Malaysia<br/><br/><br/>_____________________________________<br/><b>Labour Secretary</b>", ParagraphStyle('RightSig', parent=body_style, alignment=2))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[260, 255])
    t_sig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_sig)

    doc.build(elements)
    print("Created HD Vector PDF: al_rabeta_potential_region_demand_letter.pdf")


def create_hd_exelite():
    file_path = os.path.join(pdf_dir, 'exelite_resources_demand_employment_letter.pdf')
    doc = SimpleDocTemplate(file_path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CompanyHeader', fontName='Helvetica-Bold', fontSize=14, leading=17, alignment=1, textColor=colors.HexColor('#004D40'))
    subtitle_style = ParagraphStyle('CompanySub', fontName='Helvetica', fontSize=9, leading=12, alignment=1, textColor=colors.HexColor('#333333'))
    body_bold = ParagraphStyle('BodyBold', fontName='Helvetica-Bold', fontSize=9.5, leading=13.5)
    body_style = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=9.5, leading=13.5)

    elements = []

    elements.append(Paragraph("EXELITE RESOURCES SDN BHD", title_style))
    elements.append(Paragraph("Unit 97-2, 2nd Floor, NZX Commercial Centre, Jalan PJU 1A/41B, Ara Damansara, 47301 Petaling Jaya, Selangor, Malaysia", subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#004D40'), spaceAfter=12))

    elements.append(Paragraph("<b>Date:</b> 15th May 2026", body_style))
    elements.append(Spacer(1, 10))

    subject_style = ParagraphStyle('Subj', fontName='Helvetica-Bold', fontSize=11, leading=14, alignment=1)
    elements.append(Paragraph("<u>RE: DEMAND LETTER FOR RECRUITMENT OF FACTORY PRODUCTION OPERATORS</u>", subject_style))
    elements.append(Spacer(1, 10))

    table_data = [
        [Paragraph("<b>No.</b>", body_bold), Paragraph("<b>Item</b>", body_bold), Paragraph("<b>Terms</b>", body_bold)],
        ["1.", "Job Category", "Production Operator / Factory Worker"],
        ["2.", "Number of Workers", "1,000 Workers"],
        ["3.", "Contract Period", "3 Years"],
        ["4.", "Basic Wage", "RM 1,500.00 / Month"],
        ["5.", "Accommodation", "Free Employer-provided Hostel"]
    ]

    t_terms = Table(table_data, colWidths=[35, 160, 320])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E0F2F1')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#004D40')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B2DFDB')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ]))
    elements.append(t_terms)
    elements.append(Spacer(1, 25))

    sig_data = [
        [
            Paragraph("<b>Yours Faithfully,</b><br/>EXELITE RESOURCES SDN BHD<br/><br/><br/>_____________________________________<br/><b>Director</b>", body_style),
            Paragraph("<b>Attested By:</b><br/>MALAYSIA RECRUITMENT SERVICES<br/><br/><br/>_____________________________________<br/><b>Official Seal</b>", ParagraphStyle('RightSig', parent=body_style, alignment=2))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[260, 255])
    t_sig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_sig)

    doc.build(elements)
    print("Created HD Vector PDF: exelite_resources_demand_employment_letter.pdf")


def create_hd_osm():
    file_path = os.path.join(pdf_dir, 'agensi_pekerjaan_osm_demand_letter_template.pdf')
    doc = SimpleDocTemplate(file_path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('CompanyHeader', fontName='Helvetica-Bold', fontSize=14, leading=17, alignment=1, textColor=colors.HexColor('#1A237E'))
    subtitle_style = ParagraphStyle('CompanySub', fontName='Helvetica', fontSize=9, leading=12, alignment=1, textColor=colors.HexColor('#333333'))
    body_bold = ParagraphStyle('BodyBold', fontName='Helvetica-Bold', fontSize=9.5, leading=13.5)
    body_style = ParagraphStyle('BodyText', fontName='Helvetica', fontSize=9.5, leading=13.5)

    elements = []

    elements.append(Paragraph("AGENSI PEKERJAAN OSM SDN. BHD.", title_style))
    elements.append(Paragraph("(Registration No.: 962428-H | JTKSM Licence)", subtitle_style))
    elements.append(Paragraph("56G, Jalan PDR 5, Kawasan Perniagaan Desa Ria, 43300 Balakong, Selangor Darul Ehsan, Malaysia", subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1A237E'), spaceAfter=12))

    elements.append(Paragraph("<b>Date:</b> 15/05/2026", body_style))
    elements.append(Spacer(1, 10))

    subject_style = ParagraphStyle('Subj', fontName='Helvetica-Bold', fontSize=11, leading=14, alignment=1)
    elements.append(Paragraph("<u>RE: DEMAND LETTER FOR RECRUITMENT OF SERVICES & CLEANING WORKERS</u>", subject_style))
    elements.append(Spacer(1, 10))

    table_data = [
        [Paragraph("<b>No.</b>", body_bold), Paragraph("<b>Item</b>", body_bold), Paragraph("<b>Official Approved Terms</b>", body_bold)],
        ["1.", "Job Categories", "Commercial Cleaner / General Services Staff"],
        ["2.", "Contract Period", "2 Years (Renewable)"],
        ["3.", "Basic Salary", "RM 1,500.00 / Month"],
        ["4.", "Overtime & Benefits", "1.5× Normal OT Rate, Free Housing & Medical Insurance"]
    ]

    t_terms = Table(table_data, colWidths=[35, 160, 320])
    t_terms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E8EAF6')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1A237E')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#C5CAE9')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9.5),
    ]))
    elements.append(t_terms)
    elements.append(Spacer(1, 25))

    sig_data = [
        [
            Paragraph("<b>Yours Sincerely,</b><br/>AGENSI PEKERJAAN OSM SDN BHD<br/><br/><br/>_____________________________________<br/><b>Licensed Agency Director</b>", body_style),
            Paragraph("<b>Attested By:</b><br/>MINISTRY OF HUMAN RESOURCES (KESUMA)<br/>Malaysia<br/><br/><br/>_____________________________________<br/><b>Official Approval Stamp</b>", ParagraphStyle('RightSig', parent=body_style, alignment=2))
        ]
    ]
    t_sig = Table(sig_data, colWidths=[260, 255])
    t_sig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(t_sig)

    doc.build(elements)
    print("Created HD Vector PDF: agensi_pekerjaan_osm_demand_letter_template.pdf")


if __name__ == '__main__':
    print("Generating High-Definition, Crisp Vector PDF Demand Letters...")
    create_hd_eng_leong()
    create_hd_cck_farm()
    create_hd_sampan_maju()
    create_hd_al_rabeta()
    create_hd_exelite()
    create_hd_osm()
    print("All 7 High-Definition Vector PDFs generated successfully!")
