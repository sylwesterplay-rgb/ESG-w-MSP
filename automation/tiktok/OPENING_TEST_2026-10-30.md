# ESG360 — opening-only test

Approved in chat on 2026-10-24: implement recommendation to improve first two seconds.

Target: TikTok @esg360.academy only, episode ecovadis-vsme, 2026-10-30 18:00 Europe/Warsaw.

Change: first 2 seconds show `KLIENT PYTA O ESG? / EcoVadis czy VSME?`; original opening resumes for seconds 2–5. Remaining slides, caption, date and original synthesized audio unchanged. Other 19 episodes have no opening_hook and retain legacy rendering. Existing Buffer queue 25–29 October was read only.

Verified: local render completed; 1080x1920 H.264, AAC, duration 24.966667 seconds; full ffmpeg decode exit 0; opening PNG visually checked; JSON comparison confirmed every original episode field unchanged; remote read-back matched both updated files.

Implementation commits: f1b20b4eafdc71defe1d984186d835dd3e3ed819 and 68449be89c6fb9503abf319b7a9dfeae4e7173a6.

Status: code DEPLOYED and render VERIFIED. Cloud execution, Buffer scheduled record and public TikTok publication NOT YET VERIFIED. Existing daily scheduler will select this episode if no caption duplicate or occupied slot is found; retain all social_guard controls.

Evaluation: compare average watch time and engagement at equal 72-hour post age, accounting for analytics refresh delay. Previous seven-post aggregate: 2792 views, 6 likes, average watch 1.66s (Buffer refreshed 2026-10-23T01:29:01.911Z). This is contextual baseline, not a randomized control. No claim of causal uplift without results. No automatic review job created. Gemini was not called; no paid API, purchases or secrets used.
