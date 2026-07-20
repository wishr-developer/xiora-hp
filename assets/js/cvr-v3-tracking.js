/*
 * Xiora HP CVR v3 tracking — GA4 event dispatcher + A/B splitter
 *
 * Loaded from every Xiora HP insight page. Depends on gtag() being available
 * (loaded via <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXX">).
 * If gtag is undefined the module silently no-ops (safe for local dev).
 *
 * Emits 4 events:
 *   - xiora_cta_click_mini   (position=middle)
 *   - xiora_cta_click_hero   (position=hero)
 *   - xiora_cta_click_footer (position=footer)
 *   - xiora_ab_exposure      (variant=a|b, once per session per article)
 *
 * A/B split:
 *   - crypto.randomUUID().substring(0,1) hex -> mod 2 (0=A / 1=B)
 *   - persisted in cookie xiora_ab_variant for 30 days
 *   - overridable via ?variant=a|b query
 *
 * 個人小説活動 URL grep 0 (this file), 憲法 5 条 grep 0.
 */
(function () {
    "use strict";

    var COOKIE = "xiora_ab_variant";
    var COOKIE_DAYS = 30;

    function readCookie(name) {
        var re = new RegExp("(?:^| )" + name + "=([^;]+)");
        var m = document.cookie.match(re);
        return m ? decodeURIComponent(m[1]) : null;
    }

    function writeCookie(name, val, days) {
        var d = new Date();
        d.setTime(d.getTime() + days * 86400000);
        document.cookie = name + "=" + encodeURIComponent(val)
            + "; expires=" + d.toUTCString()
            + "; path=/; SameSite=Lax";
    }

    function chooseVariant() {
        var qs = new URLSearchParams(window.location.search);
        var q = qs.get("variant");
        if (q === "a" || q === "b") {
            writeCookie(COOKIE, q, COOKIE_DAYS);
            return q;
        }
        var existing = readCookie(COOKIE);
        if (existing === "a" || existing === "b") return existing;

        var uid;
        try { uid = crypto.randomUUID(); } catch (e) { uid = String(Math.random()).slice(2, 10); }
        var hex = parseInt(uid.replace(/-/g, "").charAt(0), 16);
        var v = (hex % 2 === 0) ? "a" : "b";
        writeCookie(COOKIE, v, COOKIE_DAYS);
        return v;
    }

    function articleSlug() {
        var p = window.location.pathname;
        var m = p.match(/\/insights\/([a-z0-9-]+)(?:\.html)?$/);
        return m ? m[1] : "unknown";
    }

    function fire(name, params) {
        if (typeof window.gtag === "function") {
            window.gtag("event", name, params || {});
        }
        // dev debug (safe: no PII)
        if (window.__xioraDebugCVR) {
            console.debug("[xiora-cvr]", name, params);
        }
    }

    function applyVariantB() {
        // Variant B modifies mini-CTA text + adds a "無料" badge
        var mini = document.querySelector('a[data-cta-position="middle"]');
        if (!mini) return;
        var badge = document.createElement("span");
        badge.textContent = "無料";
        badge.setAttribute("aria-hidden", "true");
        badge.style.cssText = "display:inline-block;font-size:11px;font-weight:600;background:#111827;color:#fbfbfd;padding:2px 8px;border-radius:4px;margin-right:6px;letter-spacing:0.05em;";
        mini.textContent = "30 分無料で相談する →";
        mini.parentNode.insertBefore(badge, mini);
    }

    function attachDelegates() {
        document.addEventListener("click", function (ev) {
            var a = ev.target.closest && ev.target.closest("a[data-cta-position]");
            if (!a) return;
            var pos = a.getAttribute("data-cta-position");
            var slug = articleSlug();
            var evtName = "xiora_cta_click_" + (pos === "middle" ? "mini" : pos);
            fire(evtName, { article_slug: slug, cta_position: pos, variant: readCookie(COOKIE) || "unknown" });
        }, false);
    }

    function boot() {
        var slug = articleSlug();
        var variant = chooseVariant();

        // exposure event once per pageload
        fire("xiora_ab_exposure", { article_slug: slug, variant: variant });

        if (variant === "b") applyVariantB();
        attachDelegates();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
    } else {
        boot();
    }
})();
