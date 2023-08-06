def list_to_re(L):
    return "|".join(sorted(L,reverse=True,key=len))
def pyversion_to_re(s):
    if not s or s.lower() == "any":
        return "[^_]*[^-]*(?=-)"

    return "(?:py2\\.py3|%s).*(?=-)"%(s,)
def os_to_re(s):
    x={
        "win":"win.*(?=\\.)",
        "linux":"[A-Za-z0-9]*linux.*(?=\\.)",
        "darwin":"macosx.*(?=\\.)",
        "win32":"win32|win.*x86(_64).*(?=\\.)",
        "win64":"win.*(?:amd|x)(?:86_)?64.*(?=\\.)",
        "darwin32":"macosx.*x86(?:_64)?.*(?=\\.)",
        "darwin64":"macosx.*x(?:86_)?64).*(?=\\.)",
        "linux32":"[A-Za-z0-9]*linux.*x86(?:_64)?.*(?=\\.)",
        "linux64":"[A-Za-z0-9]*linux.*x(?:86_)?64.*(?=\\.)",
        "any":".*(?=\\.)"
    }
    if not s:
        s = "any"
    if s.lower() in x:
        return x[s]+"|any"
    else:
        return s.replace("_",".*")+".*(?=\\.)|any"


