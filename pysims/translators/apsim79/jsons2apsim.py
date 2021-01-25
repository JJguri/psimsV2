#!/usr/bin/env python

# import modules
import abc
import airspeed
import json
import netCDF4
import os
import traceback
from numpy import double
from scipy.interpolate import interp1d as interp1d
from .. import translator


def get_field(struct, field, default='?'):
    return default if field not in struct else struct[field]


def format_date(yyyymmdd):
    if yyyymmdd == '?':
        return '?'
    else:
        return yyyymmdd[6:8] + '/' + yyyymmdd[4:6] + '/' + yyyymmdd[:4]


def date2num(ddmmyyyy):
    if ddmmyyyy:
        return '?'
    else:
        return int(ddmmyyyy[:2]) + 100 * int(ddmmyyyy[3:5]) + 10000 * int(ddmmyyyy[6:10])


def find_idx(arr, m):
    for i in range(len(arr)):
        if arr[i] == m:
            return i
    arr.append(m)
    return len(arr) - 1


def tile_to_dict(tile):
    data = dict()
    data['soils'] = [{}]
    data['soils'][0] = {}
    data['soils'][0]['soilLayer'] = []
    exclude = ["lat", "lon", "depth", "profile"]

    nlayers = len(tile.variables['depth'])
    for layer in range(0, nlayers):
        data['soils'][0]['soilLayer'].append({})

    for v in tile.variables:
        vals = []
        if v in exclude:
            continue
        if hasattr(tile.variables[v], 'units') and tile.variables[v].units == "mapping":
            vals.append(tile.variables[v].long_name)
        else:
            vals = tile.variables[v][:].flatten()
        if 'depth' in tile.variables[v].dimensions:
            for layer in range(0, nlayers):
                data['soils'][0]['soilLayer'][layer][v] = str(vals[layer])
        else:
            data['soils'][0][v] = str(vals[0])

    for a in tile.ncattrs():
        data['soils'][0][a] = str(tile.getncattr(a))
    for layer, val in enumerate(tile.variables['depth']):
        data['soils'][0]['soilLayer'][layer]['sllb'] = str(val)
    return data


class Event(object):
    """
    Management event base class
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, event_struct):
        self.date = get_field(event_struct, 'date')
        if self.date != '?':
            self.date = format_date(self.date)

    @abc.abstractmethod 
    def get_apsim_action(self): return


class Tillage(Event):

    def __init__(self, event_struct):
        super(Tillage, self).__init__(event_struct)
        self.implement_name = get_field(event_struct, 'tiimp')
        self.depth = get_field(event_struct, 'tidep')

    def get_apsim_action(self):
        act = 'SurfaceOrganicMatter tillage type=' + self.implement_name
        act += ', f_incorp=0, tillage_depth=' + self.depth
        return act


class Planting(Event):

    def __init__(self, event_struct):
        super(Planting, self).__init__(event_struct)
        self.crop_name = get_field(event_struct, 'crid')
        self.population = get_field(event_struct, 'plpop')
        self.depth = get_field(event_struct, 'pldp')
        self.cultivar = get_field(event_struct, 'apsim_cul_id')
        if self.cultivar == '?':
            cul_id = get_field(event_struct, 'cul_id')
            if cul_id != '?':
                self.cultivar = cul_id
        self.row_spacing = get_field(event_struct, 'plrs')
        if self.row_spacing != '?':
            self.row_spacing = str(10. * double(self.row_spacing))
###Edited code
        self.ftn = get_field(event_struct, 'ftn')
###Edited code

    def get_apsim_action(self):
        act = self.crop_name
        act += " sow plants = " + self.population
        act += ", sowing_depth = " + self.depth
        act += ", cultivar = " + self.cultivar
        act += ", row_spacing = " + self.row_spacing
        act += ", crop_class = plant"
###Edited code
        act += ", skiprow = solid"
        act += ", ftn = " + self.ftn
###Edited code
        return act


class Irrigation(Event):

    def __init__(self, event_struct):
        super(Irrigation, self).__init__(event_struct)
        self.amount = get_field(event_struct, 'irval')

    def get_apsim_action(self):
        return 'irrigation apply amount = ' + self.amount + ' (mm) '


class Fertilizer(Event):

    def __init__(self, event_struct):
        super(Fertilizer, self).__init__(event_struct)
        self.nitrogen = get_field(event_struct, 'feamn')
        self.depth = get_field(event_struct, 'fedep')

    def get_apsim_action(self):
        act = 'fertiliser apply amount = ' + self.nitrogen + ' (kg/ha)'
        act += ', type = no3_n (), depth = ' + self.depth + ' (mm)'
        return act


class OrganicMatter(Event):

    def __init__(self, event_struct):
        super(OrganicMatter, self).__init__(event_struct)
        self.amount = get_field(event_struct, 'omamt')
        self.depth = get_field(event_struct, 'omdep')
        self.carbon = get_field(event_struct, 'omc%')
        self.nitrogen = get_field(event_struct, 'omn%')
        self.phosphorus = get_field(event_struct, 'omp%')

    def get_apsim_action(self):
        cnr = '?'
        act = 'SurfaceOrganicMatter add_surfaceom type=manure, name=manure, '
        act += 'mass=' + self.amount + '(kg/ha), '
        act += 'depth = ' + self.depth + ' (mm)'
        if self.amount != '?':
            if self.carbon != '?':
                if self.nitrogen != '?':
                    amount_carbon = double(self.carbon) / 100. * double(self.amount)
                    amount_nitrogen = double(self.nitrogen) / 100. * double(self.amount)
                    if amount_nitrogen == 0.:
                        cnr = '0'
                    else:
                        cnr = str(amount_carbon / amount_nitrogen * 100.)
                act += ', cnr = ' + cnr
                if self.phosphorus != '?':
                    amount_carbon = double(self.carbon) / 100. * double(self.amount)
                    amount_phosphorus = double(self.phosphorus) / 100. * double(self.amount)
                    if amount_phosphorus == 0.:
                        cpr = '0'
                    else:
                        cpr = str(amount_carbon / amount_phosphorus * 100.)
                    act += ', cpr = ' + cpr
        return act


class Chemical(Event):

    def __init__(self, event_struct):
        super(Chemical, self).__init__(event_struct)

    def get_apsim_action(self):
        return ''


class Harvest(Event):

    def __init__(self, event_struct):
        super(Harvest, self).__init__(event_struct)

    def get_apsim_action(self):
        return ''


def get_layers(soil):
    num_layers = len(soil['soilLayer'])

    # add leftmost and rightmost bin edges
    kl_x = [0, 15, 30, 60, 90, 120, 150, 180, 1e10]
    kl_y = [0.08, 0.08, 0.08, 0.08, 0.06, 0.06, 0.04, 0.02, 0.02]
    kl_interp = interp1d(kl_x, kl_y)
    fbiom_per_layer = 0.03 / (num_layers - 1) if num_layers > 1 else 0.03

    # add leftmost and rightmost bin edges
    finert_x = [0, 15, 30, 60, 90, 1e10]
    finert_y = [0.4, 0.4, 0.5, 0.7, 0.95, 0.95]
    finert_interp = interp1d(finert_x, finert_y)

    # layer data
    layers = [0] * num_layers 
    cum_thickness = 0
    for i in range(num_layers):
        layers[i] = {}
        layer = soil['soilLayer'][i]
        bottom_depth = get_field(layer, 'sllb')
        if bottom_depth == '?':
            raise Exception('Soil layer depth not specified')
        else:
            bottom_depth = double(bottom_depth)
        layers[i]['thickness'] = 10 * bottom_depth - cum_thickness
        layers[i]['lowerLimit'] = get_field(layer, 'slll')
        layers[i]['kl'] = str(kl_interp(bottom_depth))
        layers[i]['bulkDensity'] = get_field(layer, 'sbdm')
        if layers[i]['lowerLimit'] == '?':
            layers[i]['airDry'] = '?'
        else:
            layers[i]['airDry'] = str(0.5 * double(layers[i]['lowerLimit']))
        layers[i]['drainedUpperLimit'] = get_field(layer, 'sdul')
        layers[i]['saturation'] = get_field(layer, 'ssat')
        layers[i]['organicCarbon'] = get_field(layer, 'sloc')
        if layers[i]['organicCarbon'] != '?':
            organic_carbon = double(layers[i]['organicCarbon'])
            if not organic_carbon: layers[i]['organicCarbon'] = '0.1'
        layers[i]['fbiom'] = str(0.04 - fbiom_per_layer * i)
        layers[i]['finert'] = str(finert_interp(bottom_depth))
        layers[i]['ph'] = get_field(layer, 'slhw')
        cum_thickness = 10 * bottom_depth

    return layers


def get_soil_structure(soil):
    soil_struct = {}

    # profile-wide values
    classification = get_field(soil, 'classification')
    soil_name = get_field(soil, 'soil_name')
    if 'sand' in classification or 'sand' in soil_name:
        diffus_const = 250
        diffus_slope = 22
    elif 'loam' in classification or 'loam' in soil_name:
        diffus_const = 88
        diffus_slope = 35
    elif 'clay' in classification or 'clay' in soil_name:
        diffus_const = 40
        diffus_slope = 16
    else:
        diffus_const = 40
        diffus_slope = 16
    soil_struct['u'] = get_field(soil, 'slu1')
    soil_struct['salb'] = get_field(soil, 'salb')
    soil_struct['cn2bare'] = get_field(soil, 'slro')
    soil_struct['diffusConst'] = diffus_const
    soil_struct['diffusSlope'] = diffus_slope
    soil_struct['classification'] = soil['classification']
    soil_struct['site'] = get_field(soil, 'soil_site')
    soil_struct['latitude'] = get_field(soil, 'soil_lat')
    soil_struct['longitude'] = get_field(soil, 'soil_long')
    soil_struct['source'] = get_field(soil, 'sl_source')
    soil_struct['layers'] = get_layers(soil)

    return soil_struct


def get_management(exp):
    man = {}

    if 'management' not in exp:
        return man
    if 'events' not in exp['management']:
        return man

    # planting crop name
    num_events = len(exp['management']['events'])
    for i in range(num_events):
        # find crop to be planted
        event = exp['management']['events'][i]
        if get_field(event, 'event') == 'planting':
            man['plantingCropName'] = get_field(event, 'crid')
            break
        elif i == num_events - 1:
            Exception('No planting event found')

    # events data
    man['events'] = [0] * num_events
    for i in range(num_events):
        man['events'][i] = {}
        event_struct = exp['management']['events'][i]
        if get_field(event_struct, 'event') == 'tillage':
            event_obj = Tillage(event_struct)
        elif get_field(event_struct, 'event') == 'planting':
            event_obj = Planting(event_struct)
        elif get_field(event_struct, 'event') == 'irrigation':
            event_obj = Irrigation(event_struct)
        elif get_field(event_struct, 'event') == 'fertilizer':
            event_obj = Fertilizer(event_struct)
        elif get_field(event_struct, 'event') == 'organic_matter':
            event_obj = OrganicMatter(event_struct)
        elif get_field(event_struct, 'event') == 'chemical':
            event_obj = Chemical(event_struct)
        elif get_field(event_struct, 'event') == 'harvest':
            event_obj = Harvest(event_struct)
        else:
            Exception('Unknown management event')
        man['events'][i]['date'] = event_obj.date
        man['events'][i]['apsimAction'] = event_obj.get_apsim_action()
    man['events'] = sorted(man['events'], key=lambda x: date2num(x['date']))
    return man


def get_initial_condition(exp, soil):
    ic_struct = {}
    ic = exp['initial_condition']

    # date, residue type, residue weight
    ic_struct['date'] = format_date(get_field(ic, 'icdat'))
    residue_type = get_field(ic, 'residue_type')
    if residue_type == '?':
        ic_struct['residue_type'] = get_field(exp, 'crop_name')
    else:
        ic_struct['residue_type'] = residue_type
    ic_struct['residueWeight'] = get_field(ic, 'icrag')
    ic_struct['standing_fraction'] = get_field(ic, 'standing_fraction')
    ic_struct['water_fraction_full'] = get_field(ic, 'water_fraction_full')

    # NH4
    if 'icnh4' not in ic:
        layers = get_field(ic, 'soilLayer', [])
        icnh4 = get_field(layers[0], 'icnh4', '-99') if layers != [] else '-99'
    else:
        icnh4 = ic['icnh4']

    # layer data
    num_layers = len(soil['layers'])
    layers = [0] * num_layers
    for i in range(num_layers):
        layers[i] = {}

        # soil water
        sdul = double(get_field(soil['layers'][i], 'drainedUpperLimit'))
        fracf = double(ic_struct['water_fraction_full'])
        soil_water = min(fracf * sdul, 0.75)

        layers[i]['thickness'] = get_field(soil['layers'][i], 'thickness')
        layers[i]['no3'] = get_field(soil['layers'][i], 'organicCarbon')
        layers[i]['nh4'] = str(icnh4)
        layers[i]['soilWater'] = str(soil_water)

    ic_struct['soilLayers'] = layers

    # carbon to nitrogen ratio
    carbon = 0.4 * double(ic_struct['residueWeight'])
    nitrogen = double(get_field(ic, 'icrn')) / 100. * double(ic_struct['residueWeight'])
    ic_struct['cnr'] = carbon / nitrogen

    return ic_struct


class Jsons2Apsim(translator.Translator):
    def run(self, latidx, lonidx):
        try:
            soiltile = self.config.get_dict(self.translator_type, 'soiltile', default="1.soil.nc4")
            expfile = self.config.get_dict(self.translator_type, 'expfile')
            templatefile = self.config.get_dict(self.translator_type, 'templatefile')
            cultivarfile = self.config.get_dict(self.translator_type, 'cultivarfile')
            outputfile = self.config.get_dict(self.translator_type, 'outputfile')
   
            soil_json = tile_to_dict(netCDF4.Dataset(soiltile))
            exp_json = json.load(open(expfile))
            
            # simulation structure
            num_experiments = len(exp_json['experiments'])
            s = {'experiments': [0] * num_experiments}
            
            # cultivar arrays for custom cultivars
            cultivars, cul_names = [], []
            
            # soil IDs
            soil_ids = [soil['soil_id'] for soil in soil_json['soils']]
            
            for i in range(num_experiments):
                exp_i = exp_json['experiments'][i]
                # global
                s_tmp = dict()
                s_tmp['cropName'] = exp_i['crop_name']
                s_tmp['startDate'] = exp_i['start_date']
                s_tmp['endDate'] = exp_i['end_date']
                s_tmp['log'] = exp_i['log']
                s_tmp['reporting_frequency'] = exp_i['reporting_frequency']
                if 'micromet' in exp_i.keys():
                    s_tmp['micromet'] = exp_i['micromet']
                else:
                    s_tmp['micromet'] = 'off'
            
                # weather
                s_tmp['weather'] = exp_i['weather']
            
                # soil
                soil_id = get_field(exp_i, 'soil_id', 'XY01234567')
                soil_idx = soil_ids.index(soil_id)
                s_tmp['soil'] = get_soil_structure(soil_json['soils'][soil_idx])
            
                # management
                s_tmp['management'] = get_management(exp_i)
            
                # initial condition
                s_tmp['initialCondition'] = get_initial_condition(exp_i, s_tmp['soil'])
            
                # planting
                s_tmp['planting'] = exp_i['planting']
                # custom cultivar definition
                if s_tmp['planting']['cultivar'] == 'custom':
                    cultivar = s_tmp['planting'].copy()
                    for v in ['pdate', 'sowing_density', 'depth', 'cultivar', 'edate', 'row_spacing']:
                        cultivar.pop(v)
                    idx = find_idx(cultivars, cultivar)
                    # new element
                    if len(cultivars) != len(cul_names):
                        cul_names += ['CC' + str(idx).zfill(4)]
                    # change cultivar name
                    s_tmp['planting']['cultivar'] = cul_names[idx]

                # fertilizer
                s_tmp['fertilizer'] = exp_i['fertilizer']
            
                # Pasture
                if 'pasture' in exp_i:
                    s_tmp['pasture'] = exp_i['pasture']
            
                # irrigation
                s_tmp['irrigation'] = exp_i['irrigation']
            
                # reset
                s_tmp['reset'] = exp_i['reset']
            
                # output variables
                s_tmp['output_variables'] = exp_i['output_variables']
                s['experiments'][i] = s_tmp
            
            # find and replace within template and write output file
            template = airspeed.Template(open(templatefile).read())
            with open(outputfile, 'w') as f:
                f.write(template.merge(s))
            
            # find and replace within cultivar template if necessary
            if len(cultivars):
                cultivar_template = airspeed.Template(open(cultivarfile).read())
                for i in range(len(cultivars)):
                    cultivars[i]['name'] = cul_names[i]
                crop_name = exp_json['experiments'][0]['crop_name']
                with open(crop_name + '.xml', 'w') as f:
                    f.write(cultivar_template.merge({'cultivars': cultivars}))
            return True
        
        except:
            print "[%s]: (%04d/%04d) %s" % (os.path.basename(__file__), latidx, lonidx, traceback.format_exc())
            return False
