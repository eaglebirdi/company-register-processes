tff(t01, type, dir: $tType).
tff(t02, type, com: $tType).
tff(t03, type, director_company: (dir * com) > $o).
tff(t04, type, dir1: dir).
tff(t05, type, com1: com).

tff(a01, axiom,
  ! [D: dir, C: com] :
    ( director_company(D, C)
      <=>
      (D = dir1 & C = com1)
    )
).

tff(tiq, conjecture,
  ? [C: com] : (director_company(dir1, C))
).
