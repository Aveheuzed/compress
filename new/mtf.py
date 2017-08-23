#!/usr/bin/env python3

def mtf(string,compressed=False):
        letters = list(range(256))
        out = list()
        for s in string :
                if not compressed :
                        i = letters.index(s)
                        letters.insert(0,letters.pop(i))
                else :
                        i = letters[s]
                        letters.insert(0,letters.pop(s))
                out.append(i)
        return bytes(out)
