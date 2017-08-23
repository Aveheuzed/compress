def compress(text):
    from pickle import dumps

    score = lambda w : (text.count(w)-1)*(len(w)-1)-8#text.count(w)*(len(w)-1)-(7+len(w))#7=> key=int ; 10=> key=bytes

    words = set()
    for l in range(20,1,-1):
        for i in range(len(text)-l):
            w = text[i:i+l]
            if w in words :
                continue
            elif score(w) > 0 :
                words.add(w)

    words = sorted(words,key=score,reverse=True)

    letters = (bytes([x,]) for x in range(256) if bytes([x,]) not in text)
    codex = dict()
    for w in words :
        if score(w) > 0 :#to avoid replacing both "foo " and "foo"
            try :
                c = next(letters)
            except StopIteration :
                break
            else :
                text = text.replace(w,c)
                codex[ord(c)] = w
    return dumps((text,codex))

def expand(text):
    from pickle import loads
    text,codex = loads(text)
    for c,w in codex.items() :
        text = text.replace(chr(c).encode(),w)
    return text

if __name__ == "__main__" :
    from time import time
    t = open("/home/aveheuzed/lorem_ipsum","rb").read()
    print("\t",time())
    a = compress(t)
    print("\t",time())
    b = expand(a)
    print("\t",time())
    print(len(a),"\t",len(t))
    print(b == t,end="\n\n")

