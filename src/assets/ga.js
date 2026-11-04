/* Google Analytics 4 events for the storefronts. Every call is guarded: if gtag is blocked or missing, nothing breaks.
   Clicks describe intent only: no lead, booking completion or purchase is inferred.
   add_to_cart and begin_checkout are sent from cart.js; paid sales must come from Shopify. */
(function(){
  function ga(n,p){try{if(typeof window.gtag==='function')window.gtag('event',n,p||{})}catch(_){}}
  window.niGA=ga;
  try{
    if(/^\/products\//.test(location.pathname)){
      var b=document.getElementById('buy'),it=null;
      if(b&&b.dataset&&b.dataset.v){var d=b.dataset;it={item_id:String(d.v),item_name:d.t+(d.vt&&d.vt!=='Default Title'?' - '+d.vt:''),price:+d.p||0,quantity:1};if(d.c)it.item_category=d.c}
      else{[].forEach.call(document.querySelectorAll('script[type="application/ld+json"]'),function(s){if(it)return;try{var j=JSON.parse(s.textContent);(Array.isArray(j)?j:[j]).forEach(function(o){if(!it&&o&&o['@type']==='Product'){var of=Array.isArray(o.offers)?o.offers[0]:(o.offers||{});it={item_id:String(o.sku||location.pathname.split('/')[2]),item_name:o.name,price:+of.price||0,quantity:1}}})}catch(_){}})}
      if(it)ga('view_item',{currency:'USD',value:it.price,items:[it]});
    }
  }catch(_){}
  var BOOK_HOSTS=['book.squareup.com','squareup.com','setmore.com','calendly.com','acuityscheduling.com','as.me','vagaro.com','booksy.com','schedulicity.com','simplybook.me','fresha.com'],
      MAP_HOSTS=['maps.google.com','maps.app.goo.gl','maps.apple.com'];
  function hostIs(host,base){return host===base||host.endsWith('.'+base)}
  function kind(a){
    var h=a.getAttribute('href')||'';
    if(/^tel:/i.test(h))return'phone';
    if(/^mailto:/i.test(h))return/^mailto:claim@/i.test(h)?'claim':'email';
    var u;try{u=new URL(h,location.href)}catch(_){return''}
    if(u.origin===location.origin&&/^\/claim(\/|$)/.test(u.pathname))return'claim';
    if(!/^https?:$/.test(u.protocol))return'';
    if(MAP_HOSTS.includes(u.hostname)||(/^(www\.)?google\.[a-z.]+$/.test(u.hostname)&&/^\/maps(\/|$)/.test(u.pathname))||(u.hostname==='goo.gl'&&u.pathname.startsWith('/maps')))return'directions';
    if(BOOK_HOSTS.some(function(h){return hostIs(u.hostname,h)})||((u.hostname==='namastebookshop.com'||u.hostname==='www.namastebookshop.com')&&/^\/pages\/(book-a-reading|phone-tarot-readings)\/?$/.test(u.pathname)))return'booking';
    if((u.hostname==='namastebookshop.com'||u.hostname==='www.namastebookshop.com')&&!a.hasAttribute('data-checkout'))return'shop';
    return'';
  }
  document.addEventListener('click',function(e){try{
    var a=e.target&&e.target.closest&&e.target.closest('a[href]');if(!a)return;var k=kind(a);if(!k)return;
    var u=new URL(a.getAttribute('href'),location.href);
    // Never send email subjects/bodies, query parameters, fragments or form content.
    var destination=/^https?:$/.test(u.protocol)?u.origin+u.pathname:u.protocol;
    ga(k+'_click',{link_type:k,link_url:destination.slice(0,200),page_path:location.pathname,
      site_brand:(window.NI_CART||{}).brand||'NYC Psychic Readers',transport_type:'beacon'});
  }catch(_){}},true);
})();
