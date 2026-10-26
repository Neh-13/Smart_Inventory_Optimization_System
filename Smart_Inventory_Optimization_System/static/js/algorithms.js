function fmtMs(v){return `${v} ms`}
async function runSearch(){
 const target=document.getElementById('searchTarget').value.trim(), field=document.getElementById('searchField').value, box=document.getElementById('searchResults');
 box.innerHTML='<div class="placeholder">Running algorithms…</div>';
 try{
  const r=await fetch('/api/search-compare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target,field})});
  const d=await r.json();
  const found=x=>x.found?`<span class="badge success">Found · ${x.found.name} (${x.found.sku})</span>`:'<span class="badge danger">Not found</span>';
  box.innerHTML=`<div class="result-card"><div><strong>Linear Search</strong>${found(d.linear)}</div><div class="result-metrics"><span><b>${fmtMs(d.linear.time_ms)}</b><small>execution time</small></span><span><b>${d.linear.comparisons}</b><small>comparisons</small></span></div><small>${d.linear.complexity}</small></div>
  <div class="result-card"><div><strong>Binary Search</strong>${found(d.binary)}</div><div class="result-metrics"><span><b>${fmtMs(d.binary.time_ms)}</b><small>execution time</small></span><span><b>${d.binary.comparisons}</b><small>comparisons</small></span></div><small>${d.binary.complexity}</small></div><p class="small-note">${d.note}</p>`;
 }catch(e){box.innerHTML='<div class="placeholder">Could not run comparison. Check the server and try again.</div>'}
}
async function runSort(){
 const field=document.getElementById('sortField').value, box=document.getElementById('sortResults');
 box.innerHTML='<div class="placeholder">Sorting products…</div>';
 try{
  const r=await fetch('/api/sort-compare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({field})});
  const d=await r.json();
  box.innerHTML=`<div class="result-card"><div><strong>Merge Sort</strong><span class="badge info">${d.count} products</span></div><div class="result-metrics"><span><b>${fmtMs(d.merge.time_ms)}</b><small>execution time</small></span></div><small>${d.merge.complexity}</small></div>
  <div class="result-card"><div><strong>Quick Sort</strong><span class="badge info">${d.count} products</span></div><div class="result-metrics"><span><b>${fmtMs(d.quick.time_ms)}</b><small>execution time</small></span></div><small>${d.quick.complexity}</small></div>
  <div class="small-note">First five results from Merge Sort: ${d.merge.items.slice(0,5).map(p=>`${p.name} [${p.sku}] (${p[field]})`).join(', ')||'No products yet.'}</div>`;
 }catch(e){box.innerHTML='<div class="placeholder">Could not run comparison. Check the server and try again.</div>'}
}
