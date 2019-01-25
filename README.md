# Konfliktplan

--------------------  Prerequisites  -------------------<br>
Die folgenden Dateien müssen vorliegen:<br>
	Credentials.txt<br>
	Regelstudienplaene.csv<br>
	Veranstaltungen.csv<br>


--------------------  Installation  --------------------
1. Von der Kommandozeile: git clone https://github.com/markus-flicke/Konfliktplan
2. Python3.x Installation: python.org/downloads
3. Vom Ordner Konfliktplan/ aus soll in der Kommandozeile der folgende Befehl ausgeführt werden: 
	pip install -r requirements.txt
4. Um einige Daten nicht öffentlich zu machen, müssen noch Dateien in die folgenden Ordner geschoben werden:<br>
<br>	(i)	Credentials.txt -> Credentials/
<br>	(ii)	Regelstudienplaene.csv -> Regelstudienplaene/
<br>	(iii)	Veranstaltungen.csv -> Veranstaltungen/

	Dabei ist der Dateiname egal und nur der Zielordner entscheidend. Die Dateien sollte der User schon haben, bevor der Installationsprozess beginnt.
5. Die Datei Konfliktplan/recipient.txt soll der Emailadresse des aktuellen Users angepasst werden. 
6. Starten des Programmes:<br>
	Aus der Kommandozeile:<br>
		python konfliktplan.py

--------------------  DataTypes  -----------------------<br>
Die Eingabedateien Regelstudienplaene.csv, Veranstaltungen.csv müssen im CSV Format vorliegen um lesbar zu sein.
