import re
t=open('index.html').read()

# add formulas tab
t=t.replace("  {id:'conv', name:'Convert'},\n];", "  {id:'conv', name:'Convert'},\n  {id:'formulas', name:'Formulas'},\n];")

# register cards in card()
t=t.replace("  grid.appendChild(c);\n}", "  grid.appendChild(c);\n  (window.CARDS=window.CARDS||[]).push({tabId,title,calc});\n}")

# add render function before </script>
marker='</script>'
i=t.rfind(marker)
render = """
function renderFormulas(){
  const g=document.getElementById('grid-formulas');
  if(!g) return;
  (window.CARDS||[]).forEach(c=>{
    const d=document.createElement('div'); d.className='card';
    const h=document.createElement('h3'); h.textContent=c.title+' ('+c.tabId+')'; d.appendChild(h);
    const pre=document.createElement('pre'); pre.style.fontSize='11px'; pre.style.whiteSpace='pre-wrap'; pre.textContent=c.calc.toString(); d.appendChild(pre);
    g.appendChild(d);
  });
}
renderFormulas();
"""
t=t[:i]+render+t[i:]

open('index.html','w').write(t)
print('ok')
