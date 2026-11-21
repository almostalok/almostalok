build_profile.py rebuilds assets/profile.svg from live GitHub data (contributions calendar + repositories).
Run locally:   python scripts/build_profile.py
Automatic:     .github/workflows/profile.yml runs it every 12 hours and commits the result.
Edit the CONFIG block at the top of the script to change text, status values, featured projects, stack or links.
