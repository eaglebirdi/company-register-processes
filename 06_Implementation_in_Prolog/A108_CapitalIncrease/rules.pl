is_application_legal(A) :-
  is_of_sort(A, app),
  is_of_sort(AA, amaoa),
  is_of_sort(CIR, ci_res),
  is_of_sort(S, ass),

  contains_AoA_full_text(A),
  are_matches_notarily_certified(A),
  is_capital_increase_resolution_legal(CIR),
  are_permit_resolution_requirements_fulfilled(A),
  is_list_of_subscribers_attached(A),
  are_subscriber_declarations_legal(A),
  has_increased_capital_been_covered(A),
  is_assurance_signed(S),
  is_amended_AoA_plausible(AA),
  do_all_directors_perform_the_application(A),

  application_amendedAoA(A, AA),
  application_capitalincreaseresolution(A, CIR),
  application_assurance(A, S).


is_capital_increase_resolution_legal(CIR) :-
  is_of_sort(CIR, ci_res),
  is_capital_increase_resolution_formally_legal(CIR),
  has_capital_increase_resolution_qualified_majority(CIR),
  is_capitalincreaseresolution_notarized(CIR).

is_capital_increase_resolution_formally_legal(CIR) :-
  is_of_sort(CIR, ci_res),
  (
    is_capital_increase_resolution_with_meeting_formally_legal(CIR);
    is_capital_increase_resolution_without_meeting_formally_legal(CIR)
  ).

is_capital_increase_resolution_with_meeting_formally_legal(CIR) :-
  is_of_sort(CIR, ci_res),
  is_of_sort(M, meet),
  capitalincreaseresolution_meeting(CIR, M),
  is_meeting_legal(M).

is_capital_increase_resolution_without_meeting_formally_legal(CIR) :-
  is_of_sort(CIR, ci_res),
  \+ capitalincreaseresolution_meeting(CIR, _),
  (
    do_all_shareholders_consent_to_the_determination_ci(CIR);
    do_all_shareholders_consent_to_voting_in_writing_ci(CIR)
  ).

do_all_shareholders_consent_to_the_determination_ci(CIR) :-
  is_of_sort(CIR, ci_res),
  is_of_sort(C, com),
  company_capitalincreaseresolution(C, CIR),
  company_shareholderlist(C, ShList),
  do_all_shareholders_consent_to_the_determination_ci(CIR, ShList).
do_all_shareholders_consent_to_the_determination_ci(_, []).
do_all_shareholders_consent_to_the_determination_ci(CIR, [Sh|Others]) :-
  is_of_sort(CIR, ci_res),
  is_of_sort(Sh, sh),
  does_shareholder_consent_to_the_determination_ci(CIR, Sh),
  do_all_shareholders_consent_to_the_determination_ci(CIR, Others).

do_all_shareholders_consent_to_voting_in_writing_ci(CIR) :-
  is_of_sort(CIR, ci_res),
  is_of_sort(C, com),
  company_capitalincreaseresolution(C, CIR),
  company_shareholderlist(C, ShList),
  do_all_shareholders_consent_to_voting_in_writing_ci(CIR, ShList).
do_all_shareholders_consent_to_voting_in_writing_ci(_, []).
do_all_shareholders_consent_to_voting_in_writing_ci(CIR, [Sh|Others]) :-
  is_of_sort(CIR, ci_res),
  is_of_sort(Sh, sh),
  does_shareholder_consent_to_voting_in_writing_ci(CIR, Sh),
  do_all_shareholders_consent_to_voting_in_writing_ci(CIR, Others).

has_capital_increase_resolution_qualified_majority(CIR) :-
  is_of_sort(CIR, ci_res),
  (
    do_all_shareholders_consent_to_the_determination_ci(CIR);
    is_capital_increase_resolution_passed_via_voting(CIR)
  ).

is_capital_increase_resolution_passed_via_voting(CIR) :-
  is_of_sort(CIR, ci_res),
  is_of_sort(V, vot),
  capitalincreaseresolution_voting(CIR, V),
  voting_yesratio(V, YesRatio),
  YesRatio > 0.75.


is_permit_resolution_legal(PR) :-
  is_of_sort(PR, per_res),
  is_permit_resolution_formally_legal(PR),
  has_permit_resolution_majority(PR).

is_permit_resolution_formally_legal(PR) :-
  is_of_sort(PR, per_res),
  (
    is_permit_resolution_with_meeting_formally_legal(PR);
    is_permit_resolution_without_meeting_formally_legal(PR)
  ).

is_permit_resolution_with_meeting_formally_legal(PR) :-
  is_of_sort(PR, per_res),
  is_of_sort(M, meet),
  permitresolution_meeting(PR, M),
  is_meeting_legal(M).

is_permit_resolution_without_meeting_formally_legal(PR) :-
  is_of_sort(PR, per_res),
  \+ permitresolution_meeting(PR, _),
  (
    do_all_shareholders_consent_to_the_determination_per(PR);
    do_all_shareholders_consent_to_voting_in_writing_per(PR)
  ).

do_all_shareholders_consent_to_the_determination_per(PR) :-
  is_of_sort(PR, per_res),
  is_of_sort(A, app),
  is_of_sort(CIR, ci_res),
  is_of_sort(C, com),
  application_permitresolution(A, PR),
  application_capitalincreaseresolution(A, CIR),
  company_capitalincreaseresolution(C, CIR),
  company_shareholderlist(C, ShList),
  do_all_shareholders_consent_to_the_determination_per(PR, ShList).
do_all_shareholders_consent_to_the_determination_per(_, []).
do_all_shareholders_consent_to_the_determination_per(PR, [Sh|Others]) :-
  is_of_sort(PR, per_res),
  is_of_sort(Sh, sh),
  does_shareholder_consent_to_the_determination_per(PR, Sh),
  do_all_shareholders_consent_to_the_determination_per(PR, Others).

do_all_shareholders_consent_to_voting_in_writing_per(PR) :-
  is_of_sort(PR, per_res),
  is_of_sort(A, app),
  is_of_sort(CIR, ci_res),
  is_of_sort(C, com),
  application_permitresolution(A, PR),
  application_capitalincreaseresolution(A, CIR),
  company_capitalincreaseresolution(C, CIR),
  company_shareholderlist(C, ShList),
  do_all_shareholders_consent_to_voting_in_writing_per(PR, ShList).
do_all_shareholders_consent_to_voting_in_writing_per(_, []).
do_all_shareholders_consent_to_voting_in_writing_per(PR, [Sh|Others]) :-
  is_of_sort(PR, per_res),
  is_of_sort(Sh, sh),
  does_shareholder_consent_to_voting_in_writing_per(PR, Sh),
  do_all_shareholders_consent_to_voting_in_writing_per(PR, Others).

has_permit_resolution_majority(PR) :-
  is_of_sort(PR, per_res),
  (
    do_all_shareholders_consent_to_the_determination_per(PR);
    is_permit_resolution_passed_via_voting(PR)
  ).

is_permit_resolution_passed_via_voting(PR) :-
  is_of_sort(PR, per_res),
  is_of_sort(V, vot),
  permitresolution_voting(PR, V),
  voting_yesratio(V, YesRatio),
  YesRatio > 0.5.


voting_yesratio(V, YesRatio) :-
  is_of_sort(V, vot),
  voting_yesvotes(V, YesVotes),
  voting_novotes(V, NoVotes),
  YesRatio is (YesVotes/(YesVotes+NoVotes)).

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
  is_of_sort(CIR, ci_res),
  is_of_sort(C, com),
  capitalincreaseresolution_meeting(CIR, M),
  company_capitalincreaseresolution(C, CIR),
  company_shareholderlist(C, ShList),
  do_all_shareholders_consent_to_teleconference_meeting(M, ShList).
do_all_shareholders_consent_to_teleconference_meeting(M) :-
  is_of_sort(M, meet),
  is_of_sort(PR, per_res),
  is_of_sort(A, app),
  is_of_sort(CIR, ci_res),
  is_of_sort(C, com),
  permitresolution_meeting(PR, M),
  application_permitresolution(A, PR),
  application_capitalincreaseresolution(A, CIR),
  company_capitalincreaseresolution(C, CIR),
  company_shareholderlist(C, ShList),
  do_all_shareholders_consent_to_teleconference_meeting(M, ShList).
do_all_shareholders_consent_to_teleconference_meeting(_, []).
do_all_shareholders_consent_to_teleconference_meeting(M, [Sh|Others]) :-
  is_of_sort(M, meet),
  is_of_sort(Sh, sh),
  does_shareholder_consent_to_teleconference_meeting(M, Sh),
  do_all_shareholders_consent_to_teleconference_meeting(M, Others).

is_newly_joining_shareholder(Sh, A) :-
  is_of_sort(Sh, sh),
  is_of_sort(A, app),
  is_of_sort(C, com),
  is_of_sort(CIR, ci_res),
  is_of_sort(Sub, sub),
  company_capitalincreaseresolution(C, CIR),
  application_capitalincreaseresolution(A, CIR),
  application_subscription(A, Sub),
  subscription_shareholder(Sub, Sh),
  \+ shareholder_company(Sh, C).

are_permit_resolution_requirements_fulfilled(A) :-
  is_of_sort(A, app),
  (
    there_is_no_newly_joining_shareholder(A);
    is_permit_resolution_legal_and_complete(A)
  ).

is_permit_resolution_legal_and_complete(A) :-
  is_of_sort(A, app),
  is_of_sort(PR, per_res),
  application_permitresolution(A, PR),
  are_all_newly_joining_shareholders_mentioned_in_permit_resolution(PR),
  is_permit_resolution_legal(PR).

there_is_no_newly_joining_shareholder(A) :-
  is_of_sort(A, app),
  is_of_sort(CIR, ci_res),
  is_of_sort(SubL, subl),
  is_of_sort(C, com),
  application_capitalincreaseresolution(A, CIR),
  company_capitalincreaseresolution(C, CIR),
  application_subscriberlist(A, SubL),
  there_is_no_newly_joining_shareholder(C, SubL).
there_is_no_newly_joining_shareholder(_, []).
there_is_no_newly_joining_shareholder(C, [Sub|Others]) :-
  is_of_sort(C, com),
  is_of_sort(Sub, sub),
  is_of_sort(Sh, sh),
  subscription_shareholder(Sub, Sh),
  shareholder_company(Sh, C),
  there_is_no_newly_joining_shareholder(C, Others).

are_all_newly_joining_shareholders_mentioned_in_permit_resolution(PR) :-
  is_of_sort(PR, per_res),
  is_of_sort(A, app),
  application_permitresolution(A, PR),
  application_subscriberlist(A, SubL),
  are_all_newly_joining_shareholders_mentioned_in_permit_resolution(PR, A, SubL).
are_all_newly_joining_shareholders_mentioned_in_permit_resolution(_, _, []).
are_all_newly_joining_shareholders_mentioned_in_permit_resolution(PR, A, [Sub|Others]) :-
  is_of_sort(PR, per_res),
  is_of_sort(A, app),
  is_of_sort(Sub, sub),
  is_of_sort(Sh, sh),
  subscription_shareholder(Sub, Sh),
  (
    \+ is_newly_joining_shareholder(Sh, A);
    permitresolution_shareholder(PR, Sh)
  ),
  are_all_newly_joining_shareholders_mentioned_in_permit_resolution(PR, A, Others).

is_list_of_subscribers_attached(A) :-
  is_of_sort(A, app),
  application_subscriberlist(A, _).

are_subscriber_declarations_legal(A) :-
  is_of_sort(A, app),
  there_is_one_declaration_per_subscriber(A),
  are_all_declarations_legal(A).

there_is_one_declaration_per_subscriber(A) :-
  is_of_sort(A, app),
  application_subscriberlist(A, SubL),
  there_is_one_declaration_per_subscriber(A, SubL).
there_is_one_declaration_per_subscriber(_, []).
there_is_one_declaration_per_subscriber(A, [Sub|Others]) :-
  is_of_sort(A, app),
  is_of_sort(Sub, sub),
  is_of_sort(Sh, sh),
  is_of_sort(Dcl, dcl),
  subscription_shareholder(Sub, Sh),
  application_declaration(A, Dcl),
  declaration_shareholder(Dcl, Sh),
  there_is_one_declaration_per_subscriber(A, Others).

are_all_declarations_legal(A) :-
  is_of_sort(A, app),
  application_declarationlist(A, DclList),
  are_all_declarations_legal(A, DclList).
are_all_declarations_legal(_, []).
are_all_declarations_legal(A, [Dcl|Others]) :-
  is_of_sort(A, app),
  is_of_sort(Dcl, dcl),
  is_declaration_notarized(Dcl),
  (
    declaration_format(Dcl, original);
    declaration_format(Dcl, certifiedcopy)
  ),
  are_all_declarations_legal(A, Others).

is_amended_AoA_plausible(AA) :-
  is_of_sort(AA, amaoa),
  is_amended_AoA_plausible_concerning_old_new_increase(AA),
  is_amended_AoA_plausible_concerning_new_sum_of_nominals(AA).

is_amended_AoA_plausible_concerning_old_new_increase(AA) :-
  is_of_sort(AA, amaoa),
  amendedAoA_formercapital(AA, FormerCapital),
  amendedAoA_increase(AA, Increase),
  amendedAoA_newcapital(AA, NewCapital),
  Sum is FormerCapital + Increase,
  Sum = NewCapital.
is_amended_AoA_plausible_concerning_new_sum_of_nominals(AA) :-
  is_of_sort(AA, amaoa),
  is_of_sort(A, app),
  is_of_sort(CIR, ci_res),
  is_of_sort(C, com),
  application_amendedAoA(A, AA),
  application_capitalincreaseresolution(A, CIR),
  company_capitalincreaseresolution(C, CIR),
  amendedAoA_newcapital(AA, NewCapital),
  application_subscriberlist(A, SubList),
  sum_of_shares(SubList, NewShares),
  company_shareholderlist(C, ShList),
  sum_of_shares(ShList, OldShares),
  Sum is NewShares + OldShares,
  NewCapital = Sum.
sum_of_shares([], 0).
sum_of_shares([Sub|Others], Sum) :-
  is_of_sort(Sub, sub),
  subscription_shares(Sub, Val),
  sum_of_shares(Others, OthersSum),
  Sum is Val + OthersSum.
sum_of_shares([Sh|Others], Sum) :-
  is_of_sort(Sh, sh),
  shareholder_votes(Sh, Val),
  sum_of_shares(Others, OthersSum),
  Sum is Val + OthersSum.

do_all_directors_perform_the_application(A) :-
  is_of_sort(A, app),
  is_of_sort(CIR, ci_res),
  is_of_sort(C, com),
  application_capitalincreaseresolution(A, CIR),
  company_capitalincreaseresolution(C, CIR),
  company_directorlist(C, DirList),
  do_all_directors_perform_the_application(A, DirList).
do_all_directors_perform_the_application(_, []).
do_all_directors_perform_the_application(A, [Dir|Others]) :-
  is_of_sort(A, app),
  is_of_sort(Dir, dir),
  application_applicant(A, Dir),
  do_all_directors_perform_the_application(A, Others).


shareholder_company(Sh, C) :-
  is_of_sort(C, com),
  company_shareholderlist(C, ShList),
  member(Sh, ShList).
director_company(Dir, C) :-
  is_of_sort(C, com),
  company_directorlist(C, DirList),
  member(Dir, DirList).
application_declaration(A, Dcl) :-
  is_of_sort(A, app),
  application_declarationlist(A, DclList),
  member(Dcl, DclList).
application_subscription(A, Sub) :-
  is_of_sort(A, app),
  application_subscriberlist(A, SubList),
  member(Sub, SubList).

