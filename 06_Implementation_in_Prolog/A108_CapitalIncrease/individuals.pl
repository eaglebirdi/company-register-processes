is_of_sort(personal, meetf).
is_of_sort(teleconference, meetf).

is_of_sort(original, dclf).
is_of_sort(certifiedcopy, dclf).

is_of_sort(com1, com).
is_of_sort(app1, app).
is_of_sort(ass1, ass).
is_of_sort(aoa1, amaoa).

is_of_sort(ci_res1, ci_res).
is_of_sort(ci_meet1, meet).
is_of_sort(ci_vot1, vot).
is_of_sort(per_res1, per_res).
is_of_sort(per_meet1, meet).
is_of_sort(per_vot1, vot).

is_of_sort(sh_dana, sh).
is_of_sort(sh_alice, sh).
is_of_sort(sh_ben, sh).
is_of_sort(sh_chris, sh).
is_of_sort(dir_jacob, dir).
is_of_sort(dir_kate, dir).
is_of_sort(dir_chris, dir).

is_of_sort(pers_dana, pers).
is_of_sort(pers_alice, pers).
is_of_sort(pers_ben, pers).
is_of_sort(pers_chris, pers).
is_of_sort(pers_jacob, pers).
is_of_sort(pers_kate, pers).

is_of_sort(sub_alice, sub).
is_of_sort(sub_dana, sub).
is_of_sort(dcl_alice, dcl).
is_of_sort(dcl_dana, dcl).

application_assurance(app1, ass1).
application_amendedAoA(app1, aoa1).
application_capitalincreaseresolution(app1, ci_res1).
company_capitalincreaseresolution(com1, ci_res1).
capitalincreaseresolution_meeting(ci_res1, ci_meet1).
capitalincreaseresolution_voting(ci_res1, ci_vot1).
application_permitresolution(app1, per_res1).
permitresolution_meeting(per_res1, per_meet1).
permitresolution_voting(per_res1, per_vot1).

