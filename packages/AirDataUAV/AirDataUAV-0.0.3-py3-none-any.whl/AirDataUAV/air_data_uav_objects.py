import csv
import numpy as np
import utm

MPH_TO_MS = MPH_TO_MS
FT_TO_M = 0.3048

KEYS = (
    'latitude',
    'longitude',
    ('time(millisecond)','t_s',float,0.001),
    ('height_above_takeoff(feet)','height_above_TO_m',float,FT_TO_M),
    ('speed(mph)','speed_ms',float,MPH_TO_MS),
    (' xSpeed(mph)','x_speed_ms',float,MPH_TO_MS),    
    (' ySpeed(mph)','y_speed_ms',float,MPH_TO_MS),
    (' zSpeed(mph)','z_speed_ms',float,MPH_TO_MS)    
    )


class UAVData:
    def __init__(self,csvfilename):
        data = []
        with open(csvfilename,'r') as f:
            for row in csv.DictReader(f):
                data.append(row)

        for k in KEYS:
            class_var = k
            dict_var = k
            type_ = float
            conversion_factor = 1
            if isinstance(k,tuple):
                dict_var = k[0]
                class_var = k[1]
                type_ = k[2]
                conversion_factor = k[3]

            d = conversion_factor*np.array([f[dict_var] for f in data]).astype(type_)
            setattr(self,class_var,d)

        self._latlng_to_local()

    def _latlng_to_local(self):
        xy = utm.from_latlon(np.array(self.latitude),np.array(self.longitude))

        # Normalize to starting position (i.e. home)
        self.x = np.copy(xy[0]-xy[0][0])
        self.y = np.copy(xy[1]-xy[1][0])


if __name__ == "__main__":
    a = UAVData('/home/jhewers/Documents/meng_project/ps_data/2020-11-19_14-18-29.csv')    