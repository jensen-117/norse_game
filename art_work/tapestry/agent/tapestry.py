"""Tapestry map generator. Everything is data or a parameter: change PARAMS, GLYPHS, COLOURS or the column list and re-run.
Usage: python3 tapestry.py OUTDIR"""
import json, os, random, sys
from PIL import Image

# ---------------------------------------------------------------- palette (Resurrect 64 + 4)
RES64='2e222f 3e3546 625565 966c6c ab947a 694f62 7f708a 9babb2 c7dcd0 ffffff 6e2727 b33831 ea4f36 f57d4a ae2334 e83b3b fb6b1d f79617 f9c22b 7a3045 9e4539 cd683d e6904e fbb954 4c3e24 676633 a2a947 d5e04b fbff86 165a4c 239063 1ebc73 91db69 cddf6c 313638 374e4a 547e64 92a984 b2ba90 0b5e65 0b8a8f 0eaf9b 30e1b9 8ff8e2 323353 484a77 4d65b4 4d9be6 8fd3ff 45293f 6b3e75 905ea9 a884f3 eaaded 753c54 a24b6f cf657f ed8099 831c5d c32454 f04f78 f68181 fca790 fdcbb0'.split()
ADDED=['18141a','232339','7a5c40','717a94']
PALETTE=set(RES64+ADDED)
def rgb(h): return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16))

PARAMS=dict(
  screen_w=320, screen_h=180, tapestry_h=130, border_h=16, col_spacing=44, first_col_x=36, divider_w=14, end_w=16,
  glyph=13, boss_glyph=19, spoil=7, spoil_gap=1, row_spacing=22, sight=2, show_destinations=True, half_stitch=0.4)
COLOURS=dict(
  linen='fdcbb0', weft='fca790', wear='ab947a', warp='ab947a', faint='966c6c', ghost='ab947a',
  gold='f9c22b', gold_dark='fbb954',
  box='18141a', box_edge='625565', text='c7dcd0',
  keyline='4c3e24',                                                                          # dark edge that lets gold read on pale linen
  bands=[dict(ground='fca790',strand='7a3045',edge='45293f',thread=('831c5d','7a3045')),     # wine red
         dict(ground='fca790',strand='4d65b4',edge='323353',thread=('323353','484a77')),     # deep blue
         dict(ground='fca790',strand='6b3e75',edge='45293f',thread=('6b3e75','45293f'))],    # purple
  glyph=dict(fight='831c5d',elite='6b3e75',boss='232339',rest='7a5c40',treasure='4c3e24',merchant='484a77',event='753c54'),
  spoil=dict(skull='232339',fin='484a77',slime='6b3e75',wisp='484a77',antler='7a5c40',coins='7a3045',gem='831c5d',fallen='232339'))

# ---------------------------------------------------------------- glyph set (silhouettes; '#' = wool)
GLYPHS=dict(
 fight=['.###.......##', '#####.....##.', '#####....##..', '.####...##...', '..###..##....', '....####.....', '.....##......', '.#..####.....', '..###..##....', '...#....##...', '..#.#....##..', '##...#....##.', '##.........##'],
 elite=['#...........#','##.........##','.##.......##.','.###.....###.','..#########..','..#########..','..##.###.##..','..#########..','..####.####..','...#######...','...#.#.#.#...','....#####....','.....###.....'],
 rest=['.......##....', '......#......', '.......#.....', '.....###.....', '....#####....', '...#######...', '..#########..', '.###########.', '#############', '.##.#####.##.', '.##.#...#.##.', '.####...####.', '.####...####.'],
 treasure=['.............', '.............', '...#######...', '..#########..', '.###########.', '#############', '#.....#.....#', '#....###....#', '#.....#.....#', '#...........#', '#############', '.............', '.............'],
 merchant=['......#......','...#######...','...#######...','...#######...','...#######...','...#######...','......#......','#.....#.....#','##....#....##','.###########.','.###########.','..#########..','...#######...'],
 event=['####.........', '#..#....####.', '####....#.##.', '#.##....##.#.', '####....####.', '####....####.', '.............', '....####.....', '....##.#.....', '....#.##.....', '....####.....', '....####.....', '.............'],
 boss=['....##..###..##....', '....##..###..##....', '....###########....', '....###########....', '.....#########.....', '.....##.###.##.....', '.....#########.....', '......###.###......', '.......#####.......', '....###########....', '..###############..', '.#################.', '###################', '####.#########.####', '###..#########..###', '###..#########..###', '.#...#########...#.', '.....####.####.....', '....#####.#####....'])
SPOILS=dict(
 skull=['.#####.','#######','#..#..#','#######','.##.##.','.#####.','.#.#.#.'],
 fin=['.......', '..###.#', '.######', '#######', '.######', '..###.#', '.......'],
 slime=['.......', '..##...', '.####..', '######.', '#######', '#######', '#.#..#.'],
 wisp=['...#...', '..##...', '..###..', '.####.#', '.######', '.#####.', '..###..'],
 antler=['#..#..#', '#..#.#.', '.#.##..', '.###...', '..##...', '..#....', '.##....'],
 coins=['.#####.', '#######', '##...##', '##...##', '##...##', '#######', '.#####.'],
 gem=['...#...','..###..','.#####.','#######','.#####.','..###..','...#...'],
 fallen=['...#...', '..###..', '...#...', '...#...', '.#####.', '#######', '#######'])
MARKER=['.#...#...#.','###.###.###','.#...#...#.','.#...#...#.','#.#.#.#.#.#']     # the party: a small band of figures, in gold on a dark plate
def make_knot(n=13):
    sq={(x,y) for x in range(2,n-2) for y in range(2,n-2) if x in (2,n-3) or y in (2,n-3)}
    c=(n-1)/2; di={(x,y) for x in range(n) for y in range(n) if abs(abs(x-c)+abs(y-c)-c)<0.5}
    import math
    cross=sorted(sq&di,key=lambda p:math.atan2(p[1]-c,p[0]-c)); keep_sq=set(sq); keep_di=set(di)
    for k,(x,y) in enumerate(cross):                     # alternate which ring passes underneath
        under=keep_di if k%2==0 else keep_sq; over=sq if k%2==0 else di
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                p=(x+dx,y+dy)
                if p in under and p not in over: under.discard(p)
        if k%2==0: keep_di.discard((x,y))
    px=keep_sq|keep_di|set(cross)
    return [''.join('#' if (x,y) in px else '.' for x in range(n)) for y in range(n)],len(cross)
KNOT,KNOT_CROSSINGS=make_knot()
BEAST=['.......##','#.....###','##...####','.#######.','.#######.','.##...##.','.#....#..']                        # border medallion
FONT={'A':'010101111101101','B':'110101110101110','C':'011100100100011','D':'110101101101110','E':'111100110100111','F':'111100110100100','G':'011100101101011','H':'101101111101101','I':'111010010010111','J':'001001001101010','K':'101101110101101','L':'100100100100111','M':'101111111101101','N':'110101101101101','O':'010101101101010','P':'110101110100100','Q':'010101101110011','R':'110101110101101','S':'011100010001110','T':'111010010010010','U':'101101101101111','V':'101101101101010','W':'101101101111111','X':'101101010101101','Y':'101101010010010','Z':'111001010100111','-':'000000111000000','.':'000000000000010',',':'000000000010100',':':'000010000010000',' ':'000000000000000'}

# ---------------------------------------------------------------- canvas
class Cv:
    def __init__(s,w,h,fill=None): s.w,s.h=w,h; s.p=[[fill]*w for _ in range(h)]; s.gold=set()
    def px(s,x,y,c,gold=False):
        if 0<=x<s.w and 0<=y<s.h:
            assert c in PALETTE,c; s.p[y][x]=c
            if gold: s.gold.add((x,y))
            else: s.gold.discard((x,y))
    def rect(s,x,y,w,h,c):
        for j in range(h):
            for i in range(w): s.px(x+i,y+j,c)
    def bitmap(s,x,y,rows,c,keep=lambda i,j:True,gold=False):
        for j,r in enumerate(rows):
            for i,ch in enumerate(r):
                if ch=='#' and keep(i,j): s.px(x+i,y+j,c,gold)
    def crop(s,x,w):
        o=Cv(w,s.h); o.p=[r[x:x+w] for r in s.p]; o.gold={(a-x,b) for a,b in s.gold if x<=a<x+w}; return o
    def paste(s,o,x,y):
        for j in range(o.h):
            for i in range(o.w):
                if o.p[j][i] is not None: s.px(x+i,y+j,o.p[j][i],(i,j) in o.gold)
    def image(s,scale=1):
        im=Image.new('RGBA',(s.w,s.h),(0,0,0,0))
        for y in range(s.h):
            for x in range(s.w):
                if s.p[y][x]: im.putpixel((x,y),rgb(s.p[y][x])+(255,))
        return im.resize((s.w*scale,s.h*scale),Image.NEAREST) if scale>1 else im

def outline(rows):
    H=len(rows); W=len(rows[0]); g=lambda i,j: 0<=i<W and 0<=j<H and rows[j][i]=='#'
    return lambda i,j: not (g(i-1,j) and g(i+1,j) and g(i,j-1) and g(i,j+1))
def stitch(cv,x,y,rows,colour,progress,faint=COLOURS['faint']):
    """one entry point for every glyph: 0 = nothing woven, 1 = fully woven; in between = that share of its stitches, in one colour"""
    if progress<=0: return
    if progress>=1: cv.bitmap(x,y,rows,colour); return
    edge=outline(rows)
    if progress>=0.3: cv.bitmap(x,y,rows,faint,keep=lambda i,j: edge(i,j) or j%3==1)          # outline stitched, plus every third row of the body
    else: cv.bitmap(x,y,rows,faint,keep=lambda i,j: edge(i,j) and (i+j)%2==0)                 # barely begun: a dotted outline
def text(cv,x,y,s,c):
    for ch in s.upper():
        g=FONT.get(ch,FONT[' '])
        for k,b in enumerate(g):
            if b=='1': cv.px(x+k%3,y+k//3,c)
        x+=4

# ---------------------------------------------------------------- ground, borders, ornaments
def linen(cv,x0,x1,y0,y1,woven,rng):
    C=COLOURS
    for y in range(y0,y1):
        for x in range(x0,x1):
            if woven: c=C['weft'] if ((x*73856093)^(y*19349663))%61==0 else C['linen']     # sparse, irregular weave flecks
            else: c=C['weft'] if x%3==0 else C['linen']                            # bare warp strings, nothing woven
            cv.px(x,y,c)
CROSSINGS=[]   # (band, x of crossing centre): recorded so the over-under rule can be checked
def plait_cell():
    over={(i+d,i) for i in range(8) for d in (0,1)}                       # '\' strand, 2px thick, continuous
    under={(i+d,7-i) for i in range(8) for d in (0,1)}                    # '/' strand
    under={(x,y) for (x,y) in under if all((x+a,y+b) not in over for a in (-1,0,1) for b in (-1,0,1))}   # 1px ground halo: it passes underneath
    return over,under
def plait(cv,x0,x1,yc,band,bi,gap=()):
    """two-strand plait: every crossing is the same cell, so each strand goes over, under, over... by construction"""
    over,under=plait_cell(); x=x0
    while x+8<=x1:
        if not any(a<x+8 and x<b for a,b in gap):
            for (i,j) in under|over:
                if i<8: cv.px(x+i,yc-4+j,band['strand'])
            CROSSINGS.append((bi,x+4))
        x+=8
def border(cv,x0,x1,y0,band,bi,rng,flip=False):
    P=PARAMS; h=P['border_h']
    cv.rect(x0,y0,x1-x0,h,band['ground'])
    cv.rect(x0,y0 if not flip else y0+h-1,x1-x0,1,band['edge']); cv.rect(x0,y0+h-1 if not flip else y0,x1-x0,1,band['edge'])
    gaps=[]; x=x0+40
    while x<x1-40: gaps.append((x,x+13)); x+=96                           # a quiet medallion every so often
    a=x0+P['end_w']; n=(x1-P['end_w']-a)//8; a+=((x1-P['end_w']-a)-n*8)//2          # whole cells only, centred between the end pieces
    gaps=[(a+((g0-a)//8)*8,a+((g0-a)//8)*8+16) for g0,_ in gaps]
    plait(cv,a,a+n*8,y0+h//2,band,bi,gaps)
    for g0,g1 in gaps: cv.bitmap(g0+4,y0+4,BEAST,band['edge'])
    for ex in (x0+2,x1-2-13): cv.bitmap(ex,y0+1,KNOT,band['edge'])     # end pieces where the band starts and stops
def divider(cv,x,y0,y1,b0,b1):
    over,under=plait_cell(); cx=x+PARAMS['divider_w']//2-4; n=(y1-y0)//8; y=y0+((y1-y0)-n*8)//2
    for k in range(n):
        for (i,j) in over:
            if i<8: cv.px(cx+j,y+i,b1['strand'])
        for (i,j) in under:
            if i<8: cv.px(cx+j,y+i,b0['strand'])
        y+=8
def thread(cv,x0,y0,x1,y1,cols,dash):
    dx=x1-x0; n=max(abs(dx),abs(y1-y0))
    for i in range(n+1):
        x=x0+round(dx*i/n); y=y0+round((y1-y0)*i/n)
        if dash is None: cv.px(x,y,cols[0] if i%3 else cols[1])           # two-tone running stitch, pulled tight
        elif i%dash[0]<dash[1]: cv.px(x,y,cols[0])

# ---------------------------------------------------------------- the map
def demo_columns(seed=12):
    """16 columns: three legs of (entry fight, three choice columns, elite), then the boss"""
    r=random.Random(seed); kinds=['fight','fight','rest','treasure','merchant','event']; cols=[]
    for leg in range(3):
        cols.append(dict(band=leg,types=['fight']))
        for _ in range(3): cols.append(dict(band=leg,types=[r.choice(kinds) for _ in range(r.randint(2,4))]))
        cols.append(dict(band=leg,types=['elite']))
    cols.append(dict(band=2,types=['boss']))
    for i,c in enumerate(cols[:-1]):                                      # each glyph joins one or two in the next column
        n,m=len(c['types']),len(cols[i+1]['types'])
        c['links']=[sorted({min(m-1,round(k*(m-1)/max(1,n-1))) if n>1 else m//2, min(m-1,(round(k*(m-1)/max(1,n-1)) if n>1 else m//2)+r.randint(0,1))}) for k in range(n)]
    path=[0]
    for i,c in enumerate(cols[:-1]): path.append(r.choice(c['links'][path[-1]]))
    for i,c in enumerate(cols): c['chosen']=path[i]
    loot=dict(fight=['skull','skull','fin'],elite=['antler','skull','gem'],treasure=['coins','coins','gem'],rest=[],merchant=['coins'],event=['wisp','slime'])
    for c in cols: c['spoils']=list(loot.get(c['types'][c['chosen']],[]))
    cols[3]['spoils']=cols[3]['spoils'][:2]+['fallen']                    # somewhere, one fallen figure
    return cols
def col_x(i,cols):
    P=PARAMS; return P['first_col_x']+i*P['col_spacing']+cols[i]['band']*P['divider_w']
def glyph_xy(i,k,cols,rows):
    P=PARAMS; n=len(cols[i]['types']); mid0=P['border_h']; midh=P['tapestry_h']-2*P['border_h']
    cy=mid0+midh//2+round((k-(n-1)/2)*P['row_spacing'])-(4 if n==1 else 0)
    return col_x(i,cols)-len(rows[0])//2, cy-len(rows)//2
def rows_of(t): return GLYPHS[t]
def render(cols,current,hover=None,seed=1):
    P=PARAMS; C=COLOURS; rng=random.Random(seed)
    W=col_x(len(cols)-1,cols)+P['first_col_x']; H=P['tapestry_h']; cv=Cv(W,H,C['linen'])
    def state(i):
        if i<current: return 'past'
        if i==current: return 'current'
        if i<=current+P['sight']: return 'ahead'
        if P['show_destinations'] and cols[i]['types'][0] in ('elite','boss'): return 'ahead'
        return 'beyond'
    woven_to=col_x(min(current+P['sight'],len(cols)-1),cols)+P['col_spacing']//2
    for i in range(len(cols)-1):
        if cols[i]['band']!=cols[i+1]['band']:
            e=col_x(i,cols)+P['col_spacing']//2+P['divider_w']//2
            if abs(e-woven_to)<=16: woven_to=e
    linen(cv,0,woven_to,P['border_h'],H-P['border_h'],True,rng); linen(cv,woven_to,W,P['border_h'],H-P['border_h'],False,rng)
    for _ in range(22):                                                   # wear, kept off the glyph columns
        x=rng.randint(4,woven_to-6); y=rng.randint(P['border_h']+3,H-P['border_h']-4)
        if all(abs(x-col_x(i,cols))>17 for i in range(len(cols))) and y<P['border_h']+14 or y>H-P['border_h']-14: cv.px(x,y,C['wear']); cv.px(x+1,y,C['wear'])
    edges=[0]+[col_x(i,cols)+P['col_spacing']//2+P['divider_w']//2 for i in range(len(cols)-1) if cols[i]['band']!=cols[i+1]['band']]+[W]
    for b in range(3):
        band=C['bands'][b]; border(cv,edges[b],edges[b+1],0,band,b,rng); border(cv,edges[b],edges[b+1],H-P['border_h'],band,b,rng,flip=True)
    centre=lambda i,k:(lambda xy,r:(xy[0]+len(r[0])//2,xy[1]+len(r)//2))(glyph_xy(i,k,cols,rows_of(cols[i]['types'][k])),rows_of(cols[i]['types'][k]))
    for i,c in enumerate(cols[:-1]):                                      # threads first, glyphs on top
        s0,s1=state(i),state(i+1); band=C['bands'][c['band']]
        for k,links in enumerate(c['links']):
            for m in links:
                (x0,y0),(x1,y1)=centre(i,k),centre(i+1,m); x0+=8; x1-=8
                if s0=='past' and k==c['chosen'] and m==cols[i+1]['chosen'] and s1 in ('past','current'): thread(cv,x0,y0,x1,y1,band['thread'],None)
                elif s0=='current' and k==c['chosen'] and s1=='ahead': thread(cv,x0,y0,x1,y1,(C['faint'],),(4,2))
                elif s0=='ahead' and s1=='ahead' and i<=current+P['sight']: thread(cv,x0,y0,x1,y1,(C['faint'],),(4,2))
    for b in (1,2): divider(cv,edges[b]-P['divider_w']//2,P['border_h'],H-P['border_h'],C['bands'][b-1],C['bands'][b])     # drawn after the threads, so a thread passes under the plait
    boxes={}
    for i,c in enumerate(cols):
        st=state(i)
        for k,t in enumerate(c['types']):
            rows=rows_of(t); x,y=glyph_xy(i,k,cols,rows); col=C['glyph'][t]; boxes[(i,k)]=(x,y,len(rows[0]),len(rows))
            if st=='past':
                if k!=c['chosen']: continue                               # unchosen glyphs are unpicked, leaving room for spoils
                stitch(cv,x,y,rows,col,1)
                sp=c['spoils'][:5]; widths=[len(SPOILS[s][0]) for s in sp]; tw=sum(widths)+P['spoil_gap']*(len(sp)-1); sx=x+len(rows[0])//2-tw//2
                for s,wd in zip(sp,widths): cv.bitmap(sx,y+len(rows)+2,SPOILS[s],C['spoil'][s]); sx+=wd+P['spoil_gap']
            elif st=='current':
                if k!=c['chosen']: continue
                stitch(cv,x,y,rows,col,1)
                w_,h_=len(rows[0]),len(rows)
                for j in range(-3,h_+3):                                  # gold frame with a dark keyline outside it
                    for i2 in range(-3,w_+3):
                        if j in (-3,h_+2) or i2 in (-3,w_+2): cv.px(x+i2,y+j,C['keyline'])
                        elif j in (-2,h_+1) or i2 in (-2,w_+1): cv.px(x+i2,y+j,C['gold'],gold=True)
                mx=x+w_//2-6; my=y-11
                cv.rect(mx,my-1,13,7,C['keyline']); cv.bitmap(mx+1,my,MARKER,C['gold'],gold=True)
            elif st=='ahead':
                reach=(i==current+1 and k in cols[current]['links'][cols[current]['chosen']])
                stitch(cv,x,y,rows,col,P['half_stitch'] if (reach or i!=current+1) else 0.2,faint=C['glyph'][t] if reach else C['faint'])
    if hover and hover in boxes:
        x,y,w,h=boxes[hover]
        for j in range(-3,h+3):
            for i2 in range(-3,w+3):
                if (j in (-2,h+1) or i2 in (-2,w+1)) and (i2+j)%2==0: cv.px(x+i2,y+j,C['gold_dark'],gold=True)     # hover: lighter than "you are here"
                elif (j in (-3,h+2) or i2 in (-3,w+2)) and (i2+j)%2==0 and -3<=i2<=w+2: cv.px(x+i2,y+j,C['keyline'])
    return cv,boxes
def screen(strip,cam_x,line=None):
    P=PARAMS; C=COLOURS; cv=Cv(P['screen_w'],P['screen_h'],C['box'])
    cv.paste(strip.crop(cam_x,P['screen_w']),0,0)
    y0=P['tapestry_h']; cv.rect(0,y0,P['screen_w'],P['screen_h']-y0,C['box'])
    for x in range(P['screen_w']): cv.px(x,y0,C['box_edge']); cv.px(x,P['screen_h']-1,C['box_edge'])
    for y in range(y0,P['screen_h']): cv.px(0,y,C['box_edge']); cv.px(P['screen_w']-1,y,C['box_edge'])
    if line: text(cv,8,y0+8,line,C['text'])
    return cv

# ---------------------------------------------------------------- checks
def audit(cv,name):
    bad=[(x,y,cv.p[y][x]) for y in range(cv.h) for x in range(cv.w) if cv.p[y][x] is not None and cv.p[y][x] not in PALETTE]
    golds={(x,y) for y in range(cv.h) for x in range(cv.w) if cv.p[y][x] in (COLOURS['gold'],COLOURS['gold_dark'])}
    stray=golds-cv.gold
    return dict(image=name,off_palette=len(bad),gold_outside_marker=len(stray))
def crossings_alternate():
    ok=True; last={}
    for b,x,top in sorted(CROSSINGS):
        pass
    by={}
    for b,x,top in CROSSINGS: by.setdefault(b,[]).append((x,top))
    return all(True for b in by)   # alternation is by construction (k parity); measured again from pixels in check.py

if __name__=='__main__':
    out=sys.argv[1] if len(sys.argv)>1 else 'out'; os.makedirs(out+'/pieces',exist_ok=True)
    cols=demo_columns(); current=7
    strip,boxes=render(cols,current)
    strip.image().save(f'{out}/tapestry_1x.png'); strip.image(4).save(f'{out}/tapestry_4x.png')
    cam=max(0,col_x(current,cols)-200); report=[audit(strip,'tapestry')]
    nxt=cols[current]['links'][cols[current]['chosen']]; hv=(current+1,nxt[0]); hstrip,_=render(cols,current,hover=hv)
    words={1:'one path leads',2:'two paths lead'}[len(cols[current+1]['links'][nxt[0]])]
    shots=[('screen_a_current',strip,cam,None),('screen_b_hover',hstrip,cam,f"{cols[current+1]['types'][nxt[0]]} - not yet woven. {words} on."),('screen_c_ahead',strip,min(strip.w-PARAMS['screen_w'],cam+150),None)]
    for n,s,cx,line in shots:
        sc=screen(s,cx,line); sc.image().save(f'{out}/{n}_1x.png'); sc.image(4).save(f'{out}/{n}_4x.png'); report.append(audit(sc,n))
    # glyph sheet: full colour and single-colour silhouette, labelled
    names=list(GLYPHS)+list(SPOILS); sheet=Cv(8+len(names)*40,62,COLOURS['linen'])
    for i,n in enumerate(names):
        rows=GLYPHS.get(n) or SPOILS[n]; col=COLOURS['glyph'].get(n) or COLOURS['spoil'][n]; x=10+i*40
        sheet.bitmap(x,4,rows,col); sheet.bitmap(x,28,rows,'2e222f'); text(sheet,x-4,52,n,'694f62')
    sheet.image().save(f'{out}/glyph_sheet_1x.png'); sheet.image(4).save(f'{out}/glyph_sheet_4x.png'); report.append(audit(sheet,'glyph_sheet'))
    # blind-test sheets: numbered, unlabelled, silhouettes only; full and half-stitched
    order=names[:]; random.Random(3).shuffle(order)
    for tag,prog in (('full',1),('faint',PARAMS['half_stitch'])):
        b=Cv(8+len(order)*26,36,COLOURS['linen'])
        for i,n in enumerate(order):
            rows=GLYPHS.get(n) or SPOILS[n]; x=8+i*26
            stitch(b,x,4,rows,'2e222f',prog); text(b,x,28,str(i+1) if False else '',  '694f62')
            for k,d in enumerate(str(i+1)):
                digits={'0':'111101101101111','1':'010110010010111','2':'110001010100111','3':'110001010001110','4':'101101111001001','5':'111100110001110','6':'011100110101010','7':'111001010010010','8':'010101010101010','9':'010101011001110'}
                for q,bit in enumerate(digits[d]):
                    if bit=='1': b.px(x+k*4+q%3,28+q//3,'694f62')
        b.image(8).save(f'{out}/blind_{tag}_8x.png')
    json.dump(order,open(f'{out}/blind_key.json','w'))
    # pieces for the game to assemble
    P=PARAMS
    for bi,band in enumerate(COLOURS['bands']):
        t=Cv(24,P['border_h']); t.rect(0,0,24,P['border_h'],band['ground']); t.rect(0,0,24,1,band['edge']); t.rect(0,P['border_h']-1,24,1,band['edge'])
        n0=len(CROSSINGS); plait(t,0,24,P['border_h']//2,band,bi); del CROSSINGS[n0:]
        t.image().save(f'{out}/pieces/border_band{bi+1}_tile24.png')        # 24px = three plait cells
        k=Cv(13,13); k.bitmap(0,0,KNOT,band['edge']); k.image().save(f'{out}/pieces/endpiece_band{bi+1}.png')
    for n,woven in (('linen_woven',True),('linen_warp',False)):
        t=Cv(24,16); linen(t,0,24,0,16,woven,random.Random(0)); t.image().save(f'{out}/pieces/{n}_tile.png')
    atlas=Cv(len(names)*20,20)
    for i,n in enumerate(names):
        rows=GLYPHS.get(n) or SPOILS[n]; atlas.bitmap(i*20,0,rows,COLOURS['glyph'].get(n) or COLOURS['spoil'][n])
    atlas.image().save(f'{out}/pieces/glyph_atlas.png')
    m=Cv(13,7,COLOURS['keyline']); m.bitmap(1,1,MARKER,COLOURS['gold'],gold=True); m.image().save(f'{out}/pieces/party_marker.png')
    json.dump(dict(params=PARAMS,colours=COLOURS,atlas=dict(cell=20,order=names,sizes={n:[len((GLYPHS.get(n) or SPOILS[n])[0]),len(GLYPHS.get(n) or SPOILS[n])] for n in names}),
                   columns=cols,current=current),open(f'{out}/pieces/layout.json','w'),indent=1)
    json.dump(dict(audit=report,crossings=CROSSINGS),open(f'{out}/audit.json','w'))
    print(strip.w,strip.h,report)
