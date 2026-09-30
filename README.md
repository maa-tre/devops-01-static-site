# Pages demo: a website that deploys itself

A tiny static website that GitHub builds, checks and publishes automatically every time you push a change to `main`. It is a learning project for the core CI/CD loop: **push, build, check, publish, roll back**.

No accounts beyond GitHub are needed, nothing to install (Python 3 is only needed if you want to run it on your own computer), and no secrets or passwords are involved.

## What is in this project

```
pages-demo/
├── .github/
│   ├── workflows/deploy.yml   The robot's instructions (the pipeline)
│   └── dependabot.yml         Keeps the pipeline's tools up to date
├── site/                      Your website (edit these files)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── scripts/
│   ├── build.py               Copies site/ to dist/ and stamps in commit + time
│   └── check_site.py          Fails the pipeline if a link or title is broken
├── .gitignore
└── README.md
```

## Setup

1. **Create a new repository** on GitHub (public is simplest; for private repos, check that your GitHub plan supports Pages).
2. **Upload this project's files** to it (keep the folder structure, including the hidden `.github` folder), or clone the repo and copy them in, then commit and push to `main`.
3. **Turn on Pages:** in the repo, open **Settings, then Pages**, and set the publishing source to **GitHub Actions**. (Menu wording changes now and then; GitHub's Pages docs show the current steps.)
4. **Watch it run:** open the **Actions** tab. The first run starts when you push (or use "Run workflow" on the workflow page). When it finishes, the **deploy** job shows your live URL.
5. **Open the URL.** You should see the "Deployment receipt" page with your commit and build time.

If the first run fails on the deploy job, the most common cause is step 3 not being done yet. Do it and re-run the job.

## Run it on your own computer (optional)

```bash
python3 scripts/build.py                  # creates dist/
python3 scripts/check_site.py dist        # should print "OK"
python3 -m http.server --directory dist 8000
# open http://localhost:8000
```

## How the pipeline works

```
Pull request  -->  build  -->  check                         (nothing is published)
Push to main  -->  build  -->  check  -->  deploy (publish)
```

- **build** runs `scripts/build.py`, which produces the finished site in `dist/`.
- **check** runs `scripts/check_site.py`. If it finds a problem, the run fails and **deploy never starts**, so visitors keep seeing the last good version.
- **deploy** uploads `dist/` to GitHub Pages. It only runs on `main`, never for pull requests.
- Permissions are read-only by default. Only the deploy job gets the two extra permissions needed to publish.

