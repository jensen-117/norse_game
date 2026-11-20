import struct, zlib, sys
from PIL import Image
path, outdir = sys.argv[1], sys.argv[2]
d = open(path,'rb').read()
(fsize, magic, nframes, W, H, depth, flags, speed) = struct.unpack_from('<IHHHHHIH', d, 0)
trans = d[28]; ncolors = struct.unpack_from('<H', d, 32)[0]
print('frames',nframes,'size',W,H,'depth',depth,'transidx',trans,'ncolors',ncolors)
off = 128
layers=[]; palette={}
frames=[]
for fi in range(nframes):
    fbytes, fmagic, oldch, dur = struct.unpack_from('<IHHH', d, off)
    newch = struct.unpack_from('<I', d, off+12)[0]
    nch = newch if newch else oldch
    p = off+16; cels=[]
    for _ in range(nch):
        csize, ctype = struct.unpack_from('<IH', d, p)
        body = d[p+6:p+csize]
        if ctype==0x2004:
            fl, lt, child, _, _, blend, op = struct.unpack_from('<HHHHHHB', body, 0)
            nl = struct.unpack_from('<H', body, 16)[0]
            name = body[18:18+nl].decode('utf8','replace')
            layers.append(dict(name=name, flags=fl, type=lt, child=child, opacity=op))
        elif ctype==0x2019:
            n, first, last = struct.unpack_from('<III', body, 0)
            q=20
            for i in range(first,last+1):
                ef,r,g,b,a = struct.unpack_from('<HBBBB', body, q); q+=6
                if ef&1:
                    sl=struct.unpack_from('<H',body,q)[0]; q+=2+sl
                palette[i]=(r,g,b,a)
        elif ctype==0x2005:
            li, x, y, op, ct = struct.unpack_from('<HhhBH', body, 0)
            if ct in (0,2):
                w,h = struct.unpack_from('<HH', body, 16)
                raw = body[20:] if ct==0 else zlib.decompress(body[20:])
                cels.append(dict(layer=li,x=x,y=y,w=w,h=h,op=op,px=raw))
            elif ct==1:
                cels.append(dict(layer=li,link=struct.unpack_from('<H',body,16)[0]))
        p += csize
    frames.append((dur,cels)); off += fbytes
print('layers',[(i,l['name'],l['type'],'hidden' if not l['flags']&1 else 'vis') for i,l in enumerate(layers)])
print('palette size',len(palette))
bpp = {32:4,16:2,8:1}[depth]
def cel_img(c):
    img = Image.new('RGBA',(c['w'],c['h']))
    px=c['px']; out=[]
    for i in range(c['w']*c['h']):
        if bpp==4: out.append(tuple(px[i*4:i*4+4]))
        elif bpp==2: v,a=px[i*2],px[i*2+1]; out.append((v,v,v,a))
        else:
            idx=px[i]; out.append((0,0,0,0) if idx==trans else palette.get(idx,(255,0,255,255)))
    img.putdata(out); return img
used=set()
for fi,(dur,cels) in enumerate(frames):
    comp = Image.new('RGBA',(W,H),(0,0,0,0))
    for c in sorted(cels,key=lambda c:c['layer']):
        if 'link' in c: c = [cc for cc in frames[c['link']][1] if cc['layer']==c['layer']][0]
        if not layers[c['layer']]['flags']&1: continue
        im=cel_img(c)
        if bpp==1: used.update(set(c['px'])-{trans})
        comp.alpha_composite(im,(c['x'],c['y']))
        cel_img(c).resize((c['w']*8,c['h']*8),Image.NEAREST).save(f"{outdir}/f{fi}_L{c['layer']}.png")
    print('frame',fi,'dur',dur,'cels',[(c['layer'],c.get('x'),c.get('y'),c.get('w'),c.get('h')) for c in cels])
    comp.save(f"{outdir}/frame{fi}.png")
    comp.resize((W*10,H*10),Image.NEAREST).save(f"{outdir}/frame{fi}_x10.png")
if used: print('palette indices used', sorted(used), [palette[i][:3] for i in sorted(used)])
