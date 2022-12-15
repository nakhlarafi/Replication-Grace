# Maps all the coverage lines generated from the Gzoltar into one coverage file.

ids = list(range(21, 42))
#ids = [8]
# ids.append(1)
#print(ids)

for n in ids:
    spectra = open('defect/Lang-'+str(n)+'b/sfl/txt/spectra.csv','r').readlines()[1:]
    tests = open('defect/Lang-'+str(n)+'b/sfl/txt/tests.csv','r').readlines()[1:]
    matrix_line = open('defect/Lang-'+str(n)+'b/sfl/txt/matrix.txt').readlines()
    size = len(spectra)

    print("Lang ",n,"----->")
    for i in range(1,len(tests)):
        test_str = tests[i].split(',')[0].replace('#','.').rstrip()
        test_pckg = tests[i].split(',')[0].split('#')[0]
        full_test_str = test_str + '(' + test_pckg + ')' + " "
        linetowrite = full_test_str
    
        m_arr = matrix_line[i].split()[:size]
        for j in range(size):
            if m_arr[j] == '1':
                ss = spectra[j].replace('$','.',1)
                sl = ss.replace(ss[ss.index('('):ss.index(')')+1],'').rstrip() + ' '
                
                linetowrite = linetowrite + sl.replace('#',':')
        with open('defect/CoverageFiles/'+str(n)+'.txt', 'a') as fr:
            fr.write(linetowrite+'\n')
        #     #print(line_str)
    print('Done!')
