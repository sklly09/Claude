import random, math, json, sys
C=dict(deep='#0b3640',water='#12505a',mid='#1a6670',lite='#3f9b98',foam='#a8e6d8',peb='#0a2e36',
 pad='#3c9a3c',padl='#74c84a',padd='#1f5a28',pink='#f49ac0',white='#fcfcfc',yel='#f8d030',
 orange='#f05a1e',gold='#f8b800',goldl='#ffe080',black='#1c1c1c',shadow='#08262c',tail='#d8f0ec',orl='#ff9a50')
def path(px):
    return ''.join(f'M{x} {y}h1v1h-1z' for x,y in px)
def P(px,col,extra=''):
    return f'<path d="{path(px)}" fill="{col}"{extra}/>' if px else ''
BODY=["........f.......",
      "....bbbbbbbbb...",
      "...bbbbbbbbbbbb.",
      "...bbbbbbbbbbbb.",
      "....bbbbbbbbb...",
      "........f......."]
TAILS={'A':["T..","TT.",".TT",".TT","TT.","T.."],
       'B':["TT.",".TT","..T","..T","...","..."],
       'C':["...","...","..T","..T",".TT","TT."]}
KOI={'kohaku':('white','tail',[(6,1),(7,1),(6,2),(7,2),(8,2),(11,2),(12,2),(11,3),(12,3),(13,2),(5,3),(6,3),(7,3)]),
     'ogon':('gold','goldl',[(9,2),(10,2),(11,2),(12,2),(13,2)]),
     'showa':('black','tail',[(7,1),(8,1),(7,2),(8,2),(9,3),(12,2),(13,2),(12,3),(13,3)]),
     'chagoi':('orange','orl',[(10,2),(11,2),(12,2),(13,2)]),
     'sanke':('white','tail',[(5,2),(6,2),(10,1),(11,1),(10,2),(11,2),(12,2),(8,3)])}
def koi(kind):
    base,tc,spots=KOI[kind]; spotc = 'orange' if kind!='ogon' else 'white'
    if kind=='showa': spotc='orange'
    body=[(x,y) for y,r in enumerate(BODY) for x,c in enumerate(r) if c=='b']
    fins=[(x,y) for y,r in enumerate(BODY) for x,c in enumerate(r) if c=='f']
    sp=[p for p in spots if p in body]
    eyes=[(13,2),(13,3)] if kind!='showa' else []
    out=P([(x+1,y+2) for x,y in body],C['shadow'],' opacity=".6"')
    out+=P(fins,C[tc],' opacity=".8"')
    for k,t in TAILS.items():
        out+=f'<g class="t{k}">'+P([(x,y) for y,r in enumerate(t) for x,c in enumerate(r) if c=='T'],C[tc])+'</g>'
    out+=P([p for p in body if p not in sp and p not in eyes],C[base])+P(sp,C[spotc])+P(eyes,C['black'] if kind!='showa' else C['white'])
    if kind=='showa': out+=P([(5,2),(5,3)],C['white'])
    return out
def disk(cx,cy,r,notch=None):
    s=set()
    for y in range(int(cy-r-1),int(cy+r+2)):
        for x in range(int(cx-r-1),int(cx+r+2)):
            dx,dy=x+.5-cx,y+.5-cy
            if dx*dx+dy*dy<=r*r:
                if notch is not None:
                    a=math.degrees(math.atan2(dy,dx))-notch; a=(a+180)%360-180
                    if abs(a)<13 and dx*dx+dy*dy>1: continue
                s.add((x,y))
    return s
def pad(cx,cy,r,notch,flower,dur):
    d=disk(cx,cy,r,notch)
    edge={p for p in d if any((p[0]+a,p[1]+b) not in d for a,b in((1,0),(-1,0),(0,1),(0,-1)))}
    hl={p for p in d-edge if (p[0]+.5-cx)+(p[1]+.5-cy) < -r*0.95}
    o=f'<g class="bob" style="animation-duration:{dur}s">'
    o+=P(sorted((x+1,y+2) for x,y in d),C['shadow'],' opacity=".6"')+P(sorted(d-edge-hl),C['pad'])+P(sorted(edge),C['padd'])+P(sorted(hl),C['padl'])
    if flower:
        F=["..p..",".pwp.","pwywp",".pwp.","..p.."]; fx,fy=int(cx)-2,int(cy)-2
        for ch,col in (('p','pink'),('w','white'),('y','yel')):
            o+=P([(fx+x,fy+y) for y,r_ in enumerate(F) for x,c in enumerate(r_) if c==ch],C[col])
    return o+'</g>'
def ring(r):
    pts=set()
    for t in range(0,360,3):
        pts.add((round(r*math.cos(math.radians(t))),round(r*math.sin(math.radians(t)))))
    return pts
def scene(W,H,swim,seed=3):
    rnd=random.Random(seed)
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" shape-rendering="crispEdges">']
    o.append('''<style>
.tA{animation:tA 1s steps(1) infinite}.tB{animation:tB 1s steps(1) infinite}.tC{animation:tC 1s steps(1) infinite}
@keyframes tA{0%{opacity:1}25%{opacity:0}50%{opacity:1}75%{opacity:0}}
@keyframes tB{0%{opacity:0}25%{opacity:1}50%{opacity:0}}
@keyframes tC{0%{opacity:0}75%{opacity:1}}
.bob{animation:bob 4s steps(1) infinite}
@keyframes bob{0%{transform:translate(0,0)}50%{transform:translate(0,1px)}}
.fb{animation:bob 2s steps(1) infinite}
.w1{animation:w1 2s steps(1) infinite}.w2{animation:w1 2s steps(1) infinite;animation-delay:-1s}
@keyframes w1{0%{opacity:1}50%{opacity:0}}
.rf{opacity:0;animation:rf 6s steps(1) infinite}
@keyframes rf{0%{opacity:1}12.5%{opacity:0}}
.sp{opacity:0;animation:sp steps(1) infinite}
@keyframes sp{0%{opacity:1}10%{opacity:0}}
</style>''')
    o.append(f'<rect width="{W}" height="{H}" fill="{C["water"]}"/>')
    # depth: darker border band
    dk=[(x,y) for y in range(H) for x in range(W) if min(x,y,W-1-x,H-1-y) < 4 and rnd.random()<0.85-0.2*min(x,y,W-1-x,H-1-y)]
    o.append(P(dk,C['deep']))
    peb=[]
    for _ in range(W*H//260):
        x,y=rnd.randrange(W),rnd.randrange(H); peb+= [(x,y),(x+1,y)] + ([(x,y+1)] if rnd.random()<.5 else [])
    o.append(P(peb,C['peb'],' opacity=".7"'))
    o.append(P([(rnd.randrange(W),rnd.randrange(H)) for _ in range(W*H//90)],C['mid']))
    # fish lanes
    kinds=['kohaku','ogon','showa','chagoi','sanke','kohaku','ogon']
    n=max(4,H//18); D=W+40
    for i in range(n):
        y=int(H*(i+0.6)/(n+0.2)); right=(i%2==0); dur=swim*(1 if i%3 else 2); delay=rnd.uniform(0,dur)
        tr=f'translate(-20 {y-3})' if right else f'translate({W+20} {y-3}) scale(-1 1)'
        o.append(f'<g transform="{tr}"><g style="animation:sw{i} {dur}s steps({D}) infinite;animation-delay:-{delay:.2f}s"><g class="fb" style="animation-delay:-{i*0.5}s">{koi(kinds[i%len(kinds)])}</g></g></g>')
        o.append(f'<style>@keyframes sw{i}{{to{{transform:translateX({D}px)}}}}</style>')
    # shimmer dashes (two alternating sets)
    for cls in ('w1','w2'):
        d=[]
        for _ in range(W*H//500):
            x,y=rnd.randrange(W-3),rnd.randrange(H); d+=[(x,y),(x+1,y),(x+2,y)]
        o.append(f'<g class="{cls}">'+P(d,C['lite'])+'</g>')
    # ripples
    for k in range(max(3,W*H//3500)):
        cx,cy=rnd.randrange(8,W-8),rnd.randrange(8,H-8); off=rnd.choice([0,1.5,3,4.5])
        for j,r in enumerate([0,2,4,6]):
            pts=[(cx+a,cy+b) for a,b in (ring(r) if r else {(0,0)})]
            o.append(f'<g class="rf" style="animation-delay:-{(off+6-j*0.75)%6:.2f}s">'+P(pts,C['foam'] if j<2 else C['lite'])+'</g>')
    # lily pads at corners
    R=max(7,min(W,H)//9)
    pads=[(R*0.9,R*0.9,R,40,True,4),(R*2.4,R*0.5,R*0.6,150,False,4),(W-R*0.8,R*1.1,R*0.9,200,False,8),
          (W-R*1.0,H-R*1.0,R*1.1,300,True,8),(W-R*2.5,H-R*0.4,R*0.6,60,False,4),(R*0.7,H-R*0.9,R*0.8,250,False,8)]
    for p in pads: o.append(pad(*p))
    sp=[]
    for _ in range(W*H//400):
        o.append(f'<rect class="sp" x="{rnd.randrange(W)}" y="{rnd.randrange(H)}" width="1" height="1" fill="{C["white"]}" style="animation-duration:{rnd.choice([2,3,4,6])}s;animation-delay:-{rnd.uniform(0,6):.2f}s"/>')
    o.append('</svg>')
    return ''.join(o)
if __name__=='__main__':
    out=sys.argv[1]
    open(out+'/pix-wide.svg','w').write(scene(160,100,24))
    open(out+'/pix-phone.svg','w').write(scene(72,156,12,seed=5))
    print(len(scene(160,100,24)),len(scene(72,156,12,seed=5)))
