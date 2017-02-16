#!/usr/bin/env python
# Brute-force Sphinx documentation from Solidity source.
# TODO: Reimplement as proper Sphinx domain?

sourcedir = '../contracts'
destdir = './gen'

import os
import re


dox = re.compile(
    """
    ( /\*\*.*\*/    # /** ... */
    |  ///[^\n]* )  # /// ...
    ( [^;{]* )      # signature
    ( ;|{ )         # end
    """,
    re.DOTALL | re.VERBOSE)
fsig = re.compile(
    """
    ( function )     {1} # function
    ( [^\(]* )       ?   # functionName
    ( \( [^\)]* \) ) {1} # (args)
    ( .* )           ?   # EVERYTHING ELSE
    """,
    re.DOTALL | re.VERBOSE)


class Contract(object):
    """TODO"""
    pass

class Function(object):
    """TODO"""
    pass

class Documented(object):
    """TODO"""
    def __init__(self, rematch):
        self.comment = self.parse_comment(rematch.group(1))
        self.type_, self.name, self.other = self.parse_signature(rematch.group(2))
        self.endsym = rematch.group(3)
        return

    def parse_comment(self, c):
        """TODO"""
        if c.startswith('///'):
            c = c[3:]    # remove ///
        elif c.startswith('/**'):
            # remove /** and */
            c = c[3:-2]
            # remove in-the-middle *s
            lines = c.split('\n')
            res = []
            for l in lines:
                l = l.strip()
                if l.startswith('* '):
                    l = l[2:]
                if l == '*':
                    l = ''
                res.append(l)
            c = '\n'.join(res)

        return c.strip() # remove leading/trailing whitespace

    def parse_signature(self, s):
        s = s.strip()

        type_ = s.partition(' ')[0]
        name = ''
        other = {}

        if type_ == 'contract':
            words = s.split(' ')
            name = words[1]
            if len(words) > 2:
                parents = []
                # skip "is"
                for i in range(3,len(words)):
                    parent = words[i].strip(',')
                    parents.append(parent)
                other = {'parents': parents}
        elif type_ == 'function':
            sig = fsig.findall(s)[0]
            name = sig[1].strip()
            argstr = sig[2].strip('()')
            modret = sig[3].strip()
            # args = {}
            # for a in argstr.strip('()').split(','):
            #     a = a.split()
            #     argtype = a[0]
            #     argname = a[1]
            other = {'args': argstr, 'modret': modret}
                
        return (type_, name, other)


def get_documented(data):
    docstrings = []
    iterator = dox.finditer(data)
    for match in iterator:
        docstrings.append(Documented(match))
    return docstrings


def main():
    for root, dirs, files in os.walk(sourcedir):
        for f in files:
            filename = os.path.join(root, f)
            print('Trying ' + filename + ' ...')
            if not filename.endswith('.sol'):
                print('Not a Solidity file!')
                continue
            with open(filename, 'r') as fd:
                filestring = fd.read()
                docstrings = get_documented(filestring)
                for d in docstrings:
                    print('=====')
                    print(d.type_)
                    print(d.name)
                    print(d.other)
                    print('-----')
                    print(d.comment)
                    print('-----')
    return


if __name__ == '__main__':
    main()
