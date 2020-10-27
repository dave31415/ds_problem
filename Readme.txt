#The data science problem

requires numpy

To run

mkdir data
python simulate.py

Note that this will output a line like

Total amount: 39.71 million

That will also create a files called ledger.csv and ledger_corrupted.csv

To create a new package, delete the old tar file if it exists

rm data/package.tar

Check that the file TheProblem.docx which mentions the total agrees with
the amount above. If not (say you have changed parameters), update the
docx file. Save it. Save it as a pdf as well.

Commit and push those changes.

Copy the new ledger_corrupted.csv and TheProblem.pdf into the new package

cp data/ledger_corrupted.csv data/package
cp data/TheProblem.pdf data/package

Make a new tar file

cd data
tar cvf package.tar package
gzip package.tar

And then you can send the package.tar.gz file to candidates.

TODO : Find a way to tag the ledger.csv and ledger_corrupted.csv files so
that we can keep track of them.

To validate a submission

python validate.py path/to/submission/ledger_corrected.py

Also see David's solution here

https://github.com/dave31415/solution2
