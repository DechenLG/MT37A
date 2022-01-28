# import necessary modulesimport astropy.units as uimport huxt as Himport huxt_inputs as Hinimport csvimport numpy as np# create empty arrays to save variablescarrington_no=np.zeros(27)carrington_lon=np.zeros(27)transit_time=np.zeros(27)# specify carrington number limitcr_min = 1851cr_max = 1901# create a loop to simulate solar wind conditions in each carrington numbefor i in range(cr_min, cr_max):        # calculate transit time if solar wind conditions are available    try:                # import solar wind conditions        vr_in = Hin.get_MAS_long_profile(i, 0.0*u.deg)                # create a loop for each day in the carrington rotation        for j in range(0, 27):                        # define dphi as the carrington longitude (value goes from 360 to 0 degrees)            dphi = (360*(27-j)/27)*u.deg                        # simulate ambient solar wind conditions            model = H.HUXt(v_boundary=vr_in, cr_num=i, cr_lon_init=dphi, lon_start=-0.1*u.rad,lon_stop=0.1*u.rad,simtime=7*u.day, dt_scale=4)                    # introduce a spherical CME            cme = H.ConeCME(t_launch=0*u.day, longitude=0.0*u.deg, width=37.4*u.deg, v=495*(u.km/u.s), thickness=0*u.solRad)            cme_list = [cme]            model.solve(cme_list)            cme = model.cmes[0]            hit, t_arrive, t_transit, hit_lon, hit_id = cme.compute_arrival_at_body('Earth')                        # print transit time to check if code works            # print(t_transit)                        # save outputs into arrays            carrington_no[j]=i            carrington_lon[j]=dphi.value            transit_time[j]=t_transit.value                # otherwise save transit time values as nan value    except:                # looping each day in one carrington rotation        for j in range(0,27):                            # defining carrington longitude            dphi = (360*(27-j)/27)*u.deg                            # saving outputs with nan values in transit time            carrington_no[j]=i            carrington_lon[j]=dphi.value            transit_time[j]=np.nan                # save the data into a csv            finally:                # open a new csv file in a specified path        with open('/Users/dven/Desktop/School/2021-22/MT37A/HUXt-master/df/%s.csv'%i,'w',newline='') as df:            writer=csv.writer(df)                        # write in the column names            writer.writerow(('Carrington Number','Carrington Longitude','Transit Time'))                            # write in the values            for k in range(0,27):                writer.writerow((carrington_no[k],carrington_lon[k],transit_time[k]))       