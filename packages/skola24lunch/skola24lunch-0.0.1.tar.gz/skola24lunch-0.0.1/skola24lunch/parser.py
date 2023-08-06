#!/usr/bin/env python3
import json, requests, re, sys

class Skola24Parser:
    def __init__(self, domain, name, xscope="8a22163c-8662-4535-9050-bc5e1923df48"):
        self.domain = domain
        self._xscope = xscope

        self.schools = None
        self.classes = None

        self.render_key = None

        self.headers = {
            "X-Scope": self._xscope,
            "Content-Type": "application/json"
        }

        self.session = requests.Session()

        self.timestamp_re = re.compile('[\d]{1,2}:[\d]{2}')

        self.current_school = self.get_school(name)


    def _get_render_key(self):
        r = self._get("https://web.skola24.se/api/get/timetable/render/key")
        self.render_key = r.json()['data']['key']
        return self.render_key


    def _post(self, url, data):
        return self.session.post(url, headers=self.headers, data=json.dumps(data))
    def _get(self, url):
        return self.session.get(url, headers=self.headers)

    def get_school(self, name):
        r = self._post("https://web.skola24.se/api/services/skola24/get/timetable/viewer/units", {
            "getTimetableViewerUnitsRequest": {
                "hostName": self.domain
            }
        })
        data = r.json()['data']['getTimetableViewerUnitsResponse']['units']
        self.schools = data
        find_school = list(filter(lambda x: x['unitId'] == name, data))
        if len(find_school) > 0:
            self.current_school = find_school[0]
        else:
            self.current_school = None
        return self.current_school

    def get_classes(self):
        body = {
            "hostName": self.domain,
            "unitGuid": self.current_school['unitGuid'],
            "filters": {
                "class": True,
                "course": False,
                "group": False,
                "period": False,
                "room": False,
                "student": False,
                "subject": False,
                "teacher": False
            }
        }
        r = self._post("https://web.skola24.se/api/get/timetable/selection", body)
        self.classes = r.json()['data']['classes']
        return self.classes

    def get_class(self, name):
        if not self.classes:
            self.get_classes()
        find = list(filter(lambda x: x['groupName'] == name, self.classes))
        if len(find) > 0:
            return find[0]
        return None

    def get_timetable_data(self, class_name):
        body = {
            "renderKey": self._get_render_key(),
            "host": self.domain,
            "unitGuid": self.current_school['unitGuid'],
            "startDate": None,
            "endDate": None,
            "scheduleDay": 0,
            "blackAndWhite": False,
            "width": 10000,
            "height": 10000,
            "selectionType": 0,
            "selection": self.get_class(class_name)['groupGuid'],
            "showHeader": False,
            "periodText": "",
            "week": 48,
            "year": 2020,
            "privateFreeTextMode": None,
            "privateSelectionMode": False,
            "customerKey": ""
        }
        r = self._post("https://web.skola24.se/api/render/timetable", body)
        data = r.json()['data']['timetableJson']
        data = json.loads(json.dumps(data)[1:-1].replace("\\", ""))

        return data

    def get_timeslot(self, class_name, timeslot):
        ignore_fontsize = 0
        data = self.get_timetable_data(class_name)
        for el in data['textList']:
            if self.timestamp_re.match(el['text']):
                ignore_fontsize = el['fontsize']
                break
        # Get all timestamps
        times = list(filter(lambda x: self.timestamp_re.match(x['text']) and x['fontsize'] != ignore_fontsize, data['textList']))

        lunch = list(filter(lambda x: timeslot.lower() in x['text'].lower(), data['textList']))
        lunch_boxes = []
        for i in range(len(lunch)):
            lunch_boxes.append(list(filter(lambda x: "width" in x
                                   and x['bcolor'] == '#C0C0C0' # TODO
                                   and lunch[i]['x'] >= x['x']
                                   and lunch[i]['x'] <= x['x'] + x['width']
                                   and lunch[i]['y'] >= x['y']
                                   and lunch[i]['y'] <= x['y'] + x['height'], data['boxList']))[0])
        def nearest(value, arr, key):
            if len(arr) < 1:
                return None
            closest = arr[0]
            for el in arr:
                if abs(el[key] - value) < abs(closest[key] - value):
                    closest = el
            return closest

        correct_times = []
        for i in range(len(lunch)):
            start = nearest(lunch_boxes[i]['y'], times, 'y')['text']
            end = nearest(lunch_boxes[i]['y']+lunch_boxes[i]['height']+times[0]['fontsize'], times, 'y')['text']
            correct_times.append((start, end))
        return correct_times
