import os,six
__version__ = "1.0.1"
class System:
    """

    >>> System(shortSep=" ").git.command("log",n=1,pretty="format:%ad %s")
    'git log -n 1 --pretty="format:%ad %s"'

    """
    def __init__(self,cwd=None,kwdSep="=",shortSep=" "):
        self.cwd = cwd or os.getcwd()
        self.sepLong=kwdSep
        self.sepShort=shortSep
    def build_command(self,name,*args,**kwargs):
        kwargs.setdefault("___kwdsep2", self.sepShort)
        kwargs.setdefault("___kwdsep", self.sepLong)
        return System.build_cmd(name, *args, **kwargs)
    def call(self,name,*args,**kwargs):
        cmd = self.build_command(name,*args,**kwargs)
        # print("CALL:",cmd,os.getcwd(),cmd)
        return System._read(cmd)

    @staticmethod
    def _read(cmd):
        return os.popen(cmd).read()
    @staticmethod
    def build_cmd(name, *args, **kwargs):
        sep = kwargs.pop("___kwdsep", "=")
        sep2 = kwargs.pop("___kwdsep2", " ")
        # print(sep,sep2)
        def formatArg(argVal):
            fmt = "%s"
            isStr = isinstance(argVal, (bytes, six.string_types))
            shouldQuote = isStr and " " in argVal
            if shouldQuote:
                fmt = '"%s"'
            if isStr:
                argVal = argVal.replace('"','\\"')
            return fmt%argVal
        def parseKWD(kwdName, kwdVal):
            dashes="-" if len(kwdName) == 1 else "--"
            mysep = sep2 if len(kwdName) == 1 else sep
            kwdVal = formatArg(kwdVal)
            # print("K:",kwdName,kwdVal)
            return '{dashes}{kwdName}{sep}{kwdVal}'.format(dashes=dashes, kwdName=kwdName,
                                                       kwdVal=kwdVal,sep=mysep)

        return "{cmd} {args} {kwds}".format(
            cmd=name,
            args=" ".join(map(formatArg,args)),
            kwds=" ".join(parseKWD(k, v) for k, v in kwargs.items())
        )
    def __getattr__(self, item):
        class CMD:
            def __init__(self,system,name):
                self.name = name
                self.system = system
            def command(self,*args,**kwargs):
                # print("SELF:",args,kwargs)
                return self.system.build_command(self.name,*args,**kwargs)
            def __getattr__(self, item):
                return CMD(self.system,"%s %s"%(self.name,item))
            def __call__(self,*args,**kwargs):
                cmd = self.command(*args,**kwargs)
                # print("EXEC:",cmd)
                # print("CWD:",os.getcwd())
                # print("CALL:", cmd, os.getcwd(), cmd)
                result = System._read(cmd)
                return result
        return CMD(self,item)
