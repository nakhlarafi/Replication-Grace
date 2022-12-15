# This python script parses all the failed tests file into a smaller format 

import os

ids = list(range(1, 66))
# ids.append(1)

for n in ids:
    #defect/Lang-3b/coverage.xml defect/Lang-3b/failing_tests

    fail_test_file = open('defect/Lang-'+str(n)+'b/failing_tests').readlines()
    s = ''
    for i in fail_test_file:
        if '---' in i:
            s = i.split()[1] + '\n'
            with open('defect/FailedTests/'+str(n)+'.txt', 'a') as fr:
                fr.write(s)