# ESG360 TikTok — retention-first experiment (V2)

**STATUS: EXPERIMENT / DRAFT.** This directory is isolated from the live scheduler. No Buffer or TikTok API calls, tokens, account IDs, GitHub Actions triggers or modifications to existing scheduled posts.

## Baseline (Buffer, 21 October 2026)

Five posts dated 16–20 Oct: **2,275 total views, 455 average views per post**; average viewing time per 25–30s video **1.28–2.15s**. 18 October's question-based "Czy VSME jest obowiązkowe?" led with **947 views**. These are small-sample observational results, not causal proof.

Current production renderer \`automation/tiktok/render.py\` shows one static card for five seconds. This experiment instead uses 2–3 second beats, immediate on-screen question, moving shapes, animated progress, original quiet soundtrack, a single useful answer and a specific CTA.

## Storyboards (no publication dates)

- \`bank-esg-3-rzeczy\`: the bank asks for data; first three checks
- \`vsme-dobrowolne-klient\`: VSME is voluntary; why a customer still asks
- \`faktura-energia-esg\`: period, kWh and source of electricity data

All three render at **720×1280 (9:16), H.264/AAC, 14 seconds**. Source scripts are editorial proposals and need content, visual and sound review before posting. Avoid unlicensed music and false regulatory claims.

## Manual local render

Use the repo's existing Pillow dependency, and installed \`ffmpeg\`:

\`\`\`bash
python automation/tiktok/experiments/retention_v2.py \
  --id bank-esg-3-rzeczy --out /tmp/esg360-bank-preview.mp4
ffprobe -v error -show_entries format=duration \
  -show_entries stream=width,height,codec_name -of json /tmp/esg360-bank-preview.mp4
\`\`\`

No Python installation is required on the creator's device; optional rendering can occur in a controlled cloud environment. Running the renderer does not upload or schedule anything.

## Quality gates before live publishing

1. Verify rendered file plays on mobile with legible Polish and no content outside platform UI safe area.
2. Editor approves regulatory wording, visual identity and licensed audio.
3. Query Buffer for duplicates by caption AND title/asset/time, and confirm exact channel \`@esg360.academy\`.
4. Human approves any reschedule/edit; do not modify Bazgranie Nocą and do not duplicate a previously published post.
5. Do not connect this renderer to \`publish.py\` or change production episodes until separately reviewed.
6. After controlled rollout, compare 24h/72h metrics: views, unique reach, average watch time, comments, shares. Record incomplete retention analytics as unavailable instead of assuming zero.
7. Test a small mixed sample (at least 6 posts per variant) before drawing conclusions. Keep baseline format as a control.

## Hypothesis, not guarantee

The goal is to increase 3-second retention and average watch duration, not to promise viral reach. The platform's algorithm considers watch time and viewer engagement among other signals.

Generated files are experiments and must **never** be mistaken for an already queued or published TikTok video.
