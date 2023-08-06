# -*- coding: utf-8 -*-
from .simplekernel import SimpleKernel

def getTokensEndLoc():
    """Method to be called from within a parse action to determine the end
       location of the parsed tokens.

       removed silenty from pyparsing
    """
    import inspect
    fstack = inspect.stack()
    try:
        # search up the stack (through intervening argument normalizers) for correct calling routine
        for f in fstack[2:]:
            if f[3] == "_parseNoCache":
                endloc = f[0].f_locals["loc"]
                return endloc
        else:
            raise ParseFatalException("incorrect usage of getTokensEndLoc - may only be called from within a parse action")
    finally:
        del fstack

def skipToMatching(opener, closer):
    nest = nestedExpr(opener, closer)
    nest.setParseAction(lambda l, s, t: l[s:getTokensEndLoc()])
    return nest

class TexSurgery(object):
    """TexSurgery allows to make some replacements in LaTeX code"""

    def __init__(self, tex_source):
        super(TexSurgery, self).__init__()
        self.original_src = tex_source
        self.src = tex_source
        #lazy
        self._kernel = self.kernel_name = None

    def __del__(self):
        """
        ## Description
        Destructor. Shuts down kernel safely.
        """
        self.shutdown()

    def shutdown(self):
        if self._kernel:
            self._kernel.kernel_manager.shutdown_kernel()
            self._kernel = None

    @property
    def kernel(self):
        if not self._kernel:
            self._kernel = SimpleKernel(self.kernel_name)
        return self._kernel

    def add_import(self, package, options):
        #TODO
        return self

    def data_surgery(self, replacements):
        #TODO: use pyparsing instead of regex, for the sake of uniformity
        src = self.src
        import re
        revars = re.compile('|'.join(r'\\'+key for key in replacements))
        pos,pieces = 0, []
        m = revars.search(src)
        while m:
            start,end = m.span()
            pieces.append(src[pos:start])
            #start+1, since the backslash \ is not part of the key
            name = src[start+1:end]
            pieces.append(replacements[name])
            pos = end
            m = revars.search(src, pos=pos)
        pieces.append(src[pos:])
        self.src = ''.join(pieces)
        return self

    def latexify(self, results):
        #TODO 'image/png'
        #TODO do something special with 'text/html'?
        return '\n'.join(
            r.get('text/plain') or r.get('text/html') or r.get('error')
            for r in results
        )

    def runsilent(self, l, s, t):
        code = l[s+18:getTokensEndLoc()-15]
        self.kernel.executesilent(code)
        return ''

    def run(self, l, s, t):
        code =  l[s+12:getTokensEndLoc()-9]
        return self.latexify(self.kernel.execute(code))

    def eval(self, l, s, t):
        code =  l[s+6:getTokensEndLoc()-1]
        return self.latexify(self.kernel.execute(code))

    def sage(self, l, s, t):
        code =  l[s+6:getTokensEndLoc()-1]
        return self.latexify(self.kernel.execute('latex(%s)'%code))

    def sif(self, l, s, t):
        return t.texif

    def code_surgery(self):
        # Look for usepackage[kernel]{surgery} markup to choose sage, python, R, julia
        #  or whatever interactive command line application
        # Use pyparsing as in student_surgery to go through sage|sagestr|sagesilent|sif|schoose in order
        # Use SimpleKernel to comunicate with a sage process ?
        from simplekernel import SimpleKernel
        from pyparsing import nestedExpr

        # TODO Look for usepackage[kernel]{surgery} markup to choose sage, python, R, julia
        self.kernel_name = 'sagemath'

        #TODO?? first pass for synonims sage->eval sagesilent->runsilent
        run = nestedExpr('\\begin{run}', '\\end{run}')
        run.setParseAction(self.run)
        runsilent = nestedExpr('\\begin{runsilent}', '\\end{runsilent}')
        runsilent.setParseAction(self.runsilent)
        eval = '\\eval' + nestedExpr('{', '}')
        eval.setParseAction(self.eval)
        sage = '\\sage' + nestedExpr('{', '}')
        sage.setParseAction(self.sage)
        sif = ('\\sif' + nestedExpr('{', '}')('condition')
                + nestedExpr('{', '}')('texif')  + nestedExpr('{', '}')('texelse')
                )
        sif.setParseAction(self.sif)
        codeparser = run | runsilent | eval | sage | sif
        self.src = codeparser.transformString(self.src)
        return self
