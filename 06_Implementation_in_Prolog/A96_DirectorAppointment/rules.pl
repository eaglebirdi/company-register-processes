is_application_legal(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(D, deed),
  is_of_sort(S, ass),

  is_resolution_legal(R),
  is_deed_legal(D),
  is_assurance_legal(S),
  are_applicants_authorized(A),

  application_resolution(A, R),
  resolution_deed(R, D),
  application_assurance(A, S).

is_resolution_legal(R) :-
  is_of_sort(R, res),
  is_resolution_formally_legal(R),
  has_resolution_majority(R).

is_resolution_formally_legal(R) :-
  is_of_sort(R, res),
  (
    is_resolution_with_meeting_formally_legal(R);
    is_resolution_without_meeting_formally_legal(R)
  ).

is_resolution_with_meeting_formally_legal(R) :-
  is_of_sort(R, res),
  is_of_sort(M, meet),
  is_meeting_legal(M).

is_resolution_without_meeting_formally_legal(R) :-
  is_of_sort(R, res),
  \+ resolution_meeting(R, _),
  (
    do_all_shareholders_consent_to_the_determination(R);
    do_all_shareholders_consent_to_voting_in_writing(R)
  ).

is_meeting_legal(M) :-
  is_of_sort(M, meet),
  (
    is_personal_meeting_legal(M);
    is_teleconference_meeting_legal(M)
  ).

is_personal_meeting_legal(M) :-
  is_of_sort(M, meet),
  meeting_format(M, personal).

is_teleconference_meeting_legal(M) :-
  is_of_sort(M, meet),
  meeting_format(M, teleconference),
  do_all_shareholders_consent_to_teleconference_meeting(M).

do_all_shareholders_consent_to_teleconference_meeting(M) :-
  is_of_sort(M, meet),
  is_of_sort(R, res),
  is_of_sort(C, com),
  resolution_meeting(R, M),
  company_resolution(C, R),
  company_shareholderlist(C, ShList),
  do_all_shareholders_consent_to_teleconference_meeting(M, ShList).
do_all_shareholders_consent_to_teleconference_meeting(_, []).
do_all_shareholders_consent_to_teleconference_meeting(M, [Sh|Others]) :-
  is_of_sort(M, meet),
  is_of_sort(Sh, sh),
  does_shareholder_consent_to_teleconference_meeting(M, Sh),
  do_all_shareholders_consent_to_teleconference_meeting(M, Others).

do_all_shareholders_consent_to_the_determination(R) :-
  is_of_sort(R, res),
  is_of_sort(C, com),
  company_resolution(C, R),
  company_shareholderlist(C, ShList),
  do_all_shareholders_consent_to_the_determination(R, ShList).
do_all_shareholders_consent_to_the_determination(_, []).
do_all_shareholders_consent_to_the_determination(R, [Sh|Others]) :-
  is_of_sort(R, res),
  is_of_sort(Sh, sh),
  does_shareholder_consent_to_the_determination(R, Sh),
  do_all_shareholders_consent_to_the_determination(R, Others).

do_all_shareholders_consent_to_voting_in_writing(R) :-
  is_of_sort(R, res),
  is_of_sort(C, com),
  company_resolution(C, R),
  company_shareholderlist(C, ShList),
  do_all_shareholders_consent_to_voting_in_writing(R, ShList).
do_all_shareholders_consent_to_voting_in_writing(_, []).
do_all_shareholders_consent_to_voting_in_writing(R, [Sh|Others]) :-
  is_of_sort(R, res),
  is_of_sort(Sh, sh),
  does_shareholder_consent_to_voting_in_writing(R, Sh),
  do_all_shareholders_consent_to_voting_in_writing(R, Others).

has_resolution_majority(R) :-
  is_of_sort(R, res),
  (
    do_all_shareholders_consent_to_the_determination(R);
    is_resolution_passed_via_voting(R)
  ).

is_resolution_passed_via_voting(R) :-
  is_of_sort(R, res),
  is_of_sort(V, vot),
  is_of_sort(C, com),
  resolution_voting(R, V),
  company_resolution(C, R),
  company_majorityrequirement(C, MajReq),
  voting_yesratio(V, YesRatio),
  YesRatio > MajReq.

voting_yesratio(V, YesRatio) :-
  is_of_sort(V, vot),
  voting_yesvotes(V, YesVotes),
  voting_novotes(V, NoVotes),
  YesRatio is (YesVotes/(YesVotes+NoVotes)).

is_deed_legal(D) :-
  is_of_sort(D, deed),
  (
    deed_format(D, original);
    deed_format(D, certifiedcopy)
  ).

is_assurance_legal(S) :-
  is_of_sort(S, ass),
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(N, dir),
  application_assurance(A, S),
  application_resolution(A, R),
  resolution_newdirector(R, N),
  is_assurance_signed(S, N).

are_applicants_authorized(A) :-
  is_of_sort(A, app),
  (
    are_applicants_authorized_via_general_sole_representation_power(A);
    are_applicants_authorized_via_individual_sole_representation_power(A);
    are_applicants_authorized_via_general_modified_representation_power(A);
    are_applicants_authorized_via_individual_modified_representation_power(A);
    are_all_directors_present(A)
  ).

are_applicants_authorized_via_general_sole_representation_power(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  is_of_sort(D, dir),
  application_resolution(A, R),
  company_resolution(C, R),
  company_representationpower(C, sole),
  director_company(D, C),
  application_applicant(A, D),
  \+ director_representationpower(D, _).

are_applicants_authorized_via_individual_sole_representation_power(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  is_of_sort(D, dir),
  application_resolution(A, R),
  company_resolution(C, R),
  director_company(D, C),
  application_applicant(A, D),
  director_representationpower(D, sole).

are_applicants_authorized_via_general_modified_representation_power(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  is_of_sort(D1, dir),
  is_of_sort(D2, dir),
  application_resolution(A, R),
  company_resolution(C, R),
  company_representationpower(C, modified),
  director_company(D1, C),
  director_company(D2, C),
  application_applicant(A, D1),
  application_applicant(A, D2),
  \+ director_representationpower(D1, _),
  D1 \= D2.

are_applicants_authorized_via_individual_modified_representation_power(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  is_of_sort(D1, dir),
  is_of_sort(D2, dir),
  application_resolution(A, R),
  company_resolution(C, R),
  director_company(D1, C),
  director_company(D2, C),
  application_applicant(A, D1),
  application_applicant(A, D2),
  director_representationpower(D1, modified),
  D1 \= D2.

are_all_directors_present(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  application_resolution(A, R),
  company_resolution(C, R),
  company_directorlist(C, DirList),
  are_all_directors_present(A, DirList).
are_all_directors_present(_, []).
are_all_directors_present(A, [Dir|Others]) :-
  is_of_sort(A, app),
  is_of_sort(Dir, dir),
  application_applicant(A, Dir),
  are_all_directors_present(A, Others).

shareholder_company(Sh, C) :-
  is_of_sort(C, com),
  company_shareholderlist(C, ShList),
  member(Sh, ShList).
director_company(Dir, C) :-
  is_of_sort(C, com),
  company_directorlist(C, DirList),
  member(Dir, DirList).

