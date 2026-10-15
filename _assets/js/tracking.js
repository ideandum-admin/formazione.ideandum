/**
 * ═══════════════════════════════════════════════════════════════
 *  tracking.js — formazione.ideandum.com
 * ═══════════════════════════════════════════════════════════════
 *
 *  File UNICO per GTM e Meta Pixel.
 *  Incluso in TUTTE le pagine del sottodominio.
 *
 *  ✅ Per aggiornare GTM o Pixel: modificare SOLO questo file.
 *     Le modifiche si applicano automaticamente a tutte le pagine.
 *
 *  GTM ID  : GTM-THCFGR
 *  Pixel ID: 774485682652320
 *
 *  Non modificare il resto del file.
 * ═══════════════════════════════════════════════════════════════
 */

(function() {

  /* ─────────────────────────────────────────────────────────────
     GOOGLE TAG MANAGER
  ───────────────────────────────────────────────────────────── */
  var GTM_ID = 'GTM-THCFGR';

  // Script GTM — va nell'<head>
  (function(w,d,s,l,i){
    w[l]=w[l]||[];
    w[l].push({'gtm.start': new Date().getTime(), event:'gtm.js'});
    var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),
        dl=l!='dataLayer'?'&l='+l:'';
    j.async=true;
    j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;
    f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer',GTM_ID);

  // <noscript> GTM — inserito come primo elemento del <body>
  document.addEventListener('DOMContentLoaded', function() {
    var ns = document.createElement('noscript');
    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.googletagmanager.com/ns.html?id=' + GTM_ID;
    iframe.height = '0'; iframe.width = '0';
    iframe.style.display = 'none'; iframe.style.visibility = 'hidden';
    ns.appendChild(iframe);
    document.body.insertBefore(ns, document.body.firstChild);
  });


  /* ─────────────────────────────────────────────────────────────
     META PIXEL
     NOTA: se gestisci già il Pixel tramite GTM, commenta
     questo blocco per evitare doppio fuoco su PageView.
  ───────────────────────────────────────────────────────────── */
  var PIXEL_ID = '774485682652320';

  !function(f,b,e,v,n,t,s){
    if(f.fbq)return;
    n=f.fbq=function(){ n.callMethod ? n.callMethod.apply(n,arguments) : n.queue.push(arguments); };
    if(!f._fbq)f._fbq=n;
    n.push=n; n.loaded=!0; n.version='2.0'; n.queue=[];
    t=b.createElement(e); t.async=!0;
    t.src=v;
    s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s);
  }(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');

  fbq('init', PIXEL_ID);
  fbq('track', 'PageView');

  // Noscript Pixel
  document.addEventListener('DOMContentLoaded', function() {
    var ns = document.createElement('noscript');
    var img = document.createElement('img');
    img.height='1'; img.width='1'; img.style.display='none';
    img.src='https://www.facebook.com/tr?id='+PIXEL_ID+'&ev=PageView&noscript=1';
    ns.appendChild(img);
    document.body.appendChild(ns);
  });


  /* ─────────────────────────────────────────────────────────────
     DATA LAYER — dati base per tutte le pagine
  ───────────────────────────────────────────────────────────── */
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    'event'    : 'page_data',
    'site'     : 'formazione.ideandum.com',
    'page_type': 'webinar'
  });

})();
