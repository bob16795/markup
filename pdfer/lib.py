from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
import os

font = TTFont('times.ttf')
cmap = font['cmap']
t = cmap.getcmap(3, 1).cmap
s = font.getGlyphSet()
units_per_em = font['head'].unitsPerEm

def get_text_size(text, font_size):
    total = 0
    for c in text:
        if ord(c) in t and t[ord(c)] in s:
            total+= s[t[ord(c)]].width
        else:
            total+= s['.notdef'].width
    total = total*float(font_size)/units_per_em;
    return total
