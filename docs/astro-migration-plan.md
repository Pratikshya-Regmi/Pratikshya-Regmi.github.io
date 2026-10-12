# Astro portfolio migration plan

Status: implemented with user-approved upload placeholders, 2026-09-16. The proposal below is retained as the design record; actual checks and limitations are recorded in `astro-validation.md`.

## Confirmed implementation scope

Privacy correction: the user requires the tracked root PDFs themselves to be public-safe. `assets/CV_PR.pdf` and `assets/Pratikshya_Resume_oct025.pdf` are replaced by the permanently redacted versions, rather than retaining private originals in preserved Jekyll source. No private storage location was supplied and no private backup is created. The complete working tree, including ignored files, is audited separately from Git history. Historical sensitive versions require a later authorized cleanup decision; history is not rewritten. The user requires all changes to remain uncommitted until review.

The user confirmed NCSU, Raleigh as the current campus and fourth-year Ph.D. candidacy at the Center for Geospatial Analytics, beginning fall 2023. Existing research material is approved for public presentation; missing data, photos, slides, and links use clear placeholders. Actual LAS files will arrive later. No synthetic LiDAR or fabricated results are used. Three.js and the future renderer remain deferred until data inspection; the current homepage/project pages provide explicit static upload placeholders. Public PDF copies are permanently redacted. The Astro site is implemented separately in `astro-site/`; no push, merge, live Pages-setting change, or deployment has occurred.

## Baseline and decision

- Working branch: `migration/astro-portfolio`.
- Original branch: `master`; recoverable baseline commit: `3f90ac2`.
- Existing Jekyll pages, assets, configuration, and workflow remain in place.
- `AGENTS.md` is an existing untracked user file; do not overwrite or stage it implicitly.
- User explicitly authorizes evaluating and migrating to Astro, superseding the brief's default preference against changing stacks. Jekyll is technically capable of the requested interactions. Astro is recommended for this approved rebuild because schema-validated content collections, reusable components, static output, and separately loaded interactive modules fit the requirements well. No React or server runtime is needed.
- This phase creates only a plan. The full migration follows the requested pre-implementation review and actual data inspection.

## Data inspection result and unresolved prerequisite

The complete workspace file inventory, including hidden files outside `.git`, contains images and two PDFs but no LAS, LAZ, COPC, PLY, PCD, XYZ, PTS, E57, TIFF, binary point assets, GLB/GLTF, or ZIP/7z data archives. No source manifest identifies an existing image as a scientifically derived LiDAR visualization. No supplied data path is present in this conversation.

Therefore point count, spatial extent, classifications, RGB availability, acquisition epochs, CRS, vertical datum, units, license, and suitability for public display cannot yet be established. Request the exact supplied-data path and public-release scope. Do not fabricate a cloud, infer coordinates from photos, or label an arbitrary terrain image as research output. Keep the existing authentic cover photo as an interim visual if implementation proceeds before approved data are available.

## Homepage concept

Near-black (#050505), off-white type, and a restrained terrain/cyan accent. A clear name, verified research descriptor, and project/CV/contact links sit beside a single oblique view of an approved survey subset. On phones the text precedes a compact static figure. The point cloud never sits behind important text.

- Start with a real static render; enhance only after the initial content is usable.
- Target 20,000–40,000 observed points, selected reproducibly to retain terrain and canopy features. No generated points, interpolated terrain, or undisclosed smoothing.
- Default color: measured elevation with labeled units and datum once verified. Use RGB or classification only if the source supports it. Canopy height needs a validated ground reference; change needs a separately validated analysis.
- Preserve equal axis scale and state vertical exaggeration is 1x. Include acquisition date, attribution, and a note that this is a decimated visualization, not an analysis dataset.
- Optional slow, bounded camera movement on capable desktops, with an explicit pause control. Pause offscreen and when the tab is hidden. Respect reduced motion immediately and when preferences change.
- Static default on small screens, data-saving/slow connections where detectable, reduced motion, and WebGL failure. Offer deliberate activation; connection detection is an enhancement, not a prerequisite for fallback.

## Project viewer concept

Attach the viewer to the project actually represented by the supplied data. Hurricane Helene terrain change and UAS visibility are candidates from existing content, not established matches to an unseen dataset.

- Static preview and written explanation appear first; an Open 3D viewer button loads code/data on demand.
- Inline expandable panel or dedicated viewer route; normal scrolling stays available. Orbit/pan gestures apply only while explicitly interacting; wheel capture is disabled by default.
- Accessible named buttons for orbit, pan, zoom, reset, and top/side views; keyboard equivalents, touch support, visible focus, loading/error states, and clear exit from expanded mode.
- Optional fullscreen dialog must trap and restore focus, support Escape, and expose an accessible title.
- Show legend, acquisition date, attribution, units, CRS, vertical datum, scale policy, subset bounds where public, and retained/source point counts.
- Start at roughly 100,000 points and progressively load spatial levels of detail up to a device-dependent point/memory budget. Target 100,000–250,000 active points on phones and at most 1 million on suitable desktops, subject to real profiling.
- Render on demand while idle; cap pixel ratio; cancel fetches and dispose GPU buffers when closed. Handle WebGL context loss.
- Multiple surveys require verified coordinate/datum alignment, per-epoch labels and selectors. Do not infer geomorphic change from unregistered clouds or differently colored acquisition years. No measurement tools until precision and scientific validity are established.
- All meaningful scientific interpretation is also in a caption and text summary; viewer interaction is not required to understand the project.

## Rendering and processing technology

Use an isolated TypeScript module with Three.js `Points`, `BufferGeometry`, and controlled orbit interaction, dynamically imported only where required. Share the renderer between the hero and project viewer. Prefer WebGL over a WebGPU-only implementation for compatibility. No React Three Fiber or full application hydration is needed.

For a bounded approved subset, use compact local-coordinate binary attributes plus JSON metadata and optional spatial LOD chunks. If inspection shows that millions of points and wide-area exploration are essential, reassess a Potree-style octree viewer; do not impose its larger conversion/runtime cost on the homepage.

Offline conversion proposal:

1. Inspect source headers and representative points with PDAL or equivalent: point count, bounds, scale/offset, CRS, vertical datum, units, fields, classifications, dates, missing values, and license.
2. Establish the public subset and project relationship; keep raw/restricted files outside both Git and public output. Derived geometry is public data too: an origin shift does not anonymize a location.
3. Validate CRS/units and axis orientation. If reprojection is required, use explicit transformations and document their accuracy; do not guess a vertical datum or substitute ellipsoidal for orthometric heights.
4. Crop and decimate deterministically, preferably retaining an observed point nearest each occupied voxel center. Record voxel size and method; do not replace observed points with invented centroids. Preserve important classes where justified and disclose any density changes.
5. Subtract a documented local origin before Float32 conversion to avoid precision loss at large projected coordinates. Choose quantization only after bounding maximum error against source accuracy and visualization scale.
6. Export hero and progressive viewer subsets with source-derived attributes. Preserve elevation offset for the legend and keep all surveys in the same frame.
7. Render static previews from the same approved points and camera. Create responsive WebP/AVIF variants with captions and dimensions.
8. Record provenance, source checksum, processing settings, point counts, bounds, maximum encoding error, dates, units, and color meaning. Keep private paths and restricted metadata out of public manifests.
9. Validate extrema, orientation, scale, alignment, and feature retention against the source in a trusted GIS/point-cloud tool; measure actual browser transfer size, GPU memory, and frame time.

## Provisional deployed asset budgets

These are design estimates, not measurements of supplied data. Decimal kB/MB. Point payload estimates use 12 bytes XYZ Float32 + 3 bytes RGB + 1 byte classification = 16 bytes per retained point, excluding small metadata; omit unsupported fields. Transfer compression is not assumed.

| Asset | Proposed budget |
| --- | --- |
| Responsive static hero image | 80–180 kB per selected variant |
| Hero point payload, 20k–40k points | 0.32–0.64 MB uncompressed |
| Viewer first level, 100k points | 1.6 MB uncompressed |
| Viewer 250k-point level | 4 MB uncompressed |
| Viewer maximum 1m-point level | 16 MB uncompressed |
| Three.js + controls + renderer | provisional 150–250 kB gzip; measure actual build |
| Base initial page including selected hero poster | target <=400 kB transferred, excluding deferred 3D/maps |

Independent 100k/250k/1m levels total 21.6 MB per survey if all are stored; additive hierarchy chunks can avoid duplicating points. One survey's point assets plus hero would therefore be roughly 16.3–22.3 MB before posters, metadata, and renderer. Multiple surveys multiply the data component. These sizes are upper planning envelopes, not a reason to send all levels to every visitor. Overall portfolio size depends on the approved media inventory and optimized outputs. No raw LAS/LAZ download on the homepage.

## Proposed directory structure

During migration, isolate Astro in `astro-site/` so the Jekyll source remains recoverable. Only its `dist/` becomes the eventual Pages artifact.

```text
docs/
  astro-migration-plan.md
astro-site/
  package.json
  package-lock.json
  astro.config.mjs
  tsconfig.json
  public/
    assets/img/                 # preserved compatible asset URLs
    assets/*.pdf               # reviewed public-safe versions only
    pointclouds/<dataset>/     # approved derived binaries + metadata
    robots.txt
    favicon.svg
  src/
    content.config.ts         # schema-validated collection definitions
    content/
      projects/
      education/
      experience/
      presentations/
      workshops/
      honors/
      publications/
      engagement/
      certifications/
      highlights/
    data/
      profile.yaml
      locations.yaml
      links.yaml
      legacy-routes.json
      content-confirmations.yaml
    assets/images/            # optimized editorial image sources
    layouts/BaseLayout.astro
    components/
      Header.astro
      Footer.astro
      Figure.astro
      Timeline.astro
      LocationMap.astro
      PointCloudHero.astro
      PointCloudViewer.astro
    scripts/pointcloud/
      renderer.ts
      controls.ts
      loader.ts
    pages/
      index.astro
      aboutme.astro
      education.astro
      experience.astro
      projects/index.astro
      projects/[id].astro
      presentations.astro
      conferences.astro
      symposiums.astro
      workshops.astro
      Publications.astro
      honors.astro
      hackathon.astro
      volunteer.astro
      certifications.astro
      geogiggles.astro
      resume.astro
      contact.astro
      404.astro
    styles/global.css
  scripts/
    validate-content.mjs
    validate-output.mjs
    pointcloud/                # reproducible offline conversion instructions
.github/workflows/
  ci.yml                      # existing Jekyll workflow preserved initially
  astro-check.yml             # future checks only during migration
  astro-pages.yml             # future controlled deployment
```

Use Astro's current build-time content loaders and schema API, with required sources/provenance, stable IDs, publication status, alt text/captions, and cross-record references. Confirm the stable Astro/Node versions at implementation time and pin dependencies with a lockfile. Draft or unapproved research records must be excluded from routes, search, metadata, and public output, not merely hidden by CSS.

## Preservation inventory and routing

| Existing source | Migration destination / policy |
| --- | --- |
| `index.html`, `_data/linkedin_post.yml` | Homepage, In Action line/photo, curated highlights; preserve IALE/CNR/GRASS and other entries |
| `aboutme.md` | About biography, research interests, human story; retain `/aboutme` and `.html` compatibility |
| `conferences.md` | Six conference records; `/conferences` retained as presentations subset |
| `symposiums.md` | Four symposium records; `/symposiums` retained |
| `workshops.md` | Two workshops and recap links; `/workshops` retained |
| `Publications.md` | Seven records with output type distinguished; retain capitalized `/Publications` |
| `hackathon.md` | Both PSI hackathons, awards, figures; preserve route and resolve placeholder article URL |
| `volunteer.md` | STEM fair, science fair judging, summer camp, CEETLE teaching; preserve route |
| `geogiggles.md` | Preserve personality content and images under More; repair markup/captions |
| `resume.md`, two PDFs | Resume page and compatible PDF paths only with sanitized public documents |
| `projects.md` | Empty source replaced by verified project index and case studies |
| CV-only content | Education, employment, service, honors, certificates, webinar, workshop repositories; reconcile status/dates |
| `_config.yml` links | Email/GitHub/LinkedIn/YouTube, certifications/honors and other meaningful destinations retained |
| `assets/img/*` | Inventory all 28 existing images; preserve originals in legacy source, publish approved useful images and optimized copies |
| `feed.xml`, `tags.html` | Check live use and preserve compatibility; do not invent blog entries for an empty post collection |
| `404.html` | Replace presentation with useful branded recovery links |

Record all literal external links in a migration ledger before conversion, preserving valid destinations; placeholders must become documented unresolved entries rather than clickable bogus links. Preserve compatibility for extensionless, trailing-slash, and `.html` routes as confirmed from deployed output. GitHub Pages has no configurable application server redirects: use generated static alias/redirect pages with canonical URLs and visible destination links where routes change. Do not rely on an SPA fallback or claim these are HTTP 301 redirects.

Known source issues from audit: missing `grass1.jpg`, placeholder volunteer highlight and hackathon article links, absent `blogs` page, incorrect image years, duplicated CNR image, unclosed GeoGiggles gallery, missing front matter in hackathon/resume, and generic search/metadata. Keep corrected content traceable to original sources.

## GitHub Pages configuration and rollout

- Repository is the user site `Pratikshya-Regmi/Pratikshya-Regmi.github.io`.
- Explicit proposed Astro configuration: `site: 'https://pratikshya-regmi.github.io'`, `base: '/'`, `output: 'static'`. Do not use the repository name as a path prefix.
- Root GitHub workflow builds within `astro-site/`; eventual deploy uploads only `astro-site/dist/`. Never copy the whole legacy `assets/` folder or repository into the public output without review.
- CI: supported pinned Node/tool versions, `npm ci`, type/content validation, production build, link/route and privacy/output checks. PRs build and validate but never deploy production.
- At cutover, use GitHub Pages Actions configuration with minimal `contents: read`, `pages: write`, `id-token: write` permissions, the `github-pages` environment, and deployment concurrency. Restrict deployment to the approved production branch (currently local `master`, verify remote settings) or explicit controlled dispatch.
- Coordinate the old Jekyll workflow and new workflow so only the selected pipeline uploads/deploys the production artifact. Keep Jekyll source; do not change live Pages settings during planning.
- Document commands and rollback in the root README when implementing. Baseline commit identifies the old source, but do not redeploy the old unsanitized CV during rollback. A safe rollback artifact must meet the same privacy policy.
- No push, production deployment, or history rewriting in this planning phase. Keeping private material out of a new artifact does not remove material already published in repository history.

## Implementation sequence and acceptance

1. Locate and inspect supplied data, confirm public subset, document actual sizes/metadata, and finalize the viewer approach.
2. Complete live-page audit (prior browser fetches of subpages failed), route/media/link ledger, and public-document review. These fetch failures are not evidence of broken pages.
3. Scaffold isolated Astro static project and validated collections; migrate verified records with original sources and explicit unresolved fields.
4. Implement custom near-black design, responsive navigation, accessible typography and shared components; build homepage and all meaningful content routes.
5. Convert approved LiDAR, validate scientific fidelity, and implement poster-first hero/project viewer with progressive loading and all fallbacks.
6. Add city/campus location maps and education timeline with fully equivalent text; choose attributed basemap only after checking provider terms.
7. Optimize media and metadata, preserve compatible URLs, sanitize documents, and add sitemap/robots/favicon.
8. Verify production output, all links, keyboard/touch controls, focus, reduced motion, no-JS/WebGL/network failures, image dimensions, privacy allowlist, and console errors.
9. Test 320/375/768/1024/1440 px, device memory/frame time, and Lighthouse targets >=90 on representative pages. Record exceptions honestly.
10. Review actual built/deployed preview, supply results and remaining gaps, then perform approved cutover with a public-safe rollback path.

## User confirmations still needed

- Exact LiDAR file/folder or derivative path, release permission, project relationship, crop boundary, permitted precision, acquisition date(s), horizontal CRS, vertical datum, units, source/attribution, and license. Do not assume that possession grants publication rights.
- Current public city/campus and hometown. University names are in the CV (NC State, Texas A&M University-Corpus Christi, Kathmandu University); confirm the correct campus and dates before verifying city/campus coordinates. Never derive these markers from a private address.
- Current professional descriptor/status; Ph.D. date interpretation; complete education/experience ranges; current roles.
- Project priority, specific contribution, publishable results and permitted research figures. A public talk title alone does not authorize underlying unpublished results.
- Public-safe CV/resume, preferred photographs and captions/credits, current contact email.
- Replacement GRASS image, real placeholder-link destinations, publication metadata, posters/slides, workshop materials, and award details where uncertain.

## Technical references consulted

- Astro GitHub Pages: https://docs.astro.build/en/guides/deploy/github/
- Astro content collections: https://docs.astro.build/en/guides/content-collections/
- Three.js documentation: https://threejs.org/docs/
- PDAL observed-point voxel sampling: https://pdal.io/en/stable/stages/filters.voxelcenternearestneighbor.html
