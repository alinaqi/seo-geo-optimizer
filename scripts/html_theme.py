"""CSS and JavaScript for the static review plan (plan.html). No external resources."""

CSS = """
:root{--bg:#f7f6f2;--fg:#1f2421;--muted:#5f6861;--line:#d8d5cc;--card:#ffffff;--accent:#1f6f5b;--warn:#b2541a;--code:#eeece6;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161a18;--fg:#e8e6df;--muted:#a3aba5;--line:#343b37;--card:#1f2522;--accent:#6fc7ad;--warn:#f0a06a;--code:#262c29;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#161a18;--fg:#e8e6df;--muted:#a3aba5;--line:#343b37;--card:#1f2522;--accent:#6fc7ad;--warn:#f0a06a;--code:#262c29;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,"Times New Roman",serif}
.wrap{max-width:1100px;margin:0 auto;padding:32px 16px 64px}
header h1{font-size:1.9rem;margin:0 0 4px;text-wrap:balance}header p{color:var(--muted);margin:0 0 24px}
nav{display:flex;flex-wrap:wrap;gap:8px 16px;margin-bottom:32px;font-family:system-ui,sans-serif;font-size:.9rem}
nav a{color:var(--accent);text-decoration:none}nav a:hover{text-decoration:underline}
section{margin-bottom:40px;min-width:0}section h2{font-size:1.35rem;border-bottom:1px solid var(--line);padding-bottom:6px;margin:0 0 12px}
h3{font-size:1.05rem;margin:18px 0 6px}
.tbl{overflow-x:auto}table{border-collapse:collapse;width:100%;font-family:system-ui,sans-serif;font-size:.9rem}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{background:var(--code);font-weight:600}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
code,pre{font-family:ui-monospace,Menlo,monospace;font-size:.85rem;background:var(--code);border-radius:4px}
code{padding:1px 4px}pre{padding:12px;overflow-x:auto}
.toolbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 12px;font-family:system-ui,sans-serif}
button{font:inherit;padding:6px 12px;border:1px solid var(--accent);background:var(--card);color:var(--accent);border-radius:6px;cursor:pointer}
button:hover{background:var(--accent);color:var(--card)}.toolbar span{color:var(--muted);font-size:.85rem}
select.decision,input.note{font:inherit;font-size:.85rem;padding:4px;border:1px solid var(--line);border-radius:4px;background:var(--card);color:var(--fg);min-width:7rem}
input.note{width:100%;min-width:10rem}
tr.approve td{border-left-color:var(--accent)}tr.reject td:first-child{text-decoration:line-through;color:var(--muted)}
.blocked{color:var(--warn);font-weight:600}.allow{color:var(--accent)}
.legend{font-family:system-ui,sans-serif;font-size:.85rem;color:var(--muted);margin:8px 0 0}
footer{color:var(--muted);font-family:system-ui,sans-serif;font-size:.85rem;border-top:1px solid var(--line);padding-top:12px}
@media (max-width:600px){body{font-size:15px}.wrap{padding-top:20px}}
"""

JS = """
(function(){
  var KEY='seo-geo-plan:'+location.pathname;
  function rows(){return Array.prototype.slice.call(document.querySelectorAll('tr[data-item]'));}
  function state(){var s={};rows().forEach(function(r){s[r.dataset.item]={d:r.querySelector('.decision').value,n:r.querySelector('.note').value};});return s;}
  function paint(r){var d=r.querySelector('.decision').value;r.className=d;}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(state()));}catch(e){}}
  function load(){var s={};try{s=JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){}
    rows().forEach(function(r){var v=s[r.dataset.item];if(v){r.querySelector('.decision').value=v.d;r.querySelector('.note').value=v.n;}paint(r);});}
  function decisionsMarkdown(){var out=['## Review decisions ('+new Date().toISOString().slice(0,10)+')'];
    rows().forEach(function(r){var c=r.cells,d=r.querySelector('.decision').value,n=r.querySelector('.note').value;
      out.push('- '+c[0].textContent.trim()+' '+c[1].textContent.trim()+': **'+d+'**'+(n?' - '+n:'')+' ('+c[2].textContent.trim()+')');});
    return out.join('\\n');}
  function copy(){var t=decisionsMarkdown(),s=document.getElementById('status');
    function done(){s.textContent='Copied. Paste it to your agent: "apply the approved items".';}
    function fail(){var ta=document.getElementById('export');ta.hidden=false;ta.value=t;ta.select();s.textContent='Select and copy the text below.';}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,fail);}else{fail();}}
  document.addEventListener('change',function(e){var r=e.target.closest('tr[data-item]');if(r){paint(r);save();}});
  document.addEventListener('input',function(e){if(e.target.classList.contains('note'))save();});
  document.getElementById('copy').addEventListener('click',copy);
  document.getElementById('reset').addEventListener('click',function(){try{localStorage.removeItem(KEY);}catch(e){}rows().forEach(function(r){r.querySelector('.decision').value='pending';r.querySelector('.note').value='';paint(r);});});
  load();
})();
"""
