tff(t01, type, vot: $tType).
tff(t02, type, voting_yesratio: (vot * $real) > $o).
tff(t03, type, has_majority: vot > $o).
tff(t04, type, vot1: vot).

tff(a01, axiom,
  ! [V: vot] : 
    ( has_majority(V)
      <=
      ( ? [YesRatio: $real] :
          ( voting_yesratio(V, YesRatio)
          & $greater(YesRatio, 0.5)
          )
      )
    )
).
tff(a02, axiom, voting_yesratio(vot1, 0.4)).

tff(tiq, conjecture, has_majority(vot1)).
