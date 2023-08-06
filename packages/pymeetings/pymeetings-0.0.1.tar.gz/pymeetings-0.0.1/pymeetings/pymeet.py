import pandas as pd
import numpy as np
from pymeetings.utils import *
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime


class GetMeetingHour():
    
    def __init__(self,cities,day):
        """
        Computes the most interesting hours for a particular day, considering 
        that you provide several cities
        
        :param vec cities: the number of cities to consider for the algorithm 
        :param str day  : the date to make the calculation in the format: 2020/02/20 
        """

        self.cities_vec = cities
        self.day = day
        self.g = Nominatim(user_agent="geoapiExercises")
        self.obj = TimezoneFinder()


    def Countries(self):
        """
        Function that computes the different countries where the cities are in
        """
        countries = []
        for city in self.cities_vec:
            if citycheck(city):
                ctry = country(city)
                countries.append(ctry)
            else:
                print('The city %s does not exist' %s)
                countries.append(None)
        return countries


    def TimeZone(self, city):
        """
        Function that computes the timezone for a particular city
        """
        if citycheck(city):
            location = self.g.geocode(city)
            timezone = self.obj.timezone_at(lng=location.longitude, lat=location.latitude)
            return timezone
        else:
            print('The city %s does not exist' %city)
            return None
            

    
    def TimeZones(self):
        """
        Function that computes the different timezones for each city 
        """
        
        timezones = []
        for city in self.cities_vec:
                timezones.append(self.TimeZone(city))
                
        return timezones

    
    def CityTimes(self, city):
        """
        Function that given the cities provides the times
        """
        hour_vec = self.__Hours()
        tz_str = self.TimeZone(city)
        city_tz = pytz.timezone(tz_str)
        gmt_tz = pytz.timezone('GMT')
        city_timestamp_vec = []
        for hour in hour_vec:
            gmt_timestamp = str2date(hour)
            localized_timestamp = gmt_tz.localize(gmt_timestamp)
            city_timestamp = localized_timestamp.astimezone(city_tz)
            city_timestamp = datetime.strftime(city_timestamp, '%Y/%m/%d %H:%M')
            city_timestamp_vec.append(city_timestamp)

        return city_timestamp_vec

            
    def __checkdate(self,date):
        """
        Function that checks that the date string is in the right format
        """
        format_date = '%Y/%m/%d'
        try:
            datetime.strptime(date, format_date)
            return True
        except:
            return False

    
    def __Hours(self):
        """
        Function that calculates the vector of times for a particular day
        """
        
        hours = []

        if self.__checkdate(self.day):
            for j in range(0, 24):
                if j<10:
                    hours.append(self.day+' '+'0'+str(j)+':00')
                else:
                    hours.append(self.day+' '+str(j)+':00')

        return hours

                    
    def BestHour(self):
        """
        Function that computes the best hour for the meeting, the `feel lucky` guess
        """
        
    
    
    def ConstructTable(self):
        """
        Function that provides the table of interest 
        """
        lowbound = datetime.strptime(self.day+' 08:00','%Y/%m/%d %H:%M')
        uppbound = datetime.strptime(self.day+' 17:00','%Y/%m/%d %H:%M')
        dic_pd = {}
        dic_pd['GMT'] = self.__Hours()
        column_fitness = []
        for city in self.cities_vec:
            dic_pd[city] = self.CityTimes(city)

            cond = []
            for i in range(len(dic_pd[city])):
                tmp_time = datetime.strptime(dic_pd[city][i],'%Y/%m/%d %H:%M')
                local_cond = (tmp_time >= lowbound) & (tmp_time <= uppbound)
                cond.append(local_cond)        
            dic_pd[city+'_fit'] = cond

            column_fitness.append(city+'_fit')
        main_table = pd.DataFrame(dic_pd)

        fitness_results = main_table[column_fitness].all(axis=1)
        main_table['fitness'] = fitness_results
        
        final_table = main_table.drop(columns=column_fitness)
        return final_table
        

