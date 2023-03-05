tff(t01, type, res: $tType).
tff(t02, type, is_legal: res > $o).
tff(t03, type, is_formally_legal: res > $o).
tff(t04, type, has_majority: res > $o).
tff(t05, type, res1: res).

tff(a01, axiom,
  ! [R: res] :
    ( is_legal(R)
      <=
      ( is_formally_legal(R)
      & has_majority(R)
      )
    )
).
tff(a02, axiom, is_formally_legal(res1)).
%tff(a03, axiom, has_majority(res1)).

tff(tiq, conjecture, is_legal(res1)).
