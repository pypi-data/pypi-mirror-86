import pandas as pd
# import therpy as tp
import scipy.optimize
import scipy.interpolate
import os.path
import os
import urllib.request
import numpy as np

from . import constants
from . import Virial
from . import classes
from . import roots1

cst_LiD2=constants.cst(atom='LiD2')

cst_FG = constants.cst()
cst_FG.c1 = ((cst_FG.twopi * cst_FG.hbar**2)/(cst_FG.mass))**(1/2)
cst_FG.c2 = 1.0/(6*cst_FG.pi**2) * (2*cst_FG.mass/cst_FG.hbar**2)**(3/2)
cst_FG.virial_coef = [1.0, 3.0*2**(1/2)/8, -0.29095295, 0.065]
cst_FG.Critical_Temperature_TF_Mark = 0.167
cst_FG.xi_Mark = 0.367



class Unitary_Fermi_Gas_Mark:
    def __init__(self, ):
        # Download the data if not already
        p_ = roots1.getpath('Projects', 'Data', 'EoS', 'UnitaryFermiGasExperiment_kPEoS.csv')
        if not os.path.isfile(p_):
            print("Downloading Database -- Might take some time!")
            url = 'https://www.dropbox.com/s/8irmfrn2zdvfgba/UnitaryFermiGasExperiment_kPEoS.csv?dl=1'
            u = urllib.request.urlopen(url)
            data = u.read()
            u.close()
            # Create folder
            os.makedirs(os.path.split(p_)[0], exist_ok=True)
            with open(p_, "wb") as f:
                f.write(data)

        # Load Data
        self.df = pd.read_csv(p_)

        # Interpolated Density Data
        x = np.array(self.df['T/T_F'])
        y = np.array(self.df['mu/E_F'])
        # VFG = Virial_Fermi_Gas()

        # c = classes.Curve(x=np.array(VFG.df['T/T_F']), y=np.array(VFG.df['mu/E_F'])).sortbyx().trim(
        #     xlim=[np.max(x), np.max(x) + 0.1])
        muEF_curve = classes.Curve(x=np.concatenate([[0], x]), y=np.concatenate([[cst_FG.xi_Mark], y]))
        TTF = np.linspace(0, muEF_curve.maxx, 10000)
        muEF = muEF_curve(TTF)
        c_muEF_extension = classes.Curve(TTF, muEF)
        density_c_low = scipy.interpolate.interp1d(x=TTF / muEF, y=muEF)
        density_c_high = scipy.interpolate.interp1d(x=muEF[1:] / TTF[1:], y=muEF[1:])
        self.density_c_low = density_c_low
        self.density_c_high = density_c_high
        self.density = np.vectorize(self.density_single)

        # Interpolated Energy Data
        # IFG = Ideal_Fermi_Gas()
        c1 = classes.Curve(np.array(self.df['T/T_F']), np.array(self.df['E/E0']))  # Mark EoS E/E0 vs T/T_F
        # c2 = tp.Curve(np.array(IFG.df['T/T_F']), np.array(IFG.df['P/P0'])).trim(xlim=[c1.maxx + 0.2,
        #                                                                               np.inf])  # Ideal Fermi Gas E/E0 = P/P0 vs T/T_F, from end of Mark EoS to end with some padding for smooth transition

        energy_c = scipy.interpolate.interp1d(x=np.concatenate([[0], c1.x]),
                                              y=np.concatenate([[cst_FG.xi_Mark], c1.y]))
        self.energy_c = energy_c
        self.E_E0 = np.vectorize(self.E_E0_single)
        E2T_fun=scipy.interpolate.interp1d(x=np.concatenate([[cst_FG.xi_Mark], c1.y]),y=np.concatenate([[0], c1.x]),fill_value=None,bounds_error=False)
        self.E2T_fun=E2T_fun
    # Various functions
    def density_single(self, kT, mu):
        # Zero T
        if kT == 0:
            return cst_FG.EF2n(mu / cst_FG.xi_Mark, neg=True)
        if mu / kT > 4:
            return cst_FG.EF2n(mu / self.density_c_low(kT / mu), neg=True)
        if mu / kT > -0.5:
            return cst_FG.EF2n(mu / self.density_c_high(mu / kT), neg=True)
        return None

    def density_hybrid(self, z, kT, mu, trapf=23.35):
        return self.density(kT, mu - 1 / 2 * cst_FG.mass * (2 * np.pi * trapf) ** 2 * z ** 2)

    def E_E0_single(self, TTF):
        if TTF < self.energy_c.x.max():
            return self.energy_c(TTF)
        else:
            # Compute using IFG
            # betamu = self.IFG.TTF_to_betamu(TTF)
            # return (self.IFG.pressure(cst_FG.h, betamu * cst_FG.h) / self.IFG.pressure(0, betamu * cst_FG.h)) + (cst_FG.xi_n-1)
            return self.energy_c.y[-1]

    def E2T(self, ETilde):
        return self.E2T_fun(ETilde)