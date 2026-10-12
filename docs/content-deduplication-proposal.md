# Content deduplication audit and approval proposal

Status: revised by user clarification. Publications and Presentations may overlap and remain separate. Only unifying the conference/symposium/webinar display under Presentations is approved and implemented. The broader consolidation below remains an unimplemented proposal; proposed publication merges are superseded and will not be performed.

## Scope and findings

Reviewed all 67 records in 11 Astro collections, all nine page templates (including dynamic routes), the seven JSON data files, shared rendering/navigation/map components, legacy Jekyll pages and data, and the existing generated HTML. Generated output is corroborating evidence, not a fresh build. Current source is authoritative where it differs from earlier reports.

The previous navigation consolidation did not finish content deduplication. Four highlights have reference fields but still retain copied titles, summaries, images and links. The fifth, GRASS Summit, is rendered in full on both Home and Community. ProjectList repeats the same project descriptions/photos on Home, Work & Research and Projects; detail pages repeat the photograph again. Four project photographs are also presentation photographs. Several summary fields repeat their own Markdown bodies. The current PSI 2025 body still repeats its award despite a separate Honors record.

Distinguish identity from relationship: one research project can produce several genuinely distinct presentations and a publication. Keep the project narrative once, the event-specific details once per event, and a bibliographic citation once per distinct scholarly output. Cross-links must not repeat those narratives, figures or metadata. A published abstract that merely documents the same presentation need not become a second full card.

Path shorthand below: `C/` = `astro-site/src/content/`; `P/` = `astro-site/src/pages/`; `D/` = `astro-site/src/data/`. Root `.md` files and `_data/linkedin_post.yml` are legacy Jekyll sources, not additional Astro routes.

## Item-by-item proposed consolidation

### 1. Hurricane Helene research

- **Current copies/overlap:** `C/projects/helene.md`, `C/presentations/conference-1.md` (AGU 2025), `C/presentations/symposium-2.md` (2026 Graduate Research Symposium), `C/experience/ncsu.md`; root `conferences.md`, `symposiums.md`; ProjectList on `/`, `/work-research/`, `/projects/`, and `/projects/helene/`; the hardcoded 2026 homepage highlight.
- **Canonical research title/category/location:** “Reading a landscape after Hurricane Helene” — Projects, `/projects/helene/`. Move all study-area, data/method and mapped-change descriptions here: Chimney Rock/western North Carolina; 2017 and November 2024 LiDAR; October 2024 SfM; elevation change, debris, drainage and infrastructure context. Preserve the stated contribution and existing uncertainty about quantitative results.
- **Distinct presentations retained:** the supplied AGU title “Geomorphic Impacts and Terrain Recovery After Hurricane Helene: A Multi-Sensor Geospatial Analysis in Western North Carolina” — Presentations, AGU 2025, New Orleans. Preserve `AGU.jpeg` there only. Keep the 2026 Graduate Research Symposium as its own Presentations entry with poster type, NCSU host, CGA nomination, personal reflection, and `graduate_symposium.JPG`. Do not invent its missing exact poster title or coauthors.
- **Links/actions:** reciprocal Related project/presentation links to exact records. Remove methods paragraphs and shared photo from the presentation/project copies as appropriate; remove full project cards from Home/overview/index, replacing them with compact linked titles. Remove the hand-authored combined 2026 highlight. Retain employment duties under Experience without copying the project narrative.

### 2. UAS visibility research, AGU 2024 abstract and CNR 2025

- **Current copies/overlap:** `C/projects/uas-visibility.md`, `C/presentations/conference-3.md`, `C/presentations/symposium-3.md`, `C/publications/publication-1.md`, `C/highlights/highlight-5.md`, `C/experience/itre.md`; root `conferences.md`, `symposiums.md`, `Publications.md`, `_data/linkedin_post.yml`; Home/overview/project listings and Work & Research's abstract link.
- **Canonical project:** “Seeing terrain. Planning safer flights.” — Projects, `/projects/uas-visibility/`; retain terrain/visibility research question, LiDAR methods and documented contribution here only.
- **Canonical AGU presentation:** “Visibility Analysis for Safe UAS Operation Using Lidar Datasets” — Presentations, `/presentations/#conference-3`; retain the shorter source title as an alternate title. Merge the abstract-only `publication-1` into this event: preserve **Regmi, P.; Mitasova, H.**, 2024, Washington DC, AGU name, ADS abstract URL and citation, `agu1.jpg`, and missing-material status. Its source explicitly describes a presented contribution, not a separate journal article. Redirect its old publication anchor to this record; no duplicate abstract card in Publications.
- **Canonical CNR presentation:** “Visibility Analysis for Safe UAS Operation” — Presentations, `/presentations/#symposium-3`; preserve 2025 CNR/NCSU host, original reflection, LinkedIn update, and both distinct photographs `cnrsyposim1.jpg` and `cnr.jpg` in one event gallery. Merge/remove `highlight-5`.
- **Links/actions:** link the two distinct presentations to the project; do not merge the events. ITRE retains parachute/Mavic/operations-over-people duties and disputed date note. The exact attribution of visibility work to this appointment needs confirmation before presenting that employment-to-project relationship as established.

### 3. Geospatial AI / IALE 2025

- **Current copies/overlap:** `C/projects/geospatial-ai.md`, `C/presentations/conference-2.md`, `C/highlights/highlight-3.md`, `C/experience/ncsu.md`, About references; root `aboutme.md`, `conferences.md`, `_data/linkedin_post.yml`; four project placements plus homepage presentation highlight.
- **Canonical project:** “A conversation with geospatial data” — Projects, `/projects/geospatial-ai/`; retain natural-language GIS question, GRASS GIS integration, documented tool/function calling and retrieval methods, missing evaluation/demo information.
- **Canonical presentation:** “Accessing the Potential of Large Language Models (LLMs) for Geospatial Analysis” — Presentations, `/presentations/#conference-2`; retain exact supplied wording, IALE North America 2025, Raleigh, digital visualization showcase type, LinkedIn link and `iale.jpeg` once here. Merge the highlight's maps-and-explanations detail into the project, without duplicating it in the event.
- **Links/actions:** merge/remove `highlight-3`; project and event link reciprocally. No repeated IALE card, full description or photograph on Home/overview/project pages. Do not silently change “Accessing” to “Assessing.”

### 4. Palm mapping research / master's thesis / TAMUCC symposium

- **Current copies/overlap:** `C/projects/palm-mapping.md`, `C/publications/publication-2.md`, `C/presentations/symposium-4.md`, `C/education/tamucc.md`, `C/experience/tamucc.md`; root `Publications.md`, `symposiums.md`, `aboutme.md`; project index/detail.
- **Canonical project:** “Mapping palms from the air” — Projects, `/projects/palm-mapping/`; research question, UAS photogrammetry/deep learning methods and role once.
- **Distinct outputs retained:** “Application of UAS Photogrammetry and Geospatial AI Techniques for Palm Tree Detection and Mapping” — Publications, `/Publications/#publication-2`; retain Regmi, 2023, master's-thesis type, institution and ProQuest link once as a citation. “Research and Innovation Symposium” — Presentations, `/presentations/#symposium-4`; retain TAMUCC 2023 participation, documented palm-detection topic and `tamuccsympo.jpg` once. Exact presentation title remains unconfirmed.
- **Links/actions:** Education retains degree/dates and advisor Dr. Michael J. Starek, linking to the thesis instead of maintaining another full thesis title/description. Employment retains flights, imagery processing, ArcGIS web maps/dashboards and historical-site responsibilities. The specific employment-to-thesis relationship needs stronger provenance; keep it flagged. Do not confuse the campus survey work below with palm mapping simply because both involve TAMUCC/UAS.

### 5. FIG Working Week 2023 campus survey

- **Current copies/overlap:** `C/presentations/conference-4.md`, `C/publications/publication-3.md`; root `conferences.md`, `Publications.md`; potentially related TAMUCC employment but no explicit event relationship established by that role text.
- **Canonical publication:** “Overview of the Uncrewed Aircraft System (UAS) Campus Survey Project at Texas A&M University-Corpus Christi” — Publications, `/Publications/#publication-3`; preserve authors **Regmi, P.; Starek, M. J.; Berryhill, J.**, year 2023, proceedings venue and FIG PDF. Consolidate research/education/planning summary here.
- **Presentation retained as a distinct event:** same paper title obtained by reference, FIG Working Week 2023, Orlando, and `fig2.jpg`, at `/presentations/#conference-4`. No second campus-survey explanation. Preserve the stated presentation contribution in the event record.
- **Links/actions:** Related publication/presentation only. Do not create a new Projects entry or merge into palm mapping without confirmation.

### 6. ASPRS 2022 campus monitoring and grant

- **Current copies/overlap:** `C/presentations/conference-5.md`, `C/publications/publication-4.md`, `C/honors/award-7.md`; root `conferences.md`, `Publications.md`.
- **Proposed canonical presentation:** “A Historical Perspective of UAS Monitoring for Campus Facilities and Geoinformatics at Texas A&M University-Corpus Christi” — Presentations, `/presentations/#conference-5`; preserve Denver, 2022, ASPRS, **Regmi, P.; Starek, M. J.; Berryhill, J.**, ResearchGate URL, historical-monitoring description and missing-photo/material notes.
- **Conditional consolidation:** `publication-4` is currently only labeled Conference contribution. It does not establish whether a distinct published paper exists. Proposed merge into the presentation if it is the same talk/abstract; if you confirm a separate publication, retain only its citation in Publications and cross-link. **Await confirmation; do not delete this record on an assumption.**
- **Separate award retained:** “ASPRS Student Conference Presentation Grant” — Honors & Awards, `/honors/#award-7`; ASPRS and 2022 once, linked to the event. Replace the award claim repeated in the talk paragraph with Related award.
- Do not merge this 2022 contribution with the different 2023 FIG work merely because both describe campus UAS monitoring.

### 7. UASG 2019 presentation / 2020 chapter / best-paper award

- **Current copies/overlap:** `C/presentations/conference-6.md`, `C/publications/publication-6.md`, `C/honors/award-8.md`, thematic overlap with `C/education/kathmandu.md` and `C/publications/publication-7.md`; root `conferences.md`, `Publications.md`.
- **Canonical publication:** “Analyzing the Effect of Distribution Pattern and Number of GCPs on Overall Accuracy of UAV Photogrammetric Results” — Publications, `/Publications/#publication-6`. Preserve **Awasthi, B.; Karki, S.; Regmi, P.; Dhami, D. S.; Thapa, S.; Panday, U. S.**, publication year **2020**, UASG 2019 proceedings, volume 1, pages 339–354 and Springer DOI link.
- **Distinct presentation:** same title by reference, UASG **2019**, IIT Roorkee, India and `UASG.jpg` — Presentations, `/presentations/#conference-6`. Put the GCP-method description in the publication record, not both entries.
- **Distinct honor:** “Best Paper Presented — UASG 2019” — Honors & Awards, `/honors/#award-8`, linked to the presentation; remove duplicate award wording elsewhere.
- **Do not merge:** the 2019 journal article “Assessing the Overall Accuracy of UAV Photogrammetry: A Methodology for Different Combination of Imagery Parameters and Terrain Types” (`publication-7`) is a different title/output with pages 22–32 and its own journal link. Undergraduate thesis relationship to these outputs needs confirmation; retain its unique title, advisor and degree information.

### 8. CSDMS 2025 workshop / social update / institutional feature / hero

- **Current copies/overlap:** `C/workshops/workshop-1.md`, `C/highlights/highlight-2.md`, `P/community.astro` media links, `P/index.astro` hero image; root `workshops.md`, `_data/linkedin_post.yml`; workshop repository hardcoded in `P/[section].astro`.
- **Canonical:** “GRASS GIS and Tangible Landscape for a Global Audience” — Workshops, `/workshops/#workshop-1`.
- **Preserve:** May 2025, CSDMS/University of Colorado Boulder, global audience, hands-on physical interface, hydrology/flood-modeling details from the highlight, environmental simulations, the LinkedIn update, NC State recap and `csdms-grass-2025` repository. Keep `IMG_0110.jpg` only in this workshop's gallery.
- **Actions:** merge/remove `highlight-2`; move repository into the record. Community may have one small Related workshop link, not another dated workshop-feature listing. Replace the duplicate workshop hero photograph with the existing original In Action `cover.jpg`, retaining the verified tagline and without adding an invented caption.
- **Confirmation:** `highlight-2` assigns `csdms1.jpeg` to 2025, but workshop-2 assigns it to 2024. Preserve the asset, flag the conflicting attribution, and do not attach it to a second event until confirmed.

### 9. CSDMS 2024 workshop / institutional feature

- **Current copies/overlap:** `C/workshops/workshop-2.md`, `P/community.astro`, root `workshops.md`; repository in `P/[section].astro`; photo also used by the 2025 highlight above.
- **Canonical:** “Intro to GRASS GIS for Coastal Hazard Analysis” — Workshops, `/workshops/#workshop-2`.
- **Preserve:** May 2024, CSDMS, Montclair location wording, student-led role, open-source GIS learning description, NC State recap and `csdms-grass-2024` repository. Retain current photo attribution as explicitly unresolved until confirmed.
- **Actions:** remove repeated media-feature metadata from Community; keep a small link if useful. Keep 2024 and 2025 workshops separate: different years, settings and teaching content. Likewise do not merge the CSDMS wildfire webinar or summer-camp outreach into these workshops.

### 10. GRASS Developer Summit 2025

- **Current copies/overlap:** `C/highlights/highlight-1.md`, full paragraph rendered by `P/index.astro` and `P/community.astro`; `_data/linkedin_post.yml`.
- **Canonical:** “GRASS Developer Summit 2025” — Community & Outreach, one new activity record and anchor.
- **Preserve:** 2025 participation, personal reflection on learning from the open-source community, original LinkedIn URL and missing-photograph status (`grass1.jpg` is an unresolved legacy reference).
- **Actions:** migrate `highlight-1` into Community; remove its Highlights record. Home may link to it by canonical ID and title only. Do not describe participation as a workshop delivered, presentation, or award.

### 11. STEM Resource Fair 2024/2025

- **Current copies/overlap:** part of `C/engagement/volunteer.md`, `C/highlights/highlight-4.md`, root `volunteer.md`, `_data/linkedin_post.yml`.
- **Canonical:** “STEM Resource Fair — Reach for the Stars! Be a Star!” — Community & Outreach, one activity record with documented participation in 2024 and 2025.
- **Preserve:** K–12 students with disabilities, hands-on geospatial/drone demonstrations, 2025 storytelling detail, `stem2.jpg`, and missing original-update URL. Preserve inclusive-outreach motivation without repeating it in every activity.
- **Actions:** split this activity out of the omnibus volunteer record; merge/remove `highlight-4`. Do not attach its photograph or missing-link warning to unrelated volunteer activities. Keep Olds Elementary judging, summer camp and CEETLE as distinct activity records.

### 12. PSI Hackathon 2025 and its award

- **Current copies/overlap:** `C/engagement/hackathon.md`, `C/honors/award-1.md`, legacy `hackathon.md` and `aboutme.md`; About's link is already appropriately small.
- **Canonical activity:** “N.C. PSI Hackathon 2025” — Hackathons, a dedicated record under `/projects/#hackathons` with its own stable anchor.
- **Preserve:** October 2025, NC Plant Sciences Initiative, climate/soil/crop outcome task, reproducible ML pipeline, EDA/feature engineering/baselines/Random Forest/XGBoost, explainability and decision-ready outputs, existing repository, `psi_hacka.png` and missing article link. Preserve team attribution; individual contribution is not fully specified.
- **Canonical achievement:** “N.C. PSI Hackathon — 1st Place, Advanced Track” — Honors & Awards, `/honors/#award-1`; retain awarding organization/year/rank only here. Reciprocal Related award/hackathon links, no repeated winner claim in the activity body.
- **Actions:** split the two-event hackathon file, not merge its two years. Keep PSI 2024 separate, preserving October 2024, 400 annotated images, crop/weed classification, Roboflow, YOLO, learning reflection and `hackathon.jpg`.

### 13. 3MT 2026 and combined homepage highlight

- **Current copies/overlap:** `C/presentations/symposium-1.md`, root `symposiums.md`, hardcoded “Three Minute Thesis & Graduate Research Symposium” card in `P/index.astro`.
- **Canonical:** “Three Minute Thesis Competition” — Presentations, `/presentations/#symposium-1`.
- **Preserve:** 2026, NCSU College of Natural Resources, the personal story about distilling three years of research into three minutes, public communication, and `3mt.jpg`. No award is claimed.
- **Actions:** remove the combined homepage card. These are two distinct events, not one activity. If one is featured, choose its canonical ID. No project relationship is established for 3MT; do not infer it from the neighboring Helene symposium entry.

### 14. Employment, service, credentials and educational context

- `C/experience/ncsu.md`, `itre.md`, `tamucc.md`, `nea.md` remain four **Professional Experience** records. Preserve employer, role, dates, teaching and unique responsibilities. Remove copied case-study explanations and retain verified related links. Do not merge employment into a project.
- `C/engagement/service.md` contains six distinct items: AGU H3S, Nepali Student Association vice presidency, GSGO External Affairs, AGU membership, ASPRS membership, and SAFE-MCP contribution. Split into **Community & Outreach** records with their existing dates and contribution details. About keeps only its existing small SAFE-MCP link. Membership and committee service remain distinct.
- `C/engagement/volunteer.md` also contains Olds Elementary judging (2025, grades 3–5), Tangible Landscape summer camp (2024, runoff/pond/buffer exercise), and CEETLE teaching (Dec 2020–Feb 2021, virtual Nepal, host, AoT streaming data and school audience). Preserve each separately in **Community & Outreach**, along with the STEM fair above. Do not duplicate CEETLE as an employment entry without confirmation of that classification.
- No duplicate activity records found among the 17 certifications. Retain separately under Experience as approved; similar Python/GIS course names do not establish duplication. FAA qualification in About becomes a short link rather than a second credential record.
- Degree records remain in Education; the eight requested activity categories do not justify recategorizing degrees. ESPIN is training, not a degree; it remains under Education. The user confirmed Workshops is for delivered workshops, so do not move attended training there or create a second ESPIN record.

## Rendering and shared-data duplication to remove

| Source | Proposed change |
| --- | --- |
| `P/index.astro`, `P/work-research.astro`, `P/[section].astro`, `components/ProjectList.astro`, `P/projects/[id].astro` | Keep full case study only at its detail URL. Project index and curated previews use title links only; no copied description, tag block or presentation photo. Remove the overview's second “Research, shared” teaser set where it repeats the same selected items. |
| `C/highlights/highlight-1..5.md`, `content.config.ts` | Merge unique details as above, then remove the content-owning Highlights collection. Replace with a small homepage configuration containing only validated collection/record IDs and order. No separate title, summary, date, image or URL copies. |
| `P/[section].astro`, `C/presentations/*` | One Presentations list with event/type fields. Remove visible Conferences/Symposiums/Webinars section navigation and separate blocks; optional accessible filters may use actual event/type data. Preserve old routes/anchors as compatibility links, not independent content pages. |
| Presentation/workshop frontmatter + body | Store event/host/date/location/type once; remove matching HTML metadata paragraphs and copied summary fields. Keep unique personal reflections or abstracts in one body field. |
| `C/publications/*`, `components/Records.astro` | Store citation fields once and render one citation per output. Avoid printing a title heading and then the same title again inside a full citation. Coauthors, DOI/source URLs, pages and years remain intact. |
| `P/community.astro` | Media section uses small canonical links only when useful; no second workshop/event listing. Professional channel links and GeoGiggles remain. |
| `D/profile.json`, `C/pages/about.md`, `C/education/ncsu.md`, `D/locations.json`, Home/Contact/CV/footer | Use references for current role, affiliation and campus. Location data owns coordinates/city; education owns degrees/dates/advisors; profile owns public contact/preferred descriptor. Map marker links to the same timeline detail rather than another full degree summary. Keep contact navigation usable; repeated navigation is not a second content record. |
| `D/pending.json`, `D/confirmations.json`, `components/LidarPlaceholder.astro` | One internal confirmation/status source; stop repeating long future-viewer feature descriptions on Home and both projects. No artificial LiDAR or missing results. |
| `D/navigation.json`, Base layout, overview link index | Keep one seven-item primary menu and one research subsection menu. Remove the overview's redundant seven-link index when it merely repeats the visible secondary navigation. Retain necessary contextual back/related links. |
| `D/images.json`, public media variants | Keep one asset identity/owner and responsive variants. Resized WebPs are not different photographs or duplicate content records. Do not delete original images while removing repeated display placements. |
| `D/redirects.json`, legacy template, aliases/feed/sitemap | Retain compatibility redirects and anchors. Redirect pages are not duplicate entries. Retired record anchors need explicit mapping, particularly `publication-1`; preserve historical links. |

**Photograph ownership:** `AGU.jpeg` → AGU 2025 presentation; `agu1.jpg` → AGU 2024 presentation; `iale.jpeg` → IALE presentation; `tamuccsympo.jpg` → TAMUCC symposium; `cnrsyposim1.jpg` and `cnr.jpg` → the one CNR 2025 event; `IMG_0110.jpg` → CSDMS 2025 workshop; `stem2.jpg` → STEM fair; PSI photos → their own years. `csdms1.jpeg` remains attribution-pending. Projects use unique approved research figures only when available; they can be text-first meanwhile. Preserve hero “Field meets data science — mapping the future.” with the original In Action image rather than repeating the workshop photograph.

## Items not to merge

- AGU 2024, AGU 2025, IALE 2025, CNR 2025, Graduate Research Symposium 2026, TAMUCC 2023, FIG 2023, ASPRS 2022, UASG 2019 and 3MT 2026 are distinct events.
- CSDMS 2024 workshop, CSDMS 2025 workshop, 2024 wildfire ash-transport webinar and ESPIN training are distinct activities. No extra wildfire project relationship is verified.
- The two PSI hackathons have different years/tasks; keep separate.
- Forest-cover article `publication-5` has no verified overlapping project/event and remains a distinct Publications entry, preserving Regmi/Wagle, 2021, journal volume 3/pages 7–12 and PDF link.
- The 2019 UAV accuracy journal article and 2020 UASG chapter are distinct outputs, even with overlapping authors/methods.
- Women in GIS, University Graduate Fellowship, C.J. Davidson, Conrad Blucher Institute and Geospatial Surveying Engineering scholarships remain distinct Honors & Awards records. Preserve recurring award years; do not collapse distinct granting organizations.
- GeoGiggles remains one Community feature with three distinct images; no duplicate activity found.

## Confirmations needed; no unsupported merges

1. Is the ASPRS 2022 ResearchGate item a distinct published paper/proceeding, or only the presentation/abstract? Its proposed consolidation stays conditional.
2. Which event/year does `csdms1.jpeg` show? Current sources assign it to different workshops.
3. Confirm the specific ITRE-to-visibility and TAMUCC-employment-to-palm-thesis relationships before treating those existing links as established attribution. Existing vague “CV and website” provenance is insufficient to strengthen them.
4. Do the undergraduate thesis, 2019 journal article and 2020 UASG chapter share a verified project? Keep separate unless confirmed.
5. Resolved by user: Workshops is exclusively for workshops delivered by Pratikshya. ESPIN training remains under Education and must not be moved to Workshops.

Missing exact presentation titles, coauthors, dates and other existing gaps remain flagged; this audit does not invent values. Earlier ITRE date/scholarship-year conflicts are not resolved by deduplication.

## Legacy source and preservation policy

Legacy Jekyll `aboutme.md`, `conferences.md`, `symposiums.md`, `Publications.md`, `workshops.md`, `hackathon.md`, `volunteer.md`, `geogiggles.md`, `resume.md`, `index.html`, `_data/linkedin_post.yml` and `_config.yml` are historical source copies, outside the Astro deployment artifact. Root `projects.md` is empty. `_data/ui-text.yml` is interface translations, not activity content; generated search corpus is legacy infrastructure.

Propose retaining those files as non-authoritative recovery sources, not editing or deleting them during content consolidation. Only Astro canonical records would be maintained and published. Generated `dist` files are outputs, not independently maintained records. Public CV/résumé are standalone documents and will not be stripped of normal academic history; replacing them is separate from removing duplicate web entries. If literal repository-wide removal of historical source copies is desired, that needs a separate explicit decision.

Before removing any copied field, preserve its unique facts/links/assets in the canonical record and record a source-to-field mapping. Use typed collection references for relationships and homepage selection, with build-time validation for missing targets. Verify one full rendered instance per canonical ID, one visible location per photograph, resolved legacy anchors and no copied narrative previews. Then rerun the production build, link/content coverage, mobile and accessibility checks.

Approval requested for this plan, with uncertain relationships left unmerged pending confirmation. No content removal, consolidation, commit, push or deployment has occurred in this audit.
