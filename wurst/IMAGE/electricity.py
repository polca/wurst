from ..searching import *
from . import load_image_data_file, REGIONS
from pathlib import Path
import pandas as pd


def read_pfc_emissions(scenario_base, gas):
    """Read IMAGE results for PFCs.

    ``scenario_base`` is a ``Path`` to the scenario results directory.

    Valid ``gas`` names are: CF4, C2F6, SF6, and C6F14.

    Returns a dataframe with index of years (int) and columns of IMAGE regions (str).

    TODO: Units in dataframe?
    """
    assert isinstance(
        scenario_base, Path
    ), "Must pass a ``pathlib.Path`` as ``scenario_base"
    GASES = ["CF4", "C2F6", "SF6", "C6F14"]
    assert gas in GASES, "Invalid gas"

    fp = scenario_base / "indicatoren" / "EMISPFC_reg.out"
    image_output = load_image_data_file(fp)

    col_index = GASES.index(gas)

    # Easiest way to create a dataframe with the right index and columns
    as_dict = {
        year: {
            a: b for a, b in zip(REGIONS, image_output.data[:, col_index, year_index])
        }
        for year_index, year in enumerate(image_output.years)
    }
    df = pd.DataFrame.from_dict(as_dict, orient="index")
    df["World"] = df.sum(axis=1)
    return df


def get_coal_biosphere_exchanges_to_be_scaled_by_efficiency(ds):
    exclude_list = [
        "Methane, fossil",
        "Sulfur dioxide",
        "Carbon monoxide, fossil",
        "Nitrogen oxides",
        "Dinitrogen monoxide",
        "Particulates",
    ]
    return biosphere(ds, doesnt_contain_any("name", exclude_list))


def get_coal_inputs_to_be_scaled_by_efficiency(ds):
    # These are related to how much NOx & SOx is removed from the exhaust and
    # not the coal input or efficiency.
    # We leave them constant as they are negligible.
    exclude_list = ["market for NOx retained", "market for SOx retained"]
    return technosphere(ds, doesnt_contain_any("name", exclude_list))
