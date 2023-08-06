import sys
import copy
import warnings
from pathlib import Path
import fnmatch

import numpy as np
from scipy.interpolate import interp1d, interp2d

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import AnchoredText
import datetime

# try to import seaborn
try:
    sns_flag = True
    import seaborn as sns
except:
    sns_flag = False

# try to import cartopy
try:
    map_flag = True
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
except:
    map_flag = False

# soft attempt to load gsw, but allow for seawater as well
try: 
    import gsw
    flagSA = True
except:
    try:
        # if this also fails, just load gsw to throw the error
        from seawater import pden
        flagSA = False
        warnings.warn('gsw package for thermodynamic equations of seawater not installed, attempting to load seawater package, however seawater is deprecated in favour of gsw-python, see https://teos-10.github.io/GSW-Python/\n')
    except:
        import gsw

from netCDF4 import Dataset

from . import io
from . import interp
from . import unit
from . import util
from . import fplt

# ----------------------------------------------------------------------------
# LOCAL MACHINE SETUP
# ----------------------------------------------------------------------------

ARGO_PATH = './'
WOA_PATH  = None
NCEP_PATH = None

__bgcindex__ = io.read_index()
global REF_PATH
REF_PATH = Path(__file__).parent.absolute() / 'ref'

def set_dirs(argo_path=ARGO_PATH, woa_path=WOA_PATH, ncep_path=NCEP_PATH):
    '''
    Set local directories to look for Argo, WOA, and NCEP data.

    Args:
        argo_path (str or path-like): location of local Argo data
        woa_path (str or path-like): location of local World Ocean Atlas data
        ncep_data (str or path-like): location of local NCEP data
    '''

    global ARGO_PATH
    ARGO_PATH = argo_path
    global WOA_PATH
    WOA_PATH  = woa_path
    global NCEP_PATH
    NCEP_PATH = ncep_path

def get_index(index='bgc'):
    '''
    Get the global, biogeochemical, synthetic, or metadata Argo index. 

    Args:
        index (str): *bgc* for the biogeochemical Argo index, *global* for the core index, *synthetic* for the synthetic index, or *meta* for the metadata index
    '''
    if index == 'bgc':
        return __bgcindex__
    elif index == 'global':
        if '__globalindex__' not in globals():
            global __globalindex__
            __globalindex__ = io.read_index(mission='C')
        return __globalindex__
    elif index == 'synthetic':
        if '__synthindex__' not in globals():
            global __synthindex__
            __synthindex__ = io.read_index(mission='S')
        return __synthindex__
    elif index == 'synthetic':
        if '__synthindex__' not in globals():
            global __metaindex__
            __metaindex__ = io.read_index(mission='M')
        return __metaindex__
    else:
        raise ValueError('Input "{}" is unrecognized'.format(index))

# ----------------------------------------------------------------------------
# FLOAT CLASS
# ----------------------------------------------------------------------------

class sprof:
    '''
    Class that loads Argo synthetic profile data for a given float ID number
    (wmo). 
    
    Uses locally downloaded files, which should be setup using the `set_dirs` 
    method::

        sprof.set_dirs(
            argo_path='/data/path/Argo', 
            ncep_path='/data/path/NCEP',
            woa_path='/data/path/WOA18'
        )

    Then, load the individual variables into fields in the class, for
    example::

        syn = sprof(wmo)
        print(syn.DOXY)
    '''

    
    set_dirs = set_dirs

    def __init__(self, wmo, keep_fillvalue=False, rcheck=True):

        self.__floatdict__, self.__Sprof__, self.__BRtraj__, self.__meta__ = load_argo(ARGO_PATH, wmo, grid=True)
        self.__rawfloatdict__ = self.__floatdict__

        # local path info
        self.argo_path = ARGO_PATH
        self.woa_path  = WOA_PATH
        self.ncep_path = NCEP_PATH

        self.assign(self.__floatdict__)
        if not keep_fillvalue:
            self.rm_fillvalue()

        if rcheck:
            self.check_range('DOXY')

    def assign(self, floatdict):
        '''
        Assign variables from float dictionary (output of load_argo(...))
        to synthetic profile sprof() object.
        '''

        # metadata and dimension variables
        self.floatName  = floatdict['floatName']
        self.floatType  = floatdict['floatType']
        self.N_CYCLES   = floatdict['N_CYCLES']
        self.N_LEVELS   = floatdict['N_LEVELS']
        self.CYCLE      = floatdict['CYCLES']
        self.CYCLE_GRID = floatdict['CYCLE_GRID']

        # time and location data
        self.SDN       = floatdict['SDN']
        self.SDN_GRID  = floatdict['SDN_GRID']
        self.LATITUDE  = floatdict['LATITUDE']
        self.LATITUDE_GRID = floatdict['LATITUDE_GRID']
        self.LONGITUDE = floatdict['LONGITUDE']
        self.LONGITUDE_GRID = floatdict['LONGITUDE_GRID']

        self.WMO = floatdict['WMO']

        # core variables
        self.PRES    = floatdict['PRES']
        self.PRES_QC = floatdict['PRES_QC']
        self.TEMP    = floatdict['TEMP']
        self.TEMP_QC = floatdict['TEMP_QC']
        self.PSAL    = floatdict['PSAL']
        self.PSAL_QC = floatdict['PSAL_QC']
        # potential density
        if flagSA:
            self.PDEN = gsw.pot_rho_t_exact(gsw.SA_from_SP(self.PSAL, self.PRES, self.LONGITUDE_GRID, self.LATITUDE_GRID), self.TEMP, self.PRES, 0) - 1000
        else:
            self.PDEN = pden(self.PSAL, self.TEMP, self.PRES, 0) - 1000

        # bgc variables - not necessarily all there so check if the fields exist
        if 'DOXY' in floatdict.keys():
            self.DOXY      = floatdict['DOXY']
            self.DOXY_QC   = floatdict['DOXY_QC']
        if 'CHLA' in floatdict.keys():
            self.CHLA      = floatdict['CHLA']
            self.CHLA_QC   = floatdict['CHLA_QC']
        if 'BBP700' in floatdict.keys():
            self.BBP700    = floatdict['BBP700']
            self.BBP700_QC = floatdict['BBP700_QC']
        if 'CDOM' in floatdict.keys():
            self.CDOM      = floatdict['CDOM']
            self.CDOM_QC   = floatdict['CDOM_QC']
        
        # adjusted variables
        if 'DOXY_ADJUSTED' in floatdict.keys():
            self.DOXY_ADJUSTED      = floatdict['DOXY_ADJUSTED']
            self.DOXY_ADJUSTED_QC   = floatdict['DOXY_ADJUSTED_QC']
        if 'CHLA_ADJUSTED' in floatdict.keys():
            self.CHLA_ADJUSTED      = floatdict['CHLA_ADJUSTED']
            self.CHLA_ADJUSTED_QC   = floatdict['CHLA_ADJUSTED_QC']
        if 'BBP700_ADJUSTED' in floatdict.keys():
            self.BBP700_ADJUSTED    = floatdict['BBP700_ADJUSTED']
            self.BBP700_ADJUSTED_QC = floatdict['BBP700_ADJUSTED_QC']
        if 'CDOM_ADJUSTED' in floatdict.keys():
            self.CDOM_ADJUSTED      = floatdict['CDOM_ADJUSTED']
            self.CDOM_ADJUSTED_QC   = floatdict['CDOM_ADJUSTED_QC']

        if 'O2Sat' in floatdict.keys():
            self.O2Sat = floatdict['O2Sat']
            self.O2Sat_QC = floatdict['O2Sat_QC']

    def rm_fillvalue(self):
        '''
        Remove FillValue from all variables.
        '''
        self.__nofillvaluefloatdict__ = dict_fillvalue_clean(self.__rawfloatdict__)
        self.__floatdict__ = copy.deepcopy(self.__nofillvaluefloatdict__)
        self.assign(self.__nofillvaluefloatdict__)

    def clean(self, bad_flags=None):
        '''
        Remove bad data from all variables, using <PARAM>_QC to determine bad data. 
        Optional input `bad_flags` can be used to specify which flag values are bad,
        with a default bad flags set to be 4, 6, 7.
        '''
        self.__cleanfloatdict__ = dict_clean(self.__floatdict__, bad_flags=bad_flags)
        self.__floatdict__ = copy.deepcopy(self.__cleanfloatdict__)
        self.assign(self.__cleanfloatdict__)

    def reset(self):
        '''
        Reset all variables back to original loaded variables. Undoes the effect of
        clean(), rm_fillvalue(), check_range().
        '''
        self.__floatdict__ = copy.deepcopy(self.__rawfloatdict__)
        self.assign(self.__rawfloatdict__)

    def check_range(self, key):
        '''
        Performs a range check for variables that have a RTQC range available.
        Replaces values outside the range with NaN values. Takes string input
        to do the range check on that variable. Available variables are
        PRES, TEMP, PSAL, and DOXY. Can also take input 'all' to do the range
        check on all four variables, or a list of strings to do each of those
        variables.
        '''
        if key == 'all':
            key = ['PRES', 'TEMP', 'PSAL', 'DOXY']
        elif type(key) is not list:
            key = [key]
        
        for k in key:
            self.__rangecheckdict__ = range_check(k, self.__floatdict__)
            self.__floatdict__ = self.__rangecheckdict__

            # recalculate O2sat if its DOXY
            if k == 'DOXY':
                self.__rangecheckdict__['O2Sat'] = 100*self.__rangecheckdict__['DOXY']/unit.oxy_sol(self.__rangecheckdict__['PSAL'], self.__rangecheckdict__['TEMP'], unit='micromole/kg')

        self.assign(self.__rangecheckdict__)
    
    def to_dict(self):
        '''
        Returns a deepcopy of __floatdict__, which is the currect active
        dictionary (i.e. subject to the effects of clean(), reset(), etc.)
        '''
        return copy.deepcopy(self.__floatdict__)
    
    def to_dataframe(self):
        '''
        Returns a pandas dataframe containing data from the synthetic oxygen
        profile file.
        '''
        import pandas as pd

        df = pd.DataFrame()
        df['CYCLE']     = self.CYCLE_GRID
        df['SDN']       = self.SDN_GRID
        df['LATITUDE']  = self.LATITUDE_GRID
        df['LONGITUDE'] = self.LONGITUDE_GRID
        df['PRES']      = self.PRES
        df['TEMP']      = self.TEMP
        df['PSAL']      = self.PSAL
        df['PDEN']      = self.PDEN
        if 'DOXY' in self.__floatdict__.keys():
            df['DOXY']      = self.DOXY
        if 'CHLA' in self.__floatdict__.keys():
            df['CHLA']      = self.CHLA
        if 'BBP700' in self.__floatdict__.keys():
            df['BBP700']    = self.BBP700
        if 'CDOM' in self.__floatdict__.keys():
            df['CDOM']      = self.CDOM
        if 'DOXY_ADJUSTED' in self.__floatdict__.keys():
            df['DOXY_ADJUSTED']      = self.DOXY_ADJUSTED
        if 'CHLA_ADJUSTED' in self.__floatdict__.keys():
            df['CHLA_ADJUSTED']      = self.CHLA_ADJUSTED
        if 'BBP700_ADJUSTED' in self.__floatdict__.keys():
            df['BBP700_ADJUSTED']    = self.BBP700_ADJUSTED
        if 'CDOM_ADJUSTED' in self.__floatdict__.keys():
            df['CDOM_ADJUSTED']      = self.CDOM_ADJUSTED
        if 'O2Sat' in self.__floatdict__.keys():
            df['O2Sat']      = self.O2Sat

        self.df = df

        return copy.deepcopy(self.df)

    def get_track(self):
        '''
        Creates a track array with columns::

            [serial datenum, latitude, longitude]

        the track array is used for the interpolation of reference data along
        the float track.
        '''
        self.track = track(self.__floatdict__)

        return copy.deepcopy(self.track)

    def get_ncep(self):
        '''
        Loads NCEP data along the float track
        '''

        if not hasattr(self, 'track'):
            self.get_track()

        self.NCEP, self.__NCEPweights__ = ncep_to_float_track('pres', self.track, local_path=self.ncep_path)
        
        return copy.deepcopy(self.NCEP)

    def get_woa(self):
        '''
        Loads WOA data along the float track
        '''

        if not hasattr(self, 'track'):
            self.get_track()
        
        self.z_WOA, self.WOA, self.__WOAweights__ = woa_to_float_track(self.track, 'O2sat', local_path=self.woa_path)

        return copy.deepcopy(self.WOA)

    def calc_gains(self, ref='NCEP', zlim=25.):
        '''
        Calculate gain values using NCEP or WOA reference data. Uses function
        calc_gain(). 
        '''

        if not hasattr(self, 'track'):
            self.get_track()

        if ref == 'NCEP':
            # check if reference data is already calculated
            if not hasattr(self, 'NCEP'):
                self.get_ncep()

            pH2O = unit.pH2O(util.get_var_by('TEMP_DOXY', 'TRAJ_CYCLE', self.__floatdict__))

            common_cycles, c1, c2 = np.intersect1d(self.CYCLE, np.unique(self.__floatdict__['TRAJ_CYCLE']), assume_unique=True, return_indices=True)

            self.NCEP_PPOX = unit.atmos_pO2(self.NCEP[c1], pH2O[c2])/100
            self.__NCEPgains__, self.__NCEPfloatref__ = calc_gain(self.__floatdict__, self.NCEP_PPOX)
            self.gains = self.__NCEPgains__

        if ref == 'WOA':
            # check if reference data is already calculated
            if not hasattr(self, 'WOA'):
                self.get_woa()

            self.__WOAgains__, self.__WOAfloatref__, self.__WOAref__ = calc_gain(self.__floatdict__, dict(z=self.z_WOA, WOA=self.WOA), inair=False, zlim=zlim)
            self.gains = self.__WOAgains__
        
        return copy.deepcopy(self.gains)

    def calc_fixed_error(self, fix_err=10):

        self.DOXY_ADJUSTED_ERROR = calc_fixed_doxy_adjusted_error(self.__floatdict__, fix_err=fix_err)
        self.__floatdict__['DOXY_ADJUSTED_ERROR'] = self.DOXY_ADJUSTED_ERROR

        return copy.deepcopy(self.DOXY_ADJUSTED_ERROR)

    def plot(self, kind, **kwargs):

        if kind == 'gain':
            ref = kwargs['ref']
            if ref == 'NCEP':
                g = fplt.gainplot(self.SDN, self.__NCEPfloatref__[:,2], self.NCEP_PPOX, self.__NCEPgains__, ref)
            elif ref == 'WOA':
                g = fplt.gainplot(self.SDN, self.__WOAfloatref__[:,2], self.__WOAref__, self.__WOAgains__, ref)

        elif kind == 'cscatter':
            var = kwargs.pop('varname')

            if not hasattr(self, 'df'):
                self.to_dataframe()

            g = fplt.var_cscatter(self.df, varname=var, **kwargs)

        elif kind == 'profiles':
            varlist = kwargs.pop('varlist')

            if not hasattr(self, 'df'):
                self.to_dataframe()

            g = fplt.profiles(self.df, varlist=varlist, **kwargs)

        else:
            raise ValueError('Invalid input for keyword argument "kind"')

        return g


    def describe(self):
        '''
        Describe the dataframe of data stored in the sprof object.
        '''

        if not hasattr(self, 'df'):
            self.to_dataframe()
        
        print('Data for synthetic profile file for float {}'.format(self.WMO))

        sys.stdout.write('Variables:\n')
        for k in self.__floatdict__.keys():
            sys.stdout.write('{}\n'.format(k))
        sys.stdout.write('\n')

    def add_independent_data(self, date=None, lat=None, lon=None, data_dict=None, label=None, **kwargs):
        '''
        Add independent data in order to easily plot and compare.

        Args:
            date (optional, str, float, or date):
                Date as a string ('YYYY-MM-DD'), serial datenumber, or python
                date object. 
            data_dict(optional, dict): 
                Dictionary containing variables to be added, key names should
                match the naming convention to Argo variables
            label (optional, str):
                Label or name of the dataset being added, important when adding
                more than one source of independent data
            **kwargs:
                Argo variable names and their values, essentailly the same as
                inputting a dictionary without having to actually build one

        Returns:
            None
        
        Example::
            syn = sprof(wmo_number)
            df = pd.read_csv('my_winkler_data.csv')

            syn.add_independent_data(
                date='2020-10-04', # metadata arguments, optional, if no date matches to first profile
                label='Winkler' # label to classify the data - for if you have more than one source
                PRES=df.pressure, # data arguments, match naming to Argo variables
                DOXY=df.dissolved_oxygen,
                LATITUDE=df.lat, LONGITUDE=df.lon, # again, optional
            )

            data = dict(PRES=df.PRES, DOXY=df.DOXY)
            syn.add_independent_data(data_dict=data, date='2020-10-04')
        '''

        if type(date) is str:
            date = mdates.datestr2num(date)
        if type(date) is datetime.datetime:
            date = mdates.date2num(date)

        meta_dict = dict(date=date)
        if lat is None:
            lat = np.nan
        if lon is None:
            lon = np.nan
        meta_dict['lat'] = lat
        meta_dict['lon'] = lon

        if data_dict is None:
            data_dict = dict(**kwargs)
        elif data_dict is not None and len(kwargs) > 0:
            # apppend kwargs to dict
            for k in kwargs.keys():
                data_dict[k] = kwargs[k]

        # default label value        
        if label is None:
            label = ' '
        # if there isn't already independent data, make a dict for it
        if not hasattr(self, '__indepdict__'):
            self.__indepdict__ = {label:data_dict}
            self.__indepmeta__ = {label:meta_dict}
        # if there is one already, append to it
        else:
            self.__indepdict__[label] = data_dict
            self.__indepmeta__[label] = meta_dict

    def compare_independent_data(self, fmt='*', **kwargs):
        '''
        Plot the independent data overtop of the nearest profile in time
        '''

        if not hasattr(self, 'df'):
            self.df = self.to_dataframe()

        plot_dict = copy.deepcopy(self.__indepdict__)
        meta_dict = copy.deepcopy(self.__indepmeta__)

        var_keys = []
        for label in plot_dict.keys():
            var_keys = var_keys + list(plot_dict[label].keys())
        var_keys = list(set(var_keys))
        var_keys.remove('PRES')

        meta_keys = []
        for label in meta_dict.keys():
            meta_keys = meta_keys + list(meta_dict[label].keys())
        meta_keys = set(meta_keys)

        meta_data_string = ''
        for label in meta_dict.keys():
            if label == ' ':
                label = 'Observation'

            if meta_dict[label]['date'] is None:
                cyc = 1
                dstr = 'N/A'
            else:
                cyc = util.cycle_from_time(meta_dict[label]['date'], self.SDN, self.CYCLE)
                dstr = mdates.num2date(meta_dict[label]['date']).strftime('%b %d, %Y')

            meta_data_string = meta_data_string + '{} date: {}\n'.format(label, dstr)
        meta_data_string = meta_data_string + 'Argo profile #{} date: {}'.format(cyc, mdates.num2date(self.SDN[self.CYCLE == cyc][0]).strftime('%b %d, %Y'))

        map_num = 0
        if 'lat' in meta_keys and 'lon' in meta_keys:
            map_num = 1 # change to 1 later, just broken right now
        
        nvar = len(set(var_keys))
        fig = plt.figure()
        ax_list = [fig.add_subplot(1, nvar+map_num, n+1) for n in range(nvar)]
        axes_dict = {v:ax for v, ax in zip(var_keys, ax_list)}
        print(var_keys)
        print(ax_list)
        if map_num > 0:
            ax_list.append(fig.add_subplot(1, nvar+map_num, nvar+1, projection=ccrs.PlateCarree()))
        
        ccount = 0
        if sns_flag:
            fcol = sns.color_palette('colorblind')[0]
            clist = sns.color_palette('colorblind')[1:]
        else:
            fcol = 'blue'
            clist = ['orange', 'green', 'cyan', 'red']
        
        for label in plot_dict.keys():
            pres = plot_dict[label].pop('PRES')

            if meta_dict[label]['date'] is None:
                cyc = 1
            else:
                cyc = util.cycle_from_time(meta_dict[label]['date'], self.SDN, self.CYCLE)

            varlist = list(plot_dict[label].keys())

            for v in varlist:
                fplt.profiles(self.df, varlist=[v], axes=axes_dict[v], Ncycle=cyc)
                axes_dict[v].plot(plot_dict[label][v], pres, fmt, label=None, color=clist[ccount])
            
            ax_list[0].plot(np.nan, np.nan, fmt, color=clist[ccount], label=label)
            ccount += 1

        ccount = 0
        if map_num > 0:
            c = []
            mx = ax_list[-1]
            dist_str = ''
            for label in meta_dict.keys():
                if meta_dict[label]['date'] is None:
                    cyc = 1
                else:
                    cyc = util.cycle_from_time(meta_dict[label]['date'], self.SDN, self.CYCLE)
                c1 = (meta_dict[label]['lat'], meta_dict[label]['lon'])
                c2 = (np.nanmean(self.LATITUDE[self.CYCLE == cyc]), np.nanmean(self.LONGITUDE[self.CYCLE == cyc]))
                c.append(c1)
                c.append(c2)
                mx.plot(c1[1], c1[0], fmt, transform=ccrs.PlateCarree(), label=label, color=clist[ccount])
                dist_str = dist_str + '\n{:.1f}km ({}) '.format(util.haversine(c1,c2), label)
                ccount += 1
            
                mx.plot(c2[1], c2[0], 'o', color=fcol, label=None, transform=ccrs.PlateCarree())
            mx.plot(np.nan, np.nan, 'o', color=fcol, label='Float {}'.format(self.WMO))

            c = np.array(c)
            print(c)
            minlon, maxlon = np.nanmin(c[:,1]), np.nanmax(c[:,1])
            minlat, maxlat = np.nanmin(c[:,0]), np.nanmax(c[:,0])

            extent = [minlon, maxlon, minlat, maxlat]
            for i in range(len(extent)):
                if extent[i] < 0 and i % 2 == 0:
                    extent[i] = 1.1*extent[i]
                elif extent[i] < 0 and i % 2 != 0:
                    extent[i] = 0.9*extent[i]
                elif extent[i] > 0 and i % 2 == 0:
                    extent[i] = 0.9*extent[i]
                elif extent[i] > 0 and i % 2 != 0:
                    extent[i] = 1.1*extent[i]
            

            extent[2] = extent[2] - 6
            extent[3] = extent[3] + 6

            print(extent)
            mx.set_extent(extent, crs=ccrs.PlateCarree())
            mx.legend(loc=4, bbox_to_anchor=(1.05, 1.0), fontsize=8)
            mx.add_feature(cfeature.COASTLINE)
            mx.add_feature(cfeature.BORDERS)
            mx.add_feature(cfeature.OCEAN)
            mx.add_feature(cfeature.LAND)
            mx.add_feature(cfeature.RIVERS)

            anc = AnchoredText('Distance between obs and float: ' + dist_str,
                loc=1, frameon=True, prop=dict(size=8))
            mx.add_artist(anc)
        
        if map_num == 0 and len(ax_list) > 1:
            for ax in ax_list[1:]:
                ax.set_title('')
                ax.set_ylabel('')
                ax.set_yticklabels([])
        elif map_num == 1 and len(ax_list) > 2:
            for ax in ax_list[1:-1]:
                ax.set_title('')
                ax.set_ylabel('')
                ax.set_yticklabels([])

        ax_list[0].legend(loc=2, fontsize=10)

        print(meta_data_string)

        anc = AnchoredText(meta_data_string,
                loc=4, frameon=True, prop=dict(size=8))
        ax_list[0].add_artist(anc)

        return fig, ax_list

class profiles:

    set_dirs = set_dirs

    def __init__(self, floats, cycles=None, mission='B', mode='RD', keep_fillvalue=False, rcheck=True):
        if type(floats) is int:
            floats = [floats]

        self.__argofiles__ = organize_files(get_files(ARGO_PATH, floats, cycles=cycles, mission=mission, mode=mode))
        self.__floatdict__ = load_profiles(self.__argofiles__)
        self.__rawfloatdict__ = self.__floatdict__

        # local path info
        self.argo_path = ARGO_PATH
        self.woa_path  = WOA_PATH
        self.ncep_path = NCEP_PATH

        self.assign(self.__floatdict__)
        if not keep_fillvalue:
            self.rm_fillvalue()

        if rcheck:
            self.check_range('DOXY')

    def assign(self, floatdict):

        # metadata and dimension variables
        self.floatName  = floatdict['floatName']
        self.floatType  = floatdict['floatType']
        self.N_LEVELS   = floatdict['N_LEVELS']
        self.CYCLE      = floatdict['CYCLES']
        self.CYCLE_GRID = floatdict['CYCLE_GRID']

        # time and location data
        self.SDN       = floatdict['SDN']
        self.SDN_GRID  = floatdict['SDN_GRID']
        self.LATITUDE  = floatdict['LATITUDE']
        self.LATITUDE_GRID  = floatdict['LATITUDE_GRID']
        self.LONGITUDE = floatdict['LONGITUDE']
        self.LONGITUDE_GRID = floatdict['LONGITUDE_GRID']

        self.WMO = floatdict['WMO']

        # core variables
        self.PRES    = floatdict['PRES']
        # self.PRES_QC = floatdict['PRES_QC']
        if 'TEMP' in floatdict.keys():
            self.TEMP    = floatdict['TEMP']
            self.TEMP_QC = floatdict['TEMP_QC']
            self.PSAL    = floatdict['PSAL']
            self.PSAL_QC = floatdict['PSAL_QC']
            # potential density
            if flagSA:
                self.PDEN = gsw.pot_rho_t_exact(gsw.SA_from_SP(self.PSAL, self.PRES, self.LONGITUDE_GRID, self.LATITUDE_GRID), self.TEMP, self.LONGITUDE_GRID, self.LATITUDE_GRID) - 1000
            else:
                self.PDEN = pden(self.PSAL, self.TEMP, self.PRES, 0) - 1000

        # bgc variables - not necessarily all there so check if the fields exist
        if 'DOXY' in floatdict.keys():
            self.DOXY      = floatdict['DOXY']
            self.DOXY_QC   = floatdict['DOXY_QC']
        if 'CHLA' in floatdict.keys():
            self.CHLA      = floatdict['CHLA']
            self.CHLA_QC   = floatdict['CHLA_QC']
        if 'BBP700' in floatdict.keys():
            self.BBP700    = floatdict['BBP700']
            self.BBP700_QC = floatdict['BBP700_QC']
        if 'CDOM' in floatdict.keys():
            self.CDOM      = floatdict['CDOM']
            self.CDOM_QC   = floatdict['CDOM_QC']
        
        # adjusted variables
        if 'DOXY_ADJUSTED' in floatdict.keys():
            self.DOXY_ADJUSTED      = floatdict['DOXY_ADJUSTED']
            self.DOXY_ADJUSTED_QC   = floatdict['DOXY_ADJUSTED_QC']
        if 'CHLA_ADJUSTED' in floatdict.keys():
            self.CHLA_ADJUSTED      = floatdict['CHLA_ADJUSTED']
            self.CHLA_ADJUSTED_QC   = floatdict['CHLA_ADJUSTED_QC']
        if 'BBP700_ADJUSTED' in floatdict.keys():
            self.BBP700_ADJUSTED    = floatdict['BBP700_ADJUSTED']
            self.BBP700_ADJUSTED_QC = floatdict['BBP700_ADJUSTED_QC']
        if 'CDOM_ADJUSTED' in floatdict.keys():
            self.CDOM_ADJUSTED      = floatdict['CDOM_ADJUSTED']
            self.CDOM_ADJUSTED_QC   = floatdict['CDOM_ADJUSTED_QC']

        if 'O2Sat' in floatdict.keys():
            self.O2Sat = floatdict['O2Sat']
            self.O2Sat_QC = floatdict['O2Sat_QC']

    def rm_fillvalue(self):
        self.__nofillvaluefloatdict__ = dict_fillvalue_clean(self.__rawfloatdict__)
        self.__floatdict__ = self.__nofillvaluefloatdict__
        self.assign(self.__nofillvaluefloatdict__)

    def clean(self, bad_flags=None):
        self.__cleanfloatdict__ = dict_clean(self.__floatdict__, bad_flags=bad_flags)
        self.__floatdict__ = self.__cleanfloatdict__
        self.assign(self.__cleanfloatdict__)

    def reset(self):
        self.__floatdict__ = self.__rawfloatdict__
        self.assign(self.__rawfloatdict__)

    def check_range(self, key):
        '''
        Performs a range check for variables that have a RTQC range available.
        Replaces values outside the range with NaN values. Takes string input
        to do the range check on that variable. Available variables are
        PRES, TEMP, PSAL, and DOXY. Can also take input 'all' to do the range
        check on all four variables, or a list of strings to do each of those
        variables.
        '''
        if key == 'all':
            key = ['PRES', 'TEMP', 'PSAL', 'DOXY']
        elif type(key) is not list:
            key = [key]
        
        for k in key:
            self.__rangecheckdict__ = range_check(k, self.__floatdict__)
            self.__floatdict__ = self.__rangecheckdict__

            # recalculate O2sat if its DOXY
            if k == 'DOXY':
                self.__rangecheckdict__['O2Sat'] = 100*self.__rangecheckdict__['DOXY']/unit.oxy_sol(self.__rangecheckdict__['PSAL'], self.__rangecheckdict__['TEMP'], unit='micromole/kg')

        self.assign(self.__rangecheckdict__)
             
    def to_dict(self):
        return copy.deepcopy(self.__floatdict__)
    
    def to_dataframe(self):
        import pandas as pd

        df = pd.DataFrame()
        df['CYCLE']     = self.CYCLE_GRID
        df['SDN']       = self.SDN_GRID
        df['WMO']       = self.WMO
        df['LATITUDE']  = self.LATITUDE_GRID
        df['LONGITUDE'] = self.LONGITUDE_GRID
        df['PRES']      = self.PRES
        df['TEMP']      = self.TEMP
        df['TEMP_QC']   = self.TEMP_QC
        df['PSAL']      = self.PSAL
        df['PSAL_QC']   = self.PSAL_QC
        df['PDEN']      = self.PDEN
        if 'DOXY' in self.__floatdict__.keys():
            df['DOXY']      = self.DOXY
            df['DOXY_QC']   = self.DOXY_QC
        if 'CHLA' in self.__floatdict__.keys():
            df['CHLA']      = self.CHLA
            df['CHLA_QC']   = self.CHLA_QC
        if 'BBP700' in self.__floatdict__.keys():
            df['BBP700']    = self.BBP700
            df['BBP700_QC'] = self.BBP700_QC
        if 'CDOM' in self.__floatdict__.keys():
            df['CDOM']      = self.CDOM
            df['CDOM_QC']   = self.CDOM_QC
        if 'DOXY_ADJUSTED' in self.__floatdict__.keys():
            df['DOXY_ADJUSTED']      = self.DOXY_ADJUSTED
            df['DOXY_ADJUSTED_QC']   = self.DOXY_ADJUSTED_QC
        if 'CHLA_ADJUSTED' in self.__floatdict__.keys():
            df['CHLA_ADJUSTED']      = self.CHLA_ADJUSTED
            df['CHLA_ADJUSTED_QC']   = self.CHLA_ADJUSTED_QC
        if 'BBP700_ADJUSTED' in self.__floatdict__.keys():
            df['BBP700_ADJUSTED']    = self.BBP700_ADJUSTED
            df['BBP700_ADJUSTED_QC'] = self.BBP700_ADJUSTED_QC
        if 'CDOM_ADJUSTED' in self.__floatdict__.keys():
            df['CDOM_ADJUSTED']      = self.CDOM_ADJUSTED
            df['CDOM_ADJUSTED_QC']   = self.CDOM_ADJUSTED_QC
        if 'O2Sat' in self.__floatdict__.keys():
            df['O2Sat']      = self.O2Sat
            df['O2Sat_QC']   = self.O2Sat_QC

        self.df = df

        return copy.deepcopy(self.df)

    def get_track(self):
        self.track = track(self.__floatdict__)
        return self.track

    def get_ncep(self):

        if not hasattr(self, 'track'):
            self.get_track()
        self.NCEP = ncep_to_float_track('pres', self.track, local_path=self.ncep_path)
        
        return self.NCEP

    def get_woa(self):

        if not hasattr(self, 'track'):
            self.get_track()
        
        self.z_WOA, self.WOA, self.__WOAweights__  = woa_to_float_track(self.track, 'O2sat', local_path=self.woa_path)

        return self.WOA

    def calc_gains(self, ref='WOA'):

        if not hasattr(self, 'track'):
            self.get_track()

        if ref == 'NCEP':
            sys.stdout.write('In-air data contained in BRtraj file, NCEP not a valid reference for individual profile files, returning None\n')
            self.gains = None

        if ref == 'WOA':
            # check if reference data is already calculated
            if not hasattr(self, 'WOA'):
                self.get_woa()

            self.__WOAgains__, self.__WOAfloatref__, self.__WOAref__ = calc_gain(self.__floatdict__, dict(z=self.z_WOA, WOA=self.WOA), inair=False)
            self.gains = self.__WOAgains__
        
        return self.gains

    def calc_fixed_error(self, fix_err=10):

        self.DOXY_ADJUSTED_ERROR = calc_fixed_doxy_adjusted_error(self.__floatdict__, fix_err=fix_err)
        self.__floatdict__['DOXY_ADJUSTED_ERROR'] = self.DOXY_ADJUSTED_ERROR

        return copy.deepcopy(self.DOXY_ADJUSTED_ERROR)

    def reassign_flags(self):

        return

    def assess_profile_flags(self):

        return

    def describe(self):

        if not hasattr(self, 'df'):
            self.to_dataframe()

        sys.stdout.write('Data for profile files for floats ')
        for i,w in enumerate(self.df.WMO.unique()):
            if i > 0:
                sys.stdout.write(', ')
            sys.stdout.write('{}'.format(int(w)))
        sys.stdout.write('\n')
        
        sys.stdout.write('Variables:\n')
        for k in self.__floatdict__.keys():
            sys.stdout.write('{}\n'.format(k))
        sys.stdout.write('\n')
# ----------------------------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------------------------

def apply_gain(DOXY, G):

    DOXY_ADJUSTED = G*DOXY

    return DOXY_ADJUSTED

def calc_doxy_error(DOXY, G, eG):

    return None

def get_files(local_path, wmo_numbers, cycles=None, mission='B', mode='RD', verbose=True):
    local_path = Path(local_path)

    if mission == 'B':
        subset_index = __bgcindex__[__bgcindex__.wmo.isin(wmo_numbers)]
    if mission == 'C':
        __coreindex__ = io.read_index(mission='C')
        subset_index = __coreindex__[__coreindex__.wmo.isin(wmo_numbers)]
    if cycles is not None:
        subset_index = subset_index[subset_index.cycle.isin(cycles)]
    wcs = ['*' + a + b + '*.nc' for a in mission for b in mode]
    wcs = [w.replace('C','') for w in wcs]

    matches = [fn for sub in [fnmatch.filter(subset_index.file, w) for w in wcs] for fn in sub]
    subset_index = subset_index[subset_index.file.isin(matches)]
    local_files = [(local_path / dac / str(wmo) / 'profiles' / fn.split('/')[-1]).as_posix() for dac, wmo, fn in zip(subset_index.dac, subset_index.wmo, subset_index.file)]

    remove_ix = []
    for i,fn in enumerate(local_files):
        if not Path(fn).exists():
            if verbose:
                sys.stdout.write('File {} does not exists locally - removing from returned list, suggest the user downloads using bgcArgo.io.get_argo(...)\n'.format(fn))
            remove_ix.append(i)
    
    if len(remove_ix) > 0:
        for ix in remove_ix[::-1]:
            local_files.pop(ix)

    return local_files

def organize_files(files):
    '''
    Sort files according to time they were recorded.
    '''
    lead_letter = files[0].split('/')[-1][0]
    if lead_letter == 'R' or lead_letter == 'D':
        index = get_index('global')
    else:
        index = __bgcindex__
    
    dates = np.array([index[index.file.str.find(fn.split('/')[-1]) != -1].date.iloc[0] for fn in files])
    sorted_files = list(np.array(files)[np.argsort(dates)])

    return sorted_files

def get_vars(files):

    nc = Dataset(Path(files[0]), 'r')
    varnames = set(nc.variables.keys())
    nc.close()

    for fn in files:
        nc = Dataset(Path(fn), 'r')
        varnames = varnames.intersection(nc.variables.keys())
        nc.close()

    varnames = list(varnames)

    return varnames

def read_qc(flags):

    decode_flags = np.array([f.decode('utf-8') for f in flags])
    decode_flags[decode_flags == ' '] = '4'

    out_flags = np.array([int(f) for f in decode_flags])

    return out_flags

def get_worst_flag(*args):
    out_flags = np.ones(args[0].shape)

    if len(args) == 1:
        out_flags = args[0]
    else:
        # make an array where all data marked as good
        out_flags = np.ones(args[0].shape)
        # loop through input flags
        for flags in args:
            # loop through each datapoint flag
            for i,f in enumerate(flags):
                if f > out_flags[i] and f <= 4:
                    out_flags[i] = f
                elif f in [5,8] and out_flags[i] <= 2:
                    out_flags[i] = f
                elif f == 9:
                    out_flags[i] = 9
        
    return out_flags

def load_argo(local_path, wmo, grid=False, verbose=True):
    '''
    Function to load in all data from a single float, using BRtraj, meta,
    and Sprof files.
    
    Args:
        local_path: local path of float data
        wmo: float ID number
    
    Returns:
        floatData: python dict() object with the following fields
            - floatName: WMO number, from input
            - floatType: Kind of float (APEX, ARVOR, etc.)
            - N_LEVELS: Number of depth levels, Argo dimension N_LEVELS
            - N_CYCLES: Number of profiles, Argo dimension N_PROF
            - CYCLES: Array from 1 to N_CYCLES
            - LATITUDE: Latitude (-90, 90) for each profile
            - LONGITUDE: Longitude (-180, 180) for each profile
            - SDN: Serial Date Number for each profile
            - PRES: Pressure (dbar), compressed to vector (1D array)
            - TEMP: Temperature (deg C)
            - PSAL: Salinity (psu)
        if the variables are available, it will also contain:
            - DOXY: Dissolved Oxygen (micromole/kg)
            - O2sat: Oxygen percent saturation (%)
            - PPOX_DOXY: Oxygen partial pressure (mbar) [if avail.]
            - TRAJ_CYCLE: Cycle number for PPOX_DOXY [if avail.]
            - inair: Boolean to indicate if in-air data exists
            
        for all the variables listen above, there will also exist
        <PARAM>_QC fields for quality flags, and <PARAM>_ADJUSTED
        fields if they exist.
    
        CYCLES, LATITUDE, LONGITUDE, and SDN all also have
        analogous <VAR>_GRID fields that match the    
        dimension of PRES, TEMP, PSAL, DOXY, and O2SAT  
    
    Author:   
        Christopher Gordon
        Fisheries and Oceans Canada
        chris.gordon@dfo-mpo.gc.ca
    
    Acknowledgement: this code is adapted from the SOCCOM SAGE_O2Argo matlab
    code, available via https://github.com/SOCCOM-BGCArgo/ARGO_PROCESSING,
    written by Tanya Maurer & Josh Plant
    
    Change log:
    
        - 2020-04-22: updated so that pressure mask determines all variables - need to add all quality flags to output
        - 2020-04-29: switched file/path handling from os module to pathlib
        - 2020-10-28: read variable DOXY from BRtraj file and convert to PPOX_DOXY if PPOX_DOXY not in file
    '''

    # make local_path a Path() object from a string, account for windows path
    local_path = Path(local_path)
    dac = io.get_dac(wmo)

    if type(wmo) is not str:
        wmo = str(wmo)

    # check that necessary files exist - can continue without BRtraj file but
    # need Sprof and meta files
    BRtraj = local_path / dac / wmo / '{}_BRtraj.nc'.format(wmo)
    Sprof  = local_path / dac / wmo / '{}_Sprof.nc'.format(wmo)
    meta   = local_path / dac /wmo / '{}_meta.nc'.format(wmo)

    # check if BRtraj is there, flag for moving forward if not
    BRtraj_flag = True
    if not BRtraj.exists():
        BRtraj_nc = None
        BRtraj_flag = False
        if verbose:
            sys.stdout.write('Continuing without BRtraj file\n')
    elif BRtraj.exists():
        BRtraj_nc = Dataset(BRtraj, 'r')
        if 'PPOX_DOXY' not in BRtraj_nc.variables.keys() and 'DOXY' not in BRtraj_nc.variables.keys():
            BRtraj_flag = False
            if verbose:
                sys.stdout.write('BRtraj file exists, but no in-air data exists, continuing without using BRtraj file\n')
    else:
        BRtraj_nc = None

    # Sprof and meta are required, so raise error if they are not there
    if not Sprof.exists():
        raise FileNotFoundError('No such Sprof file: {}'.format(Sprof))
    if not meta.exists():
        raise FileNotFoundError('No such meta file: {}'.format(meta))

    # load synthetic and meta profiles
    Sprof_nc = Dataset(Sprof, 'r')
    meta_nc  = Dataset(meta, 'r')

    # number of profile cycles
    M = Sprof_nc.dimensions['N_LEVELS'].size
    N = Sprof_nc.dimensions['N_PROF'].size
    # beginning of output dict with basic info, following variables in SAGEO2
    floatData = dict(floatName=wmo, N_CYCLES=N, N_LEVELS=M, WMO=int(wmo))
    
    mask = Sprof_nc.variables['PRES'][:].mask
    mask_vars = ['TEMP','PSAL']
    if 'DOXY' in Sprof_nc.variables.keys():
        mask_vars = mask_vars + ['DOXY']
    if 'DOXY_ADJUSTED' in Sprof_nc.variables.keys():
        mask_vars = mask_vars + ['DOXY_ADJUSTED']

    for v in mask_vars:
        mask = np.logical_or(mask, Sprof_nc.variables[v][:].mask)

    if not 'CYCLE_NUMBER' in Sprof_nc.variables.keys():
        floatData['CYCLES'] = np.arange(1,N+1)
    else:
        floatData['CYCLES'] = Sprof_nc.variables['CYCLE_NUMBER'][:].data.flatten()

    # load in variables that will be in every file
    floatData['PRES'] = Sprof_nc.variables['PRES'][:].data.flatten()
    floatData['TEMP'] = Sprof_nc.variables['TEMP'][:].data.flatten()
    floatData['PSAL'] = Sprof_nc.variables['PSAL'][:].data.flatten()
    floatData['SDN']  = Sprof_nc.variables['JULD'][:].data.flatten() + mdates.datestr2num('1950-01-01')
    floatData['LATITUDE']  = Sprof_nc.variables['LATITUDE'][:].data.flatten()
    floatData['LONGITUDE'] = Sprof_nc.variables['LONGITUDE'][:].data.flatten()

    # loop through other possible BGC variables
    bgc_vars = ['DOXY', 'CHLA', 'BBP700', 'CDOM', 'NITRATE', 'DOWNWELLING_IRRADIANCE']
    core_vars = ['PRES', 'TEMP', 'PSAL', 'POSITION']
    for v in bgc_vars:
        if v in Sprof_nc.variables.keys():
            floatData[v] = Sprof_nc.variables[v][:].data.flatten()

    for v in bgc_vars + core_vars:
        v_qc = v + '_QC'
        if v_qc in Sprof_nc.variables.keys():
            floatData[v_qc] = read_qc(Sprof_nc.variables[v_qc][:].data.flatten())
        v_adj = v + '_ADJUSTED'
        if v_adj in Sprof_nc.variables.keys():
            floatData[v_adj] = Sprof_nc.variables[v_adj][:].data.flatten()
            v_adj_qc = v_adj + '_QC'
            if v_adj_qc in Sprof_nc.variables.keys():
                floatData[v_adj_qc] = read_qc(Sprof_nc.variables[v_adj_qc][:].data.flatten())

    if grid:
        ftype = ''
        if 'PLATFORM_TYPE' in meta_nc.variables.keys():
            for let in meta_nc.variables['PLATFORM_TYPE'][:].compressed():
                ftype = ftype + let.decode('UTF-8')
        floatData['floatType'] = ftype

        floatData['SDN_GRID']       = np.tile(floatData['SDN'],(M,1)).T.flatten()
        floatData['CYCLE_GRID']     = np.tile(floatData['CYCLES'],(M,1)).T.flatten()
        floatData['LATITUDE_GRID']  = np.tile(floatData['LATITUDE'],(M,1)).T.flatten()
        floatData['LONGITUDE_GRID'] = np.tile(floatData['LONGITUDE'],(M,1)).T.flatten()

    floatData['O2Sat'] = 100*floatData['DOXY']/unit.oxy_sol(floatData['PSAL'], floatData['TEMP'], unit='micromole/kg')
    # match the fill values
    ix = np.logical_or(np.logical_or(floatData['PSAL'] >= 99999., floatData['TEMP'] >= 99999.), floatData['DOXY'] >= 99999.)
    floatData['O2Sat'][ix] = 99999.
    # get the worst QC flag from each quantity that goes into the calculation
    floatData['O2Sat_QC'] = get_worst_flag(floatData['TEMP_QC'], floatData['PSAL_QC'], floatData['DOXY_QC'])

    if BRtraj_flag:
        if 'PPOX_DOXY' in BRtraj_nc.variables.keys():
            floatData['PPOX_DOXY']  = BRtraj_nc.variables['PPOX_DOXY'][:].data.flatten()
        elif 'DOXY' in BRtraj_nc.variables.keys():
            #  unit conversion from umol kg-1 to pO2, some shaky S and P assumptions?
            floatData['PPOX_DOXY'] = unit.doxy_to_pO2(unit.umol_per_sw_to_mmol_per_L(
                BRtraj_nc.variables['DOXY'][:].data.flatten(),
                0, # salinity is 0 in air???
                BRtraj_nc.variables['TEMP_DOXY'][:].data.flatten(),
                0 # pressure is 0 in air???
            ), 0, BRtraj_nc.variables['TEMP_DOXY'][:].data.flatten())
        floatData['TEMP_DOXY']  = BRtraj_nc.variables['TEMP_DOXY'][:].data.flatten()
        floatData['TRAJ_CYCLE'] = BRtraj_nc.variables['CYCLE_NUMBER'][:].data.flatten()
        floatData['inair']      = True
    else:
        floatData['inair']      = False

    return floatData, Sprof, BRtraj, meta

# def load_profile(fn):
#     '''
#     Function to load a singe Argo profile file into a dict() object
#     NOTE: Deprecated, use load_profiles instead, which can handle multiple
#     profile files at once, but produces the same result for just one. 

#     Author:   
#         Christopher Gordon
        
#         Fisheries and Oceans Canada
        
#         chris.gordon@dfo-mpo.gc.ca
    
#     Last update: 29-04-2020
    
#     Change log:
    
#         - 22-04-2020: updated so that pressure mask determines all variables - need to add all quality flags to output
    
#         - 29-04-2020: switched file/path handling from os module to pathlib

#         - 24-06-2020: deprecated, re-wrote as load_profiles()
#     '''

    # # try to load the profile as absolute path or relative path
    # try:
    #     nc = Dataset(fn, 'r')
    # except:
    #     try:
    #         nc = Dataset(Path(ARGO_PATH) / fn, 'r')
    #     except:
    #         raise FileNotFoundError('No such file {} or {}'.format(fn, str(Path(ARGO_PATH) / fn)))

    # wmo = ''
    # for let in nc.variables['PLATFORM_NUMBER'][:].compressed():
    #     wmo = wmo + let.decode('UTF-8')

    # cycle = nc.variables['CYCLE_NUMBER'][:].compressed()[0]

    # # number of profile cycles
    # M = nc.dimensions['N_LEVELS'].size
    # # beginning of output dict with basic info, following variables in SAGEO2
    # floatData = dict(floatName=wmo, N_LEVELS=M, CYCLE=cycle)

    # ftype = ''
    # for let in nc.variables['PLATFORM_TYPE'][:].compressed():
    #     ftype = ftype + let.decode('UTF-8')

    # floatData['floatType'] = ftype

    # # load in variables that will be in every file
    # floatData['PRES'] = nc.variables['PRES'][:].data
    # floatData['TEMP'] = nc.variables['TEMP'][:].data
    # floatData['PSAL'] = nc.variables['PSAL'][:].data
    # floatData['SDN']  = nc.variables['JULD'][:].data + mdates.datestr2num('1950-01-01')
    # floatData['LATITUDE']  = nc.variables['LATITUDE'][:].data
    # floatData['LONGITUDE'] = nc.variables['LONGITUDE'][:].data

    # # loop through other possible BGC variables
    # bgc_vars = ['DOXY', 'CHLA', 'BBP700', 'CDOM', 'NITRATE', 'DOWNWELLING_IRRADIANCE']
    # for v in bgc_vars:
    #     if v in nc.variables.keys():
    #         floatData[v] = nc.variables[v][:].data

    # for v in floatData.keys():
    #     v_qc = v + '_QC'
    #     if v_qc in nc.variables.keys():
    #         floatData[v_qc] = nc.variables[v_qc][:].data
    #     v_adj = v + '_ADJUSTED'
    #     if v_adj in nc.variables.keys():
    #         floatData[v_adj] = nc.variables[v_adj][:].data
    #         floatData[v_adj + '_QC'] = nc.variabes[v_adj + '_QC'][:].data

    # return floatData

def load_profiles(files):

    common_variables = get_vars(files)
    core_files = [fn.replace('B','') for fn in files]

    floatData = dict(
        floatName=[], N_LEVELS=[], N_PROF=[], CYCLES=np.array([], dtype=int), floatType=[]
    )

    for v in ['PRES', 'TEMP', 'PSAL', 'SDN']:
        floatData[v] = np.array([])
        floatData[v + '_QC'] = np.array([])
    
    for v in ['WMO', 'LATITUDE', 'LONGITUDE', 'POSITION_QC', 'SDN_GRID', 'LATITUDE_GRID', 'LONGITUDE_GRID', 'CYCLE_GRID']:
        floatData[v] = np.array([])

    for v in ['DOXY', 'CHLA', 'BBP700', 'CDOM', 'NITRATE', 'DOWNWELLING_IRRADIANCE']:
        if v in common_variables:
            floatData[v] = np.array([])
            floatData[v + '_QC'] = np.array([])
            if v + '_ADJUSTED' in common_variables:
                floatData[v + '_ADJUSTED'] = np.array([])
                floatData[v + '_ADJUSTED' + '_QC'] = np.array([])

    for fn,cn in zip(files,core_files):
        print(fn, cn)
        # try to load the profile as absolute path or relative path
        try:
            nc = Dataset(fn, 'r')
        except:
            try:
                nc = Dataset(Path(ARGO_PATH) / fn, 'r')
            except:
                raise FileNotFoundError('No such file {} or {}'.format(fn, str(Path(ARGO_PATH) / fn)))

        try:
            cc = Dataset(cn, 'r')
        except:
            try:
                cc = Dataset(Path(ARGO_PATH) / cn, 'r')
            except:
                raise ValueError('Cannot get core Argo data, no such file {} or {}'.format(fn, str(Path(ARGO_PATH) / fn)))

        # number of profile cycles
        M = cc.dimensions['N_LEVELS'].size
        N = cc.dimensions['N_PROF'].size

        wmo = ''
        if N > 1:
            for let in nc.variables['PLATFORM_NUMBER'][:][0,:].compressed():
                wmo = wmo + let.decode('UTF-8')
        else:
            for let in nc.variables['PLATFORM_NUMBER'][:].compressed():
                wmo = wmo + let.decode('UTF-8')

        cycle = nc.variables['CYCLE_NUMBER'][:].data.flatten()

        ftype = ''
        if 'PLATFORM_TYPE' in nc.variables.keys():
            for let in nc.variables['PLATFORM_TYPE'][:].compressed():
                ftype = ftype + let.decode('UTF-8')

        floatData['floatName']  = floatData['floatName'] + [int(wmo)]
        floatData['N_LEVELS']   = floatData['N_LEVELS']  + [M]
        floatData['N_PROF']     = floatData['N_PROF']    + [N]
        floatData['CYCLES']     = np.append(floatData['CYCLES'], cycle)
        floatData['CYCLE_GRID'] = np.append(floatData['CYCLE_GRID'], np.array(N*M*[cycle[0]]))
        floatData['floatType']  = floatData['floatType'] + [ftype]
        floatData['WMO']        = np.append(floatData['WMO'], np.array(M*N*[wmo]))

        # load in variables that will be in every file
        floatData['PRES'] = np.append(floatData['PRES'], cc.variables['PRES'][:].data.flatten())
        floatData['PRES_QC'] = np.append(floatData['PRES_QC'], read_qc(cc.variables['PRES_QC'][:].data.flatten()))
        floatData['TEMP'] = np.append(floatData['TEMP'], cc.variables['TEMP'][:].data.flatten())
        floatData['TEMP_QC'] = np.append(floatData['TEMP_QC'], read_qc(cc.variables['TEMP_QC'][:].data.flatten()))
        floatData['PSAL'] = np.append(floatData['PSAL'], cc.variables['PSAL'][:].data.flatten())
        floatData['PSAL_QC'] = np.append(floatData['PSAL_QC'], read_qc(cc.variables['PSAL_QC'][:].data.flatten()))
        floatData['SDN'] = np.append(floatData['SDN'], cc.variables['JULD'][:].data.flatten() + mdates.datestr2num('1950-01-01'))
        floatData['SDN_QC'] = np.append(floatData['SDN_QC'], read_qc(cc.variables['JULD_QC'][:].data.flatten()))
        floatData['SDN_GRID'] = np.append(floatData['SDN_GRID'], np.array(N*M*[np.nanmean(cc.variables['JULD'][:].data.flatten() + mdates.datestr2num('1950-01-01'))]))
        floatData['LATITUDE'] = np.append(floatData['LATITUDE'], cc.variables['LATITUDE'][:].data.flatten())
        floatData['LATITUDE_GRID'] = np.append(floatData['LATITUDE_GRID'], np.array(N*M*[np.nanmean(cc.variables['LATITUDE'][:].data.flatten())]))
        floatData['LONGITUDE'] = np.append(floatData['LONGITUDE'], cc.variables['LONGITUDE'][:].data.flatten())
        floatData['LONGITUDE_GRID'] = np.append(floatData['LONGITUDE_GRID'], np.array(N*M*[np.nanmean(cc.variables['LONGITUDE'][:].data.flatten())]))
        floatData['POSITION_QC'] = np.append(floatData['POSITION_QC'], read_qc(cc.variables['POSITION_QC'][:].data.flatten()))

        # loop through other possible BGC variables
        bgc_vars = ['DOXY', 'CHLA', 'BBP700', 'CDOM', 'NITRATE', 'DOWNWELLING_IRRADIANCE']
        for v in bgc_vars:
            if v in common_variables:
                floatData[v] = np.append(floatData[v], vertically_align(cc.variables['PRES'][:].data.flatten(), nc.variables['PRES'][:].data.flatten(), nc.variables[v][:].data.flatten()))
            v_adj = v + '_ADJUSTED'
            if v_adj in common_variables:
                floatData[v_adj] = np.append(floatData[v_adj], vertically_align(cc.variables['PRES'][:].data.flatten(), nc.variables['PRES'][:].data.flatten(), nc.variables[v_adj][:].data.flatten()))

        floatData['dPRES'] = delta_pres(cc.variables['PRES'][:].data.flatten(), nc.variables['PRES'][:].data.flatten())

        for v in floatData.keys():
            v_qc = v + '_QC'
            if v_qc in common_variables:
                floatData[v_qc] = np.append(floatData[v_qc], read_qc(nc.variables[v_qc][:].data.flatten()))

        if 'DOXY' in floatData.keys():
            floatData['O2Sat'] = 100*floatData['DOXY']/unit.oxy_sol(floatData['PSAL'], floatData['TEMP'], unit='micromole/kg')
            floatData['O2Sat_QC'] = get_worst_flag(floatData['TEMP_QC'], floatData['PSAL_QC'], floatData['DOXY_QC'])

    return floatData

def read_history_qctest(nc):

    QC_ACTION = np.squeeze(nc.variables['HISTORY_ACTION'][:].data)
    actions = []
    for row in QC_ACTION:
        rval = ''
        for let in row:
            rval = rval + let.decode('UTF-8')
        actions.append(rval.strip())
    actions = np.array(actions)

    QC_TESTS  = np.squeeze(nc.variables['HISTORY_QCTEST'][:].data)
    tests = []
    for row in QC_TESTS:
        rval = ''
        for let in row:
            rval = rval + let.decode('UTF-8')
        tests.append(rval.strip())
    tests = np.array(tests)

    qcp_index = np.logical_or(actions == 'QCP', actions == 'QCP$')
    qcf_index = np.logical_or(actions == 'QCF', actions == 'QCF$')
    QCP, QCF = tests[qcp_index][0], tests[qcf_index][0]

    return QCP, QCF

def dict_clean(float_data, bad_flags=None):

    clean_float_data = copy.deepcopy(float_data)
    qc_flags = [k for k in clean_float_data.keys() if '_QC' in k]

    if bad_flags is None:
        for qc_key in qc_flags:
            data_key   = qc_key.replace('_QC','')
            good_index = np.logical_or(np.logical_or(clean_float_data[qc_key] < 4, clean_float_data[qc_key] == 5), clean_float_data[qc_key] == 8)
            bad_index  = np.invert(good_index)

            if data_key == 'POSITION':
                for dk in ['LATITUDE', 'LONGITUDE']:
                    clean_float_data[dk][bad_index] = np.nan
            else:
                clean_float_data[data_key][bad_index] = np.nan
    else:
        if type(bad_flags) is int:
            bad_flags = [bad_flags]
        
        for flag in bad_flags:
            for qc_key in qc_flags:
                data_key = qc_key.replace('_QC','')
                bad_index = clean_float_data[qc_key] == flag

                if data_key == 'POSITION':
                    for dk in ['LATITUDE', 'LONGITUDE']:
                        clean_float_data[dk][bad_index] = np.nan
                else:
                    clean_float_data[data_key][bad_index] = np.nan
        
    return clean_float_data

def dict_fillvalue_clean(float_data):

    clean_float_data = copy.deepcopy(float_data)
    qc_keys = [k for k in clean_float_data.keys() if '_QC' in k and 'SDN' not in k]

    for k in qc_keys:
        data_key   = k.replace('_QC','')
        if data_key == 'POSITION':
            for dk in ['LATITUDE', 'LONGITUDE', 'LATITUDE_GRID', 'LONGITUDE_GRID']:
                fillvalue_index = clean_float_data[dk] >= 99999. # use greater than because date fillval is 999999
                clean_float_data[dk][fillvalue_index] = np.nan
        else:
            fillvalue_index = clean_float_data[data_key] >= 99999. # use greater than because date fillval is 999999
            clean_float_data[data_key][fillvalue_index] = np.nan

    # check if there is in-air data present
    if 'PPOX_DOXY' in float_data.keys():
        fillvalue_index = clean_float_data['PPOX_DOXY'] >= 99999. # use greater than because date fillval is 999999
        clean_float_data['PPOX_DOXY'][fillvalue_index] = np.nan

    fillvalue_index = clean_float_data['SDN'] >= 999999.
    clean_float_data['SDN'][fillvalue_index] = np.nan

    fillvalue_index = clean_float_data['SDN_GRID'] >= 999999.
    clean_float_data['SDN_GRID'][fillvalue_index] = np.nan

    return clean_float_data

def track(float_data):
    # make 'track' array with columns (time, lat, lon) to be used in interpolation
    track = np.array([float_data['SDN'], float_data['LATITUDE'], float_data['LONGITUDE']]).T

    return track

def woa_to_float_track(track, param, zlim=(0,1000), local_path='./'):
    '''
    Function to load WOA18 climatological data for comparison with autonomous
    floats. Data to be interpolated along the provided track (t, lat, lon).
    Combines function load_woa_data() and interp_woa_data() for convenience,
    see documentation for those funcions for more detail.
    
    Args:
        track: array with the columns (SDN, lat, lon)
        param: requested variable, valid inputs are
            - T: temperature
            - S: salinity
            - O2: dissolved oxygen
            - O2sat: oxygen percent saturation
            - NO3: nitrate
            - Si: silicate
            - PO4: phosphate
        zlim: depth bounds (upper, lower), default to (0, 1000)
        local_path: local directory where WOA files are stored, assumes
                    current directory if no input
    
    Returns:
        z: WOA depth array
        woa_interp: 2D array of requested WOA parameter (depth x time)
    
    Author:   
        Christopher Gordon
        Fisheries and Oceans Canada
        chris.gordon@dfo-mpo.gc.ca
    
    Last update: 2020-04-23
    
    Change log:
    '''

    xtrack, woa_track, woa_data = io.load_woa_data(track, param, zlim=zlim, local_path=local_path)
    woa_interp, wt, yrday = interp.interp_woa_data(xtrack, woa_track, woa_data)
    z = woa_track[0]

    return z, woa_interp, wt

def ncep_to_float_track(varname, track, local_path='./'):
    '''
    Function to load NCEP reanalysis data for comparison with autonomous
    floats. Data to be interpolated along the provided track (t, lat, lon).
    Combines function load_ncep_data() and interp_ncep_data() for convenience,
    see documentation for those funcions for more detail.
    
    Args:
        varname: either 'pres' (pressure) or 'rhum' (relative humidity)
        track: array with the columns (SDN, lat, lon)
    
    Returns:
        z: WOA depth array
        woa_interp: 2D array of requested WOA parameter (depth x time)
    
    Author:   
        Christopher Gordon
        Fisheries and Oceans Canada
        chris.gordon@dfo-mpo.gc.ca
    
    Last update: 2020-04-29
    
    Change log:
    '''

    xtrack, ncep_track, data = io.load_ncep_data(track, varname, local_path=local_path)
    if track[0,0] > ncep_track[0][-1] and mdates.num2date(track[0,0]).year == mdates.datetime.date.today().year:
        raise ValueError('First float date occurs after last NCEP date, NCEP data not available yet, recommend using WOA data to calcualte gain')
    ncep_interp, wt = interp.interp_ncep_data(xtrack, ncep_track, data)

    return ncep_interp, wt


def calc_gain(data, ref, inair=True, zlim=25., verbose=True):
    '''
    Calculate the gain for each profile by comparing float oxygen data to a
    reference data set, either NCEP for in-air or WOA surface data if in-air
    comparison is not available.
    
    Args:
        data: float data dict object, output from load_argo_data()
        ref: reference data set, either NCEP pO2 or WOA O2sat
        inair: boolean flag to indicate if comparison to NCEP in-air
            data or WOA surface data should be done, default to
            in-air, but function also performs check
        zlim: lower limit to define as 'surface' and take mean within,
            default value 25 dbar, for use only when inair is False
    
    Returns:
        g: vector of gains
        surf_data: array of float surface stats (cycle, N, mean, std)
    
    Author:   
        Christopher Gordon
        Fisheries and Oceans Canada
        chris.gordon@dfo-mpo.gc.ca
    
    Last update: 2020-04-23
    
    Change log:
    '''

    # check which reference data to use
    if inair and 'PPOX_DOXY' not in data.keys():
        raise ValueError('Flag ''inair'' set to True but partial pressure data not available')

    if inair:
        if verbose:
            sys.stdout.write('\nCalculating gains using NCEP surface pressure and float in-air measurements...\n')
        g = np.nan*np.ones((ref.shape[0],))

        # float partial pressure measurements at each cycle
        ppox  = data['PPOX_DOXY']
        cycle = data['CYCLES']
        inair_cycle = data['TRAJ_CYCLE']

        intersect_cycles = np.intersect1d(cycle, np.unique(inair_cycle), assume_unique=True)

        mean_float_data = np.nan*np.ones((ref.shape[0],4))
        for i,c in enumerate(intersect_cycles):
            subset_ppox = ppox[inair_cycle == c]
            mean_float_data[i,0] = c
            mean_float_data[i,1] = np.sum(~np.isnan(subset_ppox))
            mean_float_data[i,2] = np.nanmean(subset_ppox)
            mean_float_data[i,3] = np.nanstd(subset_ppox)

            g[i] = ref[i]/mean_float_data[i,2]

        g[g == 0] = np.nan

        return g, mean_float_data

    else:
        if verbose:
            sys.stdout.write('\nCalculating gains using WOA surface data and float O2 percent saturation...\n')
        surf_ix = data['PRES'] <= zlim
        surf_o2sat = data['O2Sat'][surf_ix]
        grid_cycle = data['CYCLE_GRID'][surf_ix]
        grid_time  = data['SDN_GRID'][surf_ix]
        cycle = data['CYCLES']
        time  = data['SDN']

        z_woa = ref['z']
        woa_data = ref['WOA']

        woa_index = np.where(z_woa <= zlim)[0]
        woa_surf = np.nanmean(woa_data[woa_index,:],axis=0)
        woa_surf = woa_data[0,:]

        mean_float_data = np.nan*np.ones((woa_surf.shape[0],4))
        g = np.nan*np.ones((woa_surf.shape[0],))
        for i,t in enumerate(time):
            ref_o2sat = woa_surf[i]
            subset_o2sat = surf_o2sat[grid_time == t] # uncomment when ready
            mean_float_data[i,0] = cycle[i]
            mean_float_data[i,1] = np.sum(~np.isnan(subset_o2sat))
            mean_float_data[i,2] = np.nanmean(subset_o2sat)
            mean_float_data[i,3] = np.nanstd(subset_o2sat)

            g[i] = ref_o2sat/mean_float_data[i,2]
        
        g[g == 0] = np.nan

        return g, mean_float_data, woa_surf

def calc_gain_with_carryover(pO2_opt_air, pO2_ref_air, pO2_opt_water):
    '''
    Calculate gain with carryover parameter, following Bittig et al. (2018).

    Args:
        pO2_opt_air (array-like): partial pressure measured by the oxygen optode in-air
        pO2_ref_air (array-like): partial pressure in-air from a reference dataset such as NCEP
        pO2_opt_water (array-like): partial pressure of oxygen measured by the optode just below the surface

    Returns:
        *need to run this by Henry and see if I'm doing it right*

    Derive the O2 slope including a correction for 'carry-over' effect, to
    account for the observation that optode in-air data do not represent pure
    air but show a bias by in-water O2 saturation excess/deficiency (Bittig 
    and Kortzinger 2015). Johnson et al. (2015) confirm the 'carry-over' effect
    for optodes close to the surface (~20cm). 

    Carry-over effect is recommended to be account for Argo floats using in-air
    measurements, if enough surfacings are available (N > 20). It both removes
    an identified bias (which is most relevant for cases with strong 
    super-/undersaturation and/or carry-overs) and reduces uncertainty on the
    O2 slope factor. The equation for linear regression is as follows (see,
    e.g., Bittig et al., 2018):

    m*pO2^{optode}_{surf in-air} - pO2^{reference}_{in-air} 
        = c*(m*pO2^{optode}_{surf in-water} - pO2^{reference}_{in-air})

    where: 
        - m is the O2 slope factor: m = pO2_adjusted / pO2
        - pO2^{optode}_{surf in-air} is the oxygen partial pressure observed by
        the optode in-air (i.e., close to the water surface), e.g., MC = X+11
        - pO2^{reference}_{in-air} is the reference oxygen partial pressure in-air,
        e.g., from re-analysis data
        - pO2^{optode}_{surf in-water} is the oxygen partial pressure observed by 
        the optode at the water surface (in-water), e.g., MC = X+10 or profile 
        MC = X–10
        - c is the slope of the 'carry-over' effect, i.e., the water-fraction of 
        the observed optode in-air data.

    Above equation can be used for linear regression to obtain m and c from
    data of the partial pressures (from several cycles together). See 
    Thierry Virginie, Bittig Henry, The Argo-Bgc Team (2018). Argo quality 
    control manual for dissolved oxygen concentration. 
    https://doi.org/10.13155/46542
    '''

    x1 = pO2_opt_air - pO2_ref_air
    y1 = pO2_opt_water - pO2_ref_air

    x1 = x1[:,np.newaxis]

    carry_over, resid, _, _ = np.linalg.lstsq(x1, y1, rcond=None)
    c = carry_over

    gains = ((1-c)*pO2_ref_air)/(pO2_opt_air - c*pO2_opt_water)

    return gains, carry_over


def grid_var(gridded_cycle, Nprof, Nlevel, argo_var):

    return gV

def vertically_align(P1, P2, V2):

	out = np.nan*np.ones(P1.shape)

	for i, p in enumerate(P1):
		index  = np.abs(P2 - p) == np.min(np.abs(P2 - p))
		out[i] = np.nanmean(V2[index])

	return out

def delta_pres(P1, P2):

	dpres = np.nan*np.ones(P1.shape)

	for i, p in enumerate(P1):
		index    = np.abs(P2 - p) == np.min(np.abs(P2 - p))
		dpres[i] = np.nanmean(P2[index] - p)

	return dpres

def range_check(key, floatdict, verbose=True):
    if 'range_dict' not in globals():
        global range_dict
        range_dict = dict(
            PRES=(-5, np.inf),
            TEMP=(-2.5, 40),
            PSAL=(2, 41),
            DOXY=(-5, 600),
        )

    cleandict = copy.deepcopy(floatdict)

    argo_var = floatdict[key]
    r = range_dict[key.replace('_ADJUSTED','')]
    outside_range = np.logical_or(argo_var < r[0], argo_var > r[1])
    if verbose:
        sys.stdout.write('{} values found outside RTQC range check, replacing with NaN\n'.format(np.sum(outside_range)))

    argo_var[outside_range] = np.nan
    cleandict[key] = argo_var

    return cleandict

def calc_fixed_doxy_adjusted_error(floatdict, fix_err=10, zlim=25):
    '''
    Calculate DOXY_ADJUSTED_ERROR for fixed partial pressure of 10 mbar 
    PPOX_DOXY.
    '''

    S = floatdict['PSAL']
    T = floatdict['TEMP']
    P = floatdict['PRES']

    error = unit.pO2_to_doxy(np.array(S.shape[0]*[10]), S, T, P=P)

    return error

def oxy_b(dt, tau):
    inv_b = 1 + 2*(tau/dt)
    return 1/inv_b

def oxy_a(dt, tau):
    return 1 - 2*oxy_b(dt, tau)

def correct_response_time(t, DO, T, thickness):

    # convert time to seconds
    t_sec = t*24*60*60

    # array for the loop
    N = DO.shape[0]
    mean_oxy  = np.array((N-1)*[np.nan])
    mean_time = t_sec[:-1] + np.diff(t_sec)/2
    mean_temp = T[:-1] + np.diff(T)/2

    # load temperature, boundary layer thickness, and tau matrix from 
    # look-up table provided in the supplement to Bittig and Kortzinger (2017)
    lut_data = np.loadtxt(REF_PATH / 'T_lL_tau_3830_4330.dat')
    lut_lL = lut_data[0,1:]
    lut_T  = lut_data[1:,0]
    tau100 = lut_data[1:,1:]
    thickness = thickness*np.ones((N-1,))

    # translate boundary layer thickness to temperature dependent tau
    f_thickness = interp2d(lut_T, lut_lL, tau100.T, bounds_error=False)
    tau_T = np.squeeze(f_thickness(mean_temp, thickness))[0,:]
    print(tau_T)
    # loop through oxygen data 
    for i in range(N-1):
        dt = t_sec[i+1] - t_sec[i]

        # do the correction using the mean filter, get the mean time
        mean_oxy[i]  = (1/(2*oxy_b(dt, tau_T[i])))*(DO[i+1] - oxy_a(dt, tau_T[i])*DO[i])
    
    # interpolate back to original times for output
    f = interp1d(mean_time, mean_oxy, kind='linear', bounds_error=False, fill_value='extrapolate')
    DO_out = f(t_sec)

    return DO_out

def correct_response_time_Tconst(t, DO, tau):
    # convert time to seconds
    t_sec = t*24*60*60

    # array for the loop
    N = DO.shape[0]
    mean_oxy  = np.array((N-1)*[np.nan])
    mean_time = t_sec[:-1] + np.diff(t_sec)/2

    # loop through oxygen data
    for i in range(N-1):
        dt = t_sec[i+1] - t_sec[i]

        # do the correction using the mean filter, get the mean time
        mean_oxy[i]  = (1/(2*oxy_b(dt, tau)))*(DO[i+1] - oxy_a(dt, tau)*DO[i])
    
    # interpolate back to original times for output
    f = interp1d(mean_time, mean_oxy, kind='linear', bounds_error=False, fill_value='extrapolate')
    DO_out = f(t_sec)

    return DO_out
