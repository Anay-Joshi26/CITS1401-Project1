# Kyle Capelli
# CITS1401
# Semester 2 - Project 1

def locationDictionaryCreator(inputFile):
    """
    A function that reads the CSV file and stores the data in a dictionary
    in the form {LocID, [Latitude, Longitude, Category]}
    The location_dictionary is then returned.
    """
    data = []     # Temporary list to store matrix of CSV values
    location_dictionary = {}     # Dictionary of each location
    
    # Opens and reads the CSV file and stores values in data as a matrix
    with open(inputFile, 'r') as file:
        for line in file:
            data.append(line.rstrip("\n").upper().split(","))
    
    # Finds the index of each header title 
    loc = 0
    lat = 0
    long = 0
    cat = 0

    for col in range(len(data[0])):
        if data[0][col] == 'LOCID':
            loc = col
        if data[0][col] == 'LATITUDE':
            lat = col
        if data[0][col] == 'LONGITUDE':
            long = col
        if data[0][col] == 'CATEGORY':
            cat = col
    
    data.pop(0)
    
    # Stores the data into location_dictionary
    for row in data:
        location_dictionary[row[loc]] = [float(row[lat]), float(row[long]), \
                                         row[cat]]
        
    return location_dictionary
    
    
def locationFinder(lat, long, east_west_limit, \
                   north_south_limit, location_values):
    """
    A function that finds if the location falls within the north, south,
    east and west boundaries.
    If the location does, the location ID is added to the location_list.
    The location_list is then returned.
    """
    
    N_boundary = long + north_south_limit
    E_boundary = lat + east_west_limit
    S_boundary = long - north_south_limit
    W_boundary = lat - east_west_limit

    location_list = []
    
    for item in location_values.items():
        location = list(item)
        location_lat = location[1][0]
        location_long = location[1][1]
        
        if location_lat <= E_boundary and location_lat >= W_boundary and \
           location_long <= N_boundary and location_long >= S_boundary:
            location_list.append(location[0])
        
    return location_list


def locationCategoryFinder(location_list, category, data):
    """
    Returns a list of location ID's if they have the same category
    value as the parameter 'category'.
    """
    same_category_list = []
    
    for location in location_list:
        if data.get(location)[2] == category:
            same_category_list.append(location)
            
    return same_category_list


def sortedCartesianPoints(location_list, x1, y1, data):
    """
    A function that returns a list of the distances based on the
    Cartesian coordinate system.
    """
    location_distances = []
    
    for location in location_list:
        x2 = data.get(location)[0]
        y2 = data.get(location)[1]
        
        location_distances.append(round(((x2 - x1) ** 2 + \
                                         (y2 - y1) ** 2) ** (1/2),4))
        
    return(sorted(location_distances))


def mean(data):
    """
    A function that works out the mean of each value in a data
    set (provided as a list).
    If there is a division by 0 the value returned is 0.
    """
    average = 0
    
    if len(data) == 0:
        return 0
    else:
        for value in data:
            average += value
    
    return average / len(data)


def stdevation(data):
    """
    A funtion that works out the standard deviation of the data
    set (provided as a list).
    If the length of the data is 0 or 1, the return value will be 0.
    """
    variance = 0
    if len(data) == 0 or len(data) == 1:
        return 0
    else:
        for value in data:
            variance += (value - mean(data)) ** 2
    
    return (variance / len(data)) ** (1/2)


def main(inputFile, queryLocId, d1, d2):
    
    # Reads through CSV file and creates a dictionary containing each
    # element in the data set.
    # LocID (from CSV file) and queryLocId are converted to uppercase.
    # Throws an exception if the file is not found and returns 4 empty lists
    try:
        location_dictionary = locationDictionaryCreator(inputFile)
        location_ID = queryLocId.upper()
        location_list = None
    
        # Check to see if queryLocId is in the dictionary - if not,a message is
        # printed informing the user that the location ID provided does not exist
        if location_ID not in location_dictionary:
            print("Location ID not found.")
            location_list = []
            category_list = []
            sorted_distances = []
            mean_stdev = []
    
        # Check to see if d1 or d2 are negative - if they are it prints a message to
        # instruct the user to enter a positive number
        elif d1 < 0 or d2 < 0:
            print("Please provide a positive number for the latitude " +
                  "and longitude boundaries.")
            location_list = []
            category_list = []
            sorted_distances = []
            mean_stdev = []
    
        else:
            # Retrieves the values of the specified location ID in the parameter
            # and stores each one.
            latitude = location_dictionary.get(location_ID)[0]
            longitude = location_dictionary.get(location_ID)[1]
            category = location_dictionary.get(location_ID)[2]
    
            # Filters through the dictionary to find all values that lie within the
            # specified boundary.
            # d1 extends east-west boundary.
            # d2 extends north-south boundary.
            location_list = locationFinder(latitude, longitude, d1, d2, \
                                           location_dictionary)
            location_list.remove(location_ID)
    
            # Stores all locations from location_list (created above) that have
            # the same category as queryLocId.
            category_list = locationCategoryFinder(location_list, category, \
                                                   location_dictionary)
    
            # Stores a list containing the distances of the locations from queryLocID
            # in ascending order.
            sorted_distances = sortedCartesianPoints(category_list, latitude, \
                                                     longitude, location_dictionary)
    
        # Stores a list of the mean and standard deviation of sorted_distances.
        # Checks to see if there is the sorted distances list contains any elements -
        # if not then mean_stdev will equal an empty list.
        if len(sorted_distances) == 0:
            mean_stdev = []
        else:
            mean_stdev = ([round(mean(sorted_distances), 4), \
                           round(stdevation(sorted_distances),4)])
        
        return location_list, category_list, sorted_distances, mean_stdev
    
    except FileNotFoundError:
        print("Wrong file or file path.")
        return [], [], [], []