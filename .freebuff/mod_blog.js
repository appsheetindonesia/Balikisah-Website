/* ============================================================
   MODUL: Pencarian, Arsip (kategori/tag/penulis/bulan),
          Sidebar widget, beranda (postingan unggulan + widget).
   Dipasang sebagai blok modul setelah shell inti; memakai window.BK.
   ============================================================ */
(function(){
  "use strict";
  var BK = window.BK;
  if (!BK) return;
  /* Jumlah artikel per halaman mengikuti Pengaturan situs. */
  function PER_PAGE(){ return Math.max(3, parseInt(BK.SETTINGS && BK.SETTINGS.perPage, 10) || 6); }

  function $(id){ return document.getElementById(id); }

  /* ---------- kartu daftar blog (gaya "blog list") ---------- */
  function blogCard(a){
    var img = BK.photoForTitle(a.t, 0);
    return '<article class="bp-card">' +
      '<a class="stretched" href="#" data-goto="article" data-post="' + BK.escAttr(a.slug) + '" aria-label="' + BK.esc(a.t) + '">' +
      '<img data-photo-key="' + BK.escAttr(a.t) + '" data-img="0" alt="" loading="lazy">' +
      '</a>' +
      '<div class="bp-card__body">' +
      '<a class="bp-card__cat" href="#" data-goto="blog" data-blog="kategori" data-key="' + BK.escAttr(a.c) + '">' + BK.esc(a.c) + '</a>' +
      '<h2 class="bp-card__title"><a href="#" data-goto="article" data-post="' + BK.escAttr(a.slug) + '">' + BK.esc(a.t) + '</a></h2>' +
      '<p class="bp-card__excerpt">' + BK.esc(a.e) + '</p>' +
      '<p class="bp-card__meta">' + BK.esc(a.author) + ' · ' + BK.esc(a.d) + ' · ' + BK.readMinutes(a.body) + ' min read</p>' +
      '</div></article>';
  }

  /* ---------- widget sidebar ---------- */
  function widgetSearch(){
    return '<section class="widget"><h2 class="widget__h">Cari</h2>' +
      '<form class="widget__search" role="search" data-search-form>' +
      '<input type="search" name="s" placeholder="Kata kunci…" aria-label="Cari artikel" autocomplete="off">' +
      '<button class="btn btn--primary" type="submit">Cari</button></form></section>';
  }
  function widgetPopular(){
    var top = BK.PUBLISHED.slice().sort(function(a, b){ return (b.views||0) - (a.views||0); }).slice(0, 5);
    return '<section class="widget"><h2 class="widget__h">Paling Dibaca</h2><ul>' +
      top.map(function(a, i){
        return '<li><span class="widget__count">' + (a.views||0).toLocaleString("id-ID") + '&times;</span>' +
          '<a href="#" data-goto="article" data-post="' + BK.escAttr(a.slug) + '">' + (i+1) + '. ' + BK.esc(a.t) + '</a></li>';
      }).join("") + '</ul></section>';
  }
  function widgetCategories(){
    return '<section class="widget"><h2 class="widget__h">Kategori</h2><ul>' +
      BK.allCategories().map(function(c){
        return '<li><span class="widget__count">' + c.n + '</span>' +
          '<a href="#" data-goto="blog" data-blog="kategori" data-key="' + BK.escAttr(c.name) + '">' + BK.esc(c.name) +
          (c.visible ? '' : ' <em style="opacity:.6">(belum terbit)</em>') + '</a></li>';
      }).join("") + '</ul></section>';
  }
  function widgetTags(){
    var tags = BK.allTags();
    if (!tags.length) return "";
    var max = Math.max.apply(null, tags.map(function(t){ return t.n; }));
    return '<section class="widget"><h2 class="widget__h">Tag</h2><div class="tag-cloud">' +
      tags.map(function(t){
        var size = t.n >= 2 ? 3 : (t.n === 1 ? 2 : 1);
        return '<a href="#" data-goto="blog" data-blog="tag" data-key="' + BK.escAttr(t.name) + '" data-size="' + size + '">' + BK.esc(t.name) + '</a>';
      }).join("") + '</div></section>';
  }
  function widgetAuthors(){
    return '<section class="widget"><h2 class="widget__h">Penulis</h2><ul>' +
      BK.allAuthors().map(function(a){
        return '<li><span class="widget__count">' + a.n + '</span><a href="#" data-goto="blog" data-blog="penulis" data-key="' +
          BK.escAttr(a.name) + '">' + BK.esc(a.name) + '</a></li>';
      }).join("") + '</ul></section>';
  }
  function widgetArchives(){
    var months = BK.byMonth();
    if (!months.length) return "";
    return '<section class="widget"><h2 class="widget__h">Arsip</h2><ul>' +
      months.map(function(m){
        return '<li><span class="widget__count">' + m.n + '</span><a href="#" data-goto="blog" data-blog="bulan" data-key="' +
          m.key + '">' + BK.esc(BK.monthLabel(m.key)) + '</a></li>';
      }).join("") + '</ul></section>';
  }
  function widgetFeed(){
    return '<section class="widget"><h2 class="widget__h">Berlangganan</h2>' +
      '<p style="margin:0 0 10px">Ikuti artikel baru lewat feed RSS.</p>' +
      '<a class="btn btn--ghost" href="' + BK.esc(BK.feedUrl()) + '" target="_blank" rel="noopener">RSS Feed</a></section>';
  }
  var WIDGET_BUILD = {
    search: widgetSearch, popular: widgetPopular, categories: widgetCategories,
    tags: widgetTags, archives: widgetArchives, authors: widgetAuthors, feed: widgetFeed,
    text: function(){
      return '<section class="widget"><h2 class="widget__h">Tentang</h2>' +
        '<p style="margin:0">' + BK.esc(BK.SETTINGS.desc || "") + '</p>' +
        '<p style="margin:10px 0 0;font:400 12px/1.5 var(--font-ui);color:var(--ink-400)">' +
        BK.esc(BK.SETTINGS.email || "") + '</p></section>';
    }
  };
  function renderWidgets(el){
    if (!el) return;
    var conf = (BK.WIDGETS || []).filter(function(w){ return w && w.on !== false && WIDGET_BUILD[w.id]; });
    if (!conf.length) conf = BK.WIDGET_KINDS.slice(0, 7).map(function(k){ return {id:k.id, on:true}; });
    var html = conf.map(function(w){ try { return WIDGET_BUILD[w.id](); } catch (e) { return ""; } }).join("");
    if (BK.SETTINGS && BK.SETTINGS.rss === false){
      html = html.replace(/<section class="widget"><h2 class="widget__h">Berlangganan<\/h2>[\s\S]*?<\/section>/, "");
    }
    el.innerHTML = html;
    BK.syncPhotos(el);
  }

  /* ---------- halaman hasil pencarian ---------- */
  function renderSearchView(q){
    q = String(q || "").trim();
    var t = $("searchTitle"), c = $("searchCount"), list = $("searchList");
    if (t) t.textContent = q ? "Hasil untuk \u201c" + q + "\u201d" : "Pencarian";
    if (!q){ if (c) c.textContent = "Ketik kata kunci pada kotak pencarian."; if (list) list.innerHTML = ""; return; }
    var hits = BK.searchPosts(q);
    if (c) c.textContent = hits.length + " artikel cocok dengan \u201c" + q + "\u201d" +
      (q.length < 3 ? " \u2014 coba kata yang lebih spesifik." : "");
    if (!list) return;
    if (!hits.length){
      list.innerHTML = '<p class="dash-item__empty">Tidak ada artikel yang cocok. Coba kata kunci lain, ' +
        'atau <a href="#" data-goto="archive">telusuri arsip kategori</a>.</p>';
      return;
    }
    list.innerHTML = hits.map(function(a){
      var snip = BK.snippet((a.e ? a.e + " " : "") + BK.bodyText(a), q, 170);
      return '<article class="result"><p class="result__kind">' + BK.esc(a.c) + ' \u00b7 ' + BK.esc(a.author) + '</p>' +
        '<h2 class="result__title"><a href="#" data-goto="article" data-post="' + BK.escAttr(a.slug) + '">' +
        BK.highlight(a.t, q) + '</a></h2>' +
        '<p class="result__snippet">' + BK.highlight(snip, q) + '</p>' +
        '<p class="result__meta">' + BK.esc(a.d) + ' \u00b7 ' + BK.readMinutes(a.body) + ' min read</p></article>';
    }).join("");
  }

  /* ---------- paginasi ---------- */
  function pagerHtml(page, pages, kind, key){
    if (pages <= 1) return "";
    var out = [];
    function btn(label, target, opts){
      opts = opts || {};
      return '<button class="pager__btn" type="button" data-page="' + target + '"' +
        (opts.current ? ' aria-current="page"' : '') + (opts.off ? ' disabled' : '') +
        ' aria-label="' + BK.escAttr(opts.label || label) + '">' + label + '</button>';
    }
    out.push(btn("\u00ab Sebelumnya", page - 1, {off: page <= 1, label: "Halaman sebelumnya"}));
    var start = Math.max(1, page - 2), end = Math.min(pages, start + 4);
    start = Math.max(1, end - 4);
    if (start > 1) out.push(btn("1", 1, {}));
    if (start > 2) out.push('<span class="pager__info">\u2026</span>');
    for (var i = start; i <= end; i++) out.push(btn(String(i), i, {current: i === page}));
    if (end < pages - 1) out.push('<span class="pager__info">\u2026</span>');
    if (end < pages) out.push(btn(String(pages), pages, {}));
    out.push(btn("Berikutnya \u00bb", page + 1, {off: page >= pages, label: "Halaman berikutnya"}));
    out.push('<span class="pager__info">Halaman ' + page + ' dari ' + pages + '</span>');
    return out.join("");
  }

  /* ---------- halaman arsip dinamis ---------- */
  function resolveArchive(kind, key){
    if (kind === "kategori"){
      var name = null;
      BK.allCategories().forEach(function(c){ if (BK.slugify(c.name) === BK.slugify(key)) name = c.name; });
      if (!name) return null;
      return {kind: kind, key: name, title: name, eyebrow: "Kategori",
              desc: "Semua artikel pada kategori " + name + ".",
              items: BK.byCat(name), crumb: name};
    }
    if (kind === "tag"){
      var tag = null;
      BK.allTags().forEach(function(t){ if (BK.slugify(t.name) === BK.slugify(key)) tag = t.name; });
      if (!tag) return null;
      return {kind: kind, key: tag, title: "#" + tag, eyebrow: "Tag",
              desc: "Artikel dengan tag \u201c" + tag + "\u201d.",
              items: BK.byTag(tag), crumb: "Tag: " + tag};
    }
    if (kind === "penulis"){
      var who = null;
      BK.allAuthors().forEach(function(a){ if (BK.slugify(a.name) === BK.slugify(key)) who = a.name; });
      if (!who) return null;
      return {kind: kind, key: who, title: who, eyebrow: "Penulis",
              desc: "Artikel yang ditulis oleh " + who + ".",
              items: BK.byAuthor(who), crumb: "Penulis: " + who};
    }
    if (kind === "bulan"){
      var k = String(key);
      var ok = BK.byMonth().some(function(m){ return m.key === k; });
      if (!ok) return null;
      return {kind: kind, key: k, title: BK.monthLabel(k), eyebrow: "Arsip",
              desc: "Semua artikel yang terbit pada " + BK.monthLabel(k) + ".",
              items: BK.PUBLISHED.filter(function(a){ return BK.monthKeyOf(a) === k; }), crumb: BK.monthLabel(k)};
    }
    return null;
  }

  var lastBlog = {kind:"kategori", key:"", page:1};
  /* Dibaca shell untuk <link rel=canonical> + og:url halaman arsip. */
  window.__lastBlog = lastBlog;
  function renderBlogView(kind, key, page){
    page = Math.max(1, parseInt(page, 10) || 1);
    if (kind === "kategori-index"){
      $("blogKind").textContent = "Daftar kategori";
      $("blogTitle").textContent = "Kategori";
      $("blogDesc").textContent = "Telusuri seluruh kategori dan jumlah artikelnya.";
      $("blogCrumb").innerHTML = '<a href="#" data-goto="home">Beranda</a> / Kategori';
      $("blogCount").textContent = BK.allCategories().length + " kategori";
      $("blogPager").innerHTML = "";
      $("blogList").innerHTML = BK.allCategories().map(function(c){
        return '<article class="result"><p class="result__kind">Kategori</p>' +
          '<h2 class="result__title"><a href="#" data-goto="blog" data-blog="kategori" data-key="' +
          BK.escAttr(c.name) + '">' + BK.esc(c.name) + '</a></h2>' +
          '<p class="result__meta">' + c.n + ' artikel' + (c.visible ? '' : ' (belum ada yang terbit)') + '</p></article>';
      }).join("");
      lastBlog = {kind:kind, key:"", page:1};
      window.__lastBlog = lastBlog;
      renderWidgets($("blogWidgets"));
      return true;
    }
    var arch = resolveArchive(kind, key);
    if (!arch) return false;
    lastBlog = {kind: kind, key: arch.key, page: page};
    window.__lastBlog = lastBlog;
    var per = PER_PAGE();
    var pages = Math.max(1, Math.ceil(arch.items.length / per));
    if (page > pages) page = pages;
    var slice = arch.items.slice((page-1)*per, page*per);
    $("blogKind").textContent = arch.eyebrow;
    $("blogTitle").textContent = arch.title;
    $("blogDesc").textContent = arch.desc;
    $("blogCrumb").innerHTML = '<a href="#" data-goto="home">Beranda</a> / ' +
      '<a href="#" data-goto="blog" data-blog="' + arch.kind + '" data-key="' + BK.escAttr(arch.key) + '">' + BK.esc(arch.eyebrow) + '</a> / ' + BK.esc(arch.crumb);
    $("blogCount").textContent = arch.items.length + " artikel" +
      (pages > 1 ? " \u00b7 halaman " + page + "/" + pages : "");
    $("blogList").innerHTML = slice.length
      ? slice.map(blogCard).join("")
      : '<p class="dash-item__empty">Belum ada artikel yang terbit di sini.</p>';
    $("blogPager").innerHTML = pagerHtml(page, pages, arch.kind, arch.key);
    BK.syncPhotos($("blogList"));
    renderWidgets($("blogWidgets"));
    return true;
  }

  window.__renderSearch = renderSearchView;
  window.__renderBlog = function(kind, key, page){
    if (kind === "kategori-index") renderBlogView(kind, "", 1);
    else if (!renderBlogView(kind, key, page || 1)) { if (window.__go404) window.__go404(key); }
  };
  window.__go404 = function(what){
    var el = $("nfText");
    if (el && what) el.textContent = "\u201c" + what + "\u201d tidak ditemukan. Artikel atau arsipnya mungkin " +
      "sudah dipindahkan atau belum pernah terbit. Coba cari dengan kata kunci lain.";
    BK.show("404");
  };

  /* ---------- beranda: postingan unggulan dinamis ---------- */
  function renderHomeFeatured(){
    var a = BK.articleBySlug(BK.getFeatured()) || BK.PUBLISHED[0];
    if (!a) return;
    var t = $("heroTitle"), x = $("heroText"), img = $("heroImg"), btn = $("heroCta");
    if (t) t.textContent = a.t;
    if (x) x.textContent = a.e || BK.bodyText(a).slice(0, 160);
    if (btn){ btn.setAttribute("data-goto", "article"); btn.setAttribute("data-post", a.slug); }
    if (img) img.setAttribute("data-photo-key", a.t);
    var au = $("heroAuthor"), dt = $("heroDate");
    if (au) au.textContent = a.author || "";
    if (dt) dt.textContent = a.d ? ("\u2014 " + a.d) : "";
    /* Kolom kanan: 3 berita pendamping (unggulan dikecualikan). */
    var side = $("heroSideList");
    if (side){
      side.innerHTML = BK.PUBLISHED.filter(function(p){ return p !== a; }).slice(0, 3)
        .map(function(p, i){
          return '<a class="hero-side" href="#" data-goto="article" data-post="' +
            BK.escAttr(p.slug) + '">' +
            '<img data-photo-key="' + BK.escAttr(p.t) + '" data-img="' +
            ((i + 2) % BK.CARD_IMG.length) + '" alt="" loading="lazy">' +
            '<span class="hero-side__body"><h3>' + BK.esc(p.t) + '</h3>' +
            '<span class="cat-chip">' + BK.esc(p.c || "") + '</span>' +
            '<span class="hero-side__meta"><span class="who">' + BK.esc(p.author || "") +
            '</span><span>' + BK.esc(p.d || "") + '</span></span></span></a>';
        }).join("");
    }
    var host = $("homeHero");
    if (host) BK.syncPhotos(host);
  }

  /* ---------- interaksi: tautan arsip + paginasi ---------- */
  function hashOf(kind, key, page){
    var base = kind === "kategori-index" ? "#/kategori" :
      "#/" + (kind === "bulan" ? "arsip" : kind) + "/" + encodeURIComponent(key || "");
    if (page && page > 1) base += "/hal/" + page;
    return base;
  }
  document.addEventListener("click", function(e){
    var p = e.target.closest("#blogPager [data-page]");
    if (p){
      e.preventDefault();
      var n = Math.max(1, parseInt(p.getAttribute("data-page"), 10) || 1);
      renderBlogView(lastBlog.kind, lastBlog.key, n);
      try { location.hash = hashOf(lastBlog.kind, lastBlog.key, n); } catch (e2) {}
      return;
    }
    var b = e.target.closest("[data-blog]");
    if (b){
      e.preventDefault();
      var kind = b.getAttribute("data-blog"), key = b.getAttribute("data-key") || "";
      if (kind === "kategori-index") renderBlogView(kind, "", 1);
      else if (!renderBlogView(kind, key, 1)) window.__go404(key);
      try { location.hash = hashOf(kind, key, 1); } catch (e3) {}
      BK.show("blog");
      return;
    }
  });

  /* Modul lain memanggil ini setiap data berubah (artikel, kategori, view). */
  window.__moduleRefresh = function(){
    renderHomeFeatured();
    renderWidgets($("homeWidgets"));
    var v = window.__currentView;
    if (v === "blog" && lastBlog.key !== undefined) renderBlogView(lastBlog.kind, lastBlog.key, lastBlog.page);
    if (v === "search"){ var q = ("" + (window.__lastSearchQ || "")); renderSearchView(q); }
  };
  window.__renderSearch = function(q){
    window.__lastSearchQ = q; renderSearchView(q); renderWidgets($("searchWidgets"));
    /* canonical/og:url mengikuti kata kunci yang sedang dilihat. */
    if (window.__currentView === "search") BK.applySiteIdentity();
  };
  window.__articleWidgets = function(){ renderWidgets($("artWidgets")); };

  /* ---------- boot modul ---------- */
  renderHomeFeatured();
  renderWidgets($("homeWidgets"));
  (function(){
    var r = window.__bootRoute;
    if (r && (r.view === "search" || r.view === "blog" || r.view === "404") && window.__applyRoute){
      window.__applyRoute(r, false);
    }
  })();
})();
