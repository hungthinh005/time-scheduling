from model.Constant import Constant
from model.Reservation import Reservation
from collections import defaultdict
import streamlit as st
import json
class HtmlOutput:
    ROOM_COLUMN_NUMBER = Constant.DAYS_NUM + 1
    ROOM_ROW_NUMBER = Constant.DAY_HOURS + 1
    # COLOR1 = "#319378"
    # COLOR2 = "#CE0000"
    CRITERIAS = ('R', 'S', 'L', 'P', 'G')
    # CRITERIAS_DESCR = ("Current room has {any}overlapping", "Current room has {any}enough seats",
    #                    "Current room with {any}enough computers if they are required",
    #                    "Professors have {any}overlapping classes", "Student groups has {any}overlapping classes")
    PERIODS = (
        "","8 - 8h50", "8h50 - 9h40", "9h40 - 10h30", "10h35 - 11h25", "11h25 - 12h15", "12h15 - 13h05", "13h15 - 14h05", "14h05 - 14h55", "14h55 - 15h45", "15h50 - 16h40", "16h40 - 17h30")
    WEEK_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

    @staticmethod
    def getCourseClass(cc, criterias, ci):




        sb = []
        sb.append(" <span style='color:#00FFFF' title=''> <b>MH: <b/> </span>")
        sb.append(cc.Course.Name)
        sb.append("<br /> <span style='color:#00FFFF' title=''> <b>GV: <b/> </span>")
        sb.append(cc.Professor.Name)
        sb.append("<br /> <span style='color:#00FFFF' title=''> <b>Room: <b/> </span>")
        # sb.append(room.Name)
        # sb.append("/".join(map(lambda grp: grp.Name, cc.Groups)),)
        
        if cc.LabRequired:
            sb.append(" <br /><span style='color:#00FFFF' title=''> <b>Lab <b/> </span>")


        return sb

    @staticmethod
    def generateTimeTable(solution, slot_table):
        ci = 0

        time_table = defaultdict(list)
        items = solution.classes.items   
        ROOM_COLUMN_NUMBER = HtmlOutput.ROOM_COLUMN_NUMBER
        getCourseClass = HtmlOutput.getCourseClass

        for cc, reservation_index in items():
            reservation = Reservation.parse(reservation_index)
            # coordinate of time-space slot
            dayId = reservation.Day + 1
            dur = cc.Duration
            periodId = reservation.Time + 1
            if dur == 3:
                if 3 < periodId <= 6:
                    periodId = 4
                elif 1 <= periodId <= 3:
                    periodId = 1
                else:
                    periodId = 7
            elif dur == 4 or dur == 5:
                if periodId <= 6:
                    periodId = 1
                else:
                    periodId = 7
            else:
                periodId = 1
            roomId = reservation.Room
            key = (periodId, roomId)

            if key in slot_table:
                room_duration = slot_table[key]
            else:
                room_duration = ROOM_COLUMN_NUMBER * [0]
                slot_table[key] = room_duration
            room_duration[dayId] = dur

            for m in range(1, dur):
                next_key = (periodId + m, roomId)
                if next_key not in slot_table:
                    slot_table[next_key] = ROOM_COLUMN_NUMBER * [0]
                if slot_table[next_key][dayId] < 1:
                    slot_table[next_key][dayId] = -1

            if key in time_table:
                room_schedule = time_table[key]
            else:
                room_schedule = ROOM_COLUMN_NUMBER * [None]
                time_table[key] = room_schedule

            room_schedule[dayId] = "".join(getCourseClass(cc, solution.criteria, ci))
            ci += len(HtmlOutput.CRITERIAS)
        return time_table
    
    @staticmethod
    def getHtmlCell(content, rowspan):
        if rowspan == 0:
            return "<td></td>"

        if content is None:
            return ""
        sb = []
        if rowspan > 1:
            sb.append("<td style='border: .25em solid white; padding: .25em' rowspan='")
            sb.append(rowspan)
            sb.append("'>")
        else:
            sb.append("<td style='border: .25em solid white; padding: .25em'>")
        sb.append(content)
        sb.append("</td>")
        return "".join(str(v) for v in sb)

    @staticmethod
    def getResult(solution):
        configuration = solution.configuration
        nr = configuration.numberOfRooms
        getRoomById = configuration.getRoomById

        slot_table = defaultdict(list)
        time_table = HtmlOutput.generateTimeTable(solution, slot_table)  # Tuple[0] = time, Tuple[1] = roomId
        # st.markdown(slot_table)
        if not slot_table or not time_table:
            return ""

        sb = []
        for roomId in range(nr):
            temp = []
            room = getRoomById(roomId)
            for periodId in range(HtmlOutput.ROOM_ROW_NUMBER):
                if periodId == 0:
                    temp.append("<div id='room_")
                    temp.append(room.Name)
                    temp.append("' style='padding: 0.5em'>\n")
                    temp.append("<table style=' border: .25em solid white; text-align: center; width: 100%'>\n")
                    temp.append(HtmlOutput.getTableHeader(room))
                else:
                    key = (periodId, roomId)
                    room_duration = slot_table[key] if key in slot_table.keys() else None
                    room_schedule = time_table[key] if key in time_table.keys() else None
                    temp.append("<tr>")
                    for dayId in range(HtmlOutput.ROOM_COLUMN_NUMBER):
                        if dayId == 0:
                            temp.append("<th style='color: #00FFFF; border: .25em solid white; text-align: center; padding: .25em' scope='row' colspan='2'>")
                            temp.append(HtmlOutput.PERIODS[periodId])
                            temp.append("</th>\n")
                            continue

                        if room_schedule is None and room_duration is None:
                            continue

                        content = room_schedule[dayId] if room_schedule is not None else None
                        temp.append(HtmlOutput.getHtmlCell(content, room_duration[dayId]))
                    temp.append("</tr>\n")

                if periodId == HtmlOutput.ROOM_ROW_NUMBER - 1:
                    temp.append("</table>\n</div>\n")
            temp = json.dumps(temp).replace(" <b>Room: <b/> </span>", "<b> <b>Room: <b/> </span>{}".format(room.Name))
            temp = json.loads(temp)
            sb = sb + temp
        return "".join(str(v) for v in sb)
    
    

    @staticmethod
    def getTableHeader(room):
        sb = ["<tr><th style='color:#00FFFF; border: .25em solid white' scope='col' colspan='2'>Room: ", room.Name, "</th>\n"]
        for weekDay in HtmlOutput.WEEK_DAYS:
            sb.append("<th style='color: #00FFFF; border: .25em solid white; padding: .25em; width: 15%; text-align: center' scope='col' rowspan='2'>")
            sb.append(weekDay)
            sb.append("</th>\n")
        sb.append("</tr>\n")
        sb.append("<tr>\n")
        sb.append("<th style='color:#00FFFF; border: .25em solid white; padding: .25em'>Lab: ")
        sb.append("Yes" if room.Lab else "No")
        sb.append("</th>\n")
        sb.append("<th style='color:#00FFFF; border: .25em solid white; padding: .25em'>Seats: ")
        sb.append(room.NumberOfSeats)
        sb.append("</th>\n")
        sb.append("</tr>\n")
        return "".join(str(v) for v in sb)
