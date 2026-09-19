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

## Setup (about 10 minutes)

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

## Exercises (this is where the learning happens)

Do these in order. Each has a "what to notice" so you connect the code to what you see.

1. **Change something and watch it ship.** Edit the headline in `site/index.html`, commit, push. *Notice:* the Actions tab shows the run; the live page updates; a "newer version is live" notice can appear in an already-open tab within about a minute.
2. **Break it on purpose.** Change `href="style.css"` to `href="styles.css"` and push. *Notice:* the **check** step fails with a clear message, **deploy** is skipped, and the live site is unchanged. Then fix it.
3. **Use the pull request flow.** Make a change on a new branch and open a pull request. *Notice:* checks run, but nothing is published. Merge it and see the deploy happen.
4. **Roll back a mistake.** Push a bad headline, then undo it with `git revert HEAD` and push. *Notice:* the pipeline republishes the old content. Reverting is the standard way to undo a bad change while keeping history.
5. **Add your own check.** In `check_site.py`, add a rule (for example, fail if any image has no `alt` text). *Notice:* you extended the safety net yourself.
6. **Remove a line and predict.** Delete `permissions:` from the deploy job and predict what will happen before you push. Then check whether you were right.

## Questions to answer in your own words (a week from now)

- What triggers the pipeline, and what does it do differently for a pull request?
- Why are build and deploy two separate jobs?
- Why does the deploy job need `id-token: write`, and why is there no password anywhere?
- What does the live site show when the check step fails, and why?
- What would you change if this site needed a database?

If you can answer these without looking, you understand the pipeline.

## Keeping it healthy

- **Action versions expire.** GitHub Actions are versioned tools; old versions eventually stop working. Dependabot (configured here) opens pull requests when new versions appear. Review and merge them.
- **This project pins these actions:** `actions/checkout@v6`, `actions/configure-pages@v6`, `actions/upload-pages-artifact@v5`, `actions/deploy-pages@v5`. Versions were current when this project was written; check each action's Releases page if something warns or fails.

## Where to go next

This project is stage 1. Good next steps, one at a time:

1. A staging preview and an approval step before going live
2. More automated checks (accessibility, page speed)
3. A custom domain
4. Uptime monitoring and alerts
5. Infrastructure as code once you manage more than a couple of settings
