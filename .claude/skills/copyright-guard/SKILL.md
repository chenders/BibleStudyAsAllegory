---
name: copyright-guard
description: Scan entry or reference text for in-copyright Bible translations before saving or locking. Use whenever scripture might have been quoted, when an entry is edited, or when asked to check copyright. Flags NIV, ESV, NLT, NASB, NRSV, CSB, and The Message. The retelling must be original; only public-domain translations (WEB, KJV, ASV) may be quoted.
---
# Copyright guard

A fast, deterministic scan for markers of in-copyright Bible translations, supporting the project's hard rule: quote scripture only from public-domain translations (World English Bible, KJV, ASV), kept short; the retelling itself is always original.

## Run it
```
python3 scripts/check_copyright.py <path | entries/>
```

## What it flags
Occurrences of in-copyright translation names/abbreviations: NIV, ESV, NLT, NASB, NRSV, CSB, The Message (MSG), and their full names. It reports file, line number, and the matched line.

## Judging a flag
This is a heuristic, not a verdict. **Naming** a translation in a scholarly note ("the NRSV reads 'young woman'") is allowed; **pasting** its text is not. Treat each flag as a prompt to check: is copyrighted text being reproduced, or merely named? If text is reproduced, replace it with an original rendering or a short public-domain (WEB/KJV/ASV) quote. Never reproduce song lyrics or poems either.
