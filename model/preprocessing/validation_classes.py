from typing import List, Optional

from pydantic import BaseModel


class DataInputSchema(BaseModel):
    has_gas: Optional[str]
    origin_up: Optional[str]
    price_change_energy: Optional[str]
    cons_12m: Optional[int]
    forecast_cons_12m: Optional[float]
    forecast_discount_energy: Optional[float]
    forecast_meter_rent_12m: Optional[float]
    imp_cons: Optional[float]
    margin_gross_pow_ele: Optional[float]
    nb_prod_act: Optional[int]
    net_margin: Optional[float]
    pow_max: Optional[float]
    price_off_peak_var: Optional[float]
    price_off_peak_fix: Optional[float]
    previous_price: Optional[float]
    price_sens: Optional[float]
    end_year: Optional[int]
    modif_prod_month: Optional[int]
    renewal_year: Optional[int]
    renewal_month: Optional[int]
    diff_act_end: Optional[int]
    diff_act_modif: Optional[int]
    diff_end_modif: Optional[int]
    ratio_last_month_last12m_cons: Optional[float]


class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]
