include('./lkif-core.ax').
tff(type_res, type, res: $tType).
tff(axiom_res_is_lkif_Decision, axiom,
  ! [X: res]: lkif_core_legal_action_owl_Decision(X)
).
