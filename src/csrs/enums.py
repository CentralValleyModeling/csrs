import enum

from .schemas import NamedPath


# Define the assumption types as a Python enumeration
class AssumptionEnum(enum.StrEnum):
    hydrology = "hydrology"
    sea_level_rise = "sea_level_rise"
    land_use = "land_use"
    tucp = "tucp"
    dcp = "dcp"
    va = "va"
    south_of_delta = "south_of_delta"


class PathCategoryEnum(enum.StrEnum):
    delivery = "delivery"
    delta = "delta"
    other = "other"
    salinity = "salinity"
    storage = "storage"
    upstream_flows = "upstream_flows"
    water_year_type = "wyt"


class PeriodTypeEnum(enum.StrEnum):
    per_aver = "PER-AVER"
    per_cum = "PER-CUM"
    inst_val = "INST-VAL"
    inst_cum = "INST-CUM"


class IntervalEnum(enum.StrEnum):
    mon_1 = "1MON"
    year_1 = "1YEAR"


class StandardPathsEnum(enum.Enum):
    cvp_allocation_nod_ag = NamedPath(
        name="cvp_allocation_nod_ag",
        path="/.*/PERDV_CVPAG_SYS/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="cvp_allocation_nod_ag",
        units="NONE",
    )
    cvp_allocation_nod_mi = NamedPath(
        name="cvp_allocation_nod_mi",
        path="/.*/PERDV_CVPMI_SYS/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="cvp_allocation_nod_mi",
        units="NONE",
    )
    cvp_allocation_nod_rf = NamedPath(
        name="cvp_allocation_nod_rf",
        path="/.*/PERDV_CVPRF_SYS/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="cvp_allocation_nod_rf",
        units="NONE",
    )
    cvp_allocation_nod_sc = NamedPath(
        name="cvp_allocation_nod_sc",
        path="/.*/PERDV_CVPSC_SYS/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="cvp_allocation_nod_sc",
        units="NONE",
    )
    cvp_allocation_sod_ag = NamedPath(
        name="cvp_allocation_sod_ag",
        path="/.*/PERDV_CVPAG_S/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="cvp_allocation_sod_ag",
        units="NONE",
    )
    cvp_allocation_sod_ex = NamedPath(
        name="cvp_allocation_sod_ex",
        path="/.*/PERDV_CVPEX_S/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="cvp_allocation_sod_ex",
        units="NONE",
    )
    cvp_allocation_sod_mi = NamedPath(
        name="cvp_allocation_sod_mi",
        path="/.*/PERDV_CVPMI_S/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="cvp_allocation_sod_mi",
        units="NONE",
    )
    cvp_allocation_sod_rf = NamedPath(
        name="cvp_allocation_sod_rf",
        path="/.*/PERDV_CVPRF_S/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="cvp_allocation_sod_rf",
        units="NONE",
    )
    cvp_delivery_american = NamedPath(
        name="cvp_delivery_american",
        path="/.*/DEL_CVP_P_AMER/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_american",
        units="CFS",
    )
    cvp_delivery_nod = NamedPath(
        name="cvp_delivery_nod",
        path="/.*/DEL_CVP_TOTAL_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_nod",
        units="CFS",
    )
    cvp_delivery_pag_n = NamedPath(
        name="cvp_delivery_pag_n",
        path="/.*/DEL_CVP_PAG_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_pag_n",
        units="CFS",
    )
    cvp_delivery_pag_s = NamedPath(
        name="cvp_delivery_pag_s",
        path="/.*/DEL_CVP_PAG_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_pag_s",
        units="CFS",
    )
    cvp_delivery_pex_s = NamedPath(
        name="cvp_delivery_pex_s",
        path="/.*/DEL_CVP_PEX_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_pex_s",
        units="CFS",
    )
    cvp_delivery_pmi_n = NamedPath(
        name="cvp_delivery_pmi_n",
        path="/.*/DEL_CVP_PMI_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_pmi_n",
        units="CFS",
    )
    cvp_delivery_pmi_n_with_amer = NamedPath(
        name="cvp_delivery_pmi_n_with_amer",
        path="/.*/DEL_CVP_PMI_W_AMER/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_pmi_n_with_amer",
        units="CFS",
    )
    cvp_delivery_pmi_s = NamedPath(
        name="cvp_delivery_pmi_s",
        path="/.*/DEL_CVP_PMI_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_pmi_s",
        units="CFS",
    )
    cvp_delivery_prf_n = NamedPath(
        name="cvp_delivery_prf_n",
        path="/.*/DEL_CVP_PRF_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_prf_n",
        units="CFS",
    )
    cvp_delivery_prf_s = NamedPath(
        name="cvp_delivery_prf_s",
        path="/.*/DEL_CVP_PRF_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_prf_s",
        units="CFS",
    )
    cvp_delivery_psc_n = NamedPath(
        name="cvp_delivery_psc_n",
        path="/.*/DEL_CVP_PSC_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_psc_n",
        units="CFS",
    )
    cvp_delivery_sod = NamedPath(
        name="cvp_delivery_sod",
        path="/.*/cvptotaldel/FLOW-DELIVERY//.*/.*/",
        category="delivery",
        detail="cvp_delivery_sod",
        units="CFS",
    )
    cvp_delivery_sod_no_cvc = NamedPath(
        name="cvp_delivery_sod_no_cvc",
        path="/.*/DEL_CVP_TOTAL_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="cvp_delivery_sod_no_cvc",
        units="CFS",
    )
    short_cvp_tot_n = NamedPath(
        name="short_cvp_tot_n",
        path="/.*/SHORT_CVP_TOT_N/DELIVERY-SHORTAGE-CVP//.*/.*/",
        category="delivery",
        detail="short_cvp_tot_n",
        units="CFS",
    )
    short_cvp_tot_s = NamedPath(
        name="short_cvp_tot_s",
        path="/.*/SHORT_CVP_TOT_S/DELIVERY-SHORTAGE-CVP//.*/.*/",
        category="delivery",
        detail="short_cvp_tot_s",
        units="CFS",
    )
    swp_co_available = NamedPath(
        name="swp_co_available",
        path="/.*/co_available_dv/carryover//.*/.*/",
        category="delivery",
        detail="swp_co_available",
        units="TAF",
    )
    swp_co_est = NamedPath(
        name="swp_co_est",
        path="/.*/co_est_dv/swp-output//.*/.*/",
        category="delivery",
        detail="swp_co_est",
        units="TAF",
    )
    swp_co_final = NamedPath(
        name="swp_co_final",
        path="/.*/co_final_dv/carryover//.*/.*/",
        category="delivery",
        detail="swp_co_final",
        units="TAF",
    )
    swp_del_target_ta = NamedPath(
        name="swp_del_target_ta",
        path="/.*/deltar_a_dv/swp-output//.*/.*/",
        category="delivery",
        detail="swp_del_target_ta",
        units="TAF",
    )
    swp_del_target_ta_co = NamedPath(
        name="swp_del_target_ta_co",
        path="/.*/deltardv_total/swp-output//.*/.*/",
        category="delivery",
        detail="swp_del_target_ta_co",
        units="TAF",
    )
    # These will need to be split up in the database, and calculated client side
    # swp_delivery_co_sod = NamedPath(
    #     name="swp_delivery_co_sod",
    #     path="/.*/swp_CO_total - swp_CO_FEATH - swp_CO_NBAY///.*/.*/",
    #     category="delivery",
    #     detail="swp_delivery_co_sod",
    # )
    # swp_delivery_in_sod = NamedPath(
    #     name="swp_delivery_in_sod",
    #     path="/.*/swp_IN_total  - swp_IN_FEATH - swp_IN_NBAY///.*/.*/",
    #     category="delivery",
    #     detail="swp_delivery_in_sod",
    # )
    # swp_delivery_ta_sod = NamedPath(
    #     name="swp_delivery_ta_sod",
    #     path="/.*/swp_TA_total - swp_TA_FEATH - swp_TA_NBAY ///.*/.*/",
    #     category="delivery",
    #     detail="swp_delivery_ta_sod",
    # )
    # swp_delivery_total_frsa = NamedPath(
    #     name="swp_delivery_total_frsa",
    #     path="/.*/swp_TA_FEATH + swp_IN_FEATH + swp_CO_FEATH///.*/.*/",
    #     category="delivery",
    #     detail="swp_delivery_total_frsa",
    # )
    swp_percent_delivery = NamedPath(
        name="swp_percent_delivery",
        path="/.*/swp_perdeldv/swp-delivery//.*/.*/",
        category="delivery",
        detail="swp_percent_delivery",
        units="CFS",
    )
    swp_var_demand_deltar = NamedPath(
        name="swp_var_demand_deltar",
        path="/.*/vardeltardv/swp-output//.*/.*/",
        category="delivery",
        detail="swp_var_demand_deltar",
        units="TAF",
    )
    swp_co_feath = NamedPath(
        name="swp_co_feath",
        path="/.*/SWP_CO_FEATH/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="swp_co_feath",
        units="CFS",
    )
    swp_co_nbay = NamedPath(
        name="swp_co_nbay",
        path="/.*/SWP_CO_NBAY/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="swp_co_nbay",
        units="CFS",
    )
    swp_co_total = NamedPath(
        name="swp_co_total",
        path="/.*/swp_CO_total/swp_delivery//.*/.*/",
        category="delivery",
        detail="swp_co_total",
        units="CFS",
    )
    swp_in_feath = NamedPath(
        name="swp_in_feath",
        path="/.*/SWP_IN_FEATH/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="swp_in_feath",
        units="CFS",
    )
    swp_in_nbay = NamedPath(
        name="swp_in_nbay",
        path="/.*/SWP_IN_NBAY/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="swp_in_nbay",
        units="CFS",
    )
    swp_in_total = NamedPath(
        name="swp_in_total",
        path="/.*/swp_IN_total/swp_delivery//.*/.*/",
        category="delivery",
        detail="swp_in_total",
        units="CFS",
    )
    swp_loss = NamedPath(
        name="swp_loss",
        path="/.*/SWP_LOSS/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="swp_loss",
        units="CFS",
    )
    swp_ta_feath = NamedPath(
        name="swp_ta_feath",
        path="/.*/SWP_TA_FEATH/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="swp_ta_feath",
        units="CFS",
    )
    swp_ta_nbay = NamedPath(
        name="swp_ta_nbay",
        path="/.*/SWP_TA_NBAY/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="swp_ta_nbay",
        units="CFS",
    )
    swp_ta_total = NamedPath(
        name="swp_ta_total",
        path="/.*/swp_TA_total/swp_delivery//.*/.*/",
        category="delivery",
        detail="swp_ta_total",
        units="CFS",
    )
    swp_unused_ta_total = NamedPath(
        name="swp_unused_ta_total",
        path="/.*/unused_totaldv/swp-output//.*/.*/",
        category="delivery",
        detail="swp_unused_ta_total",
        units="TAF",
    )
    banks_cvp_exports = NamedPath(
        name="banks_cvp_exports",
        path="/.*/C_CAA003_CVP/FLOW-DELIVERY//.*/.*/",
        category="delta",
        detail="banks_cvp_exports",
        units="CFS",
    )
    banks_export_cross_valley_pumping = NamedPath(
        name="banks_export_cross_valley_pumping",
        path="/.*/C_CAA003_CVC/FLOW-DELIVERY//.*/.*/",
        category="delta",
        detail="banks_export_cross_valley_pumping",
        units="CFS",
    )
    banks_exports = NamedPath(
        name="banks_exports",
        path="/.*/D_OMR027_CAA000/DIVERSION//.*/.*/",
        category="delta",
        detail="banks_exports",
        units="CFS",
    )
    banks_swp_exports = NamedPath(
        name="banks_swp_exports",
        path="/.*/C_CAA003_SWP/FLOW-DELIVERY//.*/.*/",
        category="delta",
        detail="banks_swp_exports",
        units="CFS",
    )
    ccwd = NamedPath(
        name="ccwd",
        path="/.*/D408/FLOW-DELIVERY//.*/.*/",
        category="delta",
        detail="ccwd",
        units="CFS",
    )
    delta_inflow_ndoi = NamedPath(
        name="delta_inflow_ndoi",
        path="/.*/DELTAINFLOWFORNDOI/FLOW//.*/.*/",
        category="delta",
        detail="delta_inflow_ndoi",
        units="CFS",
    )
    delta_outflow_ndoi = NamedPath(
        name="delta_outflow_ndoi",
        path="/.*/NDOI/FLOW//.*/.*/",
        category="delta",
        detail="delta_outflow_ndoi",
        units="CFS",
    )
    dxc_flow = NamedPath(
        name="dxc_flow",
        path="/.*/D_SAC030_MOK014/DIVERSION//.*/.*/",
        category="delta",
        detail="dxc_flow",
        units="CFS",
    )
    excess_outflow_ndoi = NamedPath(
        name="excess_outflow_ndoi",
        path="/.*/NDOI_ADD/FLOW//.*/.*/",
        category="delta",
        detail="excess_outflow_ndoi",
        units="CFS",
    )
    excess_outflow_ann_ndoi = NamedPath(
        name="excess_outflow_ann_ndoi",
        path="/.*/NDOI_ADD_ANN/FLOW-CHANNEL//.*/.*/",
        category="delta",
        detail="excess_outflow_ann_ndoi",
        units="CFS",
    )
    excess_outflow_cvp_ndoi = NamedPath(
        name="excess_outflow_cvp_ndoi",
        path="/.*/NDOI_ADD_CVP/FLOW-CHANNEL//.*/.*/",
        category="delta",
        detail="excess_outflow_cvp_ndoi",
        units="CFS",
    )
    excess_outflow_swp_ndoi = NamedPath(
        name="excess_outflow_swp_ndoi",
        path="/.*/NDOI_ADD_SWP/FLOW-CHANNEL//.*/.*/",
        category="delta",
        detail="excess_outflow_swp_ndoi",
        units="CFS",
    )
    flow_at_georgiana_slough = NamedPath(
        name="flow_at_georgiana_slough",
        path="/.*/C_SAC029B/CHANNEL//.*/.*/",
        category="delta",
        detail="flow_at_georgiana_slough",
        units="CFS",
    )
    flow_at_rio_vista = NamedPath(
        name="flow_at_rio_vista",
        path="/.*/C_SAC017/CHANNEL//.*/.*/",
        category="delta",
        detail="flow_at_rio_vista",
        units="CFS",
    )
    flow_below_dxc = NamedPath(
        name="flow_below_dxc",
        path="/.*/C_SAC030/CHANNEL//.*/.*/",
        category="delta",
        detail="flow_below_dxc",
        units="CFS",
    )
    jones_exports = NamedPath(
        name="jones_exports",
        path="/.*/D_OMR028_DMC000/DIVERSION//.*/.*/",
        category="delta",
        detail="jones_exports",
        units="CFS",
    )
    modeled_required_do = NamedPath(
        name="modeled_required_do",
        path="/.*/MRDO_FINALDV/FLOW-REQ-MRDO//.*/.*/",
        category="delta",
        detail="modeled_required_do",
        units="CFS",
    )
    north_bay_aqueduct = NamedPath(
        name="north_bay_aqueduct",
        path="/.*/C_CSL004B/CHANNEL//.*/.*/",
        category="delta",
        detail="north_bay_aqueduct",
        units="CFS",
    )
    old_and_middle_river_flow = NamedPath(
        name="old_and_middle_river_flow",
        path="/.*/C_OMR014/CHANNEL//.*/.*/",
        category="delta",
        detail="old_and_middle_river_flow",
        units="CFS",
    )
    qwestflow = NamedPath(
        name="qwestflow",
        path="/.*/QWestFlow/FLOW-CHANNEL//.*/.*/",
        category="delta",
        detail="qwestflow",
        units="CFS",
    )
    required_delta_outflow = NamedPath(
        name="required_delta_outflow",
        path="/.*/NDOI_MIN/FLOW//.*/.*/",
        category="delta",
        detail="required_delta_outflow",
        units="CFS",
    )
    sac_flow_at_freeport = NamedPath(
        name="sac_flow_at_freeport",
        path="/.*/C_SAC048/CHANNEL//.*/.*/",
        category="delta",
        detail="sac_flow_at_freeport",
        units="CFS",
    )
    total_ndd_exports = NamedPath(
        name="total_ndd_exports",
        path="/.*/EXPORTACTUALIF/EXPORT-PRJ//.*/.*/",
        category="delta",
        detail="total_ndd_exports",
        units="CFS",
    )
    total_td_exports = NamedPath(
        name="total_td_exports",
        path="/.*/EXPORTACTUALTD/EXPORT-PRJ//.*/.*/",
        category="delta",
        detail="total_td_exports",
        units="CFS",
    )
    banks_export_cvp_dedicated = NamedPath(
        name="banks_export_cvp_dedicated",
        path="/.*/C_CAA003_CVPDED/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="banks_export_cvp_dedicated",
        units="CFS",
    )
    banks_export_fed_share = NamedPath(
        name="banks_export_fed_share",
        path="/.*/C_CAA003_EXP2/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="banks_export_fed_share",
        units="CFS",
    )
    banks_export_jpod = NamedPath(
        name="banks_export_jpod",
        path="/.*/C_CAA003_CVPWHL/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="banks_export_jpod",
        units="CFS",
    )
    banks_export_state_share = NamedPath(
        name="banks_export_state_share",
        path="/.*/C_CAA003_EXP1/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="banks_export_state_share",
        units="CFS",
    )
    banks_export_wts = NamedPath(
        name="banks_export_wts",
        path="/.*/C_CAA003_WTS/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="banks_export_wts",
        units="CFS",
    )
    banks_pp_north_delta = NamedPath(
        name="banks_pp_north_delta",
        path="/.*/C_CAA003_IF/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="banks_pp_north_delta",
        units="CFS",
    )
    banks_pp_swp_through_delta = NamedPath(
        name="banks_pp_swp_through_delta",
        path="/.*/C_CAA003_SWP_TD/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="banks_pp_swp_through_delta",
        units="CFS",
    )
    banks_pp_through_delta = NamedPath(
        name="banks_pp_through_delta",
        path="/.*/C_CAA003_TD/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="banks_pp_through_delta",
        units="CFS",
    )
    dcc_gate_days_open = NamedPath(
        name="dcc_gate_days_open",
        path="/.*/DXC/GATE-DAYS-OPEN//.*/.*/",
        category="other",
        detail="dcc_gate_days_open",
        units="NONE",
    )
    di_cvp = NamedPath(
        name="di_cvp",
        path="/.*/DI_CVP_sysdv/DEMAND-INDEX//.*/.*/",
        category="other",
        detail="di_cvp",
        units="NONE",
    )
    dmc_inflow_to_mendotapool = NamedPath(
        name="dmc_inflow_to_mendotapool",
        path="/.*/C_DMC116/CHANNEL//.*/.*/",
        category="other",
        detail="dmc_inflow_to_mendotapool",
        units="CFS",
    )
    ei_ratio = NamedPath(
        name="ei_ratio",
        path="/.*/EXPRATIO_/EI-RATIO-STD//.*/.*/",
        category="other",
        detail="ei_ratio",
        units="NONE",
    )
    hamilton_city_diversion = NamedPath(
        name="hamilton_city_diversion",
        path="/.*/D_SAC207_GCC007/DIVERSION//.*/.*/",
        category="other",
        detail="hamilton_city_diversion",
        units="CFS",
    )
    jones_export_fed_share = NamedPath(
        name="jones_export_fed_share",
        path="/.*/C_DMC000_EXP1/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="jones_export_fed_share",
        units="CFS",
    )
    jones_export_state_share = NamedPath(
        name="jones_export_state_share",
        path="/.*/C_DMC000_EXP2/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="jones_export_state_share",
        units="CFS",
    )
    jones_export_wts = NamedPath(
        name="jones_export_wts",
        path="/.*/C_DMC000_WTS/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="jones_export_wts",
        units="CFS",
    )
    jones_pp_north_delta = NamedPath(
        name="jones_pp_north_delta",
        path="/.*/C_DMC000_IF/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="jones_pp_north_delta",
        units="CFS",
    )
    jones_pp_through_delta = NamedPath(
        name="jones_pp_through_delta",
        path="/.*/C_DMC000_TD/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="jones_pp_through_delta",
        units="CFS",
    )
    net_dicu = NamedPath(
        name="net_dicu",
        path="/.*/net_DICU/DICU_FLOW//.*/.*/",
        category="other",
        detail="net_dicu",
        units="CFS",
    )
    red_bluff_diversion_dam_diversion = NamedPath(
        name="red_bluff_diversion_dam_diversion",
        path="/.*/D_SAC240_TCC001/DIVERSION//.*/.*/",
        category="other",
        detail="red_bluff_diversion_dam_diversion",
        units="CFS",
    )
    rpa_constraint_banks = NamedPath(
        name="rpa_constraint_banks",
        path="/.*/maxexp_rpa_SWPdv/EXPORT-LIMIT//.*/.*/",
        category="other",
        detail="rpa_constraint_banks",
        units="CFS",
    )
    rpa_constraint_jones = NamedPath(
        name="rpa_constraint_jones",
        path="/.*/maxexp_rpa_CVPdv/EXPORT-LIMIT//.*/.*/",
        category="other",
        detail="rpa_constraint_jones",
        units="CFS",
    )
    short_swp_total = NamedPath(
        name="short_swp_total",
        path="/.*/SHORT_SWP_TOTA/DELIVERY-SHORTAGE-SWP//.*/.*/",
        category="other",
        detail="short_swp_total",
        units="CFS",
    )
    swp_allocation_frsa = NamedPath(
        name="swp_allocation_frsa",
        path="/.*/PERDV_SWP_FSC/PERCENT-DELIVERY//.*/.*/",
        category="other",
        detail="swp_allocation_frsa",
        units="NONE",
    )
    swp_allocation_mi = NamedPath(
        name="swp_allocation_mi",
        path="/.*/PERDV_SWP_MWD1/PERCENT-DELIVERY//.*/.*/",
        category="other",
        detail="swp_allocation_mi",
        units="NONE",
    )
    swp_delivery_int = NamedPath(
        name="swp_delivery_int",
        path="/.*/DEL_SWP_PIN/DELIVERY-SWP//.*/.*/",
        category="other",
        detail="swp_delivery_int",
        units="CFS",
    )
    trinity_export = NamedPath(
        name="trinity_export",
        path="/.*/D_LWSTN_CCT011/DIVERSION//.*/.*/",
        category="other",
        detail="trinity_export",
        units="CFS",
    )
    trinity_export_excess = NamedPath(
        name="trinity_export_excess",
        path="/.*/D_LWSTN_ADD/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="trinity_export_excess",
        units="CFS",
    )
    trinity_export_ops_limit = NamedPath(
        name="trinity_export_ops_limit",
        path="/.*/TRIN_IMPDV/UNDEFINED//.*/.*/",
        category="other",
        detail="trinity_export_ops_limit",
        units="NONE",
    )
    trinity_export_ops_x = NamedPath(
        name="trinity_export_ops_x",
        path="/.*/D_LWSTN_IMPORT/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="trinity_export_ops_x",
        units="CFS",
    )
    wsi_cvp = NamedPath(
        name="wsi_cvp",
        path="/.*/WSI_CVP_sysdv/WATER-SUPPLY-INDEX//.*/.*/",
        category="other",
        detail="wsi_cvp",
        units="NONE",
    )
    bd_ec = NamedPath(
        name="bd_ec",
        path="/.*/BD_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="bd_ec",
        units="UMHOS/CM",
    )
    ci_ec = NamedPath(
        name="ci_ec",
        path="/.*/CI_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="ci_ec",
        units="UMHOS/CM",
    )
    co_ec = NamedPath(
        name="co_ec",
        path="/.*/CO_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="co_ec",
        units="UMHOS/CM",
    )
    em_ec = NamedPath(
        name="em_ec",
        path="/.*/EM_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="em_ec",
        units="UMHOS/CM",
    )
    jp_ec = NamedPath(
        name="jp_ec",
        path="/.*/JP_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="jp_ec",
        units="UMHOS/CM",
    )
    lv_ec = NamedPath(
        name="lv_ec",
        path="/.*/LV_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="lv_ec",
        units="UMHOS/CM",
    )
    mr_ec = NamedPath(
        name="mr_ec",
        path="/.*/MR_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="mr_ec",
        units="UMHOS/CM",
    )
    rs_ec = NamedPath(
        name="rs_ec",
        path="/.*/RS_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="rs_ec",
        units="UMHOS/CM",
    )
    vi_ec = NamedPath(
        name="vi_ec",
        path="/.*/VI_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="vi_ec",
        units="UMHOS/CM",
    )
    x2_position_prev = NamedPath(
        name="x2_position_prev",
        path="/.*/X2_PRV/X2-POSITION-PREV//.*/.*/",
        category="salinity",
        detail="x2_position_prev",
        units="KM",
    )
    folsom_storage = NamedPath(
        name="folsom_storage",
        path="/.*/S_FOLSM/STORAGE//.*/.*/",
        category="storage",
        detail="folsom_storage",
        units="TAF",
    )
    friant_storage = NamedPath(
        name="friant_storage",
        path="/.*/S_MLRTN/STORAGE//.*/.*/",
        category="storage",
        detail="friant_storage",
        units="TAF",
    )
    mcclure_storage = NamedPath(
        name="mcclure_storage",
        path="/.*/S_MCLRE/STORAGE//.*/.*/",
        category="storage",
        detail="mcclure_storage",
        units="TAF",
    )
    new_don_pedro_storage = NamedPath(
        name="new_don_pedro_storage",
        path="/.*/S_PEDRO/STORAGE//.*/.*/",
        category="storage",
        detail="new_don_pedro_storage",
        units="TAF",
    )
    new_melones_storage = NamedPath(
        name="new_melones_storage",
        path="/.*/S_MELON/STORAGE//.*/.*/",
        category="storage",
        detail="new_melones_storage",
        units="TAF",
    )
    oroville_storage = NamedPath(
        name="oroville_storage",
        path="/.*/S_OROVL/STORAGE//.*/.*/",
        category="storage",
        detail="oroville_storage",
        units="TAF",
    )
    san_luis_storage_cvp = NamedPath(
        name="san_luis_storage_cvp",
        path="/.*/S_SLUIS_CVP/STORAGE//.*/.*/",
        category="storage",
        detail="san_luis_storage_cvp",
        units="TAF",
    )
    san_luis_storage_swp = NamedPath(
        name="san_luis_storage_swp",
        path="/.*/S_SLUIS_SWP/STORAGE//.*/.*/",
        category="storage",
        detail="san_luis_storage_swp",
        units="TAF",
    )
    shasta_storage = NamedPath(
        name="shasta_storage",
        path="/.*/S_SHSTA/STORAGE//.*/.*/",
        category="storage",
        detail="shasta_storage",
        units="TAF",
    )
    sl_cvp_rule_curve = NamedPath(
        name="sl_cvp_rule_curve",
        path="/.*/CVPRuleCv/rulecurve//.*/.*/",
        category="storage",
        detail="sl_cvp_rule_curve",
        units="TAF",
    )
    sl_swp_rule_curve = NamedPath(
        name="sl_swp_rule_curve",
        path="/.*/SWPRuleCv/rulecurve//.*/.*/",
        category="storage",
        detail="sl_swp_rule_curve",
        units="TAF",
    )
    trinity_storage = NamedPath(
        name="trinity_storage",
        path="/.*/S_TRNTY/STORAGE//.*/.*/",
        category="storage",
        detail="trinity_storage",
        units="TAF",
    )
    whiskeytown = NamedPath(
        name="whiskeytown",
        path="/.*/S_WKYTN/STORAGE//.*/.*/",
        category="storage",
        detail="whiskeytown",
        units="TAF",
    )
    feather_below_thermolito = NamedPath(
        name="feather_below_thermolito",
        path="/.*/C_FTR059/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="feather_below_thermolito",
        units="CFS",
    )
    featherflowabvfremontweir = NamedPath(
        name="featherflowabvfremontweir",
        path="/.*/C_FTR003/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="featherflowabvfremontweir",
        units="CFS",
    )
    featherlowflow = NamedPath(
        name="featherlowflow",
        path="/.*/C_FTR068/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="featherlowflow",
        units="CFS",
    )
    feathermouth = NamedPath(
        name="feathermouth",
        path="/.*/C_FTR003/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="feathermouth",
        units="CFS",
    )
    featheryubaconfluence = NamedPath(
        name="featheryubaconfluence",
        path="/.*/C_FTR031/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="featheryubaconfluence",
        units="CFS",
    )
    fremont_weir_spills = NamedPath(
        name="fremont_weir_spills",
        path="/.*/SP_SAC083_YBP037/RIVER-SPILLS//.*/.*/",
        category="upstream_flows",
        detail="fremont_weir_spills",
        units="TAF",
    )
    h_street = NamedPath(
        name="h_street",
        path="/.*/C_AMR004/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="h_street",
        units="CFS",
    )
    mercedmouth = NamedPath(
        name="mercedmouth",
        path="/.*/C_MCD021/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="mercedmouth",
        units="CFS",
    )
    mokelumne_flow = NamedPath(
        name="mokelumne_flow",
        path="/.*/C_MOK022/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="mokelumne_flow",
        units="CFS",
    )
    release_american_nimbus = NamedPath(
        name="release_american_nimbus",
        path="/.*/C_NTOMA/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_american_nimbus",
        units="CFS",
    )
    release_clearcreek = NamedPath(
        name="release_clearcreek",
        path="/.*/C_CLR011/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_clearcreek",
        units="CFS",
    )
    release_friant = NamedPath(
        name="release_friant",
        path="/.*/C_MLRTN/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_friant",
        units="CFS",
    )
    release_mcclure = NamedPath(
        name="release_mcclure",
        path="/.*/C_PEDRO/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_mcclure",
        units="CFS",
    )
    release_mendotapool = NamedPath(
        name="release_mendotapool",
        path="/.*/C_MDOTA/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_mendotapool",
        units="CFS",
    )
    release_newdonpedro = NamedPath(
        name="release_newdonpedro",
        path="/.*/C_MCLRE/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_newdonpedro",
        units="CFS",
    )
    release_newmelones = NamedPath(
        name="release_newmelones",
        path="/.*/C_MELON/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_newmelones",
        units="CFS",
    )
    release_oroville = NamedPath(
        name="release_oroville",
        path="/.*/C_OROVL/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_oroville",
        units="CFS",
    )
    release_sacramento_keswick = NamedPath(
        name="release_sacramento_keswick",
        path="/.*/C_KSWCK/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_sacramento_keswick",
        units="CFS",
    )
    release_stanislaus_goodwin = NamedPath(
        name="release_stanislaus_goodwin",
        path="/.*/C_STS059/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_stanislaus_goodwin",
        units="CFS",
    )
    release_trinity = NamedPath(
        name="release_trinity",
        path="/.*/C_LWSTN/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="release_trinity",
        units="CFS",
    )
    sacflowabvfremontweir = NamedPath(
        name="sacflowabvfremontweir",
        path="/.*/C_SAC085/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="sacflowabvfremontweir",
        units="CFS",
    )
    sacflowhood = NamedPath(
        name="sacflowhood",
        path="/.*/C_SAC041/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="sacflowhood",
        units="CFS",
    )
    sacflowredbluff = NamedPath(
        name="sacflowredbluff",
        path="/.*/C_SAC240/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="sacflowredbluff",
        units="CFS",
    )
    sacflowverona = NamedPath(
        name="sacflowverona",
        path="/.*/C_SAC083/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="sacflowverona",
        units="CFS",
    )
    sacflowwilkinsslough = NamedPath(
        name="sacflowwilkinsslough",
        path="/.*/C_SAC097/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="sacflowwilkinsslough",
        units="CFS",
    )
    sacramento_weir_spills = NamedPath(
        name="sacramento_weir_spills",
        path="/.*/SP_SAC066_YBP020/RIVER-SPILLS//.*/.*/",
        category="upstream_flows",
        detail="sacramento_weir_spills",
        units="TAF",
    )
    sjr_qwest_flows = NamedPath(
        name="sjr_qwest_flows",
        path="/.*/C_SJR013/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="sjr_qwest_flows",
        units="CFS",
    )
    sjrupstreammerc = NamedPath(
        name="sjrupstreammerc",
        path="/.*/C_SJR119/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="sjrupstreammerc",
        units="CFS",
    )
    sjrupstreamstan = NamedPath(
        name="sjrupstreamstan",
        path="/.*/C_SJR075/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="sjrupstreamstan",
        units="CFS",
    )
    spring_creek_tunnel = NamedPath(
        name="spring_creek_tunnel",
        path="/.*/D_WKYTN_SPT003/DIVERSION//.*/.*/",
        category="upstream_flows",
        detail="spring_creek_tunnel",
        units="CFS",
    )
    stanislausmouth = NamedPath(
        name="stanislausmouth",
        path="/.*/C_STS030/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="stanislausmouth",
        units="CFS",
    )
    tuolumnemouth = NamedPath(
        name="tuolumnemouth",
        path="/.*/C_TUO003/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="tuolumnemouth",
        units="CFS",
    )
    vernalis_flow = NamedPath(
        name="vernalis_flow",
        path="/.*/C_SJR070/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="vernalis_flow",
        units="CFS",
    )
    verona_closure_term = NamedPath(
        name="verona_closure_term",
        path="/.*/CT_VERONA/CLOSURE-TERM//.*/.*/",
        category="upstream_flows",
        detail="verona_closure_term",
        units="CFS",
    )
    yolo_bypass = NamedPath(
        name="yolo_bypass",
        path="/.*/C_YBP020/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="yolo_bypass",
        units="CFS",
    )
    yubafeatherconfluence = NamedPath(
        name="yubafeatherconfluence",
        path="/.*/C_YUB002/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="yubafeatherconfluence",
        units="CFS",
    )
    sac = NamedPath(
        name="sac",
        path="/.*/WYT_SAC_/WATERYEARTYPE//.*/.*/",
        category="wyt",
        detail="sac",
        units="NONE",
    )
