from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = [
    ROOT / "assets" / "CV_PR.pdf",
    ROOT / "assets" / "Pratikshya_Resume_oct025.pdf",
    ROOT / "astro-site" / "public" / "assets" / "CV_PR.pdf",
    ROOT / "astro-site" / "public" / "assets" / "Pratikshya_Resume_oct025.pdf",
]

INK = colors.HexColor("#18212b")
ACCENT = colors.HexColor("#1d6b73")
MUTED = colors.HexColor("#53616d")
LIGHT = colors.HexColor("#e7edef")


def styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name", parent=base["Title"], fontName="Helvetica-Bold",
            fontSize=22, leading=26, textColor=INK, alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "Contact", parent=base["Normal"], fontSize=8.5, leading=12,
            textColor=MUTED, alignment=TA_CENTER, spaceAfter=10,
        ),
        "section": ParagraphStyle(
            "Section", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=11, leading=14, textColor=ACCENT, spaceBefore=9,
            spaceAfter=5, keepWithNext=True,
        ),
        "heading": ParagraphStyle(
            "Heading", parent=base["Heading3"], fontName="Helvetica-Bold",
            fontSize=9.4, leading=12, textColor=INK, spaceBefore=4,
            spaceAfter=1, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontSize=8.6, leading=11.4,
            textColor=INK, spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontSize=8.1, leading=10.5,
            textColor=INK, leftIndent=10, firstLineIndent=-7, spaceAfter=2,
        ),
        "resume_heading": ParagraphStyle(
            "ResumeHeading", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=10.5, leading=13, textColor=ACCENT, spaceBefore=7,
            spaceAfter=4, keepWithNext=True,
        ),
        "resume_body": ParagraphStyle(
            "ResumeBody", parent=base["BodyText"], fontSize=9, leading=11.5,
            textColor=INK, spaceAfter=3,
        ),
        "resume_role": ParagraphStyle(
            "ResumeRole", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=9, leading=11, textColor=INK, spaceBefore=3,
            spaceAfter=1, keepWithNext=True,
        ),
    }


S = styles()


def p(text, style="body"):
    return Paragraph(text, S[style])


def bullets(items, style="small"):
    return [p(f"• {item}", style) for item in items]


def header(story, subtitle):
    story.extend([
        p("Pratikshya Regmi", "name"),
        p(
            "Raleigh, North Carolina  ·  pregmi3@ncsu.edu  ·  "
            '<link href="https://pratikshya-regmi.github.io/">Portfolio</link>  ·  '
            '<link href="https://github.com/Pratikshya-Regmi">GitHub</link>  ·  '
            '<link href="https://www.linkedin.com/in/pratiregmi/">LinkedIn</link>',
            "contact",
        ),
        p(subtitle, "body"),
    ])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LIGHT)
    canvas.line(doc.leftMargin, 0.48 * inch, letter[0] - doc.rightMargin, 0.48 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.3 * inch, "Pratikshya Regmi")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.3 * inch, f"{doc.page}")
    canvas.restoreState()


def make_cv(path):
    doc = SimpleDocTemplate(
        str(path), pagesize=letter, rightMargin=0.62 * inch,
        leftMargin=0.62 * inch, topMargin=0.55 * inch, bottomMargin=0.62 * inch,
        title="Pratikshya Regmi - Curriculum Vitae",
        author="Pratikshya Regmi",
    )
    story = []
    header(
        story,
        "Geospatial scientist and researcher working with LiDAR, UAS, satellite imagery, "
        "photogrammetry, terrain change, forest disturbance, and reproducible geospatial software.",
    )

    story.append(p("EDUCATION", "section"))
    story.append(p("<b>Ph.D. in Geospatial Analytics</b> · North Carolina State University, Raleigh, NC · Fall 2023–present", "heading"))
    story.extend(bullets([
        "Fourth-year Ph.D. candidate, Center for Geospatial Analytics. Expected graduation: May 2027.",
        "Research: reproducible fusion of LiDAR, UAS, and satellite imagery to study post-disaster landscape change and forest disturbance.",
        "Advisor: Dr. Helena Mitasova.",
    ]))
    story.append(p("<b>M.S. in Geospatial Systems Engineering</b> · Texas A&M University-Corpus Christi · August 2021–August 2023", "heading"))
    story.extend(bullets([
        "Thesis: Application of UAS Photogrammetry and Geospatial AI Techniques for Palm Tree Detection and Mapping.",
        "Advisor: Dr. Michael J. Starek.",
    ]))
    story.append(p("<b>B.E. in Geomatics Engineering</b> · Kathmandu University, School of Engineering, Dhulikhel, Nepal · 2014–2018", "heading"))
    story.extend(bullets([
        "Thesis: Analyzing the Effect of Image Overlap, Number of GCPs, and Their Distribution Pattern on Overall Accuracy of UAV Photogrammetry.",
        "Advisor: Dr. Uma Shankar Panday.",
    ]))

    story.append(p("RESEARCH AND PROFESSIONAL EXPERIENCE", "section"))
    roles = [
        ("Research Intern · Oak Ridge National Laboratory · Oak Ridge, TN · May–August 2026",
         ["Mentored by KC Cushman and Jitendra Kumar on “Assessing Forest Resistance, Delayed Canopy Loss, and Early Recovery Following Hurricane Helene.”"]),
        ("Graduate Research Assistant · North Carolina State University · 2023–present",
         ["Develop reproducible spatiotemporal Earth observation workflows for post-disaster mapping by integrating multi-temporal LiDAR, SfM point clouds, and imagery.",
          "Quantify terrain change and model drainage networks and flow paths using GRASS GIS and Python.",
          "Build reusable research software and prototype an LLM-assisted geospatial workflow to support more efficient analysis."]),
        ("Summer Research Assistant · Institute for Transportation Research and Education, NCSU · June–August 2024",
         ["Worked on parachute integration and deployment in Mavic drones for operations-over-people waivers and visibility analysis for safe UAS operation."]),
        ("Graduate Research Assistant · Texas A&M University-Corpus Christi · 2021–2023",
         ["Conducted UAS flights, processed imagery, developed 2D/3D web maps and dashboards in ArcGIS Online, and maintained TAMUCC’s historic UAS imagery site."]),
        ("Geomatics Engineer · NEA Engineering Company Limited · Kathmandu, Nepal · January–July 2021",
         ["Performed GIS mapping and satellite-based analysis to optimize transmission-line routes for cost, distance, and community benefit."]),
    ]
    for role, details in roles:
        story.append(p(role, "heading"))
        story.extend(bullets(details))

    story.append(p("RESEARCH COMMUNICATION AND WORKSHOPS", "section"))
    story.extend(bullets([
        "Hosted a two-hour clinic, Intro to GRASS GIS and Tangible Landscape, CSDMS Annual Meeting, University of Colorado Boulder, 2025.",
        "Hosted a two-hour clinic, Coastal Evolution Analysis and Inundation Modeling with GRASS GIS Using Jupyter Notebook, CSDMS Annual Meeting, Montclair State University, 2024.",
        "Geomorphic Impacts and Terrain Recovery After Hurricane Helene: A Multi-Sensor Geospatial Analysis in Western North Carolina, AGU Annual Meeting, New Orleans, 2025.",
        "Assessing the Potential of Large Language Models (LLMs) for Geospatial Analysis, IALE North America, Raleigh, 2025.",
        "Visibility Analysis for Safe UAS Operation, AGU Annual Meeting, Washington, DC, 2024.",
        "Simulating Wildfire Ash Transport Following a Precipitation Event by Coupling Dorado and Overland Flow, CSDMS Fall Webinar Series, 2024.",
        "Overview of the UAS Campus Survey Project at Texas A&M University-Corpus Christi, FIG Working Week, Orlando, 2023.",
        "Application of UAS Surveying and Geospatial AI to Detect and Monitor Palm Trees, TAMUCC Symposium, 2023.",
        "A Historical Perspective of UAS Monitoring for Campus Facilities and Geoinformatics, ASPRS Annual Conference, Denver, 2022.",
        "Analyzing the Effect of Distribution Pattern and Number of GCPs on UAV Photogrammetric Accuracy, UASG 2019, IIT Roorkee, India.",
    ]))

    story.append(PageBreak())
    story.append(p("PUBLICATIONS", "section"))
    publications = [
        "<b>Regmi, P., Mitasova, H.</b> (2024). <i>Visibility Analysis for Safe UAS Operation Using Lidar Datasets.</i> Presented at the AGU Annual Meeting.",
        "<b>Regmi, P.</b> (2023). <i>Application of UAS Photogrammetry and Geospatial AI Techniques for Palm Tree Detection and Mapping.</i> Master’s thesis, Texas A&M University-Corpus Christi.",
        "<b>Regmi, P., Starek, M. J., & Berryhill, J.</b> (2023). Overview of the UAS Campus Survey Project at Texas A&M University-Corpus Christi. <i>FIG Working Week 2023.</i>",
        "<b>Regmi, P., Starek, M. J., & Berryhill, J.</b> (2022). A Historical Perspective of UAS Monitoring for Campus Facilities and Geoinformatics at Texas A&M University-Corpus Christi. <i>ASPRS 2022 Annual Conference.</i>",
        "<b>Regmi, P., & Wagle, N.</b> (2021). Encroachment of Forest Cover in Chitwan and Parsa Districts of Nepal: A Spatiotemporal Quantification Over 25 Years. <i>Journal of Land Management and Geomatics Education, 3</i>, 7–12.",
        "<b>Awasthi, B., Karki, S., Regmi, P., Dhami, D. S., Thapa, S., & Panday, U. S.</b> (2020). Analyzing the Effect of Distribution Pattern and Number of GCPs on Overall Accuracy of UAV Photogrammetric Results. In <i>Proceedings of UASG 2019: Unmanned Aerial System in Geomatics, 1</i>, 339–354.",
        "<b>Awasthi, B., Karki, S., Regmi, P., Dhami, D. S., Thapa, S., & Panday, U. S.</b> (2019). Assessing the Overall Accuracy of UAV Photogrammetry: A Methodology for Different Combination of Imagery Parameters and Terrain Types. <i>Journal of Land Management and Geomatics Education, 1</i>, 22–32.",
    ]
    story.extend([p(item, "body") for item in publications])

    story.append(p("HACKATHONS", "section"))
    story.extend(bullets([
        "<b>NC PSI Hackathon, 2025 · Advanced Track winner.</b> Developed ML models combining climate and soil data to identify North Carolina’s climate-suitable crops, predict yields, and detect historical crop-failure events.",
        "<b>SAFE-MCP Hackathon, 2025.</b> Contributed threat-scenario, risk, mitigation, and detection documentation to an open-source security framework for tool-using AI systems.",
        "<b>NC PSI Hackathon, 2024 · Beginners Track participant.</b> Annotated crop and weed imagery and trained/evaluated deep-learning models, including YOLO.",
    ]))

    story.append(p("HONORS AND AWARDS", "section"))
    story.extend(bullets([
        "Women in GIS Award- 2025, selected from worldwide candidates by Women in GIS.",
        "University Graduate Fellowship, North Carolina State University, 2023.",
        "C.J. Davidson Scholarship, Texas A&M University-Corpus Christi, 2021–2023.",
        "Conrad Blucher Institute Scholarship, 2022.",
        "Geospatial Surveying Engineering Scholarship, 2021–2022.",
        "ASPRS Student Conference Presentation Grant, 2022.",
        "Best Paper Presented, Unmanned Aerial System in Geomatics Conference, IIT Roorkee, India, 2019.",
    ]))

    story.append(p("TECHNICAL SKILLS", "section"))
    story.extend(bullets([
        "<b>Programming:</b> Python, R, JupyterLab.",
        "<b>Earth observation:</b> satellite imagery, time-series indices including NDVI, change detection, LiDAR and point-cloud workflows, SfM photogrammetry.",
        "<b>Geospatial:</b> GRASS GIS, ArcGIS Pro, ArcGIS Online, QGIS, Google Earth Engine.",
        "<b>Photogrammetry and point clouds:</b> Agisoft Metashape, Pix4D, CloudCompare.",
        "<b>Machine learning:</b> model training and evaluation, computer vision, YOLO, transformers and self-supervised learning concepts.",
        "<b>Reproducibility and open source:</b> Git/GitHub, branches, pull requests, issue tracking, LaTeX, open-source geospatial software, SAFE-MCP documentation.",
    ]))

    story.append(p("SERVICE, OUTREACH, AND CERTIFICATIONS", "section"))
    story.extend(bullets([
        "President, Nepali Student Association, NCSU (2026–present).",
        "Vice President, Nepali Student Association, NCSU (2025–2026).",
        "Member, AGU H3S Subcommittee (2025–2026); Member, American Geophysical Union (2024–present).",
        "External Affairs Officer, Geospatial Graduate Student Organization (2024–2025).",
        "Member, American Society for Photogrammetry and Remote Sensing (2023–2024).",
        "STEM Resource Fair for K–12 students with disabilities at NCSU, 2024 and 2025; created hands-on activities about satellite imagery.",
        "AUVSI Trusted Operator, May 2025; FAA Part 107 Certified sUAS Remote Pilot, July 2024.",
        "Additional certifications include Esri spatial data science, ArcGIS Notebooks, regression analysis, hot-spot analysis, time-series clustering, and Python; University of Michigan Python and data science certificates; Stanford/DeepLearning.AI machine-learning certificates.",
    ]))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def make_resume(path):
    doc = SimpleDocTemplate(
        str(path), pagesize=letter, rightMargin=0.65 * inch,
        leftMargin=0.65 * inch, topMargin=0.58 * inch, bottomMargin=0.62 * inch,
        title="Pratikshya Regmi - Résumé", author="Pratikshya Regmi",
    )
    story = []
    header(
        story,
        "Geospatial scientist and researcher specializing in LiDAR, UAS, satellite imagery, "
        "photogrammetry, terrain change, and science communication.",
    )
    story.append(p("PROFILE", "resume_heading"))
    story.append(p(
        "Fourth-year Ph.D. candidate in Geospatial Analytics at North Carolina State University. "
        "I build reproducible geospatial workflows that combine Earth observation data, terrain and "
        "drainage modeling, point clouds, and open-source tools to communicate landscape change clearly.",
        "resume_body",
    ))

    story.append(p("EDUCATION", "resume_heading"))
    story.append(p("<b>Ph.D. in Geospatial Analytics</b> · North Carolina State University · Fall 2023–present · Expected May 2027", "resume_role"))
    story.append(p("Research on reproducible fusion of LiDAR, UAS, and satellite imagery for post-disaster landscape change and forest disturbance.", "resume_body"))
    story.append(p("<b>M.S. in Geospatial Systems Engineering</b> · Texas A&M University-Corpus Christi · August 2021–August 2023", "resume_role"))
    story.append(p("Thesis on UAS photogrammetry and geospatial AI for palm-tree detection and mapping.", "resume_body"))
    story.append(p("<b>B.E. in Geomatics Engineering</b> · Kathmandu University, Nepal · 2014–2018", "resume_role"))

    story.append(p("EXPERIENCE", "resume_heading"))
    for role, detail in [
        ("Research Intern · Oak Ridge National Laboratory · May–August 2026", "Studied forest resistance, delayed canopy loss, and early recovery following Hurricane Helene using repeat Earth observation data."),
        ("Graduate Research Assistant · North Carolina State University · 2023–present", "Develop LiDAR, SfM, and satellite-image workflows for post-disaster terrain change; model drainage and flow paths with GRASS GIS and Python; build reusable research code and prototype an LLM-assisted geospatial workflow."),
        ("Summer Research Assistant · Institute for Transportation and Research Education, NCSU · June–August 2024", "Worked on Mavic-drone parachute integration for operations-over-people waivers and visibility analysis for safe UAS operation."),
        ("Graduate Research Assistant · Texas A&M University-Corpus Christi · 2021–2023", "Conducted UAS flights, processed imagery, built 2D/3D web maps and dashboards, and maintained a historic UAS imagery site."),
        ("Geomatics Engineer · NEA Engineering Company Limited, Kathmandu, Nepal · January–July 2021", "Used GIS and satellite-based analysis to optimize transmission-line routes."),
    ]:
        story.append(p(role, "resume_role"))
        story.append(p(detail, "resume_body"))

    story.append(p("SELECTED RESEARCH COMMUNICATION", "resume_heading"))
    story.extend(bullets([
        "AGU 2025: Geomorphic Impacts and Terrain Recovery After Hurricane Helene.",
        "IALE North America 2025: Assessing the Potential of Large Language Models for Geospatial Analysis.",
        "AGU 2024: Visibility Analysis for Safe UAS Operation.",
        "CSDMS Annual Meetings 2024 and 2025: Delivered GRASS GIS and Tangible Landscape clinics.",
        "FIG Working Week 2023 and TAMUCC Symposium 2023: UAS surveying, web mapping, and geospatial AI.",
    ], "small"))

    story.append(p("SELECTED SKILLS", "resume_heading"))
    story.append(p(
        "<b>Tools:</b> Python, R, GRASS GIS, ArcGIS Pro/Online, QGIS, Google Earth Engine, "
        "Agisoft Metashape, Pix4D, CloudCompare, Git/GitHub, JupyterLab.<br/>"
        "<b>Methods:</b> LiDAR and point-cloud processing, SfM photogrammetry, satellite-image analysis, "
        "NDVI and change detection, terrain and drainage modeling, computer vision, reproducible workflows, "
        "and scientific communication.",
        "resume_body",
    ))

    story.append(p("HONORS AND LEADERSHIP", "resume_heading"))
    story.extend(bullets([
        "Women in GIS Award- 2025, selected from worldwide candidates by Women in GIS; University Graduate Fellowship, NCSU, 2023; ASPRS Student Conference Presentation Grant, 2022; Best Paper, UASG 2019.",
        "Advanced Track winner, NC PSI Hackathon 2025.",
        "President, Nepali Student Association at NCSU (2026–present); Vice President, Nepali Student Association at NCSU (2025–2026); AGU H3S Subcommittee member (2025–2026).",
        "FAA Part 107 Certified sUAS Remote Pilot, July 2024; AUVSI Trusted Operator, May 2025.",
    ], "small"))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    for output in OUTPUTS:
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.name == "CV_PR.pdf":
            make_cv(output)
        else:
            make_resume(output)
        print(output)
