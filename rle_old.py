#bug ln 116
from itertools import groupby,cycle
from boolstring import to_bytes, to_bool

def group(seq,n,complete=None):
    assert hasattr(n,"__index__")\
           and hasattr(seq,"__iter__")
    i = n
    while i<=len(seq) :
        yield seq[i-n:i]
        i += n
    last = seq[i-n:]
    if len(last):
        if complete is None:
            yield last
        else :
            yield(last + complete*(n-len(last)))

def rlecompress(text,mode=3):
    """
The smallest the mode is, the most "efficient" the algorithm is
"""
    assert mode>1, "mode must be 2 or more"
    _mode = mode
    mode = 2**mode-1#represents the max value allowed (on <mode-param> bits)

    text = to_bool(text)
    if not text[0] :
        rep = list()
    else :
        rep = [0,]
    #the first value always represents a number of zeros

    for i,it in groupby(text):
        it = len(list(it))
        while it > mode :
            rep.extend([0,mode])
            it -= mode
        rep.append(it)

    d = {"0":False,"1":True}
    _rep = [d[x] for x in "".join([bin(x)[2:].zfill(_mode) for x in rep])]

    _rep.insert(0,True)

    return to_bytes(_rep)

def rleexpand(text,mode=3):
    assert mode>1, "mode must be 2 or more"
    d = {False:"0",True:"1"}
    text = [d[x] for x in to_bool(text)]

    del text[:text.index("1")+1]
    text = "".join(text)
    
    S = 0

    rep = list()
    bit = cycle([False,True])
    for x in group(text,mode):
        b = next(bit)
        x = int(x,base=2)
        rep += [b,]*x
        S += x
    assert not S%8
    return to_bytes(rep)
        
"""
compressed string binary pattern :
^0*1((0|1)[mode])+$
"""

#----------------------------------------------------------------------

def borders_compress(text,mode=(1,3)):
    """mode : (mode for enhanced (bytes), mode for rle (bits) )"""
    assert mode[0] and mode[1]>1, "mode must be at least (1,2)"
    key = [0,0,0,0,0,0,0,0]*mode[0]
    text = to_bool(text)

    for block in group(text,8*mode[0]):
        for i in range(8*mode[0]-1):
            if block[i] != block[i+1]:
                key[i+1] += 1
                key[i] += 1
        key = [i-1 for i in key]
    key = [x>=0 for x in key]
    text = to_bytes([x^y for x,y in zip(text,cycle(key))])
    return to_bytes(key)+rlecompress(text,mode[1])

def borders_expand(text,mode=(1,3)):
    """mode : (mode for enhanced (bytes), mode for rle (bits) )"""
    assert mode[0] and mode[1]>1, "mode must be at least (1,2)"
    key,text = text[:mode[0]],text[mode[0]:]
    text = rleexpand(text,mode[1])
    key,text = to_bool(key),to_bool(text)
    return to_bytes([x^y for x,y in zip(cycle(key),text)])

#----------------------------------------------------------------

def average_compress(text,mode=(1,3)):
    """mode : (mode for enhanced (bytes), mode for rle (bits) )"""
    assert mode[0] and mode[1]>1, "mode must be at least (1,2)"
    key = [0,0,0,0,0,0,0,0]*mode[0]
    text = to_bool(text)

    for block in group(text,8*mode[0]):
        key = [x+y for x,y in zip(key,block)]
    print(key)
    av = sum(key)/len(key)
    key = [x>av for x in key]
    """x>av/2 ; x<av/2 """

    text = to_bytes([x^y for x,y in zip(text,cycle(key))])
    return to_bytes(key)+rlecompress(text,mode[1])

average_expand = borders_expand#bug here
