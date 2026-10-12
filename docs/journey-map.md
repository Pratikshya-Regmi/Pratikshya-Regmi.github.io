# Journey map

## Globe storytelling update

Selecting **Start the journey** opens Earth and starts a paced camera tour: Nepal overview, Jaljala–5, Beni Horizon Academy, Capitol Hill Academy, Kathmandu University, a global Nepal-to-Texas distance view, Texas A&M–Corpus Christi, and NC State. Oak Ridge remains an optional research stop. Local stops use terrain; global views use a globe projection with country-level endpoint labels.

The distance shown is about **13,900 km**, calculated between the shared Kathmandu University and Texas A&M–Corpus Christi coordinates. It is a great-circle distance, not a claim about an actual flight itinerary. Great-circle geometry is split correctly at the international date line. Imagery has limited coverage at the poles.

Visitors can pause/resume, restart, jump to a place, open Earth view or Nepal → Texas, and maximize the interface. Manual navigation, Escape, moving the map, hiding the tab, or scrolling away pauses the tour. Reduced-motion users get static views and direct chapter selection. The map still loads only after an explicit click, uses free imagery/terrain/open labels, and needs no Google API key.

Camera beats and timing live in `astro-site/src/scripts/journey-tour.ts`; distance/arc calculations live in `astro-site/src/utils/journey-geometry.ts`. Shared places and chapter/photo data remain in their existing data files. Responsive globe framing keeps the endpoints visible on small screens.

Verification: production build and internal-reference validation passed; the complete timed tour, pause/resume, restart and interruption checks passed. General browser checks passed at 320, 375, 768, 1024 and 1440 px, including fullscreen, keyboard operation, reduced motion and failure fallbacks. The loaded journey had no axe WCAG A/AA violations or uncaught browser errors. Geometry tests cover distance, date-line splitting and arc length. Screenshots and browser reports are in ignored `astro-site/test-results/`.

The About page includes “From Nepal to North Carolina,” a six-chapter journey: home region → Beni Horizon Academy → Capitol Hill Academy → Kathmandu University → Texas A&M University-Corpus Christi → NC State. Oak Ridge is a separate research stop so the main story finishes at the current Ph.D. location.

## Updating content and photos

Edit `astro-site/src/data/journey.json` for chapter stories, order, camera angles and photographs. Edit `astro-site/src/data/locations.json` for public place labels and coordinates. The Education map uses the same location records. University/ORNL dates are read from the canonical education and experience collections at build time; their full records remain linked.

For each future photo, add an object to the chapter's `"photos"` array:

```json
{
  "src": "/assets/journey/beni.webp",
  "alt": "A factual description of the supplied photograph",
  "caption": "Your approved caption",
  "width": 1200,
  "height": 900
}
```

Place the matching file in `astro-site/public/assets/journey/`. Use an optimized WebP, ideally under 250 KB and at most 1200 pixels wide. Re-encode photos without EXIF/GPS metadata before adding them. Use actual image dimensions and descriptive alt text. No photo upload service, account, analytics, or tracking is added. The current placeholders reserve space; no photographs were invented.

## Interaction and accessibility

The map loads only on request. Named chapter links, numbered keyboard-accessible markers, Previous/Next, a six-chapter Play/Pause tour, Whole journey and a 3D terrain toggle are provided. The tour pauses on Escape, interaction, leaving the section or hiding the browser tab. Reduced motion disables playback and changes places instantly. Scroll-wheel zoom is disabled; touch uses cooperative gestures. All stories remain available without JavaScript; if WebGL or the map bundle fails, the schematic and chapter navigation remain available.

The journey intentionally follows childhood-to-present narrative order. Education and Experience continue to use newest-first ordering. Connecting lines illustrate the sequence only, not actual travel paths. Terrain uses real elevation data with a vertical scale of 1×. Satellite imagery is a 2020 composite, not live imagery, with resolution appropriate for landscapes rather than individual buildings.

## Mapping stack and attribution

MapLibre GL JS is the sole new dependency, dynamically imported with its stylesheet. Satellite imagery: EOX Sentinel-2 cloudless (2020), containing modified Copernicus Sentinel data, CC BY 4.0. Terrain: Mapterhorn and its data contributors. Attribution is visible on the map. No Google Maps API key or billing setup is needed. Third-party tile services are contacted only after opening the map; their availability is outside the site's control.

References:
- https://maplibre.org/maplibre-gl-js/docs/examples/display-a-hybrid-satellite-map-with-terrain-elevation/
- https://s2maps.eu/
- https://mapterhorn.com/attribution

## Location privacy and open fields

`My_places.kml` is kept outside the repository. Only named institution points and a home region rounded to two decimal degrees, shown with a 1 km-radius shaded area were imported; raw home coordinates, KML descriptions and KML altitudes are not shipped. The approximate home marker is not a house location.

Still awaiting confirmation: childhood/high-school dates; “Capitol Hill Academy” (user message) versus “capitol Hill College” (KML). The displayed school name follows the user message. These do not block map interaction. No private street address or personal phone number has been added.

## Validation commands

From `astro-site`, with the repository's Node runtime on PATH:

```text
npm run check
npm run build
node scripts/check-journey-data.mjs
node scripts/journey-check.mjs
```

The browser check expects a production preview at http://localhost:4321 and installed Playwright Chromium. It checks responsive widths, accessible chapter controls, lazy loading, real map loading, motion preferences and failure fallbacks. Test artifacts are written to ignored `test-results/`.

## Verified on 2026-09-24

- Production build: 30 routes; internal-link and public-file validation passed.
- Browser widths 320, 375, 768, 1024 and 1440: no horizontal overflow before or after opening the map.
- Real satellite/terrain service loading and all seven markers verified in Chromium.
- Keyboard chapter selection, Previous/Next, Play/Pause, Escape, terrain toggle, overview and reduced-motion controls passed.
- Journey accessibility scans before/after loading: no WCAG A/AA violations reported by axe.
- No-JavaScript and blocked-map-module fallbacks passed. No uncaught browser errors.
- Confirmed that the large map library, worker, stylesheet and remote tiles are not requested before the visitor opens the map.
- MapLibre is pinned through the lockfile to the patched 6.11.2 release; its worker is bundled explicitly using Vite's `?worker&url` asset import.
- Build emits a size advisory for the roughly 1 MB mapping-library chunk. It is intentionally loaded on request rather than in the initial page payload. Tile service outages still depend on third-party availability; the chapter text remains usable.
- Exact home-coordinate strings were checked against the private KML and are absent from source, public and built site files.

Nothing was committed, pushed or deployed. Photos and the unresolved labels noted above remain content inputs for a later update.

## Home correction, maximize and labels — 2026-09-24

The earlier 0.1-degree home rounding displaced the public center by 5.41 km. Rechecked the original KML and replaced it with a 0.01-degree public center and a 1 km-radius shaded region. The original Home point is inside that region. The user confirmed the place name as Jaljala–5, Parbat, Nepal. The raw KML and house coordinates remain private. The public region is approximate, not an administrative ward boundary.

Home opens at zoom 12, and schools/universities/ORNL at zoom 13.5. The fullscreen control maximizes the map and story panel; the place picker remains available there. Restore works through the button or the browser's fullscreen exit. Browsers without native fullscreen use MapLibre's viewport fallback.

User chose open labels and a Google Maps link. Labels are OpenFreeMap/OpenMapTiles/OpenStreetMap, not Google data. The Place labels button toggles the overlay. Each selected stop updates the Google Maps link; the home link uses only the generalized public center. Source: https://openfreemap.org/quick_start/. Actual Google tiles would require the configured API project and billing described at https://developers.google.com/maps/documentation/tile/usage-and-billing.

## Final refinement verification

The user requested the free version. The implementation uses EOX imagery, Mapterhorn terrain and OpenFreeMap labels; it does not provision a paid Google Maps API project or require an API key. The Google Maps destination is a normal external link.

The corrected Jaljala view was visually checked after tiles settled: imagery and labels loaded with no HTTP failures, and the approximate 1 km home area was visible. Native fullscreen and restore passed at a 375 px viewport. The CSS fullscreen fallback was separately tested with both standard and WebKit fullscreen APIs disabled: expansion, viewport width and Escape-to-restore passed. The earlier fallback-test failure came from leaving Chromium's prefixed fullscreen API enabled; no site change was required.

## Supplied journey photographs ? 2026-09-25

All ten supplied photographs are stored as optimized, metadata-free WebP assets in `astro-site/public/assets/journey/`. Each chapter has a `photos` array in `journey.json`, with alt text, caption and intrinsic dimensions. Home, Kathmandu and Texas have a second photograph in a native expandable panel; all photographs preserve their full frame. Photos are lazy-loaded. School dates remain unresolved; photographs are now supplied.
