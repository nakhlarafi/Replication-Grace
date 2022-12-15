# Parses all the methods from the project files with their corresponding lines.

import xml.etree.ElementTree as ET
import os

ids = list(range(1, 66))

for n in ids:
    #defect/Lang-3b/coverage.xml
    
    mytree = ET.parse("defect/Lang-"+str(n)+"b/coverage.xml")
    myroot = mytree.getroot()

    # pckg_name = (myroot[1][0][0][0].attrib['name'])
    packages = myroot[1]
    for i in packages:
        classes = i[0]
        for c in classes:
            qualified_name = c.attrib['name']
            methods = c[0]
            for method in methods:
                lines = method[0]
                for line in lines:
                    with open('defect/AllMethods/'+str(n)+'.txt', 'a') as f:
                        cov = qualified_name + ':' + method.attrib['name'] + method.attrib['signature'] + ':' + line.attrib['number'] + '\n'
                        f.write(cov)

