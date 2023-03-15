company_majorityrequirement(C, MajReq) :-
  is_of_sort(C, com),
  company_majorityrequirement_AoA(C, MajReq).
company_majorityrequirement(C, MajReq) :-
  is_of_sort(C, com),
  \+ company_majorityrequirement(C, _),
  MajReq is 0.5.

