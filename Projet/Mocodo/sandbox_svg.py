#!/usr/bin/env python
# encoding: utf-8
# Généré par Mocodo 2.3.7 le Thu, 21 Feb 2019 19:35:54

from __future__ import division
from math import hypot

import time, codecs

(width,height) = (520,296)
cx = {
    u"PEUT VIVRE DANS"    :   91,
    u"ENCLOS"             :  243,
    u"OCCUPE"             :  354,
    u"PÉRIODE"            :  470,
    u"ESPÈCE"             :   91,
    u"DF"                 :  243,
    u"ANIMAL"             :  354,
    u"A MÈRE"             :  470,
    u"PEUT COHABITER AVEC":   91,
    u"A PÈRE"             :  354,
}
cy = {
    u"PEUT VIVRE DANS"    :   44,
    u"ENCLOS"             :   44,
    u"OCCUPE"             :   44,
    u"PÉRIODE"            :   44,
    u"ESPÈCE"             :  157,
    u"DF"                 :  157,
    u"ANIMAL"             :  157,
    u"A MÈRE"             :  157,
    u"PEUT COHABITER AVEC":  261,
    u"A PÈRE"             :  261,
}
shift = {
    u"PEUT VIVRE DANS,ESPÈCE"         :    0,
    u"PEUT VIVRE DANS,ENCLOS"         :    0,
    u"OCCUPE,ANIMAL"                  :    0,
    u"OCCUPE,PÉRIODE"                 :    0,
    u"OCCUPE,ENCLOS"                  :    0,
    u"DF,ESPÈCE"                      :    0,
    u"DF,ANIMAL"                      :    0,
    u"A MÈRE,ANIMAL,-1.0"             :    0,
    u"A MÈRE,ANIMAL,1.0"              :    0,
    u"PEUT COHABITER AVEC,ESPÈCE,-1.0":    0,
    u"PEUT COHABITER AVEC,ESPÈCE,1.0" :    0,
    u"A PÈRE,ANIMAL,-1.0"             :    0,
    u"A PÈRE,ANIMAL,1.0"              :    0,
}
ratio = {
    u"A MÈRE,ANIMAL,1.0":  1.00,
    u"A PÈRE,ANIMAL,1.0":  1.00,
}
colors = {
    u"annotation_color"                : '#000000',
    u"annotation_text_color"           : '#FFFFFF',
    u"association_attribute_text_color": '#000000',
    u"association_cartouche_color"     : '#FFFFFF',
    u"association_cartouche_text_color": '#000000',
    u"association_color"               : '#FFFFFF',
    u"association_stroke_color"        : '#000000',
    u"background_color"                : 'none',
    u"card_text_color"                 : '#000000',
    u"entity_attribute_text_color"     : '#000000',
    u"entity_cartouche_color"          : '#FFFFFF',
    u"entity_cartouche_text_color"     : '#000000',
    u"entity_color"                    : '#FFFFFF',
    u"entity_stroke_color"             : '#000000',
    u"label_text_color"                : '#000000',
    u"leg_stroke_color"                : '#000000',
    u"transparent_color"               : 'none',
}
card_max_width = 22
card_max_height = 15
card_margin = 5
arrow_width = 12
arrow_half_height = 6
arrow_axis = 8
card_baseline = 3

def cmp(x, y):
    return (x > y) - (x < y)

def offset(x, y):
    return (x + card_margin, y - card_baseline - card_margin)

def line_intersection(ex, ey, w, h, ax, ay):
    if ax == ex:
        return (ax, ey + cmp(ay, ey) * h)
    if ay == ey:
        return (ex + cmp(ax, ex) * w, ay)
    x = ex + cmp(ax, ex) * w
    y = ey + (ay-ey) * (x-ex) / (ax-ex)
    if abs(y-ey) > h:
        y = ey + cmp(ay, ey) * h
        x = ex + (ax-ex) * (y-ey) / (ay-ey)
    return (x, y)

def straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch):
    
    def card_pos(twist, shift):
        compare = (lambda x1_y1: x1_y1[0] < x1_y1[1]) if twist else (lambda x1_y1: x1_y1[0] <= x1_y1[1])
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - shift
        (xg, yg) = line_intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = line_intersection(ex, ey, ew + cw, eh, ax, ay)
        if compare((xg, xb)):
            if compare((xg, ex)):
                if compare((yb, ey)):
                    return (xb - correction, yb)
                return (xb - correction, yb + ch)
            if compare((yb, ey)):
                return (xg, yg + ch - correction)
            return (xg, yg + correction)
        if compare((xb, ex)):
            if compare((yb, ey)):
                return (xg - cw, yg + ch - correction)
            return (xg - cw, yg + correction)
        if compare((yb, ey)):
            return (xb - cw + correction, yb)
        return (xb - cw + correction, yb + ch)
    
    def arrow_pos(direction, ratio):
        (x0, y0) = line_intersection(ex, ey, ew, eh, ax, ay)
        (x1, y1) = line_intersection(ax, ay, aw, ah, ex, ey)
        if direction == "<":
            (x0, y0, x1, y1) = (x1, y1, x0, y0)
        (x, y) = (ratio * x0 + (1 - ratio) * x1, ratio * y0 + (1 - ratio) * y1)
        return (x, y, x1 - x0, y0 - y1)
    
    straight_leg_factory.card_pos = card_pos
    straight_leg_factory.arrow_pos = arrow_pos
    return straight_leg_factory


def curved_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, spin):
    
    def bisection(predicate):
        (a, b) = (0, 1)
        while abs(b - a) > 0.0001:
            m = (a + b) / 2
            if predicate(bezier(m)):
                a = m
            else:
                b = m
        return m
    
    def intersection(left, top, right, bottom):
       (x, y) = bezier(bisection(lambda p: left <= p[0] <= right and top <= p[1] <= bottom))
       return (int(round(x)), int(round(y)))
    
    def card_pos(shift):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal)
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin > 0:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction + shift, bot + ch)
            if (xr == RIG and yr >= top) or yr == BOT:
                return (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) + correction + shift)
            if (yr == TOP and xr >= lef) or xr == RIG:
                return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) + correction + shift - cw, TOP + ch)
            return (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction + shift + ch)
        if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
            return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) + correction + shift - cw, bot + ch)
        if xr == RIG or (yr == TOP and xr >= rig):
            return (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction + shift + ch)
        if yr == TOP or (xr == LEF and yr <= top):
            return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction + shift, TOP + ch)
        return (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) + correction + shift)
    
    def arrow_pos(direction, ratio):
        t0 = bisection(lambda p: abs(p[0] - ax) > aw or abs(p[1] - ay) > ah)
        t3 = bisection(lambda p: abs(p[0] - ex) < ew and abs(p[1] - ey) < eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * ratio
        (xc, yc) = bezier(tc)
        (x, y) = derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        return (xc, yc, x, -y)
    
    diagonal = hypot(ax - ex, ay - ey)
    (x, y) = line_intersection(ex, ey, ew + cw / 2, eh + ch / 2, ax, ay)
    k = (cw *  abs((ay - ey) / diagonal) + ch * abs((ax - ex) / diagonal))
    (x, y) = (x - spin * k * (ay - ey) / diagonal, y + spin * k * (ax - ex) / diagonal)
    (hx, hy) = (2 * x - (ex + ax) / 2, 2 * y - (ey + ay) / 2)
    (x1, y1) = (ex + (hx - ex) * 2 / 3, ey + (hy - ey) * 2 / 3)
    (x2, y2) = (ax + (hx - ax) * 2 / 3, ay + (hy - ay) * 2 / 3)
    (kax, kay) = (ex - 2 * hx + ax, ey - 2 * hy + ay)
    (kbx, kby) = (2 * hx - 2 * ex, 2 * hy - 2 * ey)
    bezier = lambda t: (kax*t*t + kbx*t + ex, kay*t*t + kby*t + ey)
    derivate = lambda t: (2*kax*t + kbx, 2*kay*t + kby)
    
    curved_leg_factory.points = (ex, ey, x1, y1, x2, y2, ax, ay)
    curved_leg_factory.card_pos = card_pos
    curved_leg_factory.arrow_pos = arrow_pos
    return curved_leg_factory


def upper_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w - r, y, "a", r, r, 90, 0, 1, r, r, "V", y + h, "h", -w, "V", y + r, "a", r, r, 90, 0, 1, r, -r]])

def lower_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w, y, "v", h - r, "a", r, r, 90, 0, 1, -r, r, "H", x + r, "a", r, r, 90, 0, 1, -r, -r, "V", y, "H", w]])

def arrow(x, y, a, b):
    c = hypot(a, b)
    (cos, sin) = (a / c, b / c)
    return " ".join([str(x) for x in [ "M", x, y, "L", x + arrow_width * cos - arrow_half_height * sin, y - arrow_half_height * cos - arrow_width * sin, "L", x + arrow_axis * cos, y - arrow_axis * sin, "L", x + arrow_width * cos + arrow_half_height * sin, y + arrow_half_height * cos - arrow_width * sin, "Z"]])

def safe_print_for_PHP(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("utf8"))


lines = '<?xml version="1.0" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
lines += '\n\n<svg width="%s" height="%s" view_box="0 0 %s %s"\nxmlns="http://www.w3.org/2000/svg"\nxmlns:link="http://www.w3.org/1999/xlink">' % (width,height,width,height)
lines += u'\\n\\n<desc>Généré par Mocodo 2.3.7 le %s</desc>' % time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
lines += '\n\n<rect id="frame" x="0" y="0" width="%s" height="%s" fill="%s" stroke="none" stroke-width="0"/>' % (width,height,colors['background_color'] if colors['background_color'] else "none")

lines += u"""\n\n<!-- Association PEUT VIVRE DANS -->"""
(x,y) = (cx[u"PEUT VIVRE DANS"],cy[u"PEUT VIVRE DANS"])
(ex,ey) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
leg=straight_leg_factory(ex,ey,45,35,x,y,75,26,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"PEUT VIVRE DANS,ESPÈCE"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"ENCLOS"],cy[u"ENCLOS"])
leg=straight_leg_factory(ex,ey,45,26,x,y,75,26,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"PEUT VIVRE DANS,ENCLOS"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-PEUT VIVRE DANS">""" % {}
path = upper_round_rect(-75+x,-26+y,150,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-75+x,0.0+y,150,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="150" height="52" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -75+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -75+x, 'y0': 0+y, 'x1': 75+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">PEUT VIVRE DANS</text>""" % {'x': -57+x, 'y': -7.4+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">nb. max. congénères</text>""" % {'x': -68+x, 'y': 18.6+y, 'text_color': colors['association_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association OCCUPE -->"""
(x,y) = (cx[u"OCCUPE"],cy[u"OCCUPE"])
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
leg=straight_leg_factory(ex,ey,53,53,x,y,34,26,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"OCCUPE,ANIMAL"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"PÉRIODE"],cy[u"PÉRIODE"])
leg=straight_leg_factory(ex,ey,41,35,x,y,34,26,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"OCCUPE,PÉRIODE"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"ENCLOS"],cy[u"ENCLOS"])
leg=straight_leg_factory(ex,ey,45,26,x,y,34,26,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"OCCUPE,ENCLOS"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-OCCUPE">""" % {}
path = upper_round_rect(-34+x,-26+y,68,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-34+x,0.0+y,68,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="68" height="52" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -34+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -34+x, 'y0': 0+y, 'x1': 34+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">OCCUPE</text>""" % {'x': -27+x, 'y': -7.4+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association DF -->"""
(x,y) = (cx[u"DF"],cy[u"DF"])
(ex,ey) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
leg=straight_leg_factory(ex,ey,45,35,x,y,16,16,22+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"DF,ESPÈCE"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
leg=straight_leg_factory(ex,ey,53,53,x,y,16,16,21+2*card_margin,15+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"DF,ANIMAL"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ux,uy)=(tx+21,ty--2)
lines += u"""\n<line x1="%(tx)s" y1="%(uy)s" x2="%(ux)s" y2="%(uy)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'tx': tx, 'uy': uy, 'ux': ux, 'uy': uy, 'stroke_color': colors['card_text_color']}
lines += u"""\n<g id="association-DF">""" % {}
lines += u"""\n	<circle cx="%(cx)s" cy="%(cy)s" r="16" stroke="%(stroke_color)s" stroke-width="1.5" fill="%(color)s"/>""" % {'cx': x, 'cy': y, 'stroke_color': colors['association_stroke_color'], 'color': colors['association_cartouche_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">DF</text>""" % {'x': -9+x, 'y': 3.4+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association A MÈRE -->"""
(x,y) = (cx[u"A MÈRE"],cy[u"A MÈRE"])
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
leg=curved_leg_factory(ex,ey,53,53,x,y,31,26,21+2*card_margin,15+2*card_margin,-1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"A MÈRE,ANIMAL,-1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
leg=curved_leg_factory(ex,ey,53,53,x,y,31,26,22+2*card_margin,15+2*card_margin,1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"A MÈRE,ANIMAL,1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12" onmouseover="show(evt,'mère')" onmouseout="hide(evt)" style="cursor: pointer;">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
path=arrow(*leg.arrow_pos(">",ratio[u"A MÈRE,ANIMAL,1.0"]))
lines += u"""\n<path d="%(path)s" fill="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'stroke_color': colors['leg_stroke_color']}
lines += u"""\n<g id="association-A MÈRE">""" % {}
path = upper_round_rect(-31+x,-26+y,62,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-31+x,0.0+y,62,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="62" height="52" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -31+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -31+x, 'y0': 0+y, 'x1': 31+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">A MÈRE</text>""" % {'x': -24+x, 'y': -7.4+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association PEUT COHABITER AVEC -->"""
(x,y) = (cx[u"PEUT COHABITER AVEC"],cy[u"PEUT COHABITER AVEC"])
(ex,ey) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
leg=curved_leg_factory(ex,ey,45,35,x,y,82,26,22+2*card_margin,15+2*card_margin,-1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"PEUT COHABITER AVEC,ESPÈCE,-1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
leg=curved_leg_factory(ex,ey,45,35,x,y,82,26,22+2*card_margin,15+2*card_margin,1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"PEUT COHABITER AVEC,ESPÈCE,1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12" onmouseover="show(evt,'commensale')" onmouseout="hide(evt)" style="cursor: pointer;">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-PEUT COHABITER AVEC">""" % {}
path = upper_round_rect(-82+x,-26+y,164,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-82+x,0.0+y,164,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="164" height="52" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -82+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -82+x, 'y0': 0+y, 'x1': 82+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">PEUT COHABITER AVEC</text>""" % {'x': -75+x, 'y': -7.4+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">nb. max. commensaux</text>""" % {'x': -75+x, 'y': 18.6+y, 'text_color': colors['association_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association A PÈRE -->"""
(x,y) = (cx[u"A PÈRE"],cy[u"A PÈRE"])
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
leg=curved_leg_factory(ex,ey,53,53,x,y,30,26,22+2*card_margin,15+2*card_margin,-1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"A PÈRE,ANIMAL,-1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
leg=curved_leg_factory(ex,ey,53,53,x,y,30,26,22+2*card_margin,15+2*card_margin,1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"A PÈRE,ANIMAL,1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Verdana" font-size="12" onmouseover="show(evt,'père présumé')" onmouseout="hide(evt)" style="cursor: pointer;">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
path=arrow(*leg.arrow_pos(">",ratio[u"A PÈRE,ANIMAL,1.0"]))
lines += u"""\n<path d="%(path)s" fill="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'stroke_color': colors['leg_stroke_color']}
lines += u"""\n<g id="association-A PÈRE">""" % {}
path = upper_round_rect(-30+x,-26+y,60,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-30+x,0.0+y,60,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="60" height="52" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -30+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -30+x, 'y0': 0+y, 'x1': 30+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">A PÈRE</text>""" % {'x': -23+x, 'y': -7.4+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity ENCLOS -->"""
(x,y) = (cx[u"ENCLOS"],cy[u"ENCLOS"])
lines += u"""\n<g id="entity-ENCLOS">""" % {}
lines += u"""\n	<g id="frame-ENCLOS">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="90" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -45+x, 'y': -26+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="90" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -45+x, 'y': 0.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="90" height="52" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -45+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -45+x, 'y0': 0+y, 'x1': 45+x, 'y1': 0+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">ENCLOS</text>""" % {'x': -25+x, 'y': -7.4+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">num. enclos</text>""" % {'x': -40+x, 'y': 18.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -40+x, 'y0': 21.0+y, 'x1': 39+x, 'y1': 21.0+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity PÉRIODE -->"""
(x,y) = (cx[u"PÉRIODE"],cy[u"PÉRIODE"])
lines += u"""\n<g id="entity-PÉRIODE">""" % {}
lines += u"""\n	<g id="frame-PÉRIODE">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="82" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -41+x, 'y': -35+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="82" height="44" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -41+x, 'y': -9.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="82" height="70" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -41+x, 'y': -35+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -41+x, 'y0': -9+y, 'x1': 41+x, 'y1': -9+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">PÉRIODE</text>""" % {'x': -28+x, 'y': -16.4+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">date début</text>""" % {'x': -36+x, 'y': 9.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -36+x, 'y0': 12.0+y, 'x1': 36+x, 'y1': 12.0+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">date fin</text>""" % {'x': -36+x, 'y': 27.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -36+x, 'y0': 30.0+y, 'x1': 16+x, 'y1': 30.0+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity ESPÈCE -->"""
(x,y) = (cx[u"ESPÈCE"],cy[u"ESPÈCE"])
lines += u"""\n<g id="entity-ESPÈCE">""" % {}
lines += u"""\n	<g id="frame-ESPÈCE">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="90" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -45+x, 'y': -35+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="90" height="44" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -45+x, 'y': -9.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="90" height="70" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -45+x, 'y': -35+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -45+x, 'y0': -9+y, 'x1': 45+x, 'y1': -9+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">ESPÈCE</text>""" % {'x': -24+x, 'y': -16.4+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">code espèce</text>""" % {'x': -40+x, 'y': 9.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -40+x, 'y0': 12.0+y, 'x1': 40+x, 'y1': 12.0+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">libellé</text>""" % {'x': -40+x, 'y': 27.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity ANIMAL -->"""
(x,y) = (cx[u"ANIMAL"],cy[u"ANIMAL"])
lines += u"""\n<g id="entity-ANIMAL">""" % {}
lines += u"""\n	<g id="frame-ANIMAL">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="106" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -53+x, 'y': -53+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="106" height="80" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -53+x, 'y': -27.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="106" height="106" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -53+x, 'y': -53+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -53+x, 'y0': -27+y, 'x1': 53+x, 'y1': -27+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">ANIMAL</text>""" % {'x': -25+x, 'y': -34.4+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">nom</text>""" % {'x': -48+x, 'y': -8.4+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y)s" x2="%(x1)s" y2="%(y)s" style="fill:none;stroke:%(stroke_color)s;stroke-width:1;stroke-dasharray:4;"/>""" % {'x0': -48+x, 'y': -6.0+y, 'x1': -20+x, 'y': -6.0+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">sexe</text>""" % {'x': -48+x, 'y': 9.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">date naissance</text>""" % {'x': -48+x, 'y': 27.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Trebuchet MS" font-size="14">date décès</text>""" % {'x': -48+x, 'y': 45.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}
annotation_overlay_height = 40
annotation_baseline = 24
annotation_font = {'family': 'Trebuchet MS', 'size': 14}
annotation_text_color = "#FFFFFF"
annotation_color = "#000000"
annotation_opacity = 0.7

lines += '\n\n<!-- Annotations -->'
lines += '\n<script type="text/ecmascript">'
lines += '\n<![CDATA['
lines += '\n	function show(evt, text) {'
lines += '\n		var pos = (evt.target.getAttribute("y") < %s) ? "bottom" : "top"' % (height - annotation_overlay_height - card_margin)
lines += '\n		var annotation = document.getElementById(pos + "_annotation_2es6o3ED")'
lines += '\n		annotation.textContent = text'
lines += '\n		annotation.setAttributeNS(null, "visibility", "visible");'
lines += '\n		document.getElementById(pos + "_overlay_2es6o3ED").setAttributeNS(null, "visibility", "visible");'
lines += '\n	}'
lines += '\n	function hide(evt) {'
lines += '\n		document.getElementById("top_annotation_2es6o3ED").setAttributeNS(null, "visibility", "hidden");'
lines += '\n		document.getElementById("top_overlay_2es6o3ED").setAttributeNS(null, "visibility", "hidden");'
lines += '\n		document.getElementById("bottom_annotation_2es6o3ED").setAttributeNS(null, "visibility", "hidden");'
lines += '\n		document.getElementById("bottom_overlay_2es6o3ED").setAttributeNS(null, "visibility", "hidden");'
lines += '\n	}'
lines += '\n]]>'
lines += '\n</script>'
lines += '\n<rect id="top_overlay_2es6o3ED" x="0" y="0" width="%s" height="%s" fill="%s" stroke-width="0" opacity="%s" visibility="hidden"/>' % (width, annotation_overlay_height, annotation_color, annotation_opacity)
lines += '\n<text id="top_annotation_2es6o3ED" text-anchor="middle" x="%s" y="%s" fill="%s" font-family="%s" font-size="%s" visibility="hidden"></text>' % (width/2, annotation_baseline, annotation_text_color, annotation_font['family'], annotation_font['size'])
lines += '\n<rect id="bottom_overlay_2es6o3ED" x="0" y="%s" width="%s" height="%s" fill="%s" stroke-width="0" opacity="%s" visibility="hidden"/>' % (height-annotation_overlay_height, width, annotation_overlay_height, annotation_color, annotation_opacity)
lines += '\n<text id="bottom_annotation_2es6o3ED" text-anchor="middle" x="%s" y="%s" fill="%s" font-family="%s" font-size="%s" visibility="hidden"></text>' % (width/2, height-annotation_overlay_height+annotation_baseline, annotation_text_color, annotation_font['family'], annotation_font['size'])
lines += u'\n</svg>'

with codecs.open("sandbox.svg", "w", "utf8") as f:
    f.write(lines)
safe_print_for_PHP(u'Fichier de sortie "sandbox.svg" généré avec succès.')