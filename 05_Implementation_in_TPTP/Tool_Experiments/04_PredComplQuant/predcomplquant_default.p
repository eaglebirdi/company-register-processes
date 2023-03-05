tff(t01, type, com: $tType).
tff(t02, type, majreq: $tType).
tff(t03, type, com_majreq: (com * majreq) > $o).
tff(t04, type, com_majreq_AoA: (com * majreq) > $o).
tff(t05, type, com1: com).
tff(t06, type, special: majreq).
tff(t07, type, default: majreq).

tff(a01, axiom,
  ! [C: com, M: majreq] :
    ( com_majreq_AoA(C, M)
      <=>
      $false
    )
).

tff(a02, axiom,
  ! [C: com, M: majreq] :
    ( com_majreq(C, M)
      <=>
      (
        com_majreq_AoA(C, M)
      | ( ~? [M1: majreq] : (com_majreq_AoA(C, M1))
        & M = default      
        )
      )
    )
).
%tff(a02a, axiom, com_majreq(com1, default)).

tff(tiq, conjecture,
  ? [M: majreq] : (com_majreq(com1, M))
).

