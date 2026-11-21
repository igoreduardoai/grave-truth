# Shot list

Silent screen recording of the local demo. Synthetic fixtures only. The script does not record a microphone and does not synthesize speech. The last caption ends at 58.5s. ffprobe reports the file duration as 66.440s, one video stream, and no audio stream. Both are under 180s. The hero is visible at 0.1s. The dispute letter is visible at 6.1s. The export bytes come from GET /api/export?app=eob&format=markdown. That response is an attachment, so the recorder fetches it and shows the text instead of navigating.

Caption numbers are copied from demo/measurements.txt. That file is the stdout of evals/run_gold_and_holdout.py, the contrast count in scripts/record_demo.py, gallery/axe-report.json, and demo/pytest-last.txt.

- 0.0s–6.1s. Hero. Input, check, and result are on one screen. Caption: Synthetic fixtures only. No voice. The hero shows input, check, and result.
- 6.1s–18.2s. Judge URL. The synthetic bill is checked and the dispute letter is filled. Caption: 90/90 passed. accept_grounded 22, cited 33, not_found 17, reject_ungrounded 18.
- 18.2s–26.2s. Export letter. The markdown file is the whole page. Caption: contrast checker cited 0 of 17. contrast first sentence cited 17 of 17. contrast export spans 4. contrast copy spans 0.
- 26.2s–34.2s. Health. Static JSON from GET /health. Caption: GET /health is static JSON. The live model path is unimplemented. holdout 7/7.
- 34.2s–58.5s. Capability matrix page rendered from docs/KIRO-CAPABILITY-MATRIX.md. Caption: Capability matrix from the repository file. axe violations 0. axe incomplete 0. axe pages 8. 104 passed in 3.32s.
