import numpy as np
import csv

property_obj = open('Material Properties.txt', 'r')
read_data = csv.reader(property_obj, delimiter = ' ', quoting = csv.QUOTE_NONNUMERIC)
air_properties = []
ammonia_properties = []
engine_oil_properties = []
for num, row in enumerate(read_data):
    if num <= 34:
        air_properties.append(row)
    elif num <= 49:
        ammonia_properties.append(row)
    elif num <= 66:
        engine_oil_properties.append(row)

air_array = np.array(air_properties)
ammonia_array = np.array(ammonia_properties)
engine_oil_array = np.array(engine_oil_properties)
property_obj.close()

water_obj = open('Water Properties.txt', 'r')
water_data = csv.reader(water_obj, delimiter = ' ', quoting = csv.QUOTE_NONNUMERIC)
water_properties = []
for num, row in enumerate(water_data):
    water_properties.append(row)

water_array = np.array(water_properties)
water_array = np.delete(water_array, [1, 2, 3, 4, 6, 8, 10, 12, 13, 15], 1)
water_array = np.insert(water_array, 1, [1000], 1)
water_array = np.insert(water_array, 4, [0], 1)
water_array = np.insert(water_array, 6, [0], 1)
water_obj.close()

property_list = ['t', 'p', 'cp', 'mu', 'v', 'k', 'a', 'pr', 'b']
def search(material_name, property, temperature):
    column = property_list.index(property)
    if material_name == 'Air':
        material_array = air_array
    elif material_name == 'Ammonia':
        material_array = ammonia_array
    elif material_name == 'Water':
        material_array = water_array
    for num, row in enumerate(material_array):
        if temperature <= row[0]:
            answer = row[column] - ((row[column] - material_array[num - 1][column]) * (row[0] - temperature)) / (row[0] - material_array[num - 1][0])
            break
    return answer