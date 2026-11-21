build_profile.py   rebuilds assets/profile.svg from live GitHub data (contributions calendar + repositories).
                   Run locally:  python scripts/build_profile.py     (standard library only)
                   Automatic:    .github/workflows/profile.yml runs it every 12 hours and commits the result.
prepare_avatar.py  one-off: python scripts/prepare_avatar.py photo.png
                   builds assets/avatar_duotone.webp (front of the 3D bust) and assets/portrait.json (ASCII back face).
                   Needs: pip install pillow numpy scipy. Edit CX / TOP / CWID at the top to re-crop.
Edit the CONFIG block at the top of build_profile.py to change text, featured projects, stack or links.
