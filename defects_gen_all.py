# This python scripts generates a pkl file of the graph coverage representation

import os
import javalang
#from ast import nodes
from graphviz import Digraph
import json
import pickle
from tqdm import tqdm
import numpy as np
import json
#from run import *
#from stringfycode import stringfyRoot
from copy import deepcopy
import time
import io
import subprocess
import traceback
linenode = ['WhileStatement', 'IfStatement', 'ConstructorDeclaration', 'ThrowStatement', 'Statement_ter', 'BreakStatement_ter', 'ReturnStatement_ter', 'ContinueStatement', 'ContinueStatement_ter', 'LocalVariableDeclaration', 'control', 'BreakStatement', 'ContinueStatement', 'ReturnStatement', "parameters", 'StatementExpression', 'return_type']
class Node:
    def __init__(self, name, d):
        self.name = name
        self.id = d
        self.father = None
        self.child = []
        self.sibiling = None
        self.expanded = False
        self.fatherlistID = 0
        self.treestr = ""
        self.block = ""
        self.num = 0
        self.fname = ""
        self.position = None
        self.isunique = ''
        self.possibility = 0#max(min(np.random.normal(0.1, 0.08, 10)[0], 1), 0)
    def printTree(self, r):
      #print(r.name)
      s = r.name + "" + " "#print(r.name)
      if len(r.child) == 0:
        s += "^ "
        return s
      #r.child = sorted(r.child, key=lambda x:x.name)
      for c in r.child:
        s += self.printTree(c)
      s += "^ "#print(r.name + "^")
      return s
    def getNum(self):
        return len(self.getTreestr().strip().split())
    def getTreeProb(self, r):
      ans = [r.possibility]
      if len(r.child) == 0:
        return ans
      #r.child = sorted(r.child, key=lambda x:x.name)
      for c in r.child:
        ans += self.getTreeProb(c)
      return ans
    def getTreestr(self):
        if self.treestr == "":
            self.treestr = self.printTree(self)
            return self.treestr
        else:
            return self.treestr
    def printTreeWithVar(self, node, var):
        ans = ""
        if node.name in var:
            ans += var[node.name] + " "
        else:
            ans += node.name + " "
        for x in node.child:
            ans += self.printTreeWithVar(x, var)
        ans += '^ '  
        return ans
    def printTreeWithLine(self, node):
        ans = ""
        if node.position:
            ans += node.name + "-" + str(node.position.line)
        else:
            print(node.name)
            ans += node.name + "-"
        for x in node.child:
            ans += self.printTreeWithLine(x)
        ans += '^ '  
        return ans
    def printprob(self):
        ans = self.name + str(self.possibility) + ' '
        for x in self.child:
            ans += x.printprob()
        ans += '^ '
        return ans
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.name.lower() != other.name.lower():
            return False
        if len(self.child) != len(other.child):
            return False
        if True:#self.name == 'arguments' and (self.father.name == 'Or' or self.father.name == "And") :
            return self.getTreestr().strip() == other.getTreestr().strip() #and self.block == other.block
def getroottree(tokens, isex=False):
    root = Node(tokens[0][0], 0)
    currnode = root
    idx = 1
    for i, x in enumerate(tokens[1:]):
        if x != "^":
            if isinstance(x, tuple):
                #assert(0)
                nnode = Node(x[0], idx)
                nnode.position = x[1]
            else:
                nnode = Node(x, idx)
            nnode.father = currnode
            currnode.child.append(nnode)
            currnode = nnode
            idx += 1
        else:
            currnode = currnode.father
    return root
def generateAST(tree):
    sub = []
    if not tree:
        return ['None', '^']
    if isinstance(tree, str):
        tmpStr = tree
        tmpStr = tmpStr.replace(" ", "").replace(":", "")
        if "\t" in tmpStr or "'" in tmpStr or "\"" in tmpStr:
            tmpStr = "<string>"
        if len(tmpStr) == 0:
            tmpStr = "<empty>"
        if tmpStr[-1] == "^":
            tmpStr += "<>"
        sub.append(tmpStr)
        sub.append("^")
        return sub
    if isinstance(tree, list):
        if len(tree) == 0:
            sub.append("empty")
            sub.append("^")
        else:
            for ch in tree:
                subtree = generateAST(ch)
                sub.extend(subtree)
        return sub
    position = None
    if hasattr(tree, 'position'):
        #assert(0)
        position = tree.position
    curr = type(tree).__name__
    #print(curr)
    if True:
        if False:
            assert(0)#sub.append((str(getLiteral(tree.children)))
        else:
            sub.append((curr, position))
            try:
                for x in tree.attrs:
                    if x == "documentation":
                        continue
                    if not getattr(tree, x):
                        continue
                    '''if x == 'prefix_operators':
                        node = getattr(tree, x)
                        print(type(node))
                        print(len(node))
                        print(node[0])
                        assert(0)
                    if type(getattr(tree, x)).__name__ not in nodes:
                        print(type(getattr(tree, x)).__name__)
                        continue'''
                    sub.append(x)
                    node = getattr(tree, x)
                    if isinstance(node, list):
                        if len(node) == 0:
                            sub.append("empty")
                            sub.append("^")
                        else:
                            for ch in node:
                                subtree = generateAST(ch)
                                sub.extend(subtree)
                    elif isinstance(node, javalang.tree.Node):
                        subtree = generateAST(node)
                        sub.extend(subtree)
                    elif not node:
                        continue
                    elif isinstance(node, str):
                        tmpStr = node
                        tmpStr = tmpStr.replace(" ", "").replace(":", "")
                        if "\t" in tmpStr or "'" in tmpStr or "\"" in tmpStr:
                            tmpStr = "<string>"
                        if len(tmpStr) == 0:
                            tmpStr = "<empty>"
                        if tmpStr[-1] == "^":
                            tmpStr += "<>"
                        sub.append(tmpStr)
                        sub.append("^")
                    elif isinstance(node, set):
                        for ch in node:
                            subtree = generateAST(ch)
                            sub.extend(subtree)
                    elif isinstance(node, bool):
                        sub.append(str(node))
                        sub.append("^")
                    else:
                        print(type(node))
                        assert(0)
                    sub.append("^")
            except AttributeError:
                assert(0)
                pass
        sub.append('^')
        return sub
    else:
        print(curr)
    return sub
'''def setProb(root, subroot, prob):
    root.possibility = max(min(max(root.possibility, prob), 0.98), 0.01)
    index = 0
    assert(len(subroot.child) <= len(root.child))
    #print(len(subroot.child), len(root.child))
    for x in subroot.child:
        while root.child[index].name != x.name:
            #print(root.child[index].name, x.name)
            index += 1
        setProb(root.child[index], x, prob)
        index += 1'''
def getMethodByline(filename, lineid):
    lines1 = open(filename, "r", encoding='iso-8859-1').read().strip()
    tokens = javalang.tokenizer.tokenize(lines1)
    parser = javalang.parser.Parser(tokens)
    tree = parser.parse()
    tmproot = getroottree(generateAST(tree))
    #print(tmproot.name)
    #print(tmproot.printTreeWithLine(tmproot))     
    mnode = None
    index = 0
    while mnode is None and index < len(lineid):
        line = int(lineid[index].split(":")[1])
        currroot = getNodeById(tmproot, line)
        lnode, mnode = getSubroot(currroot)
        index += 1
    return mnode
def getNodeById(root, line):
    if root.position:
        #print(line, root.position.line)
        if root.position.line == line and root.name != 'IfStatement' and root.name != 'ForStatement' and root.name != 'WhileStatement' and root.name != 'SwitchStatement':
            return root
    for x in root.child:
        t = getNodeById(x, line)
        if t:
            return t
    return None
def getSubroot(treeroot):
    currnode = treeroot
    lnode = None
    mnode = None
    while currnode:
        if currnode.name in linenode:
            lnode = currnode
            break
        currnode = currnode.father
    currnode = treeroot
    while currnode:
        if currnode.name == 'MethodDeclaration' or currnode.name == 'ConstructorDeclaration':
            mnode = currnode
            break
        currnode = currnode.father
    return lnode, mnode
def getLnode(treeroot):
    currnode = treeroot
    lnode = None
    while currnode:
        #print(currnode.name)
        if currnode.name in linenode:
            lnode = currnode
            break
        currnode = currnode.father
    return lnode
def getMask(mnode, masked):
    if mnode.position is not None:
        if mnode.position.line not in masked:
            masked[mnode.position.line] = mnode
    for x in mnode.child:
        getMask(x, masked)
    return
def simpleGraph(node):
    x = node
    if x.isunique == "" and not (x.father == 'IfStatement' and x.name != 'condition'):
        tnode = x.father
        c = []
        for ch in tnode.child:
            if ch == x:
                #assert(0)
                c.extend(x.child)
            else:
                c.append(ch)
        tnode.child = c
        for s in x.child:
            s.father = tnode
    for s in x.child:
        simpleGraph(s)
    return
def getEdge(node, edge, liness):
    if node.isunique != 'method':
        for x in node.child:
            if x.isunique in liness and node.isunique in liness:
                edge.append((liness[x.isunique], liness[node.isunique]))
            #edge.append((liness[node.isunique], liness[x.isunique]))
    for x in node.child:
        getEdge(x, edge, liness)
def conEdge(mnode, root):
    ans = []
    if root != mnode:
        ans.append(root.isunique)
    for x in root.child:
        ans.extend(conEdge(mnode, x))
    return ans
# prlist = ['Closure']#['Chart', 'Closure', 'Lang', 'Math', 'Mockito', 'Time']
prlist = ['Lang']
# ids = [list(range(1, 134))]#[range(1, 27), list(range(1, 63)) + list(range(64, 93)) + list(range(94, 177)), list(range(3, 66)) + [1], range(1, 107), range(1, 39), list(range(1, 21)) + list(range(22, 28))]
idss = []
for jj in range(2,66):
    if jj != 23 and jj != 56 and jj !=25:
        idss.append(jj)
ids = [[1]+ idss]
#ids = [[8] + [3]]
#ids = [[1, 4, 7, 8, 9, 11, 12, 13, 15, 19, 20, 24, 26]]
#ids = [[20, 24, 26]]
#ids = [23, 56]
import sys
# ids = [[int(sys.argv[1])]]
# prlist = [sys.argv[2]]
err = []

for i, xss in enumerate(prlist):
    res = []
    for idx in ids[i]:
        if idx == -1:
            continue
        try:
            timecurr = time.time()
            x = xss
            '''locationdir = 'location/ochiai/%s/%d.txt' % (x.lower(), idx)
            if not os.path.exists(locationdir):
                continue'''
            #print(open(locationdir, 'r').read())
            if xss == 'Closure':
                if not os.path.exists("0.2/%d.txt"%idx):
                    continue
                ms = open("0.2/%d.txt"%idx, "r").readlines()
                avaiableM = []
                for y in ms:
                    avaiableM.append(y.strip())
            # if xss == 'Lang' and idx == 2:
            #     os.system("cp -r /data/zqh/FLocalization/1.2-Lang-2 buggy2")
            # else:
            #     os.system('defects4j checkout -p %s -v %db -w buggy%d'%(x, idx, idx))#os.system('defects4j')
            #os.system('defects4j checkout -p %s -v %db -w buggy2'%(x, idx))#os.system('defects4j')
            #os.system('defects4j checkout -p %s -v %df -w fixed'%(x, idx))
            #lines = open(locationdir, 'r').readlines()
            #location = []
            #locationdict = {}
            #for loc in lines:
            #    lst = loc.strip().split(',')
                #print(lst)
            #    prob = eval(lst[1])
            #    classname, lineid= lst[0].split('#')
            #    location.append((classname, prob, eval(lineid)))
            #    locationdict[lst[0]] = (classname, prob, eval(lineid))         
            dirs = os.popen('defects4j export -p dir.src.classes -w defect/Lang-%db'%idx).readlines()[-1]
            #correctpath = os.popen('defects4j export -p classes.modified -w fixed').readlines()[-1]
            #fpath = "fixed/%s/%s.java"%(dirs, correctpath.replace('.', '/'))
            #fpathx = "buggy/%s/%s.java"%(dirs, correctpath.replace('.', '/'))
            print('*************')
            for methodnamess in [1]:
                tmp = {}
                patchdict = {}
                testcase = {}
                allmethods = {}
                line2method = {}
                tests = {}
                liness = {}
                ltype = {}
                # if not os.path.exists('data_copy/FailingTests/%s/%s.txt' % (xss, idx)):
                #     os.system('gzip -d %s' % 'data_copy/FailingTests/%s/%s.txt' % (xss, idx))
                # if not os.path.exists('data_copy/AllMethods/%s/%s.txt' % (xss, idx)):
                #     os.system('gzip -d %s' % 'data_copy/AllMethods/%s/%s.txt' % (xss, idx))
                f = open('defect/FailedTests/%s.txt' % (idx))
                methods = open('defect/AllMethods/%s.txt' % (idx)).readlines()
                bmethods = []
                for x in methods:
                    lst = x.strip().split(":")
                    fname = lst[0] + ":" + lst[2] # Package : Line no
                    methodname = lst[0] + ":" + lst[1]
                    if  xss == "Closure" and methodname not in avaiableM:
                        continue
                    #print('f', fname)
                    line2method[fname] = methodname
                buggypackage = {}
                for x in f:
                    if x.strip().replace("::", ".") not in tests:
                        #print(x.strip().replace("::", "."))
                        tests[x.strip().replace("::", ".")] = len(tests)#tests.append(x.strip().replace("::", "."))
                        name = ".".join(x.split("::")[0].split("."))
                        buggypackage[name] = 1
                #print('----', tests)
                #failline = {}
                # if not os.path.exists('defect/LineCoverage/%s.txt' % (xss, idx)):
                #     os.system('gzip -d %s' % 'data_copy/LineCoverage/%s/%s.txt.gz' % (xss, idx))
                f = open('defect/CoverageFiles/%s.txt' % (idx), 'r')
                lines = f.readlines()
                methods = {}
                v = {}
                edge2 = []
                edge = []
                edge3 = []
                method2line = {}
                for x in lines:
                    #print(x)
                    lst = x.strip().split()
                    #print('err', lst[0])
                    if '(' in lst[0]:
                        name = lst[0][:lst[0].index('(')]
                    else:
                        name = lst[0]
                    #print(name)
                    if name not in tests:
                        continue
                    #print('p', name)
                    for x in lst[1:]:
                        #if x not in failline:
                        #    failline[x] = len(failline)
                        lsts = x.strip().split(":")
                        fname = lsts[0] + ":" + lsts[2]
                        if fname not in line2method:
                            continue
                        if fname not in liness:
                            #print(dirs, fname)
                            liness[fname] = len(liness)
                            '''f = open('buggy/' + dirs + '/' + lsts[0].split('$')[0].replace('.', '/') + '.java')
                            ls = f.readlines()
                            #print(ls[int(lsts[2]) - 1])
                            if 'if' in ls[int(lsts[2]) - 1]:
                                ltype[liness[fname]] = 'if'
                            elif 'return' in ls[int(lsts[2]) - 1]:
                                ltype[liness[fname]] = 'return'
                            elif 'break' in ls[int(lsts[2]) - 1]:
                                ltype[liness[fname]] = 'break'
                            elif 'continue' in ls[int(lsts[2]) - 1]:
                                ltype[liness[fname]] = 'continue'
                            elif 'for' in ls[int(lsts[2]) - 1]:
                                ltype[liness[fname]] = 'for'
                            else:
                                ltype[liness[fname]] = 'stat'''
                            #assert(0)
                        methodname = line2method[fname]#lst[0].split('$')[0] + lst[1]
                        #print(methodname, 'pp')
                        #if tlst[1] == '<init>':
                        #    continue
                        if methodname not in methods:
                            #print('ppp', methodname)
                            methods[methodname] = len(methods)
                        '''if name not in v:
                            v[name] = lst[0]
                        else:
                            print(lst[0], v[name])
                            assert(0)
                        if (liness[fname], tests[name]) in edge2:
                            print((liness[fname], tests[name]))
                            assert(0)'''
                        edge2.append((liness[fname], tests[name]))
                        method2line.setdefault(methodname, []).append(fname)
                        #edge.append((methods[methodname], liness[fname]))
                buggymethods = open('defect/BugMethod/Lang/%s.txt' % (idx)).readlines() 
                for x in buggymethods:
                    fname = x.strip()[6:]
                    x = fname
                    lst = x.strip().split(":")
                    #print(lst)
                    #fname = lst[0].split('$')[0] + ":" + lst[2]
                    fname = lst[0] + ":" + lst[1]
                    # print('1111111',fname)
                    # print(methods)
                    #print('p', fname)
                    if fname not in methods:
                        #for x in line2method:
                        #    if line2method[x] == fname:
                        #        assert(0)
                        continue
                    bmethods.append(methods[fname])
                # print(bmethods,"$$$$$$$$$$$$$")
                if len(bmethods) == 0:
                    assert(0)
                correctnum = {}
                rrdic = {}
                for x in line2method:
                    rrdic.setdefault(line2method[x], []).append(x)
                for xs in liness:
                    edge.append((methods[line2method[xs]], liness[xs]))
                for x in tqdm(methods):
                    print(x)
                    fpath = 'defect/Lang-%db/'%idx + dirs + '/' + x.split(':')[0].split('$')[0].replace('.', '/') + ".java"
                    #fpath = 'buggy/' + dirs + '/' + x.split(':')[0].replace('.', '/') + ".java"
                    lineid = list(set(method2line[x]))
                    mnode = getMethodByline(fpath, lineid)
                    if mnode is None:
                        continue
                    #masked = {}
                    #getMask(mnode, masked)
                    for xs in lineid:
                        #print(xs)
                        tnode = getNodeById(mnode, int(xs.split(":")[1]))
                        #if tnode is None:
                        #    continue
                        #print(xs, tnode.printTree(tnode))
                        tnode = getLnode(tnode)
                        if tnode is None:
                            print(xs)
                            continue
                        ltype[liness[xs]] = tnode.name
                        #print(tnode.getTreestr())
                        tnode.isunique = xs
                    mnode.isunique = 'method'
                    #print(mnode.printTree(mnode))
                    simpleGraph(mnode)
                    #controlGraph(root)
                    print(mnode.printTree(mnode))
                    getEdge(mnode, edge3, liness)
                    #print(mnode.printTree(mnode))
                    #print(edge)
                    ans = conEdge(mnode, mnode)
                    for xs in ans:
                        #print(xs.name)
                        edge.append((methods[x], liness[xs]))
                    for j in range(len(mnode.child)):
                        if j == 0:
                            continue
                        edge3.append((liness[mnode.child[j].isunique], liness[mnode.child[j - 1].isunique]))
                #print(edge3)
                #print(testcase)
                #if not os.path.exists('data_copy/BugMethod/%s/%s.txt' % (xss, idx)):
                #    os.system('gzip -d %s' % 'data_copy/BugMethod/%s/%s.txt.gz' % (xss, idx))
                #f = open('data_copy/BugMethod/%s/%s.txt' % (xss, idx), 'r')
                #lines = f.readlines()
                #ms = []
                lcorrect = {}
                rtest = {}
                edge10 = []
                for x in tqdm(lines):
                    lst = x.strip().split()
                    if '(' in lst[0]:
                        name = lst[0][:lst[0].index('(')]
                    else:
                        name = lst[0]
                    if name in tests:
                        continue
                    cnum = 0
                    if xss == 'Closure' and len(rtest) >= 300:
                        break
                    for x in lst[1:]:
                        lst2 = x.strip().split(":")
                        fname = lst2[0] + ":" + lst2[2]
                        if fname not in line2method:
                            continue
                        if fname in liness:
                            if fname not in lcorrect:
                                lcorrect[liness[fname]] = 0
                            lcorrect[liness[fname]] += 1
                            if name not in rtest:
                                rtest[name] = len(rtest)
                            edge10.append((liness[fname], rtest[name]))
                            cnum += 1
                        methodname = line2method[fname]#lst[0].split('$')[0] + lst[1]
                        #print(methodname)
                        if methodname in methods:
                            if methods[methodname] in correctnum:
                                correctnum[methods[methodname]] += 1
                            else:
                                correctnum[methods[methodname]] = 0#methods[methodname] = len(methods)
                    '''if cnum != 0:
                        if name not in rtest:
                            rtest[name] = len(rtest)
                        for x in lst[1:]:
                            lst2 = x.strip().split(":")
                            fname = lst2[0] + ":" + lst2[2]
                            if fname not in line2method:
                                continue
                            if fname in liness:
                                edge10.append((liness[fname], rtest[name]))'''
                # blines = open('data_copy/BugLines/%s/%s' % (xss, idx)).readlines() 
                # bl = []
                # for x in blines:
                #    x = x.strip().split("||")[0]
                #    ls = x.strip().split(":")#print(x.strip())
                #    x = ".".join(ls[0].split(".")[:-1]) + ":" + ls[1]
                #    if x not in liness:
                #        continue
                #    bl.append(liness[x])
                
                    
                
                
                tmp['ftest'] = tests
                tmp['edge'] = set(edge2)
                tmp['edge2'] = set(edge)
                tmp['edge3'] = set(edge3)
                # tmp['edge4'] = set(edge4)
                # tmp['edge5'] = set(edge5)
                # tmp['edge6'] = set(edge6)
                tmp['edge10'] = set(edge10)
                print(len(tmp['edge10']), len(liness), len(tmp['edge']), len(tmp['edge10']), len(tmp['edge2']), len(tmp['edge3']))
                # tmp['edge6'] = set(edge6)
                # tmp['edge7'] = set(edge7)
                # tmp['edge8'] = set(edge8)
                tmp['proj'] = xss + str(idx)
                tmp['correctnum'] = correctnum
                tmp['ans'] = bmethods
                tmp['methods'] = methods
                tmp['lines'] = liness
                tmp['ltype'] = ltype
                # tmp['lans'] = bl
                tmp['lcorrectnum'] = lcorrect
                # tmp['mutation'] = mutation
                # tmp['linem'] = linem
                # tmp['st'] = stll
                tmp['rtest'] = rtest
                print(len(rtest))
                #assert(0)
                res.append(tmp)
                #open('time%s_%s'%(xss, idx).write(time.time() - timecurr))
        except:
            print(traceback.print_exc(), xss, str(idx))
            err.append(xss + str(idx))
            assert(0)
            continue
        #os.system('rm -rf buggy%d'%(idx))
        open('PklFiles/%s%d.pkl' % (xss, idx), 'wb').write(pickle.dumps(res))#res.append(tmp)
print(err)
        
