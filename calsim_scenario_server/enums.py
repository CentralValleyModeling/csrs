import enum

from .schemas import NamedDatasetPath


# Define the assumption types as a Python enumeration
class AssumptionEnum(enum.StrEnum):
    hydrology = "hydrology"
    sea_level_rise = "sea_level_rise"
    land_use = "land_use"
    tucp = "tucp"
    dcp = "dcp"
    va = "va"
    south_of_delta = "south_of_delta"


class DimensionalityEnum(enum.StrEnum):
    volume = "[length] ** 3"
    area = "[length] ** 2"
    length = "[length]"
    flow = "[length] ** 3 / [time]"
    flux = "[length] ** 2 / [time]"
    mass = "[mass]"
    mass_flow = "[mass] / [time]"
    temperature = "[temperature]"


class PathCategoryEnum(enum.StrEnum):
    delivery = "delivery"
    delta = "delta"
    other = "other"
    salinity = "salinity"
    storage = "storage"
    upstream_flows = "upstream_flows"
    water_year_type = "wyt"


class StandardPathsEnum(enum.Enum):
    cvp_allocation_nod_ag = NamedDatasetPath(
        name="cvp_allocation_nod_ag",
        path="",
        category="delivery",
        detail="",
    )
    cvp_allocation_nod_mi = NamedDatasetPath(
        name="cvp_allocation_nod_mi",
        path="/.*/PERDV_CVPMI_SYS/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_allocation_nod_rf = NamedDatasetPath(
        name="cvp_allocation_nod_rf",
        path="/.*/PERDV_CVPRF_SYS/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_allocation_nod_sc = NamedDatasetPath(
        name="cvp_allocation_nod_sc",
        path="/.*/PERDV_CVPSC_SYS/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_allocation_sod_ag = NamedDatasetPath(
        name="cvp_allocation_sod_ag",
        path="/.*/PERDV_CVPAG_S/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_allocation_sod_ex = NamedDatasetPath(
        name="cvp_allocation_sod_ex",
        path="/.*/PERDV_CVPEX_S/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_allocation_sod_mi = NamedDatasetPath(
        name="cvp_allocation_sod_mi",
        path="/.*/PERDV_CVPMI_S/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_allocation_sod_rf = NamedDatasetPath(
        name="cvp_allocation_sod_rf",
        path="/.*/PERDV_CVPRF_S/PERCENT-DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_american = NamedDatasetPath(
        name="cvp_delivery_american",
        path="/.*/DEL_CVP_P_AMER/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_nod = NamedDatasetPath(
        name="cvp_delivery_nod",
        path="/.*/DEL_CVP_TOTAL_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_pag_n = NamedDatasetPath(
        name="cvp_delivery_pag_n",
        path="/.*/DEL_CVP_PAG_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_pag_s = NamedDatasetPath(
        name="cvp_delivery_pag_s",
        path="/.*/DEL_CVP_PAG_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_pex_s = NamedDatasetPath(
        name="cvp_delivery_pex_s",
        path="/.*/DEL_CVP_PEX_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_pmi_n = NamedDatasetPath(
        name="cvp_delivery_pmi_n",
        path="/.*/DEL_CVP_PMI_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_pmi_n_with_amer = NamedDatasetPath(
        name="cvp_delivery_pmi_n_with_amer",
        path="/.*/DEL_CVP_PMI_W_AMER/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_pmi_s = NamedDatasetPath(
        name="cvp_delivery_pmi_s",
        path="/.*/DEL_CVP_PMI_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_prf_n = NamedDatasetPath(
        name="cvp_delivery_prf_n",
        path="/.*/DEL_CVP_PRF_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_prf_s = NamedDatasetPath(
        name="cvp_delivery_prf_s",
        path="/.*/DEL_CVP_PRF_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_psc_n = NamedDatasetPath(
        name="cvp_delivery_psc_n",
        path="/.*/DEL_CVP_PSC_N/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_sod = NamedDatasetPath(
        name="cvp_delivery_sod",
        path="/.*/cvptotaldel/FLOW-DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    cvp_delivery_sod_no_cvc = NamedDatasetPath(
        name="cvp_delivery_sod_no_cvc",
        path="/.*/DEL_CVP_TOTAL_S/DELIVERY-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    short_cvp_tot_n = NamedDatasetPath(
        name="short_cvp_tot_n",
        path="/.*/SHORT_CVP_TOT_N/DELIVERY-SHORTAGE-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    short_cvp_tot_s = NamedDatasetPath(
        name="short_cvp_tot_s",
        path="/.*/SHORT_CVP_TOT_S/DELIVERY-SHORTAGE-CVP//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_co_available = NamedDatasetPath(
        name="swp_co_available",
        path="/.*/co_available_dv/carryover//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_co_est = NamedDatasetPath(
        name="swp_co_est",
        path="/.*/co_est_dv/swp-output//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_co_final = NamedDatasetPath(
        name="swp_co_final",
        path="/.*/co_final_dv/carryover//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_del_target_ta = NamedDatasetPath(
        name="swp_del_target_ta",
        path="/.*/deltar_a_dv/swp-output//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_del_target_ta_co = NamedDatasetPath(
        name="swp_del_target_ta_co",
        path="/.*/deltardv_total/swp-output//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_delivery_co_sod = NamedDatasetPath(
        name="swp_delivery_co_sod",
        path="/.*/swp_CO_total - swp_CO_FEATH - swp_CO_NBAY///.*/.*/",
        category="delivery",
        detail="",
    )
    swp_delivery_in_sod = NamedDatasetPath(
        name="swp_delivery_in_sod",
        path="/.*/swp_IN_total  - swp_IN_FEATH - swp_IN_NBAY///.*/.*/",
        category="delivery",
        detail="",
    )
    swp_delivery_ta_sod = NamedDatasetPath(
        name="swp_delivery_ta_sod",
        path="/.*/swp_TA_total - swp_TA_FEATH - swp_TA_NBAY ///.*/.*/",
        category="delivery",
        detail="",
    )
    swp_delivery_total_frsa = NamedDatasetPath(
        name="swp_delivery_total_frsa",
        path="/.*/swp_TA_FEATH + swp_IN_FEATH + swp_CO_FEATH///.*/.*/",
        category="delivery",
        detail="",
    )
    swp_percent_delivery = NamedDatasetPath(
        name="swp_percent_delivery",
        path="/.*/swp_perdeldv/swp-delivery//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_var_demand_deltar = NamedDatasetPath(
        name="swp_var_demand_deltar",
        path="/.*/vardeltardv/swp-output//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_co_feath = NamedDatasetPath(
        name="swp_co_feath",
        path="/.*/SWP_CO_FEATH/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_co_nbay = NamedDatasetPath(
        name="swp_co_nbay",
        path="/.*/SWP_CO_NBAY/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_co_total = NamedDatasetPath(
        name="swp_co_total",
        path="/.*/swp_CO_total/swp_delivery//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_in_feath = NamedDatasetPath(
        name="swp_in_feath",
        path="/.*/SWP_IN_FEATH/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_in_nbay = NamedDatasetPath(
        name="swp_in_nbay",
        path="/.*/SWP_IN_NBAY/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_in_total = NamedDatasetPath(
        name="swp_in_total",
        path="/.*/swp_IN_total/swp_delivery//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_loss = NamedDatasetPath(
        name="swp_loss",
        path="/.*/SWP_LOSS/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_ta_feath = NamedDatasetPath(
        name="swp_ta_feath",
        path="/.*/SWP_TA_FEATH/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_ta_nbay = NamedDatasetPath(
        name="swp_ta_nbay",
        path="/.*/SWP_TA_NBAY/SWP_DELIVERY//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_ta_total = NamedDatasetPath(
        name="swp_ta_total",
        path="/.*/swp_TA_total/swp_delivery//.*/.*/",
        category="delivery",
        detail="",
    )
    swp_unused_ta_total = NamedDatasetPath(
        name="swp_unused_ta_total",
        path="/.*/unused_totaldv/swp-output//.*/.*/",
        category="delivery",
        detail="",
    )
    banks_cvp_exports = NamedDatasetPath(
        name="banks_cvp_exports",
        path="/.*/C_CAA003_CVP/FLOW-DELIVERY//.*/.*/",
        category="delta",
        detail="",
    )
    banks_export_cross_valley_pumping = NamedDatasetPath(
        name="banks_export_cross_valley_pumping",
        path="/.*/C_CAA003_CVC/FLOW-DELIVERY//.*/.*/",
        category="delta",
        detail="",
    )
    banks_exports = NamedDatasetPath(
        name="banks_exports",
        path="/.*/D_OMR027_CAA000/DIVERSION//.*/.*/",
        category="delta",
        detail="",
    )
    banks_swp_exports = NamedDatasetPath(
        name="banks_swp_exports",
        path="/.*/C_CAA003_SWP/FLOW-DELIVERY//.*/.*/",
        category="delta",
        detail="",
    )
    ccwd = NamedDatasetPath(
        name="ccwd",
        path="/.*/D408/FLOW-DELIVERY//.*/.*/",
        category="delta",
        detail="",
    )
    delta_inflow_ndoi = NamedDatasetPath(
        name="delta_inflow_ndoi",
        path="/.*/DELTAINFLOWFORNDOI/FLOW//.*/.*/",
        category="delta",
        detail="",
    )
    delta_outflow_ndoi = NamedDatasetPath(
        name="delta_outflow_ndoi",
        path="/.*/NDOI/FLOW//.*/.*/",
        category="delta",
        detail="",
    )
    dxc_flow = NamedDatasetPath(
        name="dxc_flow",
        path="/.*/D_SAC030_MOK014/DIVERSION//.*/.*/",
        category="delta",
        detail="",
    )
    excess_outflow_ndoi = NamedDatasetPath(
        name="excess_outflow_ndoi",
        path="/.*/NDOI_ADD/FLOW//.*/.*/",
        category="delta",
        detail="",
    )
    excess_outflow_ann_ndoi = NamedDatasetPath(
        name="excess_outflow_ann_ndoi",
        path="/.*/NDOI_ADD_ANN/FLOW-CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    excess_outflow_cvp_ndoi = NamedDatasetPath(
        name="excess_outflow_cvp_ndoi",
        path="/.*/NDOI_ADD_CVP/FLOW-CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    excess_outflow_swp_ndoi = NamedDatasetPath(
        name="excess_outflow_swp_ndoi",
        path="/.*/NDOI_ADD_SWP/FLOW-CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    flow_at_georgiana_slough = NamedDatasetPath(
        name="flow_at_georgiana_slough",
        path="/.*/C_SAC029B/CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    flow_at_rio_vista = NamedDatasetPath(
        name="flow_at_rio_vista",
        path="/.*/C_SAC017/CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    flow_below_dxc = NamedDatasetPath(
        name="flow_below_dxc",
        path="/.*/C_SAC030/CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    jones_exports = NamedDatasetPath(
        name="jones_exports",
        path="/.*/D_OMR028_DMC000/DIVERSION//.*/.*/",
        category="delta",
        detail="",
    )
    modeled_required_do = NamedDatasetPath(
        name="modeled_required_do",
        path="/.*/MRDO_FINALDV/FLOW-REQ-MRDO//.*/.*/",
        category="delta",
        detail="",
    )
    north_bay_aqueduct = NamedDatasetPath(
        name="north_bay_aqueduct",
        path="/.*/C_CSL004B/CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    old_and_middle_river_flow = NamedDatasetPath(
        name="old_and_middle_river_flow",
        path="/.*/C_OMR014/CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    qwestflow = NamedDatasetPath(
        name="qwestflow",
        path="/.*/QWestFlow/FLOW-CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    required_delta_outflow = NamedDatasetPath(
        name="required_delta_outflow",
        path="/.*/NDOI_MIN/FLOW//.*/.*/",
        category="delta",
        detail="",
    )
    sac_flow_at_freeport = NamedDatasetPath(
        name="sac_flow_at_freeport",
        path="/.*/C_SAC048/CHANNEL//.*/.*/",
        category="delta",
        detail="",
    )
    total_ndd_exports = NamedDatasetPath(
        name="total_ndd_exports",
        path="/.*/EXPORTACTUALIF/EXPORT-PRJ//.*/.*/",
        category="delta",
        detail="",
    )
    total_td_exports = NamedDatasetPath(
        name="total_td_exports",
        path="/.*/EXPORTACTUALTD/EXPORT-PRJ//.*/.*/",
        category="delta",
        detail="",
    )
    banks_export_cross_valley_pumping = NamedDatasetPath(
        name="banks_export_cross_valley_pumping",
        path="/.*/C_CAA003_CVC/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    banks_export_cvp_dedicated = NamedDatasetPath(
        name="banks_export_cvp_dedicated",
        path="/.*/C_CAA003_CVPDED/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    banks_export_fed_share = NamedDatasetPath(
        name="banks_export_fed_share",
        path="/.*/C_CAA003_EXP2/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    banks_export_jpod = NamedDatasetPath(
        name="banks_export_jpod",
        path="/.*/C_CAA003_CVPWHL/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    banks_export_state_share = NamedDatasetPath(
        name="banks_export_state_share",
        path="/.*/C_CAA003_EXP1/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    banks_export_wts = NamedDatasetPath(
        name="banks_export_wts",
        path="/.*/C_CAA003_WTS/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    banks_pp_north_delta = NamedDatasetPath(
        name="banks_pp_north_delta",
        path="/.*/C_CAA003_IF/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    banks_pp_swp_through_delta = NamedDatasetPath(
        name="banks_pp_swp_through_delta",
        path="/.*/C_CAA003_SWP_TD/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    banks_pp_through_delta = NamedDatasetPath(
        name="banks_pp_through_delta",
        path="/.*/C_CAA003_TD/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    dcc_gate_days_open = NamedDatasetPath(
        name="dcc_gate_days_open",
        path="/.*/DXC/GATE-DAYS-OPEN//.*/.*/",
        category="other",
        detail="",
    )
    di_cvp = NamedDatasetPath(
        name="di_cvp",
        path="/.*/DI_CVP_sysdv/DEMAND-INDEX//.*/.*/",
        category="other",
        detail="",
    )
    dmc_inflow_to_mendotapool = NamedDatasetPath(
        name="dmc_inflow_to_mendotapool",
        path="/.*/C_DMC116/CHANNEL//.*/.*/",
        category="other",
        detail="",
    )
    ei_ratio = NamedDatasetPath(
        name="ei_ratio",
        path="/.*/EXPRATIO_/EI-RATIO-STD//.*/.*/",
        category="other",
        detail="",
    )
    hamilton_city_diversion = NamedDatasetPath(
        name="hamilton_city_diversion",
        path="/.*/D_SAC207_GCC007/DIVERSION//.*/.*/",
        category="other",
        detail="",
    )
    jones_export_fed_share = NamedDatasetPath(
        name="jones_export_fed_share",
        path="/.*/C_DMC000_EXP1/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    jones_export_state_share = NamedDatasetPath(
        name="jones_export_state_share",
        path="/.*/C_DMC000_EXP2/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    jones_export_wts = NamedDatasetPath(
        name="jones_export_wts",
        path="/.*/C_DMC000_WTS/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    jones_pp_north_delta = NamedDatasetPath(
        name="jones_pp_north_delta",
        path="/.*/C_DMC000_IF/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    jones_pp_through_delta = NamedDatasetPath(
        name="jones_pp_through_delta",
        path="/.*/C_DMC000_TD/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    net_dicu = NamedDatasetPath(
        name="net_dicu",
        path="/.*/net_DICU/DICU_FLOW//.*/.*/",
        category="other",
        detail="",
    )
    red_bluff_diversion_dam_diversion = NamedDatasetPath(
        name="red_bluff_diversion_dam_diversion",
        path="/.*/D_SAC240_TCC001/DIVERSION//.*/.*/",
        category="other",
        detail="",
    )
    rpa_constraint_banks = NamedDatasetPath(
        name="rpa_constraint_banks",
        path="/.*/maxexp_rpa_SWPdv/EXPORT-LIMIT//.*/.*/",
        category="other",
        detail="",
    )
    rpa_constraint_jones = NamedDatasetPath(
        name="rpa_constraint_jones",
        path="/.*/maxexp_rpa_CVPdv/EXPORT-LIMIT//.*/.*/",
        category="other",
        detail="",
    )
    short_swp_total = NamedDatasetPath(
        name="short_swp_total",
        path="/.*/SHORT_SWP_TOTA/DELIVERY-SHORTAGE-SWP//.*/.*/",
        category="other",
        detail="",
    )
    swp_allocation_frsa = NamedDatasetPath(
        name="swp_allocation_frsa",
        path="/.*/PERDV_SWP_FSC/PERCENT-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    swp_allocation_mi = NamedDatasetPath(
        name="swp_allocation_mi",
        path="/.*/PERDV_SWP_MWD1/PERCENT-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    swp_delivery_int = NamedDatasetPath(
        name="swp_delivery_int",
        path="/.*/DEL_SWP_PIN/DELIVERY-SWP//.*/.*/",
        category="other",
        detail="",
    )
    trinity_export = NamedDatasetPath(
        name="trinity_export",
        path="/.*/D_LWSTN_CCT011/DIVERSION//.*/.*/",
        category="other",
        detail="",
    )
    trinity_export_excess = NamedDatasetPath(
        name="trinity_export_excess",
        path="/.*/D_LWSTN_ADD/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    trinity_export_ops_limit = NamedDatasetPath(
        name="trinity_export_ops_limit",
        path="/.*/TRIN_IMPDV/UNDEFINED//.*/.*/",
        category="other",
        detail="",
    )
    trinity_export_ops_x = NamedDatasetPath(
        name="trinity_export_ops_x",
        path="/.*/D_LWSTN_IMPORT/FLOW-DELIVERY//.*/.*/",
        category="other",
        detail="",
    )
    wsi_cvp = NamedDatasetPath(
        name="wsi_cvp",
        path="/.*/WSI_CVP_sysdv/WATER-SUPPLY-INDEX//.*/.*/",
        category="other",
        detail="",
    )
    bd_ec = NamedDatasetPath(
        name="bd_ec",
        path="/.*/BD_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="",
    )
    ci_ec = NamedDatasetPath(
        name="ci_ec",
        path="/.*/CI_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="",
    )
    co_ec = NamedDatasetPath(
        name="co_ec",
        path="/.*/CO_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="",
    )
    em_ec = NamedDatasetPath(
        name="em_ec",
        path="/.*/EM_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="",
    )
    jp_ec = NamedDatasetPath(
        name="jp_ec",
        path="/.*/JP_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="",
    )
    lv_ec = NamedDatasetPath(
        name="lv_ec",
        path="/.*/LV_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="",
    )
    mr_ec = NamedDatasetPath(
        name="mr_ec",
        path="/.*/MR_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="",
    )
    rs_ec = NamedDatasetPath(
        name="rs_ec",
        path="/.*/RS_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="",
    )
    vi_ec = NamedDatasetPath(
        name="vi_ec",
        path="/.*/VI_EC_MONTH/SALINITY//.*/.*/",
        category="salinity",
        detail="",
    )
    x2_position_prev = NamedDatasetPath(
        name="x2_position_prev",
        path="/.*/X2_PRV/X2-POSITION-PREV//.*/.*/",
        category="salinity",
        detail="",
    )
    folsom_storage = NamedDatasetPath(
        name="folsom_storage",
        path="/.*/S_FOLSM/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    friant_storage = NamedDatasetPath(
        name="friant_storage",
        path="/.*/S_MLRTN/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    mcclure_storage = NamedDatasetPath(
        name="mcclure_storage",
        path="/.*/S_MCLRE/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    new_don_pedro_storage = NamedDatasetPath(
        name="new_don_pedro_storage",
        path="/.*/S_PEDRO/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    new_melones_storage = NamedDatasetPath(
        name="new_melones_storage",
        path="/.*/S_MELON/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    oroville_storage = NamedDatasetPath(
        name="oroville_storage",
        path="/.*/S_OROVL/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    san_luis_storage_cvp = NamedDatasetPath(
        name="san_luis_storage_cvp",
        path="/.*/S_SLUIS_CVP/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    san_luis_storage_swp = NamedDatasetPath(
        name="san_luis_storage_swp",
        path="/.*/S_SLUIS_SWP/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    shasta_storage = NamedDatasetPath(
        name="shasta_storage",
        path="/.*/S_SHSTA/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    sl_cvp_rule_curve = NamedDatasetPath(
        name="sl_cvp_rule_curve",
        path="/.*/CVPRuleCv/rulecurve//.*/.*/",
        category="storage",
        detail="",
    )
    sl_swp_rule_curve = NamedDatasetPath(
        name="sl_swp_rule_curve",
        path="/.*/SWPRuleCv/rulecurve//.*/.*/",
        category="storage",
        detail="",
    )
    trinity_storage = NamedDatasetPath(
        name="trinity_storage",
        path="/.*/S_TRNTY/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    whiskeytown = NamedDatasetPath(
        name="whiskeytown",
        path="/.*/S_WKYTN/STORAGE//.*/.*/",
        category="storage",
        detail="",
    )
    feather_below_thermolito = NamedDatasetPath(
        name="feather_below_thermolito",
        path="/.*/C_FTR059/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    featherflowabvfremontweir = NamedDatasetPath(
        name="featherflowabvfremontweir",
        path="/.*/C_FTR003/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    featherlowflow = NamedDatasetPath(
        name="featherlowflow",
        path="/.*/C_FTR068/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    feathermouth = NamedDatasetPath(
        name="feathermouth",
        path="/.*/C_FTR003/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    featheryubaconfluence = NamedDatasetPath(
        name="featheryubaconfluence",
        path="/.*/C_FTR031/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    fremont_weir_spills = NamedDatasetPath(
        name="fremont_weir_spills",
        path="/.*/SP_SAC083_YBP037/RIVER-SPILLS//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    h_street = NamedDatasetPath(
        name="h_street",
        path="/.*/C_AMR004/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    mercedmouth = NamedDatasetPath(
        name="mercedmouth",
        path="/.*/C_MCD021/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    mokelumne_flow = NamedDatasetPath(
        name="mokelumne_flow",
        path="/.*/C_MOK022/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_american_nimbus = NamedDatasetPath(
        name="release_american_nimbus",
        path="/.*/C_NTOMA/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_clearcreek = NamedDatasetPath(
        name="release_clearcreek",
        path="/.*/C_CLR011/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_friant = NamedDatasetPath(
        name="release_friant",
        path="/.*/C_MLRTN/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_mcclure = NamedDatasetPath(
        name="release_mcclure",
        path="/.*/C_PEDRO/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_mendotapool = NamedDatasetPath(
        name="release_mendotapool",
        path="/.*/C_MDOTA/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_newdonpedro = NamedDatasetPath(
        name="release_newdonpedro",
        path="/.*/C_MCLRE/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_newmelones = NamedDatasetPath(
        name="release_newmelones",
        path="/.*/C_MELON/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_oroville = NamedDatasetPath(
        name="release_oroville",
        path="/.*/C_OROVL/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_sacramento_keswick = NamedDatasetPath(
        name="release_sacramento_keswick",
        path="/.*/C_KSWCK/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_stanislaus_goodwin = NamedDatasetPath(
        name="release_stanislaus_goodwin",
        path="/.*/C_STS059/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    release_trinity = NamedDatasetPath(
        name="release_trinity",
        path="/.*/C_LWSTN/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sacflowabvfremontweir = NamedDatasetPath(
        name="sacflowabvfremontweir",
        path="/.*/C_SAC085/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sacflowhood = NamedDatasetPath(
        name="sacflowhood",
        path="/.*/C_SAC041/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sacflowredbluff = NamedDatasetPath(
        name="sacflowredbluff",
        path="/.*/C_SAC240/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sacflowverona = NamedDatasetPath(
        name="sacflowverona",
        path="/.*/C_SAC083/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sacflowwilkinsslough = NamedDatasetPath(
        name="sacflowwilkinsslough",
        path="/.*/C_SAC097/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sacramento_weir_spills = NamedDatasetPath(
        name="sacramento_weir_spills",
        path="/.*/SP_SAC066_YBP020/RIVER-SPILLS//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sjr_qwest_flows = NamedDatasetPath(
        name="sjr_qwest_flows",
        path="/.*/C_SJR013/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sjrupstreammerc = NamedDatasetPath(
        name="sjrupstreammerc",
        path="/.*/C_SJR119/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sjrupstreamstan = NamedDatasetPath(
        name="sjrupstreamstan",
        path="/.*/C_SJR075/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    spring_creek_tunnel = NamedDatasetPath(
        name="spring_creek_tunnel",
        path="/.*/D_WKYTN_SPT003/DIVERSION//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    stanislausmouth = NamedDatasetPath(
        name="stanislausmouth",
        path="/.*/C_STS030/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    tuolumnemouth = NamedDatasetPath(
        name="tuolumnemouth",
        path="/.*/C_TUO003/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    vernalis_flow = NamedDatasetPath(
        name="vernalis_flow",
        path="/.*/C_SJR070/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    verona_closure_term = NamedDatasetPath(
        name="verona_closure_term",
        path="/.*/CT_VERONA/CLOSURE-TERM//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    yolo_bypass = NamedDatasetPath(
        name="yolo_bypass",
        path="/.*/C_YBP020/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    yubafeatherconfluence = NamedDatasetPath(
        name="yubafeatherconfluence",
        path="/.*/C_YUB002/CHANNEL//.*/.*/",
        category="upstream_flows",
        detail="",
    )
    sac = NamedDatasetPath(
        name="sac",
        path="/.*/WYT_SAC_/WATERYEARTYPE//.*/.*/",
        category="wyt",
        detail="",
    )
