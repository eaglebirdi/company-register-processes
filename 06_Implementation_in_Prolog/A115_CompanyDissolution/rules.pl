is_application_legal(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  is_of_sort(D, deed),

  is_resolution_legal(R),
  is_liquidator_appointment_deed_legal(D),
  are_all_liquidator_assurances_signed(A),
  are_applicants_authorized(A),

  application_resolution(A, R),
  application_deed(A, D),
  company_resolution(C, R),
  company_liquidatorlist(C, _).

is_resolution_legal(R) :-
  is_of_sort(R, res),
  is_resolution_formally_legal(R),
  has_resolution_qualified_majority(R),
  is_resolution_notarized_if_AoA_are_amended(R).

is_resolution_formally_legal(R) :-
  is_of_sort(R, res),
  (
    is_resolution_with_meeting_formally_legal(R);
    is_resolution_without_meeting_formally_legal(R)
  ).

is_resolution_with_meeting_formally_legal(R) :-
  is_of_sort(R, res),
  is_of_sort(M, meet),
  resolution_meeting(R, M),
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

has_resolution_qualified_majority(R) :-
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
  voting_yesratio(V, YesRatio),
  YesRatio > 0.75.

voting_yesratio(V, YesRatio) :-
  is_of_sort(V, vot),
  voting_yesvotes(V, YesVotes),
  voting_novotes(V, NoVotes),
  YesRatio is (YesVotes/(YesVotes+NoVotes)).

is_resolution_notarized_if_AoA_are_amended(R) :-
  is_of_sort(R, res),
  (
    \+ are_AoA_amended(R);
    is_resolution_notarized(R)
  ).

company_liquidatorlist(C, LiqList) :-
  is_of_sort(C, com),
  company_AoA_liquidatorlist(C, LiqList).
company_liquidatorlist(C, LiqList) :-
  is_of_sort(C, com),
  is_of_sort(R, res),
  company_resolution(C, R),
  resolution_liquidatorlist(R, LiqList).
company_liquidatorlist(C, LiqList) :-
  is_of_sort(C, com),
  is_of_sort(R, res),
  company_resolution(C, R),
  \+ company_AoA_liquidatorlist(C, _),
  \+ resolution_liquidatorlist(R, _),
  company_directorlist(C, DirList),
  LiqList = DirList.

application_responsibleapplicantlist(A, ResList) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  application_resolution(A, R),
  company_resolution(C, R),
  are_AoA_amended(R),
  company_directorlist(C, DirList),
  ResList = DirList.
application_responsibleapplicantlist(A, ResList) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  application_resolution(A, R),
  company_resolution(C, R),
  \+ are_AoA_amended(R),
  company_liquidatorlist(C, LiqList),
  ResList = LiqList.

is_liquidator_appointment_deed_legal(D) :-
  is_of_sort(D, deed),
  (
    deed_format(D, original);
    deed_format(D, certifiedcopy)
  ).

are_all_liquidator_assurances_signed(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(S, ass),
  is_of_sort(C, com),
  application_resolution(A, R),
  application_assurance(A, S),
  company_resolution(C, R),
  company_liquidatorlist(C, LiqList),
  have_all_liquidators_signed_the_assurance(S, LiqList).
have_all_liquidators_signed_the_assurance(_, []).
have_all_liquidators_signed_the_assurance(S, [Liq|Others]) :-
  is_of_sort(S, ass),
  is_of_sort(Liq, dir),
  is_of_sort(P, pers),
  director_person(Liq, P),
  assurance_signer(S, P),
  have_all_liquidators_signed_the_assurance(S, Others).

are_applicants_authorized(A) :-
  is_of_sort(A, app),
  (
    are_applicants_authorized_via_general_sole_representation_power(A);
    are_applicants_authorized_via_individual_sole_representation_power(A);
    are_applicants_authorized_via_general_modified_representation_power(A);
    are_applicants_authorized_via_individual_modified_representation_power(A);
    are_all_responsibleapplicants_present(A)
  ).

are_applicants_authorized_via_general_sole_representation_power(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  is_of_sort(D, dir),
  is_of_sort(P, pers),
  application_resolution(A, R),
  company_resolution(C, R),
  company_representationpower(C, sole),
  application_responsibleapplicant(A, D),
  director_person(D, P),
  application_applicant(A, P),
  \+ director_representationpower(D, _).

are_applicants_authorized_via_individual_sole_representation_power(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  is_of_sort(D, dir),
  is_of_sort(P, pers),
  application_resolution(A, R),
  company_resolution(C, R),
  application_responsibleapplicant(A, D),
  director_person(D, P),
  application_applicant(A, P),
  director_representationpower(D, sole).

are_applicants_authorized_via_general_modified_representation_power(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  is_of_sort(D1, dir),
  is_of_sort(D2, dir),
  is_of_sort(P1, pers),
  is_of_sort(P2, pers),
  application_resolution(A, R),
  company_resolution(C, R),
  company_representationpower(C, modified),
  application_responsibleapplicant(A, D1),
  application_responsibleapplicant(A, D2),
  director_person(D1, P1),
  director_person(D2, P2),
  application_applicant(A, P1),
  application_applicant(A, P2),
  \+ director_representationpower(D1, _),
  P1 \= P2.

are_applicants_authorized_via_individual_modified_representation_power(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  is_of_sort(D1, dir),
  is_of_sort(D2, dir),
  is_of_sort(P1, pers),
  is_of_sort(P2, pers),
  application_resolution(A, R),
  company_resolution(C, R),
  application_responsibleapplicant(A, D1),
  application_responsibleapplicant(A, D2),
  director_person(D1, P1),
  director_person(D2, P2),
  application_applicant(A, P1),
  application_applicant(A, P2),
  director_representationpower(D1, modified),
  P1 \= P2.

are_all_responsibleapplicants_present(A) :-
  is_of_sort(A, app),
  is_of_sort(R, res),
  is_of_sort(C, com),
  application_resolution(A, R),
  company_resolution(C, R),
  application_responsibleapplicantlist(A, ResList),
  are_all_responsibleapplicants_present(A, ResList).
are_all_responsibleapplicants_present(_, []).
are_all_responsibleapplicants_present(A, [D|Others]) :-
  is_of_sort(A, app),
  is_of_sort(D, dir),
  is_of_sort(P, pers),
  director_person(D, P),
  application_applicant(A, P),
  are_all_responsibleapplicants_present(A, Others).

are_AoA_amended(R) :-
  is_of_sort(R, res),
  is_of_sort(C, com),
  company_resolution(C, R),
  has_company_expiration_date(C).


shareholder_company(Sh, C) :-
  is_of_sort(C, com),
  company_shareholderlist(C, ShList),
  member(Sh, ShList).
director_company(Dir, C) :-
  is_of_sort(C, com),
  company_directorlist(C, DirList),
  member(Dir, DirList).
liquidator_company(Liq, C) :-
  is_of_sort(C, com),
  company_liquidatorlist(C, LiqList),
  member(Liq, LiqList).
application_responsibleapplicant(A, RA) :-
  is_of_sort(A, app),
  is_of_sort(RA, dir),
  application_responsibleapplicantlist(A, RAList),
  member(RA, RAList).

