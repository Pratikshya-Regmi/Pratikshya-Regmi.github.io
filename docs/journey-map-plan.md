# Journey map implementation

Add a single interactive journey to About, replacing its current-campus-only map. Keep the seven primary navigation destinations. Education retains its newest-first detail records and gains verified campus coordinates from the supplied KML.

Use a shared public location file for all map coordinates and a journey file for story order, linked canonical education/experience records, and future photos. Import only named public institutions and an approximately 1 km home area (refined after the user reported that the initial 10 km rounding was misplaced); never copy the raw KML, its precise home point, altitudes, or embedded descriptions into the repository.

Show six life/education chapters from Nepal to NC State, with the ORNL internship as a separate optional research stop. Render accessible text and a schematic before loading MapLibre on request. Add satellite imagery, real terrain at 1x vertical scale, manual next/previous, play/pause, overview, reduced-motion behavior and graceful network/WebGL fallback. Stop playback offscreen or when the browser tab is hidden. No automatic page scrolling.

Use EOX Sentinel-2 cloudless imagery and Mapterhorn terrain with attribution. Add photo fields to each chapter; no invented or stock photos. Preserve canonical education/experience descriptions through links instead of duplicating them. Validate production build, mobile widths, keyboard controls, reduced motion, fallback, and sanitized location data.

Open fields: village label, school dates, Capitol Hill Academy vs College naming, future photo captions and alt text. User message takes precedence for displayed school name until clarified.
