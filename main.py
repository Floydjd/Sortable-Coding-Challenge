import json
import collections

# FUNCTIONS START
# Formats data so it is easier to match
def format(str):
    return str.replace("-", "") \
                .replace(" ", "") \
                .replace("'", "") \
                .replace('"', '') \
                .replace("+", "") \
                .replace(";", "") \
                .replace(":", "") \
                .replace(",", "") \
                .upper()


# Reads in a file of JSON lines format and returns dictionaries contained in array
def parseFile(f):
    with open(f, "r") as ins:
        objs = []
        for line in ins:
            obj = json.loads(line)
            objs.append(obj)
        return objs

# FUNCTIONS END

#SCRIPT START

# Filenames
productsFilename = "products.txt"
listingsFilename = "listings.txt"
resultsFilename = "results.txt"

# Input files
products = parseFile(productsFilename)
listings = parseFile(listingsFilename)

output = open(resultsFilename, "wb")

print "Matching...\n"

# Begin matching loop
# Iterate through products and listings
for product in products:
    result = collections.OrderedDict()
    matchedListings = []
    for listing in listings:
        # Step 1: Match manufacturers
        if product['manufacturer'] in listing['manufacturer']:
            # Step 2: Search for product.model in listing.title
            # (First do some formatting for matching purposes)
            prodModel = format(product['model'])
            # Split title into words and then format each word
            listTitle = listing['title'].split()
            for i in range(len(listTitle)):
                listTitle[i] = format(listTitle[i])
            # If the model id is found in title,
            # add this listing to matches collection
            if prodModel in listTitle:
                matchedListings.append(listing)


    # Remove all matches from listings
    for match in matchedListings:
        listings.remove(match)

    # Format any results and write them to output file
    result['product_name'] = product['product_name']
    result['listings'] = matchedListings
    resultJson = json.dumps(result)
    output.write(resultJson + "\n")



output.close()

print "Done!\n"
# SCRIPT END
