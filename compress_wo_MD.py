def compress(text):
    score = lambda x : (text.count(x)-1)*(len(x)-2)-2

    i = 0
    while bytes([i,]) in text :
        i += 1
        if i == 256 :
            raise DeprecationWarning(\
                "Too many different letters in the text to comprees it !")
    NEW = bytes([i,])
    i += 1
    while bytes([i,]) in text :
        i += 1
        if i == 256 :
            raise DeprecationWarning(\
                "Too many different letters in the text to comprees it !")
    REPLACE = bytes([i,])

    words = list()
    for l in range(15,1,-1):
        wds = set()
        for i in range(len(text)-l):
            w = text[i:i+l]
            if w in wds :
                continue
            elif score(w) > 0 :
                wds.add(w)
                words.append(dict(start=i,stop=i+l,\
                                  score=score(w),content=w,howmany=text.count(w)))
        
    words = sorted(words,key=(lambda x:x["score"]),reverse=1)

    i = 0
    while i<len(words):
        group = words[i+1:]
        tested = words[i]
        _t = text.replace(tested["content"],REPLACE)
        to_be_removed = list()
        for j,n in enumerate(group,i+1) :
            if text.count(n["content"]) != _t.count(n["content"]):
                to_be_removed.append(j)
        to_be_removed.sort(reverse=True)
        for x in to_be_removed :
            del words[x]
        i += 1
    
    words = sorted(words[:254],key=lambda x:x["start"])
    words = [x["content"] for x in words]
    #building a list of the words being replaced, sorted by its indexes in the
    #original text

    for i,w in enumerate(words):
        if i >= ord(NEW) :
            i += 1
        if i >= ord(REPLACE) :
            i += 1
        text = text.split(w)
        text = [text[0] + NEW + w + NEW + text[1],]+text[2:]
        text = (REPLACE+bytes([i,])).join(text)
    return NEW+REPLACE+text


def expand(text):
    NEW = text[0:1]
    REPLACE = text[1:2]
    text = text[2:].split(NEW)
    r = False
    words = list()
    t = bytes()
    for x in text :
        if r :
            words.append(x)
        t += x
        r = not r
    words.insert(ord(NEW),None)
    words.insert(ord(REPLACE),None)
    t = t.split(REPLACE)
    rep = t.pop(0)
    for x in t:
        rep += words[x[0]]+x[1:]
    return rep

if __name__ == "__main__" :
    from time import time
    t = open("/home/aveheuzed/lorem_ipsum","rb").read()#"telle mere, telle fille".encode()
    print("\t",time())
    a = compress(t)
    print("\t",time())
    b = expand(a)
    print("\t",time())
    print(len(a),"\t",len(t))
    print(b == t,end="\n\n")
