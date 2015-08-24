import csv

csvFile = 'chicago_landmarks_reconstructed.csv'
xmlFile = 'chicago_landmarks_reconstructed.kml'

csvData = csv.reader(open(csvFile), delimiter=';')
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
              '</LookAt>' + '\n')

fieldIndices = [1,2,3,4,5,6]
fieldNames = ['NAME','ID','ADDRESS','DATE_BUILT','ARCHITECT','LANDMARK']
geomIndex = 8

rowNum = 0
for row in csvData:
    if rowNum > 1:
        xmlData.write('<Placemark>' + '\n')
        xmlData.write('<description>' + '\n')
        xmlData.write('<![CDATA[<h4>geo_bddq-yxar-1</h4>' + '\n\n')
        xmlData.write('<ul class=\"textattributes\">' + '\n\n')

        for i in range(len(fieldIndices)):
            xmlData.write('<li><strong><span class="atr-name">' + 
                          fieldNames[i] +
                          '</span>:</strong> <span class="atr-value">' +
                          row[fieldIndices[i]].strip() +
                          '</span></li>' + '\n')
        
        xmlData.write('</ul>' + '\n')
        xmlData.write(']]>')
        xmlData.write('</description>' + '\n')

        # Most importantly, the geom information
        xmlData.write(row[geomIndex])
        
        xmlData.write('</Placemark>' + '\n')
        
    rowNum +=1

xmlData.write('</Document>')
xmlData.write('</kml>')
xmlData.close()
