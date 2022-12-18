# Replication: Grace

1. Run `defects_gen.sh` and `gzoltar_test.sh` for checking out all the buggy version of Lang and run Gzoltar on them for generating fault localization data.
2. Run `run_coverage_gzoltar.sh` for generating the cobertura XML data.
3. Run `fail_test_gen.py` for parsing the failed tests from the text files.
4. Run `coverage_gen.py` for getting the full coverage data.
5. Finally run `defects_gen_all.py` for generating the graph based coverage representation. 

All the generated files can be found here: https://drive.google.com/drive/folders/1n1Hd2x-hVU8MRaeuVtkir9hri0BlnoJL?usp=sharing