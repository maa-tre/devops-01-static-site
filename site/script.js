// Tells the visitor when a newer version of the site has been published.
//
// How it works: build.py writes the current commit into this page (a <meta> tag)
// and into version.json. Every minute, and whenever the tab becomes visible again,
// we fetch version.json and compare. If the commits differ, a newer deployment is live.

(() => {
  const loaded = document.querySelector('meta[name="deployed-commit"]')?.content;
  const notice = document.getElementById("update-notice");
  const reload = document.getElementById("reload");

  if (!loaded || !notice) return;

  async function checkForUpdate() {
    try {
      // Relative URL, so it works under /repo-name/ on project sites.
      const response = await fetch("version.json?t=" + Date.now(), { cache: "no-store" });
      if (!response.ok) return;
      const latest = await response.json();
      if (latest.commit && latest.commit !== loaded) {
        notice.hidden = false;
      }
    } catch (error) {
      // Offline, or opened straight from disk: nothing to check, so stay quiet.
    }
  }

  reload?.addEventListener("click", () => location.reload());
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) checkForUpdate();
  });
  setInterval(checkForUpdate, 60 * 1000);
})();
