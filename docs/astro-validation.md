# Astro migration review

Date: 2026-09-16. Branch: `migration/astro-portfolio`.

All changes are local and uncommitted. No push, merge, deployment, history rewrite, or deletion of the Jekyll implementation has occurred. The default branch is `master`, not `main`; both its tip and migration HEAD still point to baseline `3f90ac2` while the changes await review.

## Implemented

- Custom near-black static Astro portfolio, with responsive navigation, skip link, reduced-motion CSS, verified biography, research case studies, and all meaningful legacy content.
- 67 schema-validated content records across projects, education, experience, presentations, workshops, honors, publications, engagement, certifications, highlights, and biography.
- Clear user-authorized upload placeholders in the homepage and relevant project pages. No fabricated LiDAR geometry or inferred results. The actual renderer will be implemented after the LAS files and metadata are available.
- On-request Leaflet campus map with textual equivalents, keyboard selection, touch-friendly controls, no wheel-scroll capture, attribution, and network-failure messaging. Only the confirmed NCSU campus has a marker; other campus markers and hometown remain pending.
- Optimized images, responsive sources, preserved image/PDF URLs, canonical metadata, Person structured data, sitemap, robots, favicon, 404, and legacy `.html` compatibility pages.
- Both original tracked root PDFs replaced with permanently redacted versions. Astro public and deployment copies match them byte-for-byte. No private originals or backups are retained outside Git history.
- Isolated `astro-site/dist` deployment via GitHub Actions. Existing Jekyll source remains; its workflow is manual-only and uses sanitized PDFs for its recovery artifact.

## Verification

- Astro check: zero errors, warnings, or hints after using the explicit Zod dependency.
- Production build: 26 pages, plus static aliases/feed/sitemap; output validator passed for 179 output files and 1,064 internal references. It checks internal asset/page references and rejects raw LiDAR, source-file exposure, and known placeholder-link patterns.
- Public PDFs: decoded-text privacy guard, removed PDF metadata/embedded files, and visual first-page inspection. Repository-wide exact-value scan and historical-presence results are in `privacy-audit.json`; sensitive values are never included in that report.
- Browser checks: 110 route/viewport combinations (22 routes at 320, 375, 768, 1024, and 1440 px) passed image loading, horizontal overflow, one-H1, HTTP status, and JavaScript exception checks. Automated WCAG and accessibility best-practice checks passed on eight representative routes. Keyboard skip navigation, mobile menu, reduced motion, and no-JavaScript content also passed. This is automated checking plus visual review, not a claim of comprehensive assistive-technology certification.
- Map checks: deferred loading, named campus selection, popup, focusable marker, mobile layout, automated accessibility, and blocked tile-network fallback passed.
- External link audit: all meaningful legacy content pages retrieved successfully. The old Blogs route is a confirmed 404 and now has an explicit content-pending page. Some LinkedIn/ResearchGate/ADS/Springer pages block automation or present a challenge; two NCSU recap fetches could not be verified by the HTTP client. These destinations were preserved rather than replaced speculatively.
- Final Lighthouse, local production preview with simulated mobile settings and no concurrent build/browser/privacy scan:

| Page | Performance | Accessibility | Best Practices | SEO |
| --- | ---: | ---: | ---: | ---: |
| Homepage | 94 | 100 | 100 | 100 |
| Hurricane Helene project | 100 | 100 | 100 | 100 |

Initial measurements under competing local workload were lower (homepage 72, then 89); accessibility details, image delivery, and page-specific CSS were improved, followed by the final isolated run above. Scores are local measurements and may vary on deployed hosting and real devices. Some additional image-byte savings remain possible.

Screenshots: [desktop, 1440 × 1000](previews/homepage-desktop.png), [mobile, 375 × 1000](previews/homepage-mobile.png). Full-page screenshots and detailed browser/Lighthouse reports remain in ignored `astro-site/test-results/`. The concise Lighthouse summary is also copied into this documentation directory for review.

## Remaining placeholders and conflicting facts

- LAS files, approved subset geometry, acquisition date(s), horizontal CRS, vertical datum, units, and attribution. The user's approval covers existing research content; unknown data fields remain unknown.
- Hometown; exact TAMUCC and Kathmandu University map markers.
- Missing GRASS Developer Summit photograph; slides, posters, graphical abstracts, and research result figures; ASPRS event photograph.
- Volunteer highlight original link and 2025 hackathon article link. The existing project repository is linked separately.
- Blog content has not yet been supplied.
- ITRE role dates differ between the CV and résumé; the displayed CV dates are labeled for confirmation.
- Conrad Blucher Institute Scholarship year differs between the two documents; the displayed CV year is labeled for confirmation.
- The existing résumé contains an anticipated graduation date, while the CV has an ambiguous Ph.D. year. The website uses the explicitly confirmed fall 2023 start and fourth-year candidacy; sanitized PDFs otherwise retain their existing editions and are labeled accordingly.
- Professional service “present” end dates are taken from the CV and labeled as such; updated end dates can be added later.

## Preview and deployment

```sh
cd astro-site
npm ci
npm run build
npm run preview -- --host 127.0.0.1
```

Preview: `http://127.0.0.1:4321/`. Node 22.12+ is required. A portable Node installation was used locally under ignored `.tools/`; it is not part of the website or deployment.

For this Windows workspace, run `powershell -ExecutionPolicy Bypass -File .\astro-site\preview.ps1` from the repository root. The helper uses installed Node or the existing local portable installation and previews the already-built files; it does not install or publish anything.

At an approved cutover, select GitHub Actions in repository Settings → Pages. `.github/workflows/astro-pages.yml` checks pull requests and deploys only from `master` using the `github-pages` environment. The uploaded directory is exclusively `astro-site/dist/`; site URL is `https://pratikshya-regmi.github.io`, base `/`. No repository-name prefix and no server adapter are required.

Git history contains sensitive versions of the two named PDFs. Replacing the current files does not remove older commits, previously deployed artifacts, forks, or caches. A separate, explicitly approved history/hosting cleanup may be needed. No such cleanup has been attempted.

## Changed-file summary

Modified tracked files: the two root PDFs, `README.md`, `.gitignore`, `_config.yml`, and `.github/workflows/ci.yml`. Created: the isolated Astro app (configuration, lockfile, content collections, components, layouts, pages, styles, optimized media, sanitized documents, and verification scripts), `.github/workflows/astro-pages.yml`, and migration/review documentation with screenshots. `AGENTS.md` was an existing user-provided untracked file and was not modified. See `changed-files.txt` for the complete file inventory.
