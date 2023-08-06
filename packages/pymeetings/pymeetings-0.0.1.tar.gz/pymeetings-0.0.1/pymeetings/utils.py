import pandas as pd
from datetime import datetime
import os

def str2date(strdat):
    """
    Function that transforms a str into datetime format
    
    :param str strdat: date in the format of a string
    """
    return datetime.strptime(strdat,'%Y/%m/%d %H:%M')


def date2str(datstr):
    """
    Function that transforms a datetime into a string

    :param date datstr: date in datetime format
    """
    return datetime.strftime(datstr, '%Y/%m/%d %H:%M')




def citycheck(city):
    """
    Function that checks if the city is within the list of cities available
    
    :param str city: the city that we would like to check against
    """
    dirname = os.path.dirname(__file__)
    city = city.lower()
    df_cities = pd.read_csv(dirname+'/'+'world_cities.csv')
    cities_list = df_cities['name'].tolist()
    cities_list = [cit.lower() for cit in cities_list]
    condition = city in cities_list
    return condition


def country(city):
    """
    Function that gets the country where the city is 

    :param str city: the city that we would like to check against
    """
    dirname = os.path.dirname(__file__)
    df = pd.read_csv(dirname+'/'+'world_cities.csv')
    if citycheck(city):
        thecountry = df[df['name'] == city]['country'].tolist()
        return thecountry[0]
    else:
        print('The city is not in our DB')
        
