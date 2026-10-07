/* ============================================================
   MODUL: Halaman artikel lanjutan — daftar isi (TOC), statistik
          baca + suka, tag, tombol bagikan, kotak penulis, navigasi
          postingan sebelumnya/berikutnya, dan komentar.
   ============================================================ */
/* (modul mandiri; butuh window.BK dari shell) */
(function(){
  "use strict";
  var BK = window.BK;
  if (!BK) return;
  function $(id){ return document.getElementById(id); }

  /* ---------- komentar (disimpan di browser ini) ---------- */
  var C_STORE = "balikisah.comments.v1";
  var COMMENTS = (function(){ try { return JSON.parse(localStorage.getItem(C_STORE)) || []; } catch (e) { return []; } })();
  function saveComments(){ try { localStorage.setItem(C_STORE, JSON.stringify(COMMENTS)); } catch (e) {} }
  function commentsFor(slug, onlyApproved){
    return COMMENTS.filter(function(c){
      return c.slug === slug && (!onlyApproved || c.status === "approved");
    }).sort(function(a, b){ return (a.at || 0) - (b.at || 0); });
  }
  function addComment(slug, name, text, status, parent){
    var c = {id: "c" + Date.now().toString(36) + Math.floor(Math.random()*1e4).toString(36),
             slug: slug, name: name, text: text, at: Date.now(), status: status || "approved",
             parent: parent || ""};
    COMMENTS.push(c);
    saveComments();
    return c;
  }
  /* Kebijakan komentar diambil dari Pengaturan situs. */
  function commentPolicy(){ return (BK.SETTINGS && BK.SETTINGS.comments) || "moderasi"; }
  window.__comments = {
    all: function(){ return COMMENTS.slice(); },
    for: commentsFor,
    setStatus: function(id, status){
      COMMENTS.forEach(function(c){ if (c.id === id) c.status = status; });
      saveComments();
    },
    remove: function(id){
      COMMENTS = COMMENTS.filter(function(c){ return c.id !== id; });
      saveComments();
    },
    add: addComment,
    save: saveComments
  };

  function fmtTime(ts){ return BK.relTime(ts); }
  function initials(name){
    return String(name || "?").trim().split(/\s+/).map(function(w){ return w.charAt(0); }).slice(0, 2).join("").toUpperCase();
  }

  /* ---------- daftar isi dari heading artikel ---------- */
  function renderToc(a){
    var box = $("artToc");
    if (!box) return;
    var toc = (a && a.toc) || [];
    if (toc.length < 2){ box.hidden = true; box.innerHTML = ""; return; }
    box.hidden = false;
    box.innerHTML = '<h2 class="toc__h">Daftar isi</h2><ol>' +
      toc.map(function(h){
        return '<li><a href="#' + h.id + '" data-lvl="' + h.level + '" data-toc="' + h.id + '">' +
          BK.esc(h.text) + '</a></li>';
      }).join("") + '</ol>';
  }

  /* ---------- statistik baca + suka ---------- */
  function renderStats(a){
    var box = $("artStats");
    if (!box || !a) return;
    var liked = BK.readCookie("bk_like_" + a.slug) === "1";
    box.innerHTML =
      '<div class="stat"><p class="stat__num">' + (a.views || 0).toLocaleString("id-ID") + '</p>' +
      '<p class="stat__lab">dibaca</p></div>' +
      '<button class="stat" type="button" id="likeBtn" aria-pressed="' + liked + '" style="text-align:left">' +
      '<p class="stat__num" id="likeNum">' + (a.likes || 0) + '</p>' +
      '<p class="stat__lab">' + (liked ? "Anda menyukai" : "suka") + '</p></button>' +
      '<div class="stat"><p class="stat__num">' + BK.readMinutes(a.body) + '</p>' +
      '<p class="stat__lab">menit baca</p></div>' +
      '<div class="stat"><p class="stat__num">' + (a.tags || []).length + '</p>' +
      '<p class="stat__lab">tag</p></div>';
  }

  /* ---------- tag artikel ---------- */
  function renderTags(a){
    var box = $("artTagList");
    if (!box) return;
    var tags = a.tags || [];
    box.innerHTML = tags.map(function(t){
      return '<a href="#" data-goto="blog" data-blog="tag" data-key="' + BK.escAttr(t) + '">#' + BK.esc(t) + '</a>';
    }).join("");
    box.hidden = tags.length === 0;
  }

  /* ---------- tombol bagikan ---------- */
  function renderShare(a){
    var box = $("artShare");
    if (!box) return;
    var url = location.href;
    box.innerHTML = '<span class="share__label">Bagikan</span>' +
      '<button type="button" data-share="wa">WhatsApp</button>' +
      '<button type="button" data-share="fb">Facebook</button>' +
      '<button type="button" data-share="x">X / Twitter</button>' +
      '<button type="button" data-share="copy">Salin tautan</button>' +
      '<button type="button" data-print="1">Cetak</button>';
    box.setAttribute("data-url", url);
    box.setAttribute("data-text", a.t);
  }

  /* ---------- kotak penulis ---------- */
  function renderAuthorBox(a){
    var box = $("artAuthorBox");
    if (!box) return;
    var n = BK.byAuthor(a.author).length;
    var bio = a.authorBio || ("Penulis di " + (BK.SETTINGS.name || "balikisah.com") + " dengan " + n +
      " artikel terbit. Menulis seputar sejarah, babad, dan warisan budaya Bali.");
    box.innerHTML = '<div class="author-box">' +
      '<div class="author-box__ava" aria-hidden="true">' + BK.esc(initials(a.author)) + '</div>' +
      '<div><p class="author-box__name">' + BK.esc(a.author) + '</p>' +
      '<p class="author-box__bio">' + BK.esc(bio) + '</p>' +
      '<p style="margin:8px 0 0"><a class="btn btn--ghost" href="#" data-goto="blog" data-blog="penulis" data-key="' +
      BK.escAttr(a.author) + '">Semua artikel penulis ini</a></p></div></div>';
  }

  /* ---------- navigasi postingan sebelumnya/berikutnya ---------- */
  function renderPostNav(a){
    var box = $("artPostNav");
    if (!box) return;
    var pn = BK.prevNext(a.slug);
    box.innerHTML =
      (pn.next ? '<a class="postnav postnav--prev" href="#" data-goto="article" data-post="' + BK.escAttr(pn.next.slug) + '">' +
        '<span class="postnav__dir">\u2190 Postingan berikutnya</span><span class="postnav__title">' + BK.esc(pn.next.t) + '</span></a>' :
        '<span class="postnav__empty"></span>') +
      (pn.prev ? '<a class="postnav postnav--next" href="#" data-goto="article" data-post="' + BK.escAttr(pn.prev.slug) + '">' +
        '<span class="postnav__dir">Postingan sebelumnya \u2192</span><span class="postnav__title">' + BK.esc(pn.prev.t) + '</span></a>' : "");
  }

  /* ---------- komentar: tampilan ---------- */
  function commentHtml(c, isReply){
    return '<article class="citem' + (isReply ? ' citem--reply' : '') + '" data-cid="' + BK.escAttr(c.id) + '">' +
      '<div class="citem__ava" aria-hidden="true">' + BK.esc(initials(c.name)) + '</div>' +
      '<div class="citem__b"><p class="citem__head">' + BK.esc(c.name) +
      ' <span class="citem__time">' + fmtTime(c.at) + '</span></p>' +
      '<p class="citem__text">' + BK.esc(c.text).replace(/\n/g, "<br>") + '</p>' +
      '<button class="citem__reply" type="button" data-reply="' + BK.escAttr(c.id) + '">Balas</button>' +
      '</div></article>';
  }
  function renderComments(a){
    var box = $("cmtList");
    if (!box || !a) return;
    var rows = commentsFor(a.slug, true);
    var sub = $("cmtSub");
    if (sub) sub.textContent = commentPolicy() === "tutup" ? "Komentar ditutup untuk artikel ini."
      : (rows.length ? rows.length + " komentar." : "Belum ada komentar. Jadilah yang pertama berdiskusi.");
    var form = $("cmtForm");
    if (form) form.hidden = commentPolicy() === "tutup";
    var roots = rows.filter(function(c){ return !c.parent || !rows.some(function(x){ return x.id === c.parent; }); });
    box.innerHTML = roots.map(function(c){
      var kids = rows.filter(function(x){ return x.parent === c.id; });
      return commentHtml(c, false) + kids.map(function(k){ return commentHtml(k, true); }).join("");
    }).join("");
  }

  /* ---------- dipanggil shell setiap renderArticle() ---------- */
  window.__extrasSync = function(a){
    if (!a) return;
    renderToc(a);
    renderStats(a);
    renderTags(a);
    renderShare(a);
    renderAuthorBox(a);
    renderPostNav(a);
    renderComments(a);
    if (window.__articleWidgets) window.__articleWidgets();
  };

  /* Modul dimuat setelah shell sempat merender artikel: lengkapi tampilan
     artikel yang sedang aktif sekali lagi setelah __extrasSync terpasang. */
  (function(){
    var a = BK.articleBySlug(BK.currentSlug);
    if (a) window.__extrasSync(a);
  })();

  /* ---------- interaksi: suka, bagikan, klik TOC ---------- */
  document.addEventListener("click", function(e){
    var toc = e.target.closest("[data-toc]");
    if (toc){
      e.preventDefault();
      var el = document.getElementById(toc.getAttribute("data-toc"));
      if (el) el.scrollIntoView({behavior: "smooth", block: "start"});
      return;
    }
    var like = e.target.closest("#likeBtn");
    if (like){
      var a = BK.articleBySlug(BK.currentSlug);
      if (!a) return;
      var now = (function(){
        var key = "bk_like_" + a.slug, cur = BK.readCookie(key) === "1";
        BK.writeCookie(key, cur ? "0" : "1", 365);
        a.likes = Math.max(0, (a.likes || 0) + (cur ? -1 : 1));
        try {
          var map = JSON.parse(localStorage.getItem("balikisah.likes.v1")) || {};
          map[a.slug] = a.likes; localStorage.setItem("balikisah.likes.v1", JSON.stringify(map));
        } catch (err) {}
        return !cur;
      })();
      renderStats(a);
      BK.toast(now ? "Terima kasih! Anda menyukai artikel ini." : "Suka dibatalkan.");
      return;
    }
    var sh = e.target.closest("[data-share]");
    if (sh){
      e.preventDefault();
      var which = sh.getAttribute("data-share");
      var host = sh.closest("#artShare");
      var url = host ? host.getAttribute("data-url") : location.href;
      var text = host ? host.getAttribute("data-text") : document.title;
      var eu = encodeURIComponent(url), et = encodeURIComponent(text + " \u2014 " + url);
      if (which === "wa") window.open("https://wa.me/?text=" + et, "_blank", "noopener");
      else if (which === "fb") window.open("https://www.facebook.com/sharer/sharer.php?u=" + eu, "_blank", "noopener");
      else if (which === "x") window.open("https://twitter.com/intent/tweet?text=" + et, "_blank", "noopener");
      else {
        var done = function(){ BK.toast("Tautan disalin."); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, function(){ BK.toast("Salin manual: " + url); });
        else BK.toast("Salin manual: " + url);
      }
      return;
    }
  });

  /* ---------- kirim komentar ---------- */
  var replyTo = "";
  var replyHint = document.createElement("p");
  replyHint.className = "cform__reply";
  replyHint.hidden = true;
  replyHint.innerHTML = 'Membalas <b id="replyWho"></b> <button type="button" class="citem__reply" id="replyCancel">batal</button>';
  var form = $("cmtForm");
  if (form && form.parentNode) form.parentNode.insertBefore(replyHint, form);
  document.addEventListener("click", function(e){
    if (e.target.closest("#replyCancel")){ replyTo = ""; replyHint.hidden = true; return; }
    var r = e.target.closest("[data-reply]");
    if (!r) return;
    var host = r.closest(".citem");
    var cid = r.getAttribute("data-reply");
    replyTo = cid;
    var who = document.getElementById("replyWho");
    if (who && host) who.textContent = host.querySelector(".citem__head").textContent.replace(/·.*/, "").trim();
    replyHint.hidden = false;
    if ($("cmtText")) $("cmtText").focus();
  });
  if (form) form.addEventListener("submit", function(e){
    e.preventDefault();
    var a = BK.articleBySlug(BK.currentSlug);
    if (!a) return;
    if (commentPolicy() === "tutup"){ BK.toast("Komentar ditutup."); return; }
    var name = ($("cmtName").value || "").trim();
    var mail = ($("cmtMail").value || "").trim();
    var text = ($("cmtText").value || "").trim();
    var err = $("cmtErr");
    if (err) err.textContent = "";
    if (!name){ if (err) err.textContent = "Isi nama dulu."; return; }
    if (mail && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(mail)){ if (err) err.textContent = "Alamat email belum benar."; return; }
    if (text.length < 4){ if (err) err.textContent = "Komentar terlalu pendek."; return; }
    if (/https?:\/\//i.test(text) && commentPolicy() === "moderasi"){
      if (err) err.textContent = "Komentar memuat tautan \u2014 akan ditinjau redaksi dulu.";
    }
    var status = commentPolicy() === "auto" ? "approved" : "pending";
    var wasReply = replyTo;
    addComment(a.slug, name, text, status, replyTo);
    var mail2 = $("cmtMail");
    if (mail2 && BK.writeCookie) BK.writeCookie("bk_cmt_name", name, 180);
    $("cmtName").value = BK.readCookie("bk_cmt_name") || "";
    $("cmtMail").value = ""; $("cmtText").value = "";
    replyTo = ""; replyHint.hidden = true;
    renderComments(a);
    BK.toast(status === "approved" ? "Komentar terkirim." : "Komentar terkirim dan menunggu moderasi.");
    if (err){ err.setAttribute("data-tone", "ok"); err.textContent = status === "approved" ? "" : "Menunggu persetujuan redaksi."; }
    if (window.__commentsAdminSync) window.__commentsAdminSync();
  });
  (function restoreName(){
    var el = $("cmtName");
    if (el && BK.readCookie) el.value = BK.readCookie("bk_cmt_name") || "";
  })();
})();
