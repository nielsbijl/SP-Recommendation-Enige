import psycopg2
import csv
import CSVgenerate

try:
    connection = psycopg2.connect(user="postgres",
                                  password="niels16",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()
    fetchproductsSQL = """ select * from profiles;"""
    cursor.execute(fetchproductsSQL)
    profiles = cursor.fetchall()
    fetchproductsSQL = """ select * from profiles_previously_viewed;"""
    cursor.execute(fetchproductsSQL)
    profiles_previously_viewed = cursor.fetchall()
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

def listSegmentWithProfiles(profiles):
    """Create list in format:"""
    """['buyer', [['5a39710ded2959000103ce9d', []], ['5a397159ed2959000103ceff', []], ['5a3982eca825610001bbd607', []]]]"""
    print("Create list of segment with all the profiles")
    segmentWithProfile = []
    segments = set({})
    for segmentSearch in profiles:
        segments.add(segmentSearch[2])
    segments = list(segments)
    for item in segments:
        segmentWithProfile.append([item, []])
    for profile in profiles:
        count = 0
        for segment in segments:
            if segment == profile[2]:
                segmentWithProfile[count][1] += [[profile[0], []]]
            count += 1
    return segmentWithProfile

def segmentWithViewedProducts(segmentWithProfiles, profiles_previously_viewed):
    """Create list in format:"""
    """['buyer', ["productID", "productID"]]"""
    print("Making a list with al the viewed products on all the segments")
    segmentCount = 0
    segmentWithProduct = []
    for segment in segmentWithProfiles:
        segmentWithProduct += [[segment[0], []]]
        for profiles in segment[1]:
            for profilesViewed in profiles_previously_viewed:
                if profiles[0] == profilesViewed[0]:
                    segmentWithProduct[segmentCount][1] += [profilesViewed[1]]
        print(segmentWithProduct[segmentCount])
        segmentCount += 1
    return segmentWithProduct

def mostFrequentItemInList(lst):
    if not lst:
        return None
    counter = 0
    mostFreq = lst[0]
    for item in lst:
        currentFreq = lst.count(item)
        if (currentFreq > counter):
            counter = currentFreq
            mostFreq = item
    return mostFreq

def segmentWithMostViewedProduct(segmentWithAllViewedProducts):
    print("Choosing most populair product......")
    segmentWithPopulairProduct = []
    for segment in segmentWithAllViewedProducts:
        populairProduct = mostFrequentItemInList(segment[1])
        segmentWithPopulairProduct += [[segment[0], populairProduct]]
    return segmentWithPopulairProduct


segmentWithProfile = listSegmentWithProfiles(profiles)
segmentWithAllViewedProducts = segmentWithViewedProducts(segmentWithProfile, profiles_previously_viewed)
segmentPopulairProduct = segmentWithMostViewedProduct(segmentWithAllViewedProducts)
CSVgenerate.ListToCSVFileGenerate(segmentPopulairProduct, "segmentPopulairProduct", ['segment', 'prodid'])

