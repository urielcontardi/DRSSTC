"""Small lossless-enough reader/writer for KiCad S expressions (stdlib only)."""
import re,json
class Atom(str): pass
def parse(s):
    tokens=re.findall(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',s)
    stack=[]; out=None
    for t in tokens:
        if t=='(':
            v=[]
            if stack: stack[-1].append(v)
            stack.append(v)
        elif t==')': out=stack.pop()
        else: stack[-1].append(json.loads(t) if t.startswith('"') else Atom(t))
    return out
def dump(v,depth=0):
    if isinstance(v,Atom):return str(v)
    if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
    if not isinstance(v,list):return str(v)
    if not any(isinstance(x,list) for x in v):return '('+' '.join(dump(x) for x in v)+')'
    head=[];tail=[]
    for x in v:
        (tail if isinstance(x,list) or tail else head).append(x)
    return '('+' '.join(dump(x) for x in head)+'\n'+'\n'.join('  '*(depth+1)+dump(x,depth+1) for x in tail)+'\n'+'  '*depth+')'
def children(v,k):return [x for x in v if isinstance(x,list) and x and x[0]==k]
def child(v,k):return next(iter(children(v,k)),None)
def prop(v,k):return next((x for x in children(v,'property') if x[1]==k),None)
