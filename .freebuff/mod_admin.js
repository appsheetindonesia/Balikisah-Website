/* ============================================================
   MODUL: Dasbor Redaksi lanjutan (ala WordPress)
   - Editor kaya (toolbar, pratinjau, penghitung, slug)
   - Daftar artikel (filter/urut/aksi massal/CSV)
   - Media library, Kategori & Tag, moderasi komentar
   - Revisi artikel + ekspor/impor seluruh situs
   ============================================================ */
(function(){
  "use strict";
  var BK = window.BK;
  if (!BK) return;
  function $(id){ return document.getElementById(id); }
  function pct(n){ return BK.esc(String(n)); }

  /* ---------- revisi artikel: balikisah.revisions.v1 ---------- */
  var REV_KEY = "balikisah.revisions.v1";
  var REVS = (function(){ try { return JSON.parse(localStorage.getItem(REV_KEY)) || {}; } catch (e) { return {}; } })();
  function saveRevs(){ try { localStorage.setItem(REV_KEY, JSON.stringify(REVS)); } catch (e) { BK.toast("Penyimpanan browser penuh; revisi lama dibuang.", "err"); } }
  function revKeyOf(title){ return BK.slugify(title); }
  function addRevision(title, snapshot){
    var k = revKeyOf(title);
    var arr = REVS[k] || [];
    arr.unshift({at: Date.now(), data: snapshot});
    REVS[k] = arr.slice(0, 10);
    saveRevs();
  }
  function revisionsFor(title){ return REVS[revKeyOf(title)] || []; }
  function revisionsAllCount(){
    return Object.keys(REVS).reduce(function(n, k){ return n + REVS[k].length; }, 0);
  }

  /* ---------- util format ---------- */
  function statusLabel(s){
    return {publish:"Terbit", draft:"Draf", scheduled:"Terjadwal", private:"Privat"}[s] || (s || "Terbit");
  }
  function statusPill(s){
    return '<span class="pm-row__badge" data-src="' + (s === "publish" ? "drive" : "link") + '">' + statusLabel(s) + '</span>';
  }
  function today(){
    var d = new Date();
    return d.toLocaleDateString("id-ID", {day:"2-digit", month:"short", year:"numeric"});
  }

  /* ---------- editor kaya ---------- */
  function wrapSelection(ta, before, after){
    var s = ta.selectionStart, e = ta.selectionEnd, v = ta.value;
    var sel = v.slice(s, e);
    ta.value = v.slice(0, s) + before + sel + (after || "") + v.slice(e);
    var pos = s + before.length + sel.length + (after ? 0 : 0);
    ta.focus();
    try { ta.setSelectionRange(pos, pos); } catch (err) {}
  }
  function linePrefix(ta, prefix){
    var s = ta.selectionStart, v = ta.value;
    var lineStart = v.lastIndexOf("\n", s - 1) + 1;
    var lineEnd = v.indexOf("\n", s);
    if (lineEnd < 0) lineEnd = v.length;
    var block = v.slice(lineStart, lineEnd);
    var lines = block.split("\n").map(function(l){
      return l.replace(/^(#{2,4}\s+|[-*+]\s+|\d+[.)]\s+|>\s?)/, "");
    });
    var out = lines.map(function(l){ return l ? prefix + l : l; }).join("\n");
    ta.value = v.slice(0, lineStart) + out + v.slice(lineEnd);
    var pos = lineStart + out.length;
    ta.focus();
    try { ta.setSelectionRange(pos, pos); } catch (err) {}
  }
  function toneOf(n, lo, hi){ return n === 0 ? "" : (n >= lo && n <= hi ? "ok" : "warn"); }
  function syncCounters(){
    var body = $("artBody"), ex = $("artExcerpt");
    var bc = $("bodyCount"), ec = $("excerptCount");
    if (body && bc){
      var words = (body.value || "").trim().split(/\s+/).filter(Boolean).length;
      bc.textContent = words + " kata \u00b7 " + Math.max(1, Math.round(words / 200)) + " menit baca";
    }
    if (ex && ec){
      var n = (ex.value || "").length;
      ec.textContent = n + "/160 karakter";
      ec.setAttribute("data-tone", toneOf(n, 100, 160));
    }
    var st = $("artSeoTitle"), stc = $("seoTitleCount");
    if (st && stc){ var a = (st.value || "").length; stc.textContent = a + "/70 karakter"; stc.setAttribute("data-tone", toneOf(a, 40, 70)); }
    var sd = $("artSeoDesc"), sdc = $("seoDescCount");
    if (sd && sdc){ var b = (sd.value || "").length; sdc.textContent = b + "/160 karakter"; sdc.setAttribute("data-tone", toneOf(b, 100, 160)); }
  }

  /* Tag cepat: tombol toggle yang menambah/menghapus tag di kolom teks. */
  function renderTagPick(){
    var box = $("artTagPick");
    if (!box) return;
    var tags = BK.allTags().slice(0, 24);
    box.innerHTML = tags.length ? tags.map(function(t){
      return '<button type="button" data-tag-pick="' + BK.escAttr(t.name) + '" aria-pressed="false">#' + BK.esc(t.name) + '</button>';
    }).join("") : '<span class="dash-photo__hint" style="margin:0">Belum ada tag. Tulis di kolom di atas.</span>';
    syncTagPick();
  }
  function currentTags(){
    var el = $("artTags");
    return el ? (el.value || "").split(",").map(function(s){ return s.trim(); }).filter(Boolean) : [];
  }
  function syncTagPick(){
    var box = $("artTagPick");
    if (!box) return;
    var cur = currentTags().map(function(t){ return BK.slugify(t); });
    box.querySelectorAll("[data-tag-pick]").forEach(function(b){
      b.setAttribute("aria-pressed", String(cur.indexOf(BK.slugify(b.getAttribute("data-tag-pick"))) > -1));
    });
  }
  function toggleTag(name){
    var el = $("artTags");
    if (!el) return;
    var list = currentTags().filter(function(t){ return BK.slugify(t) !== BK.slugify(name); });
    var had = currentTags().some(function(t){ return BK.slugify(t) === BK.slugify(name); });
    if (!had) list.push(name);
    el.value = list.join(", ");
    syncTagPick();
  }
  function syncPreview(){
    var body = $("artBody"), prev = $("artPrev");
    if (!body || !prev) return;
    prev.innerHTML = BK.renderBody(body.value || "", {});
    BK.syncPhotos($("artPrevBox"));
  }
  function syncSlugFromTitle(){
    var t = $("artTitle"), s = $("artSlug");
    if (!t || !s) return;
    if (!s.dataset.touched) s.value = BK.slugify(t.value);
  }
  function renderRevisions(title){
    var box = $("artRevList");
    if (!box) return;
    var arr = revisionsFor(title || ($("artTitle") ? $("artTitle").value.trim() : ""));
    if (!arr.length){ box.innerHTML = '<p class="dash-item__empty" style="padding:12px">Belum ada revisi. Simpan artikel untuk mulai mencatat.</p>'; return; }
    box.innerHTML = arr.map(function(r, i){
      var words = (r.data.body || "").trim().split(/\s+/).filter(Boolean).length;
      return '<div class="rev-row"><div><p class="rev-row__t">Revisi #' + (arr.length - i) + '</p>' +
        '<p class="rev-row__s">' + BK.relTime(r.at) + ' \u00b7 ' + words + ' kata \u00b7 ' + statusLabel(r.data.status) + '</p></div>' +
        '<button class="btn btn--ghost" type="button" data-rev="' + i + '">Pulihkan</button></div>';
    }).join("");
  }

  /* Dipanggil shell setiap kali artikel tersimpan (collectEntry). */
  window.__onArticleSaved = function(entry, title){
    addRevision(title, {title: entry.title, cat: entry.cat, author: entry.author,
      excerpt: entry.excerpt, body: entry.body, tags: entry.tags, status: entry.status,
      publishAt: entry.publishAt, featured: entry.featured, slug: entry.slug,
      seoTitle: entry.seoTitle, seoDesc: entry.seoDesc, sticky: entry.sticky,
      authorBio: entry.authorBio, format: entry.format});
    renderRevisions(title);
    refreshTermsDatalists();
    renderTagPick();
    var up = $("artUpdated");
    if (up) up.value = entry.updated || "";
    BK.toast((entry.status === "publish" ? "Artikel diterbitkan." : "Draf disimpan."), entry.status === "publish" ? "ok" : "");
  };

  /* Shell memanggil ini setelah initEditor() untuk memasang editor kaya. */
  window.__editorWired = function(scope){
    var body = $("artBody"), title = $("artTitle"), slug = $("artSlug"), ex = $("artExcerpt");
    var tb = $("artToolbar");
    if (tb && body) tb.addEventListener("click", function(e){
      var b = e.target.closest("[data-md]");
      if (!b) return;
      var k = b.getAttribute("data-md");
      if (k === "bold") wrapSelection(body, "**", "**");
      else if (k === "italic") wrapSelection(body, "*", "*");
      else if (k === "h2") linePrefix(body, "## ");
      else if (k === "h3") linePrefix(body, "### ");
      else if (k === "quote") linePrefix(body, "> ");
      else if (k === "ul") linePrefix(body, "- ");
      else if (k === "ol") linePrefix(body, "1. ");
      else if (k === "code") wrapSelection(body, "\n```\n", "\n```\n");
      else if (k === "hr") wrapSelection(body, "\n\n---\n\n", "");
      else if (k === "link") wrapSelection(body, "[", "](https://)");
      else if (k === "img") wrapSelection(body, "![keterangan](", ")");
      syncPreview(); syncCounters();
    });
    if (body) body.addEventListener("input", function(){ syncCounters(); syncPreview(); });
    if (ex) ex.addEventListener("input", syncCounters);
    ["artSeoTitle","artSeoDesc"].forEach(function(id){
      var el = $(id); if (el) el.addEventListener("input", syncCounters);
    });
    var tagPick = $("artTagPick");
    if (tagPick) tagPick.addEventListener("click", function(e){
      var b = e.target.closest("[data-tag-pick]"); if (!b) return;
      toggleTag(b.getAttribute("data-tag-pick"));
    });
    var tagsEl = $("artTags");
    if (tagsEl) tagsEl.addEventListener("input", syncTagPick);
    if (title) title.addEventListener("input", syncSlugFromTitle);
    if (slug) slug.addEventListener("input", function(){ slug.dataset.touched = "1"; });
    var pt = $("artPreviewToggle");
    if (pt) pt.addEventListener("click", function(){
      var box = $("artPrevBox");
      if (!box) return;
      var on = box.style.display !== "none";
      box.style.display = on ? "none" : "";
      pt.textContent = on ? "Pratinjau" : "Sembunyikan";
    });
    var editSite = $("artPreviewPost");
    if (editSite) editSite.addEventListener("click", function(){
      var sl = BK.slugify(slug && slug.value ? slug.value : (title ? title.value : ""));
      var a = BK.articleBySlug(sl);
      if (!a){ BK.toast("Simpan artikel dulu supaya bisa dilihat di situs."); return; }
      if (!BK.isVisible(a)){ BK.toast("Artikel berstatus " + statusLabel(a.status) + " belum tampil di situs."); return; }
      BK.openArticle(a.slug);
    });
    var revBox = $("artRevList");
    if (revBox) revBox.addEventListener("click", function(e){
      var b = e.target.closest("[data-rev]");
      if (!b || !title) return;
      var arr = revisionsFor(title.value.trim());
      var r = arr[parseInt(b.getAttribute("data-rev"), 10)];
      if (!r) return;
      if (!confirm("Pulihkan revisi ini? Perubahan yang belum disimpan akan diganti.")) return;
      if (window.__fillEditor) window.__fillEditor(r.data);
      BK.toast("Revisi dipulihkan ke editor. Tekan Simpan untuk menerapkan.");
    });
    window.__editorSync = function(){ syncCounters(); syncPreview(); syncSlugFromTitle(); renderRevisions(); renderTagPick(); syncTagPick(); };
    window.__editorSync();
  };

  /* ---------- daftar artikel: filter, urut, aksi ---------- */
  function allRows(){
    return BK.ART.filter(function(a){ return !a.trashed; }).map(function(a){
      return {a: a, title: a.t, cat: a.c, author: a.author, status: a.status,
              date: a.d, views: a.views || 0, admin: a.admin};
    });
  }
  function filteredRows(){
    var q = ($("listSearch") ? $("listSearch").value : "").trim().toLowerCase();
    var st = $("listStatus") ? $("listStatus").value : "";
    var sort = $("listSort") ? $("listSort").value : "new";
    var rows = allRows().filter(function(r){
      if (st && r.status !== st) return false;
      if (q && (r.title + " " + r.author + " " + r.cat).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
    rows.sort(function(x, y){
      if (sort === "title") return x.title.localeCompare(y.title);
      if (sort === "views") return y.views - x.views;
      var dx = BK.parseDateText(x.date), dy = BK.parseDateText(y.date);
      var vx = dx ? dx.y * 10000 + dx.m * 100 + dx.d : 0;
      var vy = dy ? dy.y * 10000 + dy.m * 100 + dy.d : 0;
      return sort === "old" ? vx - vy : vy - vx;
    });
    return rows;
  }
  window.__renderAdminList = function(){
    var list = $("adminList");
    if (!list) return;
    var rows = filteredRows();
    if (!rows.length){ list.innerHTML = '<p class="dash-item__empty">Tidak ada artikel yang cocok dengan filter.</p>'; return; }
    list.innerHTML = rows.map(function(r){
      var a = r.a;
      return '<div class="dash-item" data-key="' + BK.escAttr(a.t) + '" data-slug="' + BK.escAttr(a.slug) + '">' +
        '<input type="checkbox" data-pick aria-label="Pilih ' + BK.escAttr(a.t) + '" style="width:auto">' +
        '<img class="dash-item__thumb" data-photo-key="' + BK.escAttr(a.t) + '" data-img="0" alt="">' +
        '<div class="dash-item__body"><p class="dash-item__title">' + BK.esc(a.t) + ' ' + statusPill(a.status) +
        (a.featured ? ' <span class="pm-row__badge" data-src="baked">Unggulan</span>' : '') + '</p>' +
        '<p class="dash-item__meta">' + BK.esc(a.c) + ' \u00b7 ' + BK.esc(a.author) + ' \u00b7 ' + BK.esc(a.d) +
        ' \u00b7 ' + (a.views||0) + ' dibaca \u00b7 /' + BK.esc(a.slug) +
        (a.sticky ? ' \u00b7 \u2b50 disematkan' : '') + (a.updated ? ' \u00b7 diperbarui ' + BK.esc(a.updated) : '') + '</p></div>' +
        '<div class="dash-item__ctl">' +
        '<button class="btn btn--ghost" type="button" data-act="edit">Edit</button>' +
        '<button class="btn btn--ghost" type="button" data-act="view">Lihat</button>' +
        (a.status === "publish" ? '<button class="btn btn--ghost" type="button" data-act="unpublish">Jadikan draf</button>'
          : '<button class="btn btn--primary" type="button" data-act="publish">Terbitkan</button>') +
        (a.admin ? '<button class="btn btn--ghost" type="button" data-act="feature">' + (a.featured ? "Lepas unggulan" : "Unggulan") + '</button>' : '') +
        (a.admin ? '<button class="btn btn--ghost" type="button" data-act="sticky">' + (a.sticky ? "Lepas semat" : "Sematkan") + '</button>' : '') +
        (a.admin ? '<button class="btn btn--ghost" type="button" data-act="duplicate">Duplikat</button>' : '') +
        (a.admin ? '<button class="btn btn--danger" type="button" data-act="del">Sampah</button>' : '') +
        '<div class="pm-row__url" style="flex-basis:100%">' + location.origin + location.pathname +
          '?post=' + BK.escAttr(a.slug) + '</div>' +
        '</div></div>';
    }).join("");
    BK.syncPhotos(list);
  };
  window.__adminListSync = function(){ if (!$("dashList") || $("dashList").hidden) return; if (!$("adminList")) return; window.__renderAdminList(); };

  window.__adminListAction = function(e){
    var btn = e.target.closest("[data-act]");
    if (!btn) return;
    var item = e.target.closest(".dash-item");
    var title = item.getAttribute("data-key");
    var act = btn.getAttribute("data-act");
    var a = BK.ART.filter(function(x){ return x.t === title; })[0];
    var entry = BK.ARTICLES.filter(function(x){ return x.title === title; })[0];
    if (act === "view"){
      if (a && BK.isVisible(a)) BK.openArticle(a.slug); else BK.toast("Artikel berstatus " + statusLabel(a && a.status) + "; belum tampil di situs.");
      return;
    }
    if (act === "feature"){
      if (!entry) return;
      entry.featured = !entry.featured;
      BK.setFeatured(entry.featured ? BK.slugify(entry.slug || entry.title) : "");
      BK.saveArticles(); BK.refreshAll(); BK.toast(entry.featured ? "Ditetapkan sebagai unggulan beranda." : "Unggulan dilepas.");
      return;
    }
    if (!entry) return;
    if (act === "del"){
      if (!confirm("Pindahkan \u201c" + title + "\u201d ke Sampah? Bisa dipulihkan dari tab Sampah.")) return;
      if (entry){ entry.trashed = true; entry.trashAt = Date.now(); }
      else if (a && a.admin){
        BK.ARTICLES.push({title: title, cat: a.c, author: a.author, excerpt: a.e, body: a.body,
          tags: a.tags, status: a.status, trashed: true, trashAt: Date.now(), date: a.d});
      }
      BK.saveArticles(); BK.refreshAll(); window.__renderAdminList();
      BK.toast("Artikel dipindahkan ke Sampah.");
      return;
    }
    if (act === "untrash"){
      if (entry){ entry.trashed = false; delete entry.trashAt; }
      BK.saveArticles(); BK.refreshAll(); window.__renderAdminList(); window.__renderTrash && window.__renderTrash();
      BK.toast("Artikel dipulihkan.", "ok");
      return;
    }
    if (act === "purge"){
      if (!confirm("Hapus \u201c" + title + "\u201d secara permanen? Tidak bisa dibatalkan.")) return;
      BK.ARTICLES = BK.ARTICLES.filter(function(x){ return x.title !== title; });
      BK.saveArticles(); delete BK.PHOTOS[title]; BK.savePhotos();
      BK.refreshAll(); window.__renderAdminList(); window.__renderTrash && window.__renderTrash();
      BK.toast("Artikel dihapus permanen.");
      return;
    }
    if (act === "sticky"){
      if (!entry) return;
      entry.sticky = !entry.sticky;
      BK.saveArticles(); BK.refreshAll(); window.__renderAdminList();
      BK.toast(entry.sticky ? "Artikel disematkan di atas." : "Sematkan dilepas.", "ok");
      return;
    }
    if (act === "duplicate"){
      if (!entry) return;
      var copy = JSON.parse(JSON.stringify(entry));
      copy.title = title + " (salinan)";
      copy.slug = "";
      copy.status = "draft";
      copy.trashed = false;
      BK.ARTICLES.push(copy);
      BK.saveArticles(); BK.refreshAll(); window.__renderAdminList();
      BK.toast("Salinan dibuat sebagai draf.", "ok");
      return;
    }
    if (act === "publish" || act === "unpublish"){
      entry.status = act === "publish" ? "publish" : "draft";
      entry.date = entry.date || today();
      BK.saveArticles(); BK.refreshAll(); window.__renderAdminList();
      BK.toast(act === "publish" ? "Artikel diterbitkan." : "Artikel dijadikan draf.", "ok");
      return;
    }
    if (act === "edit"){
      if (window.__fillEditor) window.__fillEditor(entry);
      var wt = document.querySelector('[data-dash-tab="write"]');
      if (wt) wt.click();
      return;
    }
  };

  /* ---------- aksi massal + ekspor CSV ---------- */
  function pickedKeys(){
    var out = [];
    document.querySelectorAll("#adminList [data-pick]:checked").forEach(function(c){
      var row = c.closest(".dash-item");
      if (row) out.push(row.getAttribute("data-key"));
    });
    return out;
  }
  function promptSelection(){
    var keys = pickedKeys();
    if (!keys.length){ setBulk("Pilih dulu artikel pada kotak centang.", "err"); return null; }
    return keys;
  }
  function setBulk(msg, tone){ var el = $("listBulkState"); if (el){ el.textContent = msg || ""; el.setAttribute("data-tone", tone || ""); } }
  function bulkApply(fn, label){
    var keys = promptSelection();
    if (!keys) return;
    keys.forEach(function(k){ var e = BK.ARTICLES.filter(function(x){ return x.title === k; })[0]; if (e) fn(e, k); });
    BK.saveArticles(); BK.refreshAll(); window.__renderAdminList();
    setBulk(keys.length + " artikel " + label + ".", "ok");
    BK.toast(keys.length + " artikel " + label + ".", "ok");
  }
  function exportCsv(){
    var rows = filteredRows();
    var head = ["Judul","Kategori","Penulis","Status","Tanggal","Dibaca","Slug"];
    function cell(v){ return '"' + String(v == null ? "" : v).replace(/"/g, '""') + '"'; }
    var lines = [head.map(cell).join(",")].concat(rows.map(function(r){
      return [r.title, r.cat, r.author, statusLabel(r.status), r.date, r.views, r.a.slug].map(cell).join(",");
    }));
    BK.downloadText("balikisah-artikel.csv", lines.join("\n"), "text/csv");
    setBulk(rows.length + " baris diekspor ke CSV.", "ok");
  }
  (function wireList(){
    var tools = $("listTools");
    if (tools && !$("bulkBar")){
      var bar = document.createElement("div");
      bar.className = "btn-row"; bar.id = "bulkBar";
      bar.innerHTML = '<button class="btn btn--primary" type="button" id="bulkPublish">Terbitkan terpilih</button>' +
        '<button class="btn btn--ghost" type="button" id="bulkDraft">Jadikan draf</button>' +
        '<button class="btn btn--danger" type="button" id="bulkDel">Hapus terpilih</button>';
      tools.parentNode.insertBefore(bar, $("listBulkState"));
    }
    if ($("bulkPublish")) $("bulkPublish").addEventListener("click", function(){ bulkApply(function(e){ e.status = "publish"; e.date = e.date || today(); }, "diterbitkan"); });
    if ($("bulkDraft")) $("bulkDraft").addEventListener("click", function(){ bulkApply(function(e){ e.status = "draft"; }, "dijadikan draf"); });
    if ($("bulkDel")) $("bulkDel").addEventListener("click", function(){
      if (!confirm("Hapus artikel terpilih? Tindakan ini tidak bisa dibatalkan.")) return;
      bulkApply(function(e, k){ delete BK.PHOTOS[k]; }, "dihapus");
      BK.savePhotos();
    });
    ["listSearch","listStatus","listSort"].forEach(function(id){
      var el = $(id);
      if (el) el.addEventListener(id === "listSearch" ? "input" : "change", window.__renderAdminList);
    });
    var csv = $("listExportCsv");
    if (csv) csv.addEventListener("click", exportCsv);
  })();

  /* ---------- kategori & tag (pengelola taksonomi) ---------- */
  var CAT_KEY = "balikisah.cats.v1";
  var TAG_KEY = "balikisah.tagdefs.v1";
  window.__extraCats = (function(){ try { return JSON.parse(localStorage.getItem(CAT_KEY)) || []; } catch (e) { return []; } })();
  var TAGDEFS = (function(){ try { return JSON.parse(localStorage.getItem(TAG_KEY)) || []; } catch (e) { return []; } })();
  function saveCats(){ try { localStorage.setItem(CAT_KEY, JSON.stringify(window.__extraCats)); } catch (e) {} }
  function saveTagDefs(){ try { localStorage.setItem(TAG_KEY, JSON.stringify(TAGDEFS)); } catch (e) {} }
  function countCat(name){ return BK.ART.filter(function(a){ return a.c === name; }).length; }
  function countTag(name){ return BK.allTags().filter(function(t){ return t.name === name; })[0] || {n:0}; }
  function refreshTermsDatalists(){
    if (window.__restoreSettings) window.__restoreSettings();
    var catSel = $("artCat");
    if (catSel){
      var cur = catSel.value;
      catSel.innerHTML = BK.allCategories().map(function(c){
        return '<option>' + BK.esc(c.name) + '</option>';
      }).join("");
      catSel.value = cur || (BK.allCategories()[0] ? BK.allCategories()[0].name : "Kerajaan");
    }
    var tagList = $("tagList");
    if (tagList) tagList.innerHTML = BK.allTags().map(function(t){ return '<option>' + BK.escAttr(t.name) + '</option>'; }).join("");
    var auList = $("authorList");
    if (auList) auList.innerHTML = BK.allAuthors().map(function(a){ return '<option>' + BK.escAttr(a.name) + '</option>'; }).join("");
  }
  function renderTerms(){
    var box = $("catList");
    if (box) box.innerHTML = BK.allCategories().map(function(c){
      return '<div class="dash-item" data-cat="' + BK.escAttr(c.name) + '" style="padding:9px 11px">' +
        '<div class="dash-item__body"><p class="dash-item__title" style="font-size:14px">' + BK.esc(c.name) + '</p>' +
        '<p class="dash-item__meta">' + c.n + ' artikel</p></div>' +
        '<div class="dash-item__ctl"><button class="btn btn--ghost" type="button" data-act="rename">Ganti nama</button>' +
        '<button class="btn btn--danger" type="button" data-act="del">Hapus</button></div></div>';
    }).join("");
    var tb = $("tagListBox");
    if (tb){
      var tags = BK.allTags();
      tb.innerHTML = tags.length ? tags.map(function(t){
        return '<div class="dash-item" data-tag="' + BK.escAttr(t.name) + '" style="padding:9px 11px">' +
          '<div class="dash-item__body"><p class="dash-item__title" style="font-size:14px">#' + BK.esc(t.name) + '</p>' +
          '<p class="dash-item__meta">' + t.n + ' artikel</p></div>' +
          '<div class="dash-item__ctl"><button class="btn btn--ghost" type="button" data-act="rename">Ganti nama</button></div></div>';
        }).join("") : '<p class="dash-item__empty" style="padding:12px">Belum ada tag. Tulis tag di editor artikel.</p>';
    }
    refreshTermsDatalists();
  }
  (function wireTerms(){
    var add = $("addCat");
    if (add) add.addEventListener("click", function(){
      var inp = $("newCat");
      var name = (inp.value || "").trim();
      if (!name) return;
      if (BK.allCategories().some(function(c){ return BK.slugify(c.name) === BK.slugify(name); })){
        BK.toast("Kategori dengan nama itu sudah ada.", "err"); return;
      }
      window.__extraCats.push(name); saveCats(); inp.value = "";
      renderTerms(); BK.refreshAll(); BK.toast("Kategori \u201c" + name + "\u201d ditambahkan.", "ok");
    });
    var catList = $("catList");
    if (catList) catList.addEventListener("click", function(e){
      var b = e.target.closest("[data-act]"); if (!b) return;
      var name = b.closest("[data-cat]").getAttribute("data-cat");
      var n = countCat(name);
      if (b.getAttribute("data-act") === "rename"){
        var to = prompt("Nama baru untuk kategori \u201c" + name + "\u201d:", name);
        if (!to || to === name) return;
        BK.ARTICLES.forEach(function(a){ if (a.cat === name) a.cat = to; });
        BK.saveArticles();
        window.__extraCats = window.__extraCats.map(function(c){ return c === name ? to : c; }); saveCats();
        renderTerms(); BK.refreshAll(); BK.toast("Kategori diganti.", "ok");
      } else {
        if (n && !confirm("Kategori ini masih dipakai " + n + " artikel bawaan/terbit. Hapus dari daftar tetap?")) return;
        window.__extraCats = window.__extraCats.filter(function(c){ return c !== name; }); saveCats();
        renderTerms(); BK.refreshAll(); BK.toast("Kategori dihapus dari daftar.", "ok");
      }
    });
    var tagBox = $("tagListBox");
    if (tagBox) tagBox.addEventListener("click", function(e){
      var b = e.target.closest("[data-act]"); if (!b) return;
      var name = b.closest("[data-tag]").getAttribute("data-tag");
      var to = prompt("Nama baru untuk tag \u201c" + name + "\u201d:", name);
      if (!to || to === name) return;
      BK.ARTICLES.forEach(function(a){
        if (!a.tags) a.tags = [];
        a.tags = a.tags.map(function(t){ return BK.slugify(t) === BK.slugify(name) ? to : t; });
      });
      BK.saveArticles(); renderTerms(); BK.refreshAll(); BK.toast("Tag diganti.", "ok");
    });
  })();

  /* ---------- perpustakaan media ---------- */
  function mediaItems(){
    var seen = {}, out = [];
    function push(url, key, src, name){
      if (!url || seen[url]) return;
      seen[url] = 1;
      out.push({url: url, key: key, src: src || "", name: name || key});
    }
    BK.ART.forEach(function(a){
      var u = BK.photoForTitle(a.t, 0);
      if (u) push(u, a.t, (BK.PHOTOS[a.t] && BK.PHOTOS[a.t].src) || "default", BK.PHOTOS[a.t] && BK.PHOTOS[a.t].name);
      var m, rx = /!\[[^\]]*\]\(([^)\s]+)\)/g, body = a.body || "";
      while ((m = rx.exec(body))) push(BK.safeImageUrl(m[1]), a.t, "isi", "gambar isi: " + a.t);
    });
    return out;
  }
  function renderMedia(){
    var grid = $("mediaGrid");
    if (!grid) return;
    var items = mediaItems();
    if (!items.length){ grid.innerHTML = '<p class="dash-item__empty">Belum ada gambar.</p>'; return; }
    grid.innerHTML = items.map(function(it){
      return '<div class="media-item" data-url="' + BK.escAttr(it.url) + '" data-key="' + BK.escAttr(it.key) + '">' +
        '<img src="' + BK.escAttr(it.url) + '" alt="" loading="lazy">' +
        '<div class="media-item__b"><p class="media-item__n">' + BK.esc(it.name || it.key) + '</p>' +
        '<div class="media-item__c"><button class="btn btn--primary" type="button" data-act="cover">Set jadi cover</button>' +
        '<button class="btn btn--ghost" type="button" data-act="copy">Salin URL</button>' +
        '<button class="btn btn--ghost" type="button" data-act="body">Ke isi</button></div></div></div>';
    }).join("");
  }
  (function wireMedia(){
    var grid = $("mediaGrid");
    if (grid) grid.addEventListener("click", function(e){
      var b = e.target.closest("[data-act]"); if (!b) return;
      var item = b.closest(".media-item");
      var url = item.getAttribute("data-url");
      var act = b.getAttribute("data-act");
      var st = $("mediaState");
      if (act === "copy"){
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(function(){ BK.toast("URL disalin."); });
        else BK.toast("URL: " + url);
        return;
      }
      if (act === "cover" || act === "body"){
        var title = prompt("Nama/judul artikel yang memakai gambar ini:", Object.keys(BK.PHOTOS).find(function(k){ return BK.PHOTOS[k].url === url; }) || "");
        if (!title) return;
        if (act === "cover"){
          BK.PHOTOS[title] = {url: url, src: "link", at: Date.now()}; BK.savePhotos(); BK.syncPhotos();
          BK.toast("Cover \u201c" + title + "\u201d diganti.", "ok");
        } else {
          var box = $("artBody");
          if (!box){ BK.toast("Buka tab Tulis artikel dulu."); return; }
          var md = "![" + (title || "gambar") + "](" + url + ")";
          var wpane = document.querySelector('[data-dash-tab="write"]'); if (wpane) wpane.click();
          var start = box.selectionStart || box.value.length;
          box.value = box.value.slice(0, start) + "\n\n" + md + "\n\n" + box.value.slice(start);
          if (window.__editorSync) window.__editorSync();
          BK.toast("Gambar disisipkan ke isi artikel.", "ok");
        }
        if (st) st.textContent = "";
      }
    });
    var mf = $("mediaFile");
    if (mf) mf.addEventListener("change", function(){
      var f = mf.files && mf.files[0]; if (!f) return;
      var st = $("mediaState");
      BK.shrinkImage(f).then(function(r){
        var title = prompt("Simpan sebagai cover artikel (judul):", "");
        if (title){ BK.PHOTOS[title] = {url: r.url, src: "file", name: f.name, at: Date.now()}; BK.savePhotos(); BK.syncPhotos(); }
        renderMedia();
        if (st) st.textContent = "Berkas diproses (" + r.w + "\u00d7" + r.h + ").";
      }).catch(function(err){ if (st) st.textContent = err.message; });
    });
    var md = $("mediaDrive");
    if (md) md.addEventListener("click", function(){
      var st = $("mediaState");
      if (!BK.driveConnected() && !BK.driveDemoActive()){
        if (st) st.textContent = "Hubungkan Google Drive dulu di panel Kelola Foto — atau aktifkan mode demo lewat tombol “Mode demo” di editor Tulis artikel.";
        return;
      }
      if (st) st.textContent = BK.driveDemoActive() ? "Memuat gambar contoh (mode demo)…" : "Membaca Drive\u2026";
      BK.listDriveImages().then(function(files){
        if (st) st.textContent = files.length + (BK.driveDemoActive() ? " gambar contoh (mode demo). Klik Sekali untuk menjadikan cover." : " gambar di Drive. Klik Sekali untuk menjadikan cover.");
        var grid = $("mediaGrid");
        if (!grid) return;
        var cur = grid.innerHTML;
        grid.innerHTML = files.map(function(f){
          return '<div class="media-item" data-url="' + BK.escAttr(f.url) + '" data-key="' + BK.escAttr(f.name) + '">' +
            '<img src="' + BK.escAttr(f.thumb || BK.driveThumbUrl(f.id, 400)) + '" alt="" loading="lazy">' +
            '<div class="media-item__b"><p class="media-item__n">' + BK.esc(f.name) + '</p>' +
            '<div class="media-item__c"><button class="btn btn--primary" type="button" data-act="cover">Set jadi cover</button>' +
            '<button class="btn btn--ghost" type="button" data-act="copy">Salin URL</button>' +
            '<button class="btn btn--ghost" type="button" data-act="body">Ke isi</button></div></div></div>';
        }).join("") + cur;
      }).catch(function(err){ if (st) st.textContent = err.message; });
    });
  })();

  /* ---------- moderasi komentar ---------- */
  function renderCommentsAdmin(){
    var box = $("cmtAdminList");
    if (!box || !window.__comments) return;
    var f = $("cmtFilter") ? $("cmtFilter").value : "";
    var rows = window.__comments.all().filter(function(c){ return !f || c.status === f; });
    rows.sort(function(a, b){ return (b.at || 0) - (a.at || 0); });
    if (!rows.length){ box.innerHTML = '<p class="dash-item__empty">Tidak ada komentar pada filter ini.</p>'; return; }
    box.innerHTML = rows.map(function(c){
      var art = BK.articleBySlug(c.slug);
      return '<div class="dash-item" data-id="' + BK.escAttr(c.id) + '" style="align-items:flex-start">' +
        '<div class="dash-item__body"><p class="dash-item__title" style="font-size:14px">' + BK.esc(c.name) +
        ' ' + statusPill(c.status) + '</p>' +
        '<p class="dash-item__meta">' + BK.esc(art ? art.t : c.slug) + ' \u00b7 ' + BK.relTime(c.at) + '</p>' +
        '<p style="margin:6px 0 0;font:400 13px/1.6 var(--font-ui);color:var(--ink-700)">' + BK.esc(c.text) + '</p></div>' +
        '<div class="dash-item__ctl">' +
        (c.status !== "approved" ? '<button class="btn btn--ghost" type="button" data-act="approve">Setujui</button>' : '') +
        (c.status !== "spam" ? '<button class="btn btn--ghost" type="button" data-act="spam">Spam</button>' : '') +
        '<button class="btn btn--danger" type="button" data-act="del">Hapus</button></div></div>';
    }).join("");
  }
  window.__commentsAdminSync = function(){ if ($("dashComments") && !$("dashComments").hidden) renderCommentsAdmin(); };
  (function wireComments(){
    var box = $("cmtAdminList");
    if (box) box.addEventListener("click", function(e){
      var b = e.target.closest("[data-act]"); if (!b || !window.__comments) return;
      var id = b.closest(".dash-item").getAttribute("data-id");
      var act = b.getAttribute("data-act");
      if (act === "del"){ window.__comments.remove(id); BK.toast("Komentar dihapus."); }
      else { window.__comments.setStatus(id, act === "spam" ? "spam" : "approved"); BK.toast("Komentar diperbarui.", "ok"); }
      renderCommentsAdmin();
      var a = BK.articleBySlug(BK.currentSlug);
      if (a && window.__extrasSync) window.__extrasSync(a);
    });
    var cf = $("cmtFilter");
    if (cf) cf.addEventListener("change", renderCommentsAdmin);
  })();

  /* ---------- ekspor / impor seluruh situs (ala WXR) ---------- */
  function exportAll(){
    var data = {
      generator: "balikisah.com", version: 1, exportedAt: new Date().toISOString(),
      articles: BK.ARTICLES, photos: BK.PHOTOS, cats: window.__extraCats,
      comments: window.__comments ? window.__comments.all() : [], revisions: REVS
    };
    BK.downloadText("balikisah-situs.json", JSON.stringify(data, null, 2));
    BK.toast("Seluruh isi situs diekspor.", "ok");
  }
  function importAll(file){
    var fr = new FileReader();
    fr.onload = function(){
      try {
        var d = JSON.parse(fr.result);
        window.__importDriveFixes = 0;
        if (d.articles) {
          var driveFixes = 0;
          BK.ARTICLES = d.articles.map(function(a){
            if (!a) return a;
            ["body", "excerpt", "seoTitle", "seoDesc", "authorBio"].forEach(function(k){
              if (typeof a[k] === "string" && a[k]){
                var r = BK.normalizeDriveLinksInText(a[k]);
                if (r.count){ a[k] = r.text; driveFixes += r.count; }
              }
            });
            return a;
          });
          BK.saveArticles();
          window.__importDriveFixes = driveFixes;
        }
        if (d.photos){ Object.keys(d.photos).forEach(function(k){ BK.PHOTOS[k] = d.photos[k]; }); BK.savePhotos(); }
        if (d.cats){ window.__extraCats = d.cats; saveCats(); }
        if (d.comments && window.__comments){
          d.comments.forEach(function(c){ window.__comments.add(c.slug, c.name, c.text, c.status); });
        }
        if (d.revisions){ Object.keys(d.revisions).forEach(function(k){ REVS[k] = d.revisions[k]; }); saveRevs(); }
        BK.refreshAll(); renderTerms(); renderMedia(); renderCommentsAdmin();
        var fx = window.__importDriveFixes || 0;
        window.__importDriveFixes = 0;
        BK.toast("Impor selesai." + (fx ? " " + fx + " tautan Google Drive diubah ke URL gambar lh3." : ""), "ok");
      } catch (err){ BK.toast("Berkas tidak valid: " + err.message, "err"); }
    };
    fr.readAsText(file);
  }

  /* ---------- Sampah (soft delete) ---------- */
  function trashedRows(){ return BK.ART.filter(function(a){ return a.trashed; }); }
  function renderTrash(){
    var box = $("trashList");
    if (!box) return;
    var rows = trashedRows();
    if (!rows.length){ box.innerHTML = '<p class="dash-item__empty">Sampah kosong.</p>'; return; }
    box.innerHTML = rows.map(function(a){
      return '<div class="dash-item" data-key="' + BK.escAttr(a.t) + '">' +
        '<div class="dash-item__body"><p class="dash-item__title">' + BK.esc(a.t) + ' ' + statusPill(a.status) + '</p>' +
        '<p class="dash-item__meta">' + BK.esc(a.c) + ' \u00b7 ' + BK.esc(a.author) + ' \u00b7 /' + BK.esc(a.slug) + '</p></div>' +
        '<div class="dash-item__ctl">' +
        (a.admin ? '<button class="btn btn--primary" type="button" data-act="untrash">Pulihkan</button>' : '') +
        '<button class="btn btn--danger" type="button" data-act="purge"' + (a.admin ? '' : ' disabled') + '>Hapus permanen</button>' +
        '</div></div>';
    }).join("");
  }
  window.__renderTrash = renderTrash;
  (function wireTrash(){
    var box = $("trashList");
    if (box) box.addEventListener("click", function(e){ window.__adminListAction(e); renderTrash(); });
    var em = $("trashEmpty");
    if (em) em.addEventListener("click", function(){
      if (!confirm("Kosongkan Sampah? Artikel di dalamnya dihapus permanen.")) return;
      BK.ARTICLES = BK.ARTICLES.filter(function(a){ return !a.trashed; });
      BK.saveArticles(); BK.refreshAll(); renderTrash(); window.__renderAdminList();
      var st = $("trashState"); if (st) st.textContent = "Sampah dikosongkan.";
      BK.toast("Sampah dikosongkan.", "ok");
    });
  })();

  /* ---------- Tampilan: widget & menu ---------- */
  function renderWidgetAdmin(){
    var box = $("widgetList");
    if (!box) return;
    var conf = BK.WIDGETS.slice();
    BK.WIDGET_KINDS.forEach(function(k){ if (!conf.some(function(w){ return w.id === k.id; })) conf.push({id:k.id, on:false}); });
    box.innerHTML = conf.map(function(w, i){
      var k = BK.WIDGET_KINDS.filter(function(x){ return x.id === w.id; })[0] || {label:w.id};
      return '<div class="dash-item" data-wid="' + BK.escAttr(w.id) + '" style="padding:9px 11px">' +
        '<div class="dash-item__body"><p class="dash-item__title" style="font-size:14px">' + BK.esc(k.label) + '</p>' +
        '<p class="dash-item__meta">' + (w.on === false ? "tidak aktif" : "aktif") + '</p></div>' +
        '<div class="dash-item__ctl">' +
        '<button class="btn btn--ghost" type="button" data-wact="up" data-i="' + i + '"' + (i === 0 ? ' disabled' : '') + '>\u2191</button>' +
        '<button class="btn btn--ghost" type="button" data-wact="down" data-i="' + i + '"' + (i === conf.length-1 ? ' disabled' : '') + '>\u2193</button>' +
        '<button class="btn ' + (w.on === false ? 'btn--primary' : 'btn--ghost') + '" type="button" data-wact="toggle" data-i="' + i + '">' +
          (w.on === false ? "Aktifkan" : "Matikan") + '</button></div></div>';
    }).join("");
  }
  (function wireWidgets(){
    var box = $("widgetList");
    if (!box) return;
    box.addEventListener("click", function(e){
      var b = e.target.closest("[data-wact]"); if (!b) return;
      var conf = BK.WIDGETS.slice();
      BK.WIDGET_KINDS.forEach(function(k){ if (!conf.some(function(w){ return w.id === k.id; })) conf.push({id:k.id, on:false}); });
      var i = parseInt(b.getAttribute("data-i"), 10);
      var act = b.getAttribute("data-wact");
      if (act === "toggle") conf[i].on = conf[i].on === false;
      else {
        var j = act === "up" ? i - 1 : i + 1;
        if (j < 0 || j >= conf.length) return;
        var tmp = conf[i]; conf[i] = conf[j]; conf[j] = tmp;
      }
      BK.WIDGETS = conf; BK.saveWidgets();
      renderWidgetAdmin();
      if (window.__moduleRefresh) window.__moduleRefresh();
    });
  })();

  var MENU_ROUTE_LABEL = {
    kategori:"Halaman kategori", tag:"Halaman tag", penulis:"Halaman penulis",
    arsip:"Arsip bulanan", unggulan:"Postingan unggulan", berita:"Beranda/blog",
    dokumen:"Dokumen PRD", beranda:"Beranda", tentang:"Halaman tentang"
  };
  /* Label target menu untuk ditampilkan di daftar; target kategori bernama
     ("kategori:<Nama>") dijelaskan sebagai "Kategori: <Nama>". */
  function menuTargetLabel(target){
    var t = String(target || "").toLowerCase();
    if (/^kategori\s*:/.test(t)){
      var name = String(target).split(":").slice(1).join(":").trim();
      return name ? ("Kategori: " + name) : "Halaman kategori";
    }
    return MENU_ROUTE_LABEL[t] || target;
  }
  function renderMenuAdmin(){
    var box = $("menuList");
    if (!box) return;
    box.innerHTML = BK.MENU.map(function(m, i){
      return '<div class="dash-item" data-mi="' + i + '" style="padding:9px 11px">' +
        '<div class="dash-item__body"><p class="dash-item__title" style="font-size:14px">' + BK.esc(m.label) + '</p>' +
        '<p class="dash-item__meta">' + BK.esc(menuTargetLabel(m.target)) + '</p></div>' +
        '<div class="dash-item__ctl">' +
        '<button class="btn btn--ghost" type="button" data-mact="up" data-i="' + i + '"' + (i === 0 ? ' disabled' : '') + '>\u2191</button>' +
        '<button class="btn btn--ghost" type="button" data-mact="down" data-i="' + i + '"' + (i === BK.MENU.length-1 ? ' disabled' : '') + '>\u2193</button>' +
        '<button class="btn btn--ghost" type="button" data-mact="rename" data-i="' + i + '">Ganti nama</button>' +
        '<button class="btn btn--danger" type="button" data-mact="del" data-i="' + i + '">Hapus</button></div></div>';
    }).join("");
    var presets = $("menuPresets");
    if (presets) presets.innerHTML = Object.keys(MENU_ROUTE_LABEL).map(function(k){ return '<option>' + k + '</option>'; }).join("");
  }
  (function wireMenu(){
    var box = $("menuList");
    if (box) box.addEventListener("click", function(e){
      var b = e.target.closest("[data-mact]"); if (!b) return;
      var menu = BK.MENU.slice();
      var i = parseInt(b.getAttribute("data-i"), 10);
      var act = b.getAttribute("data-mact");
      if (act === "rename"){
        var to = prompt("Label baru:", menu[i].label);
        if (!to) return;
        menu[i] = {label: to, target: menu[i].target};
      } else if (act === "del"){
        menu.splice(i, 1);
      } else {
        var j = act === "up" ? i - 1 : i + 1;
        if (j < 0 || j >= menu.length) return;
        var tmp = menu[i]; menu[i] = menu[j]; menu[j] = tmp;
      }
      BK.MENU = menu; BK.saveMenu(); renderMenuAdmin(); BK.applyMenu();
    });
    var add = $("addMenuItem");
    if (add) add.addEventListener("click", function(){
      var inp = $("newMenuItem");
      var raw = (inp.value || "").trim();
      if (!raw) return;
      var parts = raw.split(/\s*\|\s*/);
      var label = (parts[0] || "").trim();
      var rawTarget = (parts[1] || parts[0] || "").trim();
      /* Dukung entri seperti "Budaya | kategori:Budaya" dan "Tips | kategori:Tips Traveling".
         Nama kategori di belakang ":" dipertahankan apa adanya (case asli). */
      var km = rawTarget.match(/^([A-Za-z]+)\s*:\s*(.+)$/);
      var target;
      if (km && MENU_ROUTE_LABEL[km[1].toLowerCase()]) {
        target = km[1].toLowerCase() + ":" + km[2].trim();
      } else {
        target = rawTarget.toLowerCase();
        var known = Object.keys(MENU_ROUTE_LABEL).some(function(k){ return target.indexOf(k) > -1 || k.indexOf(target) > -1; });
        if (!known) target = "beranda";
      }
      var menu = BK.MENU.slice();
      menu.push({label: label, target: target});
      BK.MENU = menu; BK.saveMenu(); inp.value = "";
      renderMenuAdmin(); BK.applyMenu();
      BK.toast("Tautan menu ditambahkan.", "ok");
    });
  })();

  /* ---------- Pengaturan situs ---------- */
  function fillSettings(){
    var S = BK.SETTINGS;
    function set(id, v){ var el = $(id); if (el) el.value = v; }
    function chk(id, v){ var el = $(id); if (el) el.checked = !!v; }
    set("setName", S.name); set("setTagline", S.tagline); set("setDesc", S.desc);
    set("setEmail", S.email); set("setPerPage", S.perPage);
    var pm = $("setPermalink"); if (pm) pm.value = S.permalink;
    var cm = $("setComments"); if (cm) cm.value = S.comments;
    chk("setRss", S.rss); chk("setSitemap", S.sitemap); chk("setIndex", S.index);
  }
  window.__restoreSettings = fillSettings;
  (function wireSettings(){
    var btn = $("saveSettings");
    if (btn) btn.addEventListener("click", function(){
      function v(id, d){ var el = $(id); return el ? el.value : d; }
      function c(id){ var el = $(id); return el ? !!el.checked : false; }
      BK.setSettings({
        name: v("setName", "balikisah.com").trim() || "balikisah.com",
        tagline: v("setTagline", "").trim(), desc: v("setDesc", "").trim(),
        email: v("setEmail", "").trim(), perPage: parseInt(v("setPerPage", 6), 10) || 6,
        permalink: v("setPermalink", "/?post=%slug%"),
        comments: v("setComments", "moderasi"),
        rss: c("setRss"), sitemap: c("setSitemap"), index: c("setIndex")
      });
      BK.applySiteIdentity();
      if (window.__moduleRefresh) window.__moduleRefresh();
      var st = $("setState");
      if (st) st.textContent = "Pengaturan disimpan.";
      BK.toast("Pengaturan situs disimpan.", "ok");
    });
  })();

  /* ---------- tab switching dari shell ---------- */
  window.__dashTab = function(which){
    if (which === "list") window.__renderAdminList();
    else if (which === "media") renderMedia();
    else if (which === "terms") renderTerms();
    else if (which === "comments") renderCommentsAdmin();
    else if (which === "trash") renderTrash();
    else if (which === "appearance"){ renderWidgetAdmin(); renderMenuAdmin(); }
    else if (which === "settings") fillSettings();
    else if (which === "write"){ refreshTermsDatalists(); renderTagPick(); if (window.__editorSync) window.__editorSync(); }
  };

  /* ---------- boot modul dasbor ---------- */
  /* Editor & daftar artikel dirakit di shell SEBELUM blok modul ini jalan,
     jadi kait yang disiapkan shell dilewati. Pasang di sini. */
  if (typeof window.__editorWired === "function") window.__editorWired(window);
  (function wireAdminList(){
    var list = $("adminList");
    if (list && !list.dataset.wired){ list.dataset.wired = "1"; list.addEventListener("click", window.__adminListAction); }
  })();
  refreshTermsDatalists();
  renderTerms();
  var expBtn = document.createElement("button");
  expBtn.className = "btn btn--ghost"; expBtn.type = "button"; expBtn.textContent = "Ekspor seluruh situs";
  expBtn.addEventListener("click", exportAll);
  var impBtn = document.createElement("label");
  impBtn.className = "btn btn--ghost"; impBtn.textContent = "Impor seluruh situs";
  impBtn.innerHTML += '<input type="file" accept=".json,application/json" hidden id="fullImport">';
  var panelRow = document.querySelector("#adminPanel .admin-panel__row");
  if (panelRow){ panelRow.appendChild(expBtn); panelRow.appendChild(impBtn); }
  document.addEventListener("change", function(e){
    if (e.target && e.target.id === "fullImport" && e.target.files && e.target.files[0]) importAll(e.target.files[0]);
  });

  /* Segarkan widget/taksonomi tiap data berubah. */
  if (window.__moduleRefresh) window.__moduleRefresh();
})();
