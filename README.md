# ds_problem
Data science problem: Corrupted Ledger
--------------------

To install:

source install.sh

This will leave you in the virtual environment. If you open a new shell
you will need to do:

source venv/bin/activate

To generate the simulated legder and corrupted ledger:

python simulate.py

To check any corrected ledger file against the original ledger:

python validate.py path_to_your_corrected_ledger_file score

This will print out the validation info such as number and percent of lines
that are correct and the amount recovered. The percent recovered is the thing 
we are  trying to optimize for.

You can only do that if you actually have the ledger file. An applicant taking
this coding test can do this instead:

python validate.py path_to_your_corrected_ledger_file

This will check that the file has the right format but not actually check
how correct it is. File must have the same number of lines as original ledger 
and the same three fields and they must sum up to the same amount. Only the 
assignment of the numbers can be different.
