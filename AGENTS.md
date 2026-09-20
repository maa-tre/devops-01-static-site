# AGENTS.md

This repository is a small GitHub Pages demo that builds a static site from [site/](site/) and validates it before publication. The main guidance for the CI/CD flow lives in [README.md](README.md); the build and validation logic lives in [scripts/build.py](scripts/build.py) and [scripts/check_site.py](scripts/check_site.py).

## Start here

- Edit website content in [site/](site/), not in generated output under `dist/`.
- Treat [scripts/build.py](scripts/build.py) and [scripts/check_site.py](scripts/check_site.py) as the source of truth for build-time behavior and validation rules.
- Keep changes small and aligned with the static-site pattern: plain HTML, CSS, and JavaScript only.

## Build and validation

Run these from the repository root:

```bash
python3 scripts/build.py
python3 scripts/check_site.py dist
```

The first command generates `dist/`. The second command fails the check if any page has broken links, a missing title/lang, an absolute `/` path, or a leftover placeholder such as `__COMMIT_SHORT__`.

## Repository rules for AI agents

- Do not hand-edit files in `dist/`; they are generated artifacts.
- Prefer relative links like `style.css` or `assets/logo.png` instead of `/style.css`.
- Every HTML page should include a non-empty `<title>` and a `lang` attribute on the `<html>` tag.
- If a change affects the site, validate it with the build and check scripts before considering the task complete.
- Keep the Pages deployment model in mind: pull requests should only build and check, while pushes to `main` may publish.

## File map

- [site/](site/) contains the source website.
- [scripts/build.py](scripts/build.py) copies the site to `dist/` and replaces build placeholders with commit metadata.
- [scripts/check_site.py](scripts/check_site.py) enforces page quality and catches broken references.
- [README.md](README.md) explains the learning objectives and the GitHub Actions flow.

## Common pitfalls

- `dist/` is generated output and should not be treated as editable source.
- Absolute root-relative URLs break on GitHub Pages project sites served under a repo-name prefix.
- Placeholder values are not optional; leaving them in output is a validation failure.
- Do not add frameworks, backends, or package dependencies unless the task explicitly requires them.
