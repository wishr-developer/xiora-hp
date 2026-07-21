// Xiora HP Rakuten CVR watchdog — click redirect + log
// Vercel Serverless Function (Node.js 20 runtime, zero external deps).
//
// Request:  GET /r?a=<article_slug>&l=<link_id>
// Response: 302 Location: <rakuten target_url>
// Side effect: single-line JSON stdout log (picked up by Vercel Log Drains
// or `pull_vercel_logs_and_flush.py` for affiliate-hub.db insert).
//
// Fallback: unknown link_id -> 302 books.rakuten.co.jp (safe generic).

const fs = require("fs");
const path = require("path");

// Load link mapping once per lambda cold start.
let LINKS = null;
function loadLinks() {
  if (LINKS) return LINKS;
  try {
    const p = path.join(__dirname, "_links.json");
    LINKS = JSON.parse(fs.readFileSync(p, "utf-8"));
  } catch (e) {
    LINKS = {};
    console.log(JSON.stringify({
      ts: new Date().toISOString(),
      event: "r.load_error",
      error: String(e && e.message || e),
    }));
  }
  return LINKS;
}

function truncate(s, n) {
  if (!s) return "";
  return String(s).slice(0, n);
}

function uaFamily(ua) {
  if (!ua) return "unknown";
  const u = ua.toLowerCase();
  if (u.includes("bot") || u.includes("crawler") || u.includes("spider")) return "bot";
  if (u.includes("mobile") || u.includes("iphone") || u.includes("android")) return "mobile";
  if (u.includes("ipad") || u.includes("tablet")) return "tablet";
  return "desktop";
}

module.exports = (req, res) => {
  const links = loadLinks();

  // Parse query string manually (no external deps).
  const url = new URL(req.url, "https://xiora-official.com");
  const article = url.searchParams.get("a") || "";
  const linkId = url.searchParams.get("l") || "";

  const entry = links[linkId];
  const target = (entry && entry.target)
    ? entry.target
    : "https://books.rakuten.co.jp/";

  const ua = req.headers["user-agent"] || "";
  const referer = req.headers["referer"] || req.headers["referrer"] || "";
  const ip = req.headers["x-forwarded-for"] || req.headers["x-real-ip"] || "";
  const country = req.headers["x-vercel-ip-country"] || "";

  // Structured single-line log (parsable by pull_vercel_logs_and_flush.py).
  console.log(JSON.stringify({
    ts: new Date().toISOString(),
    event: "r.click",
    article: truncate(article, 128),
    link_id: truncate(linkId, 16),
    target_known: Boolean(entry),
    ua_family: uaFamily(ua),
    ua: truncate(ua, 256),
    referer: truncate(referer, 256),
    country: truncate(country, 8),
    ip_hash: ip ? truncate(String(ip).split(",")[0].trim(), 64) : "",
  }));

  res.setHeader("Cache-Control", "no-store");
  res.setHeader("Referrer-Policy", "no-referrer-when-downgrade");
  res.writeHead(302, { Location: target });
  res.end();
};
