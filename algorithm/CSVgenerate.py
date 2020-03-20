import csv
def ListToCSVFileGenerate(lst, CSVname, fieldnames):
    print("generate CSV file....")
    with open(CSVname+'.csv', 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=fieldnames)
        writer.writeheader()
        for item in lst:
            writer.writerow({fieldnames[0]: item[0],
                             fieldnames[1]: item[1]})
    print("Your CSV file is generated!")