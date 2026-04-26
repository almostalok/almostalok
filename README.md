
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Serif+Display:ital@0;1&family=Instrument+Sans:wght@400;500;600&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
:root{--cream:#F5F0E8;--ink:#1A1611;--rust:#C4500A;--sage:#4A6741;--warm:#8C8278;--paper:#EDE8DE;--line:#C8BFB0;--gold:#D4A853}
body{background:var(--cream);color:var(--ink);font-family:'Instrument Sans',sans-serif;overflow-x:hidden}

/* CANVAS BG */
#bgcanvas{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;opacity:0.18}

.page{position:relative;z-index:1;padding:32px 28px;max-width:680px;margin:0 auto}

/* MASTHEAD */
.masthead{border-top:3px solid var(--ink);padding-top:20px;margin-bottom:0}
.mh-eyebrow{font-size:9px;letter-spacing:4px;text-transform:uppercase;color:var(--warm);margin-bottom:14px;font-family:'Instrument Sans',sans-serif}
.mh-name{font-family:'Syne',sans-serif;font-weight:800;font-size:58px;line-height:.88;letter-spacing:-2px;color:var(--ink);overflow:hidden}
.mh-name .char{display:inline-block;transform:translateY(80px);opacity:0;transition:transform .6s cubic-bezier(.16,1,.3,1),opacity .4s}
.mh-name em{font-family:'DM Serif Display',serif;font-style:italic;color:var(--rust)}
.mh-bottom{display:flex;justify-content:space-between;align-items:center;margin-top:18px;padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.mh-role{font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--warm)}
.mh-live{display:flex;align-items:center;gap:6px;font-family:'DM Serif Display',serif;font-style:italic;font-size:13px;color:var(--warm)}
.live-dot{width:7px;height:7px;border-radius:50%;background:var(--rust);animation:livepulse 1.4s ease-in-out infinite}
@keyframes livepulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.5);opacity:.5}}

/* TICKER */
.ticker-wrap{background:var(--ink);color:var(--cream);padding:10px 0;overflow:hidden;white-space:nowrap;margin:0 -28px}
.ticker-inner{display:inline-flex;animation:ticker 22s linear infinite}
.ticker-inner span{font-family:'Instrument Sans',sans-serif;font-size:11px;letter-spacing:2px;text-transform:uppercase;padding:0 24px;color:#9A9085}
.ticker-inner b{color:var(--gold)}

@keyframes ticker{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* VISITOR */
.visitor-block{display:flex;align-items:center;justify-content:space-between;padding:20px 0;border-bottom:1px solid var(--line)}
.vb-left{}
.vb-label{font-size:9px;letter-spacing:4px;text-transform:uppercase;color:var(--warm);margin-bottom:6px}
.vb-count{font-family:'Syne',sans-serif;font-weight:800;font-size:52px;line-height:1;color:var(--ink)}
.vb-count .count-num{display:inline-block}
.vb-sub{font-family:'DM Serif Display',serif;font-style:italic;font-size:13px;color:var(--warm);margin-top:4px}
.vb-right{text-align:right}
.vb-note{font-family:'DM Serif Display',serif;font-style:italic;font-size:14px;color:var(--warm);line-height:1.6}

/* SECTION */
.sec{margin:28px 0}
.sec-head{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.sec-n{font-family:'DM Serif Display',serif;font-style:italic;font-size:12px;color:var(--warm)}
.sec-rule{flex:1;height:1px;background:var(--line);position:relative;overflow:hidden}
.sec-rule::after{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:var(--rust);animation:rulesweep 1.8s ease forwards}
@keyframes rulesweep{to{left:100%}}
.sec-label{font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--warm)}

/* PULL QUOTE */
.pq{border-left:3px solid var(--rust);padding:14px 18px;background:var(--paper);margin:16px 0;transform:translateX(-12px);opacity:0;transition:all .7s cubic-bezier(.16,1,.3,1)}
.pq.visible{transform:translateX(0);opacity:1}
.pq-text{font-family:'DM Serif Display',serif;font-style:italic;font-size:18px;line-height:1.45;color:var(--ink)}
.pq-attr{font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--warm);margin-top:8px}

/* VITALS */
.vitals{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--ink);margin:4px 0}
.vital{padding:16px 10px;text-align:center;border-right:1px solid var(--line);position:relative;overflow:hidden}
.vital:last-child{border-right:none}
.vital::before{content:'';position:absolute;bottom:0;left:0;width:100%;height:2px;background:var(--rust);transform:scaleX(0);transform-origin:left;transition:transform .8s cubic-bezier(.16,1,.3,1)}
.vital.animate::before{transform:scaleX(1)}
.vital-num{font-family:'Syne',sans-serif;font-weight:800;font-size:26px;line-height:1;color:var(--ink)}
.vital-lbl{font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--warm);margin-top:5px}
.vital-sub{font-family:'DM Serif Display',serif;font-style:italic;font-size:11px;color:var(--line);margin-top:2px}

/* SKILL BARS */
.skill-row{margin:8px 0;display:flex;align-items:center;gap:12px}
.skill-name{font-size:11px;letter-spacing:1px;text-transform:uppercase;color:var(--ink);width:90px;flex-shrink:0}
.skill-bar-bg{flex:1;height:3px;background:var(--line);position:relative}
.skill-bar-fill{height:100%;background:var(--ink);width:0%;transition:width 1.2s cubic-bezier(.16,1,.3,1)}
.skill-bar-fill.rust{background:var(--rust)}
.skill-bar-fill.sage{background:var(--sage)}
.skill-pct{font-family:'DM Serif Display',serif;font-style:italic;font-size:12px;color:var(--warm);width:32px;text-align:right}

/* GIT TABLE */
.git-table{width:100%;border-collapse:collapse}
.git-row{border-bottom:1px solid var(--line);opacity:0;transform:translateX(-16px);transition:all .5s cubic-bezier(.16,1,.3,1)}
.git-row.visible{opacity:1;transform:translateX(0)}
.git-row td{padding:10px 6px;font-size:12px;vertical-align:middle}
.gh{font-family:'DM Serif Display',serif;font-style:italic;font-size:13px;color:var(--warm);width:60px}
.gm{color:var(--ink);line-height:1.4}
.gt{font-size:8px;letter-spacing:2px;text-transform:uppercase;padding:3px 8px;font-family:'Instrument Sans',sans-serif}
.feat{background:var(--sage);color:#fff}.fix{background:var(--rust);color:#fff}
.wip{background:var(--gold);color:var(--ink)}.lol{border:1px solid var(--line);color:var(--warm)}

/* STACK PILLS */
.pills{display:flex;flex-wrap:wrap;gap:7px}
.pill{font-size:10px;letter-spacing:1px;text-transform:uppercase;padding:5px 11px;border:1px solid var(--ink);color:var(--ink);cursor:default;transition:all .25s;transform:scale(0);opacity:0}
.pill.shown{transform:scale(1);opacity:1}
.pill:hover{background:var(--ink);color:var(--cream)}
.pill.f{background:var(--ink);color:var(--cream)}
.pill.r{background:var(--rust);color:#fff;border-color:var(--rust)}
.pill.s{background:var(--sage);color:#fff;border-color:var(--sage)}
.pill:hover{transform:scale(1.06)!important}

/* LINKS */
.links-grid{display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--line)}
.link-card{padding:12px 16px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);cursor:pointer;transition:background .2s;opacity:0;transform:translateY(8px);transition:opacity .4s,transform .4s,background .2s}
.link-card.visible{opacity:1;transform:translateY(0)}
.link-card:nth-child(even){border-right:none}
.link-card:nth-last-child(-n+2){border-bottom:none}
.link-card:hover{background:var(--paper)}
.lk-name{font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:var(--ink)}
.lk-handle{font-family:'DM Serif Display',serif;font-style:italic;font-size:12px;color:var(--rust);margin:2px 0}
.lk-vibe{font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--warm)}

/* FOOTER */
.footer{border-top:3px solid var(--ink);padding-top:20px;margin-top:32px;display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:16px}
.footer-quote{font-family:'DM Serif Display',serif;font-style:italic;font-size:19px;line-height:1.4;color:var(--ink);max-width:340px}
.footer-right{text-align:right}
.footer-email{font-family:'Instrument Sans',sans-serif;font-size:12px;letter-spacing:1px;color:var(--rust)}
.footer-sub{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--warm);margin-top:5px}
.footer-bot{border-top:1px solid var(--line);padding-top:12px;margin-top:20px;display:flex;justify-content:space-between;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--line)}

/* CLOCK */
#clock{font-family:'Syne',sans-serif;font-size:11px;font-weight:700;color:var(--rust);letter-spacing:2px}

/* TYPING CURSOR */
.typed-wrap{font-family:'DM Serif Display',serif;font-style:italic;font-size:14px;color:var(--warm);min-height:22px}
.cursor-blink{display:inline-block;width:2px;height:14px;background:var(--rust);margin-left:2px;vertical-align:middle;animation:blink .9s step-end infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

.divider{border:none;border-top:1px solid var(--line);margin:24px 0}

/* MARQUEE SKILLS */
.mq-wrap{overflow:hidden;margin:12px -28px;padding:0}
.mq-inner{display:inline-flex;animation:mq 18s linear infinite}
.mq-inner:hover{animation-play-state:paused}
.mq-chip{font-size:10px;letter-spacing:2px;text-transform:uppercase;padding:6px 16px;border:1px solid var(--line);margin:0 5px;white-space:nowrap;color:var(--warm);transition:all .2s;cursor:default}
.mq-chip:hover{border-color:var(--rust);color:var(--rust)}
@keyframes mq{from{transform:translateX(0)}to{transform:translateX(-50%)}}
</style>

<div style="position:relative;background:var(--cream);overflow:hidden;border-radius:8px">
<canvas id="bgcanvas"></canvas>

<div class="page">

  <!-- MASTHEAD -->
  <div class="masthead">
    <div class="mh-eyebrow">Full Stack Developer &nbsp;·&nbsp; India &nbsp;·&nbsp; <span id="clock"></span></div>
    <div class="mh-name" id="heroname">
      <span>A</span><span>l</span><span>o</span><span>k</span>&nbsp;
      <em><span>K</span><span>u</span><span>m</span><span>a</span><span>r</span>&nbsp;
      <span>S</span><span>i</span><span>n</span><span>g</span><span>h</span><span>.</span></em>
    </div>
    <div class="mh-bottom">
      <div class="mh-role">Building · Breaking · Repeating</div>
      <div class="mh-live"><div class="live-dot"></div> <span id="live-status">Currently debugging something</span></div>
    </div>
  </div>

  <!-- TICKER -->
  <div class="ticker-wrap">
    <div class="ticker-inner">
      <span>almostalok.tech</span><span>·</span><span><b>Hospate</b> — in progress</span><span>·</span>
      <span>47 tabs open</span><span>·</span><span>3am commits</span><span>·</span>
      <span>almostalokblogs.tech</span><span>·</span><span>open to collab</span><span>·</span>
      <span><b>Full Stack Developer</b></span><span>·</span><span>almostalokresume.tech</span><span>·</span>
      <span>almostalok.tech</span><span>·</span><span>·</span><span><b>Hospate</b> — in progress</span><span>·</span>
      <span>47 tabs open</span><span>·</span><span>3am commits</span><span>·</span>
      <span>almostalokblogs.tech</span><span>·</span><span>open to collab</span><span>·</span>
      <span><b>Full Stack Developer</b></span><span>·</span><span>almostalokresume.tech</span><span>·</span>
    </div>
  </div>

  <!-- VISITOR -->
  <div class="visitor-block">
    <div class="vb-left">
      <div class="vb-label">Confirmed sightings</div>
      <div class="vb-count"><span class="count-num" id="vcount">0</span></div>
      <div class="vb-sub">humans · bots · that one person at 3am · probably me</div>
    </div>
    <div class="vb-right">
      <div class="vb-note">Each visit logged.<br>None forgotten.<br><span style="color:var(--rust)">Welcome.</span></div>
    </div>
  </div>

  <!-- TYPING -->
  <div class="sec">
    <div class="typed-wrap"><span id="typed-text"></span><span class="cursor-blink"></span></div>
  </div>

  <div class="pq" id="pq1">
    <div class="pq-text">"First, solve the problem. Then write the code. Then question every life choice that led to this moment."</div>
    <div class="pq-attr">— Sun Tzu, probably &nbsp;·&nbsp; also me at 3am</div>
  </div>

  <!-- VITALS -->
  <div class="sec">
    <div class="sec-head"><span class="sec-n">№ 01</span><div class="sec-rule"></div><span class="sec-label">Vitals</span></div>
    <div class="vitals" id="vitals">
      <div class="vital"><div class="vital-num" id="v1">3am</div><div class="vital-lbl">Avg commit</div><div class="vital-sub">chronically</div></div>
      <div class="vital"><div class="vital-num" id="v2">∞</div><div class="vital-lbl">Bugs</div><div class="vital-sub">impressively</div></div>
      <div class="vital"><div class="vital-num" id="v3" style="color:var(--rust)">4</div><div class="vital-lbl">Coffees</div><div class="vital-sub">minimum viable</div></div>
      <div class="vital"><div class="vital-num" id="v4" style="color:var(--sage)">2%</div><div class="vital-lbl">Sleep</div><div class="vital-sub">critically low</div></div>
    </div>
  </div>

  <!-- SKILL BARS -->
  <div class="sec">
    <div class="sec-head"><span class="sec-n">№ 02</span><div class="sec-rule"></div><span class="sec-label">Character Stats</span></div>
    <div id="skillbars">
      <div class="skill-row"><span class="skill-name">Caffeine dep.</span><div class="skill-bar-bg"><div class="skill-bar-fill rust" data-w="99"></div></div><span class="skill-pct">99%</span></div>
      <div class="skill-row"><span class="skill-name">Code output</span><div class="skill-bar-bg"><div class="skill-bar-fill" data-w="88"></div></div><span class="skill-pct">88%</span></div>
      <div class="skill-row"><span class="skill-name">Debugging</span><div class="skill-bar-bg"><div class="skill-bar-fill rust" data-w="100"></div></div><span class="skill-pct">100%</span></div>
      <div class="skill-row"><span class="skill-name">Stack Overflow</span><div class="skill-bar-bg"><div class="skill-bar-fill sage" data-w="74"></div></div><span class="skill-pct">74%</span></div>
      <div class="skill-row"><span class="skill-name">Sleep</span><div class="skill-bar-bg"><div class="skill-bar-fill" data-w="2"></div></div><span class="skill-pct">2%</span></div>
      <div class="skill-row"><span class="skill-name">Chai intake</span><div class="skill-bar-bg"><div class="skill-bar-fill sage" data-w="95"></div></div><span class="skill-pct">95%</span></div>
    </div>
  </div>

  <!-- MARQUEE TECH -->
  <div class="sec">
    <div class="sec-head"><span class="sec-n">№ 03</span><div class="sec-rule"></div><span class="sec-label">Weapons (hover to pause)</span></div>
    <div class="mq-wrap">
      <div class="mq-inner">
        <div class="mq-chip">React</div><div class="mq-chip">Next.js</div><div class="mq-chip">TypeScript</div>
        <div class="mq-chip">Node.js</div><div class="mq-chip">Python</div><div class="mq-chip">Java</div>
        <div class="mq-chip">MongoDB</div><div class="mq-chip">PostgreSQL</div><div class="mq-chip">Redis</div>
        <div class="mq-chip">Docker</div><div class="mq-chip">AWS</div><div class="mq-chip">GraphQL</div>
        <div class="mq-chip">Tailwind</div><div class="mq-chip">Linux</div><div class="mq-chip">Firebase</div>
        <div class="mq-chip">NestJS</div><div class="mq-chip">Spring</div><div class="mq-chip">Jest</div>
        <div class="mq-chip">React</div><div class="mq-chip">Next.js</div><div class="mq-chip">TypeScript</div>
        <div class="mq-chip">Node.js</div><div class="mq-chip">Python</div><div class="mq-chip">Java</div>
        <div class="mq-chip">MongoDB</div><div class="mq-chip">PostgreSQL</div><div class="mq-chip">Redis</div>
        <div class="mq-chip">Docker</div><div class="mq-chip">AWS</div><div class="mq-chip">GraphQL</div>
        <div class="mq-chip">Tailwind</div><div class="mq-chip">Linux</div><div class="mq-chip">Firebase</div>
        <div class="mq-chip">NestJS</div><div class="mq-chip">Spring</div><div class="mq-chip">Jest</div>
      </div>
    </div>
  </div>

  <!-- PILLS -->
  <div class="pills" id="pills">
    <span class="pill f">React</span><span class="pill f">Next.js</span>
    <span class="pill r">Node.js</span><span class="pill f">TypeScript</span>
    <span class="pill">Python</span><span class="pill s">MongoDB</span>
    <span class="pill">PostgreSQL</span><span class="pill">Docker</span>
    <span class="pill r">Tailwind</span><span class="pill">AWS</span>
    <span class="pill s">Linux</span><span class="pill">GraphQL</span>
    <span class="pill">Java</span><span class="pill">Redis</span>
    <span class="pill">Firebase</span><span class="pill">Jest</span>
  </div>

  <!-- GIT LOG -->
  <div class="sec">
    <div class="sec-head"><span class="sec-n">№ 04</span><div class="sec-rule"></div><span class="sec-label">An Honest Account</span></div>
    <table class="git-table" id="gittable">
      <tr class="git-row"><td class="gh">a3f91b2</td><td class="gm">feat: added feature that actually works — first time this month</td><td><span class="gt feat">feat</span></td></tr>
      <tr class="git-row"><td class="gh">8c2d441</td><td class="gm">fix: fixed the fix that broke the fix. the fix is fixed.</td><td><span class="gt fix">fix</span></td></tr>
      <tr class="git-row"><td class="gh">3b7e102</td><td class="gm">wip: DO NOT PUSH — obviously I pushed</td><td><span class="gt wip">wip</span></td></tr>
      <tr class="git-row"><td class="gh">9a1f553</td><td class="gm">style: moved semicolon 0.3px to the right. closed 3 PRs.</td><td><span class="gt lol">style</span></td></tr>
      <tr class="git-row"><td class="gh">2d8c991</td><td class="gm">yolo: deployed to prod. no tests. good luck everyone.</td><td><span class="gt fix">yolo</span></td></tr>
    </table>
  </div>

  <!-- LINKS -->
  <div class="sec">
    <div class="sec-head"><span class="sec-n">№ 05</span><div class="sec-rule"></div><span class="sec-label">Whereabouts</span></div>
    <div class="links-grid" id="linksgrid">
      <div class="link-card" onclick="openLink('https://linkedin.com/in/almostalok')"><div class="lk-name">LinkedIn</div><div class="lk-handle">almostalok</div><div class="lk-vibe">Professional mode: barely</div></div>
      <div class="link-card" onclick="openLink('https://twitter.com/almostalok')"><div class="lk-name">Twitter / X</div><div class="lk-handle">almostalok</div><div class="lk-vibe">3am takes, unfiltered</div></div>
      <div class="link-card" onclick="openLink('https://almostalok.tech')"><div class="lk-name">Portfolio</div><div class="lk-handle">almostalok.tech</div><div class="lk-vibe">The good stuff</div></div>
      <div class="link-card" onclick="openLink('https://almostalokblogs.tech')"><div class="lk-name">Blog</div><div class="lk-handle">almostalokblogs</div><div class="lk-vibe">Hot takes, warm code</div></div>
      <div class="link-card" onclick="openLink('https://leetcode.com/almostalok')"><div class="lk-name">LeetCode</div><div class="lk-handle">almostalok</div><div class="lk-vibe">Pain as a service™</div></div>
      <div class="link-card" onclick="openLink('https://github.com/almostalok')"><div class="lk-name">GitHub</div><div class="lk-handle">almostalok</div><div class="lk-vibe">Scene of the crime</div></div>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div class="footer-quote">If you got this far —<br>drop a ⭐ somewhere.<br><span style="color:var(--warm);font-size:15px">It costs nothing.</span></div>
    <div class="footer-right">
      <div class="footer-email">almostalok@gmail.com</div>
      <div class="footer-sub">almostalok.tech · open to collab</div>
    </div>
  </div>
  <div class="footer-bot">
    <span>© Alok Kumar Singh</span>
    <span id="footerclock"></span>
    <span>India 🇮🇳</span>
  </div>

</div>
</div>

<script>
const cream='#F5F0E8',ink='#1A1611',rust='#C4500A',warm='#8C8278',line='#C8BFB0';

/* PARTICLE CANVAS */
const cv=document.getElementById('bgcanvas');
const ctx=cv.getContext('2d');
function resizeCv(){cv.width=cv.offsetWidth;cv.height=cv.offsetHeight||1200}
resizeCv();
const dots=Array.from({length:55},()=>({x:Math.random()*680,y:Math.random()*1200,vx:(Math.random()-.5)*.18,vy:(Math.random()-.5)*.18,r:Math.random()*1.4+.4}));
function drawDots(){
  ctx.clearRect(0,0,cv.width,cv.height);
  dots.forEach(d=>{
    d.x+=d.vx;d.y+=d.vy;
    if(d.x<0||d.x>680)d.vx*=-1;
    if(d.y<0||d.y>1200)d.vy*=-1;
    ctx.beginPath();ctx.arc(d.x,d.y,d.r,0,Math.PI*2);
    ctx.fillStyle='#C4500A';ctx.fill();
  });
  dots.forEach((a,i)=>dots.forEach((b,j)=>{
    if(j<=i)return;
    const dist=Math.hypot(a.x-b.x,a.y-b.y);
    if(dist<90){ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.strokeStyle=`rgba(200,191,176,${(1-dist/90)*.35})`;ctx.lineWidth=.5;ctx.stroke()}
  }));
  requestAnimationFrame(drawDots);
}
drawDots();

/* CLOCK */
function updateClock(){
  const now=new Date();
  const ist=new Date(now.toLocaleString('en',{timeZone:'Asia/Kolkata'}));
  const h=ist.getHours().toString().padStart(2,'0');
  const m=ist.getMinutes().toString().padStart(2,'0');
  const s=ist.getSeconds().toString().padStart(2,'0');
  const str=`IST ${h}:${m}:${s}`;
  document.getElementById('clock').textContent=str;
  document.getElementById('footerclock').textContent=str;
}
setInterval(updateClock,1000);updateClock();

/* LIVE STATUS ROTATE */
const statuses=['Currently debugging something','Probably on tab #47','Building Hospate rn','Drinking chai #4','Should be sleeping','Writing code that works (maybe)','Staring at a bug for 2 hrs','Open to collabs'];
let si=0;
setInterval(()=>{
  si=(si+1)%statuses.length;
  const el=document.getElementById('live-status');
  el.style.opacity=0;
  setTimeout(()=>{el.textContent=statuses[si];el.style.opacity=1;el.style.transition='opacity .4s'},300);
},3200);

/* NAME ENTRANCE */
setTimeout(()=>{
  document.querySelectorAll('.mh-name .char').forEach((c,i)=>{
    setTimeout(()=>{c.style.transform='translateY(0)';c.style.opacity='1'},i*55);
  });
},200);

/* VISITOR COUNT-UP */
let vc=41800;
const vcEl=document.getElementById('vcount');
const step=()=>{if(vc<42069){vc+=Math.floor(Math.random()*11+4);vcEl.textContent=vc.toLocaleString();setTimeout(step,28)}else vcEl.textContent='42,069'};
setTimeout(step,600);

/* TYPING EFFECT */
const lines=['Building Hospate at hours no doctor recommends.','almostalok.tech · almostalokblogs.tech','Open to collabs. Always online. Send chai.','git commit -m "it works, don\'t touch it"'];
let li=0,ci=0,deleting=false;
const tel=document.getElementById('typed-text');
function typeStep(){
  const t=lines[li];
  if(!deleting){tel.textContent=t.slice(0,++ci);if(ci>=t.length){deleting=true;setTimeout(typeStep,1800);return}}
  else{tel.textContent=t.slice(0,--ci);if(ci<=0){deleting=false;li=(li+1)%lines.length;setTimeout(typeStep,400);return}}
  setTimeout(typeStep,deleting?32:65);
}
setTimeout(typeStep,1000);

/* SCROLL ANIMATIONS */
const observer=new IntersectionObserver(entries=>{
  entries.forEach(e=>{
    if(!e.isIntersecting)return;
    const el=e.target;
    if(el.classList.contains('pq')){el.classList.add('visible')}
    if(el.id==='vitals'){el.querySelectorAll('.vital').forEach((v,i)=>setTimeout(()=>v.classList.add('animate'),i*150))}
    if(el.id==='skillbars'){el.querySelectorAll('.skill-bar-fill').forEach((b,i)=>{setTimeout(()=>{b.style.width=b.dataset.w+'%'},i*180+300)})}
    if(el.id==='pills'){el.querySelectorAll('.pill').forEach((p,i)=>setTimeout(()=>p.classList.add('shown'),i*55+200))}
    if(el.id==='gittable'){el.querySelectorAll('.git-row').forEach((r,i)=>setTimeout(()=>r.classList.add('visible'),i*140+200))}
    if(el.id==='linksgrid'){el.querySelectorAll('.link-card').forEach((c,i)=>setTimeout(()=>c.classList.add('visible'),i*90+200))}
    observer.unobserve(el);
  });
},{threshold:0.15});

['pq1','vitals','skillbars','pills','gittable','linksgrid'].forEach(id=>{
  const el=document.getElementById(id);
  if(el)observer.observe(el);
});

/* COFFEE COUNTER FLICKER */
setInterval(()=>{
  const el=document.getElementById('v3');
  const n=Math.floor(Math.random()*3+3);
  el.style.opacity=0;setTimeout(()=>{el.textContent=n;el.style.opacity=1;el.style.transition='opacity .3s'},200);
},6000);
</script>
