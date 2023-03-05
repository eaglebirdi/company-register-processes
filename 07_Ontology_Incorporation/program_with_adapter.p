include('./lkif-core.ax').

tff(type_res, type, res: $tType).
tff(pred_lkiflink_res, type,
  lkiflink_res: (res * $i) > $o
).

tff(inst_res1, type, res1: res).
tff(lkiflink_res1_adapter, axiom,
  lkiflink_res(res1, lkiflink_adapter_res1)
).

tff(lkiflink_res_adapting, axiom,
  ! [X: res, Y] : (
    lkiflink_res(X, Y)
    =>
    lkif_core_legal_action_owl_Decision(Y)
  )
).

tff(tiq, conjecture,
  ? [X] :
  (
    lkiflink_res(res1, X)
  & lkif_core_legal_action_owl_Decision(X)
  )
).
