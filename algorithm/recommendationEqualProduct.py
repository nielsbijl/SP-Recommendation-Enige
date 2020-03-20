import psycopg2
import random
import CSVgenerate

try:
    connection = psycopg2.connect(user="postgres",
                                  password="niels16",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()
    fetchproductsSQL = """ select * from products;"""
    cursor.execute(fetchproductsSQL)
    products = cursor.fetchall()
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

def subsubcatSorted(products):
    """Zorgt dat per subsubcategorie alle producten zijn onderverdeeld"""
    """maak lijst met de volgende format [['Voetschimmel', [ '29614']], ['Muziek', ['42268']]]"""
    subsubcat = set({})
    catandproductid = []
    for product in products:
        subsubcat.add(product[6])
    for cat in subsubcat:
        catandproductid.append([cat,[]])
    for product2 in products:
        count = 0
        for cat2 in catandproductid:
            if product2[6] == cat2[0]:
                catandproductid[count][1] += [product2[0]]
                break
            count += 1
    return catandproductid

def giveAllProductsEqualProduct(subsubcatSortedlist):
    """Maakt de uiteindelijke lijst van [[product, vergelijkbaar product], [product, vergelijkbaar product]]"""
    equalProductList = []
    for category in subsubcatSortedlist:
        for productID in category[1]:
            randomProduct = random.choice(category[1])
            if productID == randomProduct:
                randomProduct = random.choice(category[1])
            equalProductList += [[productID, randomProduct]]
    return equalProductList

CSVgenerate.ListToCSVFileGenerate(giveAllProductsEqualProduct(subsubcatSorted(products)), "equalProducts", ['prodid', 'equalid'])


