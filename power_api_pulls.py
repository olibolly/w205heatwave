import urllib, json, csv

states={"AL","AK","AZ","AR","CA","CO","CT","DC","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"}
sectors={"RES","COM","TRA","IND"}
series = {"SALES","PRICE"}

for t in series:
    writerFile = open("c:\Temp\%s_schema.csv" % t, 'wb')
    wr = csv.writer(writerFile, quoting=csv.QUOTE_ALL)
    wr.writerow(['STATE:string','SECTOR:string','YEAR:integer','MONTH:integer',t+':float'])
    writerFile.close()
    writerFile = open("c:\Temp\%s.csv" % t, 'wb')
    wr = csv.writer(writerFile, quoting=csv.QUOTE_ALL)
    for st in states:
        for sec in sectors:
            print "%s,%s" % (st,sec)
            url = "http://api.eia.gov/series/?api_key=A240105C5656C5D46316A0E93888F152&series_id=ELEC.%s.%s-%s.M" % (t,st,sec)
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            if 'series' in dict.keys(data):
                for x in data['series'][0]['data']:
                    wr.writerow([st,sec,x[0][:4],x[0][4:],x[1]])
    writerFile.close()

#Schema and API requirements for Generation are different, hence slightly different code
t = "GEN"
writerFile = open("c:\Temp\%s_schema.csv" % t, 'wb')
wr = csv.writer(writerFile, quoting=csv.QUOTE_ALL)
wr.writerow(['STATE:string','YEAR:integer','MONTH:integer',t+':float'])
writerFile.close()
writerFile = open("c:\Temp\%s.csv" % t, 'wb')
wr = csv.writer(writerFile, quoting=csv.QUOTE_ALL)
for st in states:
    url = "http://api.eia.gov/series/?api_key=A240105C5656C5D46316A0E93888F152&series_id=ELEC.%s.ALL-%s-99.M" % (t,st)
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    for x in data['series'][0]['data']:
        wr.writerow([st,x[0][:4],x[0][4:],x[1]])
writerFile.close()
