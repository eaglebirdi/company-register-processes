contains_AoA_full_text(app1).
has_increased_capital_been_covered(app1).

application_applicant(app1, dir_jacob).
application_applicant(app1, dir_kate).
application_applicant(app1, dir_chris).

are_matches_notarily_certified(app1).

amendedAoA_formercapital(aoa1, 100000).
amendedAoA_increase(aoa1, 30000).
amendedAoA_newcapital(aoa1, 130000).

is_assurance_signed(ass1).

does_shareholder_consent_to_the_determination_ci(_, _) :- false.
does_shareholder_consent_to_voting_in_writing_ci(_, _) :- false.
is_capitalincreaseresolution_notarized(ci_res1).

does_shareholder_consent_to_the_determination_per(_, _) :- false.
does_shareholder_consent_to_voting_in_writing_per(_, _) :- false.
permitresolution_shareholder(per_res1, sh_dana).

does_shareholder_consent_to_teleconference_meeting(ci_meet1, sh_alice).
does_shareholder_consent_to_teleconference_meeting(ci_meet1, sh_ben).
does_shareholder_consent_to_teleconference_meeting(ci_meet1, sh_chris).

meeting_format(ci_meet1, teleconference).
meeting_format(per_meet1, personal).

voting_yesvotes(ci_vot1, 90001).
voting_yesvotes(per_vot1, 90001).
voting_novotes(ci_vot1, 10000).
voting_novotes(per_vot1, 10000).
voting_abstentions(ci_vot1, 0).
voting_abstentions(per_vot1, 0).

% shareholder_company(sh_alice, com1).
% shareholder_company(sh_ben, com1).
% shareholder_company(sh_chris, com1).
company_shareholderlist(com1, [sh_alice, sh_ben, sh_chris]).
shareholder_person(sh_dana, pers_dana).
shareholder_person(sh_alice, pers_alice).
shareholder_person(sh_ben, pers_ben).
shareholder_person(sh_chris, pers_chris).
shareholder_votes(sh_alice, 50001).
shareholder_votes(sh_ben, 39999).
shareholder_votes(sh_chris, 10000).

% director_company(dir_jacob, com1).
% director_company(dir_kate, com1).
% director_company(dir_chris, com1).
company_directorlist(com1, [dir_jacob, dir_kate, dir_chris]).
director_person(dir_jacob, pers_jacob).
director_person(dir_kate, pers_kate).
director_person(dir_chris, pers_chris).

% subscriberlist_subscription(subl1, sub_alice).
% subscriberlist_subscription(subl1, sub_dana).
application_subscriberlist(app1, [sub_alice, sub_dana]).
subscription_shareholder(sub_alice, sh_alice).
subscription_shareholder(sub_dana, sh_dana).
subscription_shares(sub_alice, 10000).
subscription_shares(sub_dana, 20000).

% application_declaration(app1, dcl_alice).
% application_declaration(app1, dcl_dana).
application_declarationlist(app1, [dcl_alice, dcl_dana]).
declaration_shareholder(dcl_alice, sh_alice).
declaration_shareholder(dcl_dana, sh_dana).
declaration_format(dcl_alice, original).
declaration_format(dcl_dana, original).
is_declaration_notarized(dcl_alice).
is_declaration_notarized(dcl_dana).

