#!/usr/bin/env nix-shell --run python3

import csv
import os
import json
import easygui
import datetime
import pdfkit

class Member:
    def __init__(self, name):
      self.first_name = name.split(",")[1]
      self.last_name = name.split(",")[0]
      self.tithes = []
      self.missions = []
      self.building = []
      self.special = []

    def add_tithe(self, date, amount):
        self.tithes.append([date,amount])

    def add_missions(self, date, amount):
        self.missions.append([date,amount])

    def add_building(self, date, amount):
        self.building.append([date,amount])

    def add_special(self, date, amount):
        self.special.append([date, amount])

    def get_name(self):
        return self.last_name + ", " + self.first_name

    def get_tithes(self):
        return self.tithes

    def get_missions(self):
        return self.missions

    def get_building(self):
        return self.building

    def get_special(self):
        return self.special

    def get_total_tithes(self):
        total = 0
        for c in self.tithes:
            total += int(c[1])
        return total

    def get_total_missions(self):
        total = 0
        for c in self.missions:
            total += int(c[1])
        return total

    def get_total_building(self):
        total = 0
        for c in self.building:
            total += int(c[1])
        return total

    def get_total_special(self):
        total = 0
        for c in self.special:
            total += int(c[1])
        return total

    def get_all_total(self):
        total = 0
        total += self.get_total_tithes()
        total += self.get_total_missions()
        total += self.get_total_building()
        total += self.get_total_special()
        return total

def extract_name(line):
    # Extract name
    if(line[0] != "" and ("Total" not in line[0] )):
        last_name = line[0].strip().lstrip(' \ufeff" ')
        first_name = line[1].strip().rstrip('"')
        return last_name + "," + first_name

def extract_data(line, report):
    # Expects ,,date,account,amount

    if("Tithes and Offerings" in line[3]):
        report.add_tithe(line[2], line[4])
    elif("Mission Offerings" in line[3]):
        report.add_missions(line[2], line[4])
    elif("Building" in line[3]):
        report.add_building(line[2], line[4])
    elif("Special Love Offerings" in line[3]):
        report.add_special(line[2], line[4])

class Format():
  def __init__(self, data, template):
    self.data = data
    self.file = template;
    self.options = {
      'page-size': 'Letter',
      'encoding': 'UTF-8',
      'dpi': 600,
      'grayscale': False,
      'enable-local-file-access': None
    }
    with open(self.file,"r") as file:
      self.template = file.read()

  def injectDates(self):
    self.date = datetime.datetime.now()
    self.today_date = self.date.strftime("%m/%d/%Y")
    self.year_begin_date = self.date.strftime("1/1/%Y")
    self.year_end_date = self.date.strftime("12/31/%Y")
    self.template = self.template.replace("%%STATEMENT_DATE%%", self.today_date)
    self.template = self.template.replace("%%YEAR_BEGIN_DATE%%", self.year_begin_date)
    self.template = self.template.replace("%%YEAR_END_DATE%%", self.year_end_date)

  def injectTotals(self):
    self.template = self.template.replace('%%TOTAL_CONTRIBUTIONS%%', '$'+str(self.data['total']))
    self.template = self.template.replace('%%TOTAL_TITHES%%', '$'+str(self.data['totalTithes']))
    self.template = self.template.replace('%%TOTAL_MISSIONS%%', '$'+str(self.data['totalMissions']))
    self.template = self.template.replace('%%TOTAL_BUILDING%%', '$'+str(self.data['totalBuilding']))
    self.template = self.template.replace('%%TOTAL_SPECIAL%%', '$'+str(self.data['totalSpecial']))

  def injectDataRowsHTML(self, category):
    self.html = ""
    for d in self.data[category]:
      self.html = self.html + f'<tr><td>{d[0]}</td><td align="right">${d[1]}</td></tr>\n'
    return self.html

  def injectTithesData(self):
    self.template = self.template.replace('%%TITHE_DATA_ROWS%%', self.injectDataRowsHTML('tithes'))

  def injectMissionsData(self):
    self.template = self.template.replace('%%MISSIONS_DATA_ROWS%%', self.injectDataRowsHTML('missions'))

  def injectBuildingData(self):
    self.template = self.template.replace('%%BUILDING_DATA_ROWS%%', self.injectDataRowsHTML('building'))

  def injectSpecialData(self):
    self.template = self.template.replace('%%SPECIAL_DATA_ROWS%%', self.injectDataRowsHTML('special'))

  def injectNames(self):
    self.template = self.template.replace('%%CONTRIBUTER_NAME%%', self.data['name'])


  def generateReport(self, target_folder):
    self.injectNames()
    self.injectDates()
    self.injectTotals()
    self.injectTithesData()
    self.injectMissionsData()
    self.injectBuildingData()
    self.injectSpecialData()
    with open(target_folder+self.data['name']+".html","w") as file:
      file.write(self.template)
    pdfkit.from_file(target_folder+self.data['name']+".html",target_folder+self.data['name']+'.pdf',options=self.options)


def main():
    reports = []
    current_record = 0
    target = easygui.fileopenbox()
    report_folder = os.path.dirname(target)+"/reports/"

    # Iterate through CSV lines and process into 'reports'
    for line in csv.reader(open("joe.csv")):
        if(line[0] != "" and "Total" not in line[0]):
            name = extract_name(line).rstrip(",")
            reports.append(Member(name))
        if("Total" in line[0]):
            # This is how I know that this report is done
            # It is not needed since the Member class totals everything for us
            current_record += 1
        else:
            extract_data(line,reports[current_record])

    # Inject JSON data into html template
    for r in reports:
      templateData = {
          "name": r.get_name(),
          "tithes": r.get_tithes(),
          "missions": r.get_missions(),
          "building": r.get_building(),
          "special": r.get_special(),
          "total": r.get_all_total(),
          "totalTithes": r.get_total_tithes(),
          "totalBuilding": r.get_total_building(),
          "totalMissions": r.get_total_missions(),
          "totalSpecial": r.get_total_special()
          }
      f = Format(templateData,'template.html')
      f.injectDataRowsHTML('tithes')
      f.generateReport(report_folder)

    return 0


if __name__=="__main__":
    main()
