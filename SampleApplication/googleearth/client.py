import psycopg2
import csv
import os, subprocess

xmlFile = 'chicago_landmarks_selection.kml'
xmlData = open(xmlFile, 'w')

# Write out the beginning of the kml
xmlData.write('<?xml version="1.0" encoding="UTF-8"?>'
              '<kml xmlns="http://www.opengis.net/kml/2.2" '
              'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
              'xsi:schemaLocation="http://www.opengis.net/kml/2.2 '
              'http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd">'
              '<Document xmlns:atom="http://purl.org/atom/ns#">'
              '<name>geo_bddq-yxar:geo_bddq-yxar-1</name>'
              '<LookAt>'
              '<longitude>-87.67361275067813</longitude>'
              '<latitude>41.8427972613491</latitude>'
              '<altitude>56756.72380582584</altitude>'
              '<range>45862.40982007242</range>'
              '<tilt>0.0</tilt>'
              '<heading>0.0</heading>'
              '<altitudeMode>clampToGround</altitudeMode>'
              '</LookAt>'
              '<Style id="myIcon">'
              '<IconStyle>'
              '<Icon>'
              '<href>http://maps.google.com/mapfiles/kml/pal4/icon25.png</href>'
              '</Icon>'
              '<scale>1.2</scale>'
              '</IconStyle>'
              '</Style>')

# Connect to an existing database
conn = psycopg2.connect("dbname=landmarks_db user=postgres host=/tmp")

# Open a cursor to perform database operations
cur = conn.cursor()

# Query the database and obtain data as Python objects
cur.execute(
    "SELECT  L.shortname, D.name, D.desc_id, D.address, D.date_built, "
    "D.architect, "
    "to_char(D.landmark,'MM/DD/YYYY') AS lm, "
    "to_char(L.longitude,'S999D999999999') AS lt, "
    "to_char(L.latitude,'S99D999999999') AS la "
    "FROM description D, landmarks L "
    "WHERE L.land_id = D.desc_id AND D.name LIKE '%Theater%';"
)

fieldIndices = [2,3,4,5,6]
fieldNames = ['ID','ADDRESS','DATE_BUILT','ARCHITECT','LANDMARK']

# Loop over the returned tuples and build the kml
for record in cur:
    xmlData.write('<Placemark id=\"' + record[0].strip() + '\">' + '\n')
    xmlData.write('<name><![CDATA[' + record[1].strip() + ']]></name>' + '\n')
    xmlData.write('<styleUrl>#myIcon</styleUrl>' + '\n')
    xmlData.write('<description>' + '\n')
    xmlData.write('<![CDATA[' + '\n\n')
    xmlData.write('<ul class=\"textattributes\">' + '\n\n')
    
    for i in range(len(fieldIndices)):
        fieldValue = record[fieldIndices[i]]
        if fieldValue is not None:
            xmlData.write('<li><strong><span class="atr-name">' + 
                          fieldNames[i] +
                          '</span>:</strong> <span class="atr-value">' +
                          fieldValue.strip() +
                          '</span></li>' + '\n')
        
    xmlData.write('</ul>' + '\n')
    xmlData.write(']]>')
    xmlData.write('</description>' + '\n')

    # Most importantly, the location of the landmark
    xmlData.write('<Point><coordinates>' + record[7].strip() + ',' + record[8].strip() 
                  + '</coordinates></Point>')

    xmlData.write('</Placemark>' + '\n')

xmlData.write('</Document>')
xmlData.write('</kml>')
xmlData.close()

# Close communication with the database
cur.close()
conn.close()

# Open Google Earth on the produced kml
# FNULL = open(os.devnull, 'w')
# args = ['/opt/google/earth/free/google-earth', 
#         '/home/alice/Downloads/LDV/chicago_landmarks_selection.kml']
# subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

