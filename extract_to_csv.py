import sys
import os

import pandas as pd

codedir = "/Users/admin/UDel/FASTLab/Summer2021_Research/SESNspectraPCA/code"
sys.path.insert(0, codedir)
import SNIDdataset as snid


def snid_to_arr(spec):
    """
    Take relevant arrays from a SNIDsn object and return them.

    Arguments
    ---------
    spec : SNIDsn object
        This SNIDsn object contains way more information than just the fluxes,
        wavelengths, and uncertainties that we care about. So, extract them
        separately.

    Returns
    -------
    SNdata : dict
        Dictionary containing arrays for the wavelength bin centers, the flux
        values, the uncertainties on each flux measurement, the phase key
        (epoch) of the supernova, and the name of the supernova.
    """
    flux = spec.data.astype(float)
    wvl = spec.wavelengths.astype(float)
    phase_key = list(spec.smooth_uncertainty.keys())[0]
    err = spec.smooth_uncertainty[phase_key].astype(float)

    SNdata = {
        "wvl": wvl,
        "flux": flux,
        "err": err,
        "phase_key": phase_key,
        "SN": spec.header["SN"]
    }

    return SNdata


def arr_to_csv(SNdata, directory):
    """
    Save wavelength, flux, and uncertainty information in a csv.

    Arguments
    ---------
    SNdata : dict
        Dictionary containing arrays for the wavelength bin centers, the flux
        values, the uncertainties on each flux measurement, the phase key
        (epoch) of the supernova, and the name of the supernova.

    Returns
    -------
    None
    """
    data = {
        "wvl": SNdata["wvl"],
        "flux": SNdata["flux"],
        "err": SNdata["err"]
    }
    df = pd.DataFrame(data, columns=["wvl", "flux", "err"])

    name = SNdata["SN"]
    df.to_csv(os.path.join(directory, f"{name}.csv"), index=False)


def dataset_to_csv(pickle, dataset_dir):
    """
    Convert a pickle file to individual csv files.

    Currently, the stripped envelope supernova data and metadata are in these
    pickle files from the SESNspectraPCA github repo. However, I want them as
    individual csv files. So this function takes in a pickle file, which
    represents a whole bunch of supernovae at a particular epoch, and converts
    them indivudally to csv files and saves them in a chosen directory.

    Arguments
    ---------
    pickle : str
        Path to the pickled dataset of SNIDsn objects.
    dataset_dir
        The directory to save the csv files to.

    Returns
    -------
    None
    """

    dataset = snid.loadPickle(os.path.join(datadir, "dataset0.pickle"))

    if not os.path.isdir(dataset_dir):
        os.mkdir(dataset_dir)

    for sn, spec in dataset.items():
        snid_to_csv(spec, dataset_dir)


csv_dir = os.path.join(codedir, "../wfortino/csv_data")
datadir = os.path.join(codedir, "../Data/DataProducts")

pickle0 = os.path.join(datadir, "dataset0.pickle")
pickle5 = os.path.join(datadir, "dataset5.pickle")
pickle10 = os.path.join(datadir, "dataset10.pickle")
pickle15 = os.path.join(datadir, "dataset15.pickle")

dataset_to_csv(pickle0, os.path.join(csv_dir, "dataset0"))
dataset_to_csv(pickle5, os.path.join(csv_dir, "dataset5"))
dataset_to_csv(pickle10, os.path.join(csv_dir, "dataset10"))
dataset_to_csv(pickle15, os.path.join(csv_dir, "dataset15"))
