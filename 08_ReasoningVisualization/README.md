# Reasoning Visualization

## Technical Requirements
* Ubuntu 22.04 LTS
* OpenJDK 19
* Python 3.10
* several Python packages (installable via pip)
* TPTP prover tools (see /05\_Implementation\_in\_TPTP)

## How to try it out
You can try out the reasoning visualization by calling test.py with appropriate command line arguments. See below for exemplary command lines.
In order to reason on your individual case, modify the example.json file.

## Exemplary command line invocations of test.py

### For cvc5
```
python3 test.py --process A96 --prover cvc5 --reassert_predicate_completion ./ExampleCases/A96_DirectorAppointment/example.json
python3 test.py --process A115 --prover cvc5 --reassert_predicate_completion ./ExampleCases/A115_CompanyDissolution/example.json
python3 test.py --process A108 --prover cvc5 --reassert_predicate_completion ./ExampleCases/A108_CapitalIncrease/example.json
```

### For Vampire
```
python3 test.py --process A96 --prover vampire --precompute_arithmetics ./ExampleCases/A96_DirectorAppointment/example.json
python3 test.py --process A115 --prover vampire --precompute_arithmetics ./ExampleCases/A115_CompanyDissolution/example.json
python3 test.py --process A108 --prover vampire --precompute_arithmetics ./ExampleCases/A108_CapitalIncrease/example.json
```

### For iProver
```
python3 test.py --process A96 --prover iprover --precompute_arithmetics --single_file_axioms ./ExampleCases/A96_DirectorAppointment/example.json
python3 test.py --process A115 --prover iprover --precompute_arithmetics --single_file_axioms ./ExampleCases/A115_CompanyDissolution/example.json
python3 test.py --process A108 --prover iprover --precompute_arithmetics --single_file_axioms ./ExampleCases/A108_CapitalIncrease/example.json
```

