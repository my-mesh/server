# Web Server
Der Web Server für das Projekt, welcher die Kommunikation, Darstellung und das Speicher der Daten verwaltet. Als WebFramework wird Flask benutzt mit einer sqlite Datenbank.

## Einstieg
```sh
git clone https://github.com/my-mesh/server.git
cd server
python -m venv env
. env/bin/activate
pip install -r requirements.txt
flask init-db
flask run
```

## Projekt Aufbau
- Ein Dashboard welches aktuelle Daten sowie neue Nodes anzeigt
- Nodes Übersichtsseite, welche alle Geräte anzeight
- Node Detailseiten welche die gesammelten Daten für die jeweilige Node anzeigen
- Info Seite welche auf dem Bildschirm der Box abgebildet wird
- Einstellungs Seite für den Info Screen bei welchem dieser angepasst werden kann
- Die Möglichkeit neue Nodes hinzuzufügen
- Die Möglichkeit Nodes anzupassen
- Die Möglichkeit Daten in der Datenbank abzuspeichern
