# Oak Ridge National Laboratory internship update

Added from the user's explicit confirmation: internship at Oak Ridge National Laboratory, May–August 2026, with project “Assessing Forest Resistance, Delayed Canopy Loss, and Early Recovery Following Hurricane Helene.” No formal job title beyond Intern, location, supervisor, study area, outcomes or actual survey dates were invented.

## Placement

- Professional Experience: `src/content/experience/ornl.md`, linked to the project.
- Canonical project: `src/content/projects/helene-forest-recovery.md`, distinct from the existing geomorphic-change Helene project. Overview/index/home previews link to it without reproducing its image or description.
- Original figure preserved byte-for-byte in root assets and Astro public assets; optimized WebP variants are 480 and 857 pixels wide. Descriptive alt text, an explicit conceptual caption, written explanation and full-resolution link are provided. Image appears only on its project page.
- Public CV: `assets/CV_PR.pdf` and `astro-site/public/assets/CV_PR.pdf` updated identically; internship, dates and full project title added under Positions and Affiliations. The employment résumé was not changed in this task.

## PDF preservation and verification

The PDF remains five pages. Header/education spacing on page one was adjusted to fit the internship. The existing Summer Research Assistant heading was moved to page two beside its details. All pre-existing text words and all 18 URI links were checked for preservation; the first two pages were visually inspected. No original private documents were recovered or stored. Current PDF privacy guard passed, and the served/downloaded CV matches the updated public file.

The one-time, edition-specific `scripts/add-ornl-cv.py` documents the PDF operation and refuses to insert a duplicate internship. It writes a review copy before replacement and is not a general CV regeneration tool. Earlier document date discrepancies remain unchanged.

## Site checks

Astro check: zero errors, warnings or hints. Production build and internal-link validation passed. Thirty route/width combinations across the six affected pages passed at 320, 375, 768, 1024 and 1440 pixels with no horizontal overflow or broken images. Automated accessibility checks passed on Experience, the new project and CV; no JavaScript errors. Diagram spacing was corrected after visual inspection and checked again before completion. Test artifacts are under ignored `astro-site/test-results/`.

All changes are local and uncommitted. No push or deployment occurred. Previously documented sensitive PDF versions in Git history have not been altered by this update.
