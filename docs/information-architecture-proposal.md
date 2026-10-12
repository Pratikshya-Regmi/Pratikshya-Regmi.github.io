# Proposed information architecture and migration ledger

Status: approved by the user; implementation and verification recorded in information-architecture-validation.md. Audit date: 2026-09-23. Documentation only; no implementation, commit, push, merge, or deployment.

## Audit scope and limits

Inspected the Jekyll content and configuration, Astro routes, all 67 Markdown records in 11 collections, navigation, components, profile/location/pending data, asset inventory, alias generation, deployment workflow, and previous validation/privacy reports. Existing changes on `migration/astro-portfolio` are preserved.

The live homepage was readable at https://pratikshya-regmi.github.io/ and still shows the legacy site. Detail-page requests (extensionless, trailing slash, and .html) failed through the web tool; the local HTTP client also could not connect. This does not establish that the pages are broken. Detailed migration mapping is based on local Jekyll and Astro sources; fresh live-route verification remains required. Previous September 16 test results are historical evidence, not tests rerun for this proposal.

Astro is a static build in `astro-site/`, with base `/` and output `astro-site/dist/`. Keep that stack, near-black styling, existing optimized WebP imagery, Figure/Records/ProjectList components, and deferred Leaflet map. No new runtime framework is needed. There are currently 26 generated pages including 404 and four project detail pages. The desktop header has nine top-level controls including More and Contact; its destinations total 16, matching the flat mobile menu. Conference and symposium routes render subsets of the same presentation collection. The generic Records component often renders both a summary and a body containing the same prose.

## Proposed sitemap

Exactly seven primary navigation items:

| Navigation label | Canonical URL | Scope |
| --- | --- | --- |
| About | `/` | Combine homepage and About: concise biography, affiliation, research motivation/interests, selected photographs, location map, two featured-project links, CV/social/contact links, and a small set of referenced highlights. Preserve In Action and ?Field meets data science ? mapping the future.? |
| Education | `/education/` | Three degree institutions, linked timeline/map, full text fallback; clearly separate ESPIN short-course training from degrees. |
| Work & Research | `/work-research/` | Brief overview, two or three featured projects, selected research outputs, and seven secondary destinations below. |
| Honors & Awards | `/honors/` | Existing eight records; awards, scholarships/fellowship, and funding grouped only where helpful. |
| Community & Outreach | `/community/` | One page with Volunteering and Service, Media and Features, and GeoGiggles sections. |
| CV | `/cv/` | View CV and Download CV, public-safe document; distinguish the existing shorter resume as an employment document if retained. |
| Contact | `/contact/` | Public email, GitHub, LinkedIn, professional affiliation, and invitation to connect. |

Work & Research secondary navigation:

| Label | Destination | Design |
| --- | --- | --- |
| Experience | `/experience/` | Professional timeline, plus technical certifications below. |
| Projects | `/projects/` | Two or three featured studies, compact remaining project list with filters, then hackathons. |
| Presentations | `/presentations/` | All conference, symposium, and webinar records; optional type filters and stable event anchors. |
| Workshops | `/workshops/` | Both workshops, roles, photographs, recap links and materials; separate page justified by useful teaching resources. |
| Publications | `/Publications/` | Preserve case-sensitive URL; consistent citations and verified output types/statuses. |
| Hackathons | `/projects/#hackathons` | Two compact event case studies; retain team outputs and individual contribution where documented. |
| Certifications | `/experience/#certifications` | Compact categorized list of 17 source-backed credentials, rather than 17 cards. |

Keep all four `/projects/{id}/` case-study URLs. Logical section membership does not require changing existing URLs. This gives 16 substantive pages, plus 404, rather than 25 substantive pages plus 404. Alias pages are compatibility infrastructure and do not appear in navigation or sitemap.

The header stays at seven items. On Work & Research and its child pages, show a labeled secondary navigation that wraps on small screens. The compact mobile header exposes the seven items and an independently expandable Work & Research list; no hover dependency. Use normal links and progressive enhancement instead of JS-only tabs. Community sections use short in-page links. Keep essential information visible without opening maps or filters.

## Route migration

| Existing route | Action / destination |
| --- | --- |
| `/` | Retain; consolidate homepage and About content. |
| `/aboutme/` | Redirect to `/`; preserve biography, images and location information there. |
| `/education/`, `/experience/`, `/projects/`, `/projects/{id}/`, `/presentations/`, `/workshops/`, `/honors/`, `/Publications/`, `/contact/` | Retain; change navigation grouping and remove repeated prose. |
| `/conferences/` | Redirect to `/presentations/#conferences`. |
| `/symposiums/` | Redirect to `/presentations/#symposiums`. |
| `/hackathon/` | Redirect to `/projects/#hackathons`. |
| `/certifications/` | Redirect to `/experience/#certifications`. |
| `/engagement/` | Replace broad directory with `/community/`; research links belong in Work & Research. Redirect old route. |
| `/volunteer/`, `/service/` | Redirect to `/community/#volunteering-service`. |
| `/media/` | Redirect to `/community/#media-features`. |
| `/geogiggles/` | Redirect to `/community/#geogiggles`; preserve all three images, captions and participation invitation. |
| `/resume/` | Redirect to `/cv/`; document URLs retained. |
| `/blogs/` | Empty placeholder only; remove from navigation and redirect to `/community/#media-features`. No posts exist to migrate. |
| `/tags.html` | Keep compatibility to project topics/filter listing. |
| `/feed.xml` | Retain valid existing empty feed; do not invent posts. |
| `/404.html` | Retain useful recovery page, update its navigation links. |
| `/assets/CV_PR.pdf`, `/assets/Pratikshya_Resume_oct025.pdf`, existing image paths | Preserve public-safe document and image compatibility paths. |

Generate explicit aliases for legacy extensionless, slash and `.html` forms, including capitalized Publications. GitHub Pages static aliases use canonical metadata, a redirect and a visible fallback link, not server-side 301 rules. Preserve or translate existing record-ID fragments when merging pages; test old bookmarked event anchors. Rewrite internal links to canonical destinations. Update alias/sitemap generation, which currently assumes top-level pages plus projects, and exclude redirect URLs from sitemap.

## Content consolidation and canonical records

Retain all facts, meaningful prose, images, downloadable resources and meaningful links from both implementations. Remove repetition only; no event or research output is discarded. The per-record ledger below accounts for all 67 Astro records. Legacy-only links and nested activities are itemized separately.

Keep the existing collections where practical, but add stable cross-record references and type-specific fields (institution/degree/dates; employer/role; citation/authors/output type/status; credential issuer/date/URL; project role/method/results; media and related records). Split the multi-event hackathon/outreach/service Markdown into individual records without losing their text. Keep source/provenance and unresolved fields editable in structured content. Centralize navigation, redirects, location data, and unresolved confirmations.

Highlights become references, with short display excerpts and source links, rather than duplicate event records:

- IALE highlight -> IALE 2025 presentation -> geospatial AI project.
- CNR highlight -> CNR 2025 presentation -> UAS visibility project.
- CSDMS highlight -> 2025 workshop; retain its LinkedIn link, confirm its image because `csdms1.jpeg` is also used for the 2024 workshop.
- STEM highlight -> STEM fair service activity; retain the authentic photograph and pending original link.
- GRASS Developer Summit -> canonical open-source/community activity with its original update.
- PSI 2025 -> one hackathon record with award data; Honors references that award. UASG best paper and ASPRS grant likewise link to their related conference events.
- Publications and presentations remain distinct scholarly-output and event records, linked to each other and projects. A talk and its publication are not automatically the same item.
- Workshop institutional recaps appear as linked media features referencing the workshop; avoid copying the entire workshop story into Community.
- CEETLE teaching can be referenced in Experience while its service record remains canonical. Leadership and SAFE-MCP contributions can be referenced from About/Experience without duplicate narratives.

## Legacy and nested-content ledger

| Source / item | Destination and preservation policy |
| --- | --- |
| `index.html`, `aboutme.md`, About collection | Unified About homepage; retain professional story, scientific interests, FAA pilot background, research motivation, mentoring/open science and selected photographs. Detailed SAFE-MCP and PSI descriptions move to their canonical activities. |
| Empty `projects.md` | No authored legacy project text; retain all four Astro case studies. |
| `conferences.md` | All six presentations: AGU 2025, IALE 2025, AGU 2024, FIG 2023, ASPRS 2022, UASG 2019; preserve figures, locations, topics and source descriptions. |
| `symposiums.md` | 3MT 2026, Graduate Research Symposium 2026, CNR 2025, TAMUCC 2023 retained in Presentations. 3MT participation is not an award. |
| `workshops.md` | CSDMS 2025 and 2024, institutional recap URLs, photographs and both existing workshop repository links retained. |
| `Publications.md` | All seven citations and destinations retained; journal articles, proceedings, thesis and conference abstract distinguished. |
| `hackathon.md` | PSI 2025 climate/soil/crop ML pipeline and Advanced Track first place; PSI 2024 crop/weed task with 400 images, Roboflow and YOLO; both team photographs; existing Astro 2025 repository retained. Placeholder ARTICLE_URL becomes unresolved data, never a clickable link. |
| `volunteer.md` | STEM Resource Fair 2024/2025, Olds Elementary judging 2025, Tangible Landscape summer camp 2024, CEETLE teaching Dec 2020-Feb 2021, and motivation for inclusive outreach retained. |
| Service collection | AGU H3S 2025-26, Nepali Student Association vice presidency, Geospatial Graduate Student Organization External Affairs Officer, AGU membership, ASPRS membership, SAFE-MCP contribution preserved as service/professional community records. |
| `geogiggles.md` | All three humor images, descriptions/captions and invitation preserved; public contact email to be reconciled. |
| `_data/linkedin_post.yml` | All five updates retained by references; not limited to three displayed on live homepage. |
| `_config.yml`, Astro media page | Preserve LinkedIn tutorials/profile, YouTube channel, LinkedIn honors and credential destinations. A channel link is not presented as a verified interview or institutional feature. |
| `resume.md`, both PDFs | Independent CV destination; preserve compatible public-safe asset URLs and distinguish document editions. |
| `assets/img/`, `public/media/`, `images.json` | Preserve 28 legacy source images and existing optimized variants; reuse real assets. Correct misleading old image alt text without inventing captions. |
| Contact/profile data | NCSU public email, GitHub, LinkedIn, Raleigh affiliation retained; no personal street address or phone. |
| Templates/styles, search corpus, tags/feed, 404 | Infrastructure rather than additional authored content; retain useful compatibility, update generated navigation/search metadata if used, and avoid deploying stale duplicate content. |

## Duplicates, conflicts and missing content

1. Repeated presentation subset pages, Engagement directory, Media directory, empty Blog, duplicated summary/body prose, and standalone short hackathon/service/volunteer pages cause unnecessary navigation. Consolidation above addresses these.
2. Education contains three degrees plus ESPIN training, not four degrees. Existing map has only NCSU coordinates; TAMUCC and Kathmandu University coordinates are null. Hometown is unknown. Verify city/campus coordinates before adding markers and connect timeline selection to map details. Keep complete mobile/no-JS text.
3. ITRE dates conflict between CV and resume. Conrad Blucher Institute scholarship year conflicts (2022 vs 2021). Do not silently resolve either.
4. Profile records previous confirmation of fall 2023 start and fourth-year Ph.D. candidacy. Legacy About says Ph.D. student; old PDFs have ambiguous/anticipated dates. Use documented confirmed profile for web text and mark document editions; do not silently rewrite academic status or graduation dates.
5. All 17 certifications have titles, issuers and years in the migration, but no individual credential URLs. Preserve source-backed items; verify against the public-safe source documents and linked credentials before publication; unresolved verification stays in internal content data, not fabricated badges.
6. Publication records use generic ?Research output? and lack structured status/authors/year. Extract only supported metadata from existing citations and sources. Do not classify every item as a journal article or invent accepted/in-review work.
7. Several presentations have event names rather than paper titles as headings. Preserve their supplied topic/title, known coauthors, dates and presentation types. Missing exact dates, roles, coauthors, study areas or quantitative results remain unresolved. Hackathon descriptions describe team outputs; do not invent individual responsibilities.
8. LiDAR source data and metadata are absent. Keep authentic photographs and an honest pending-data state; no random point cloud. Detailed research figures, slides/posters, some photos and links remain pending. IALE wording ?Accessing? is source wording; do not silently change the title.
9. GeoGiggles uses a different Gmail address from the preferred NCSU profile address. Propose using NCSU consistently; retain the alternate as an unresolved content decision rather than assuming it is the preferred contact.
10. Historical privacy report flags sensitive versions of both PDFs in Git history despite sanitized working-tree copies. This proposal cannot certify the entire public repository as safe. Before publication, recheck current PDF copies and deployed documents; historical cleanup requires a separate review, since replacing working files does not erase Git history. Never include sensitive values in reports.
11. Unknown current end dates in CV-derived service roles, missing award significance/evidence, the hackathon article, STEM update URL, absent research visuals, and the distinct purpose/currentness of the resume remain content-confirmation fields.

## Implementation after approval

1. Add canonical record references, typed fields, redirect/navigation config and a centralized confirmation list; preserve sources and IDs in the migration ledger.
2. Implement the seven-item header, consolidated About and Community, Work & Research overview and secondary navigation; retain the near-black design and useful components.
3. Reorganize records, shorten repeated prose, link related work, add accessible map/timeline selection, and provide independent CV view/download actions.
4. Generate compatibility aliases and update canonical links, metadata, sitemap and test route lists.
5. Verify production build, content-ledger coverage, links/assets, PDF privacy, keyboard navigation, map/failure/no-JS fallbacks, reduced motion, and widths 320/375/768/1024/1440; review local production preview and subsequently an approved deployed preview. Recheck performance/accessibility rather than reusing previous scores.

No meaningful content is planned for deletion. Approval is for this restructuring plan; no commit, push, merge or deployment is performed in this audit.

## Complete Astro record ledger

Every current Markdown record appears below. ?Reference? means its original meaningful content and links are merged into the canonical activity, not discarded.

| Current record | Title | Proposed destination |
| --- | --- | --- |
| `certifications/certificate-1.md` | AUVSI Trusted Operator | /experience/#certifications |
| `certifications/certificate-10.md` | Optimal Facility Location Using ArcGIS Pro | /experience/#certifications |
| `certifications/certificate-11.md` | Introduction to the Crime Analysis Solution | /experience/#certifications |
| `certifications/certificate-12.md` | Space-Time Analysis: Time-Series Clustering | /experience/#certifications |
| `certifications/certificate-13.md` | Capstone: Retrieving, Processing & Visualizing Data with Python | /experience/#certifications |
| `certifications/certificate-14.md` | Machine Learning | /experience/#certifications |
| `certifications/certificate-15.md` | Neural Networks and Deep Learning | /experience/#certifications |
| `certifications/certificate-16.md` | Python Data Structures | /experience/#certifications |
| `certifications/certificate-17.md` | Python for Everybody: Getting Started | /experience/#certifications |
| `certifications/certificate-2.md` | FAA Part 107 Certified sUAS Remote Pilot | /experience/#certifications |
| `certifications/certificate-3.md` | Spatial Data Science: The New Frontier in Analytics | /experience/#certifications |
| `certifications/certificate-4.md` | ArcGIS Notebooks Basics | /experience/#certifications |
| `certifications/certificate-5.md` | Data Science Workflows Using ArcGIS Notebooks | /experience/#certifications |
| `certifications/certificate-6.md` | Introduction to ArcGIS API for Python | /experience/#certifications |
| `certifications/certificate-7.md` | Introduction to Regression Analysis Using ArcGIS Pro | /experience/#certifications |
| `certifications/certificate-8.md` | Mapping Clusters: Hot Spot & Outlier Analysis | /experience/#certifications |
| `certifications/certificate-9.md` | Crime Analysis: Tactical and Strategic | /experience/#certifications |
| `education/espin.md` | Earth Surface Processes Institute (ESPIN) | /education/ |
| `education/kathmandu.md` | B.E. in Geomatics Engineering | /education/ |
| `education/ncsu.md` | Ph.D. in Geospatial Analytics | /education/ |
| `education/tamucc.md` | M.S. in Geospatial Systems Engineering | /education/ |
| `engagement/geogiggles.md` | GeoGiggles | /community/#geogiggles |
| `engagement/hackathon.md` | Hackathons | /projects/#hackathons |
| `engagement/service.md` | Professional service | /community/#volunteering-service |
| `engagement/volunteer.md` | Outreach & STEM engagement | /community/#volunteering-service |
| `experience/itre.md` | Summer Research Assistant | /experience/ |
| `experience/ncsu.md` | Graduate Research and Teaching Assistant | /experience/ |
| `experience/nea.md` | Geomatics Engineer | /experience/ |
| `experience/tamucc.md` | Graduate Research Assistant | /experience/ |
| `highlights/highlight-1.md` | Participated in the 2025 GRASS Developer Summit | Reference: GRASS Summit -> /community/ |
| `highlights/highlight-2.md` | Reflecting on an Amazing Experience at the CSDMS Annual Meeting! | Reference: workshop-1 -> /workshops/ |
| `highlights/highlight-3.md` | Just wrapped up IALE North America 2025! | Reference: conference-2 -> /presentations/ |
| `highlights/highlight-4.md` | Volunteer at the “Reach for the Stars! Be a Star!” STEM Fair | Reference: STEM fair -> /community/ |
| `highlights/highlight-5.md` | Presented at the CNR 2025 Symposium! | Reference: symposium-3 -> /presentations/ |
| `honors/award-1.md` | N.C. PSI Hackathon — 1st Place, Advanced Track | /honors/ |
| `honors/award-2.md` | Women in GIS Award | /honors/ |
| `honors/award-3.md` | University Graduate Fellowship | /honors/ |
| `honors/award-4.md` | C.J. Davidson Scholarship | /honors/ |
| `honors/award-5.md` | Conrad Blucher Institute Scholarship | /honors/ |
| `honors/award-6.md` | Geospatial Surveying Engineering Scholarship | /honors/ |
| `honors/award-7.md` | ASPRS Student Conference Presentation Grant | /honors/ |
| `honors/award-8.md` | Best Paper Presented | /honors/ |
| `pages/about.md` | About | / |
| `presentations/conference-1.md` | AGU 2025 | /presentations/ |
| `presentations/conference-2.md` | IALE North America 2025 | /presentations/ |
| `presentations/conference-3.md` | AGU Annual Meeting 2024 | /presentations/ |
| `presentations/conference-4.md` | FIG Working Week 2023 | /presentations/ |
| `presentations/conference-5.md` | ASPRS Annual Conference 2022 | /presentations/ |
| `presentations/conference-6.md` | UASG-2019 Conference | /presentations/ |
| `presentations/symposium-1.md` | Three Minute Thesis Competition | /presentations/ |
| `presentations/symposium-2.md` | Graduate Research Symposium | /presentations/ |
| `presentations/symposium-3.md` | College of Natural Resources Graduate Research Symposium | /presentations/ |
| `presentations/symposium-4.md` | Research and Innovation Symposium | /presentations/ |
| `presentations/webinar.md` | Simulating Wildfire Ash Transport Following a Precipitation Event by Coupling Dorado and Overland Flow | /presentations/ |
| `projects/geospatial-ai.md` | A conversation with geospatial data | /projects/geospatial-ai/ |
| `projects/helene.md` | Reading a landscape after Hurricane Helene | /projects/helene/ |
| `projects/palm-mapping.md` | Mapping palms from the air | /projects/palm-mapping/ |
| `projects/uas-visibility.md` | Seeing terrain. Planning safer flights. | /projects/uas-visibility/ |
| `publications/publication-1.md` | Visibility Analysis for Safe UAS Operation Using Lidar Datasets | /Publications/ |
| `publications/publication-2.md` | Application of UAS Photogrammetry and Geospatial AI Techniques for Palm Tree Detection and Mapping | /Publications/ |
| `publications/publication-3.md` | Overview of the Uncrewed Aircraft System (UAS) Campus Survey Project at Texas A&M University-Corpus Christi | /Publications/ |
| `publications/publication-4.md` | A Historical Perspective of UAS Monitoring for Campus Facilities and Geoinformatics at Texas A&M University-Corpus Christi | /Publications/ |
| `publications/publication-5.md` | Encroachment of Forest Cover in Chitwan and Parsha Districts of Nepal: A Spatiotemporal Quantification Over 25 Years | /Publications/ |
| `publications/publication-6.md` | Analyzing the Effect of Distribution Pattern and Number of GCPs on Overall Accuracy of UAV Photogrammetric Results | /Publications/ |
| `publications/publication-7.md` | Assessing the Overall Accuracy of UAV Photogrammetry: A Methodology for Different Combination of Imagery Parameters and Terrain Types | /Publications/ |
| `workshops/workshop-1.md` | GRASS GIS and Tangible Landscape for a Global Audience | /workshops/ |
| `workshops/workshop-2.md` | Intro to GRASS GIS for Coastal Hazard Analysis | /workshops/ |
