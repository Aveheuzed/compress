#!/usr/bin/env python3

"""The goal of that script is to compress a python3 script the most it can,
and then to expand it so that it runs the same.
Assertions, comments, docstrings, additionnal '\\n'  are to be saved, but the expanded version
should differ from the original one by its respect of PEP 8 :
https://openclassrooms.com/courses/apprenez-a-programmer-en-python/de-bonnes-pratiques#/id/r-235217
"""
import re, keyword

separators = ",=()[]{}+-*/&|^%~:><!;."

def compress(text):
        # 1. Separating strings / commens from true code
        code, strings = list(), list()
        start = 0
        while True :
                simple, double, hashtag = text.find("'", start), text.find('"', start), text.find("#", start)
                if simple == double == hashtag : # == -1
                        break

                if simple < 0 :
                        simple = float("+inf")
                if double < 0 :
                        double = float("+inf")
                if hashtag < 0 :
                        hashtag = float("+inf")

                first = min(simple, double, hashtag)
                code.append(text[start:first])
                string_start = start = first + (first is not hashtag)
                # we want to keep the # before the comments
                # to differentiate them from docstrings
                if first is simple :
                        delimiter = "'"
                elif first is double :
                        delimiter = '"'
                else :
                        delimiter = "\n"

                string_end = text.index(delimiter, start) - (delimiter=="\n")
                # better keep the trailing "\n" after a comment, so that the next row's indentation can be compressed
                start = string_end+1
                while text[string_end-1] == "\\" and  text[string_end-2] != "\\"  and delimiter != "\n" :
                        # even \ can be escaped, but at the end of a comment
                        string_end = text.index(delimiter, start)
                        start = string_end+1
                strings.append(text[string_start:string_end].replace("\\'","'").replace('\\"','"'))
        code.append(text[start:])

        del text, simple, double, start, first,string_start, string_end, delimiter


        # 2. removing useless spaces
        # as '#' is not present any more in the code, we can use it to mark the places the strings were
        code = "#".join(code)
        for l in separators :
                code.replace(l+" ",l)
                code.replace(" "+l,l)
        del l

        code = re.split("\n|;", code)


        # 3. work around indentation level : everything is removed except dedentation,
        # indetation being fixed by a ":" at the end of a line
        indentation = 0
        block = None
        for i,row in enumerate(code):
                row_strip = row.lstrip()
                if not len(row_strip):
                        continue
                        # empty lines are to be ignored
                new_indentation = len(row) - len(row_strip)
                if new_indentation > 0 and block is None :
                        block = new_indentation
                if new_indentation < indentation :
                        # line dedented
                        # we symbolize it with a heading "-"
                        row_strip = "-"*((new_indentation-indentation)//block) + row_strip
                indentation = new_indentation
                code[i] = row_strip

        code = ";".join(code)

        del i, row, row_strip, indentation, new_indentation


        # 4. replacing the variable, attribute names and keywords by a smaller form
        maybe_vars = set(re.split( "["+re.escape(separators)+" \t#]+", code))

        # the line before includes litterals, such as numbers or lists
        # we filter it there to keep only the vars and attributes of the code
        var_re = re.compile("^[a-zA-Z_][a-zA-Z0-9_]+$")
        allnames = [x.strip() for x in maybe_vars if var_re.fullmatch(x.strip()) and x not in keyword.kwlist]
        allnames.sort(key=len, reverse=True)
        # we have to replace the longest vars first, to avoid replacing
        # only a part of a long name when replacing a smaller one
        # example in this code with row and row_strip : if you replace
        # row first, row_strip would become $x_strip,
        # and wouldn't be replaced on its turn

        for j,name in enumerate(allnames) :
                code = code.replace(name,"$"+chr(j))
                # j's limited to 1114111,
                # so there can't be more than 1114111 vars
                # in the same script (hope it will be enough ;)
        for j,name in enumerate(sorted(keyword.kwlist,key=len,reverse=True)) :
                code = code.replace(name,"µ"+chr(j))

        code = code.replace(":;",";") # we know where ':' are, just with the keywords in the line


        # 5. Compressing the strings
        # we use a non-printable char to mark the separation btw strings,
        # so that we're quite sure it will never appear in a source code file
        assert chr(1) not in "".join(strings)
        strings = chr(1).join(strings)


        # 6. putting all that stuff together (strings, code, vars/attributes)
        allnames = ",".join(allnames)

        return "!".join([allnames,code, strings])
        # there is no"!" in code not in allnames
        # but for a $! that may replace a name,
        # so re.split('(^$)!', compressed, maxsplit=3) should be enough
        # to separate the 3 parts back

def expand(text):
        pass
