import pandas as pd
from pyquery import PyQuery
import subprocess
import requests
import sys
import os

global nl
nl = b'\n'

working_apn = sys.argv[1]
working_apn_path = "apns/split-apns/" + working_apn


global apn
apn = []
with open(working_apn_path, "r") as f:
	for line in f:
		line = line.strip("\n")
		apn.append(line)
    
assesor_link = "https://maps.clarkcountynv.gov/assessor/AssessorParcelDetail/ParcelDetail.aspx?hdnParcel=178-20-814-117&hdnInstance=pcl7"

treasury_link = "https://trweb.co.clark.nv.us/WEP_summary.asp?Parcel=178-20-814-117" 

def grep(expression, file):
    cmd = ["grep", expression, file]
    line = subprocess.run(cmd, stdout=subprocess.PIPE)
    text = line.stdout
    l = text.strip(nl)
    return l

global assesor_spanz
assesor_spanz = ["span#lblParcel", "span#lblOwner1", "span#lblAddr1",
         "span#lblAddr2", "span#lblAddr3", "span#lblAddr4",
         "span#lblLocation", "span#lblTown", "span#lblAcres",
         "span#lblSalePrice", "span#lblSaleDate", "span#lblSaleType",
         "span#lblLandUse"]

global treasury_spanz
treasury_spanz = ["span#lblConstrYr", "span#lblSalePrice", "span#lblSaleDate",
                 "span#lblSaleType", "span#lblLandUse"]

dict = {"A": [], "B": [], "C": [], "D": [], "E": [], "F": [],
        "G": [], "H": [], "I": [], "J": [], "K": [], "L": [],
        "M": [], "N": [], "N2": []}

def ass_scrape(ass_link, apn_number):
    try:
        link = assesor_link.replace("178-20-814-117", apn_number)
        html = requests.get(link).text
        pq = PyQuery(html)
        texts = []
        for item in assesor_spanz:
            texts.append(pq(item).text())

        A = texts[0]
        B = texts[1]
        C = texts[2]
        D = texts[3] + " " + texts[4] + " " + texts[5]
        E = texts[6] + " " + texts[7]
        F = texts[8]
        G = texts[9]
        H = texts[10]
        I = texts[11]
        J = texts[12]

        spans = [A, B, C, D, E, F, G, H, I, J]
        Keys = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        for x in range(10):
            dict[Keys[x]].append(spans[x])
        return dict, 1

    except:
        print("Error ass_scrape() APN: %s", apn_number)
        pass

def tres_scrape(tres_link, apn_number, dict):
    try:
        link = tres_link.replace("178-20-814-117", apn_number)
        print(link)

        html = requests.get(link).text
        pq = PyQuery(html)

        items = [item.text() for item in pq.items('font')]
        itemz = [item.text() for item in pq.items("td.CellData")]

        K = items[9]
        L = itemz[-5]
        M = itemz[-4]
        N = itemz[-1]
        N_two = itemz[-2]

        dict["K"].append(K)
        dict["L"].append(L)
        dict["M"].append(M)
        dict["N"].append(N)
        dict["N2"].append(N_two)
        
        return dict

    except:
        print("Error in tres_scrape() APN: ", apn_number)

############################################################################

count = 0
try:

    for num in range(len(apn)):
        data = ass_scrape(assesor_link, apn[num])
        if data[1] == 1:
            tres_scrape(treasury_link, apn[num], data[0])
            print("SUCCESS on : ", apn[num], "\n\n")
            count += 1
            print(count)

        if count % 500 == 0:
            df = pd.DataFrame.from_dict(dict, orient="columns")

        else:
            pass
            x = apn[num]
except:
        print("Error at ", x)

   

df.to_csv("Virostek-Data-" + working_apn, index=False, header=True)


#############################################################################


#for x in range(5):
#    data = ass_scrape(assesor_link, apn[x])
#    if data[1] == 1:
#        print(tres_scrape(treasury_link, apn[x], data[0]))
#        print("\n\n")
#    else:
#        print("Failed on : %s", apn[x])



    
    
    



    



