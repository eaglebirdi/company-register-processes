application_resolution(app1, res1).
company_resolution(com1, res1).
resolution_meeting(res1, meet1).
application_deed(app1, deed1).
resolution_voting(res1, vot1).
application_assurance(app1, ass1).
company_AoA_liquidatorlist(_, _) :- false.
resolution_liquidatorlist(res1, [liq_jacob, liq_kate, liq_luca]).

company_representationpower(com1, joint).
has_company_expiration_date(_) :- false.

% shareholder_company(sh_alice, com1).
% shareholder_company(sh_ben, com1).
% shareholder_company(sh_chris, com1).
company_shareholderlist(com1, [sh_alice, sh_ben, sh_chris]).
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
director_person(liq_jacob, pers_jacob).
director_person(liq_kate, pers_kate).
director_person(liq_luca, pers_luca).
director_representationpower(dir_kate, modified).
director_representationpower(dir_chris, sole).
director_representationpower(liq_luca, sole).
director_exemption181(dir_chris).

meeting_format(meet1, teleconference).
voting_yesvotes(vot1, 90001).
voting_novotes(vot1, 10000).
voting_abstentions(vot1, 0).
does_shareholder_consent_to_teleconference_meeting(meet1, sh_alice).
does_shareholder_consent_to_teleconference_meeting(meet1, sh_ben).
does_shareholder_consent_to_teleconference_meeting(meet1, sh_chris).
does_shareholder_consent_to_the_determination(_, _) :- false.
does_shareholder_consent_to_voting_in_writing(_, _) :- false.
is_resolution_notarized(_) :- false.

assurance_signer(ass1, pers_jacob).
assurance_signer(ass1, pers_kate).
assurance_signer(ass1, pers_luca).
deed_format(deed1, certifiedcopy).
application_applicant(app1, pers_luca).

