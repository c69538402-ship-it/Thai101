import streamlit as st
from datetime import date
import math

# =========================================================
# ค่าหลักของสูตร
# =========================================================

GOLDEN_RATIO = 1.618
MOON_CYCLE = 29.53

# =========================================================
# ปฏิทินจันทรคติไทย
# =========================================================

try:
    from pythaidate import CsDate
    THAI_LUNAR_AVAILABLE = True
except Exception:
    THAI_LUNAR_AVAILABLE = False


# =========================================================
# วัน
# =========================================================

WEEKDAYS = {
    0: ("จันทร์", 1),
    1: ("อังคาร", 2),
    2: ("พุธ", 3),
    3: ("พฤหัสบดี", 4),
    4: ("ศุกร์", 5),
    5: ("เสาร์", 6),
    6: ("อาทิตย์", 7),
}


# =========================================================
# เดือน
# =========================================================

MONTHS = {
    1: "มกราคม",
    2: "กุมภาพันธ์",
    3: "มีนาคม",
    4: "เมษายน",
    5: "พฤษภาคม",
    6: "มิถุนายน",
    7: "กรกฎาคม",
    8: "สิงหาคม",
    9: "กันยายน",
    10: "ตุลาคม",
    11: "พฤศจิกายน",
    12: "ธันวาคม",
}


# =========================================================
# นักษัตร
# =========================================================

ZODIACS = {
    1: "ชวด",
    2: "ฉลู",
    3: "ขาล",
    4: "เถาะ",
    5: "มะโรง",
    6: "มะเส็ง",
    7: "มะเมีย",
    8: "มะแม",
    9: "วอก",
    10: "ระกา",
    11: "จอ",
    12: "กุน",
}


# =========================================================
# แปลงปี พ.ศ. → นักษัตร
# =========================================================

def zodiac_from_be(be_year):

    value = ((be_year - 2560) % 12) + 10

    if value > 12:
        value -= 12

    return value, ZODIACS[value]


# =========================================================
# แยกตัวเลขออกเป็นหลัก
# =========================================================

def split_digits(number):

    text = str(abs(int(number)))

    result = []

    for position, char in enumerate(reversed(text)):

        digit = int(char)

        if position == 0:
            name = "หลักหน่วย"
        elif position == 1:
            name = "หลักสิบ"
        elif position == 2:
            name = "หลักร้อย"
        elif position == 3:
            name = "หลักพัน"
        elif position == 4:
            name = "หลักหมื่น"
        else:
            name = f"หลักที่ {position + 1}"

        result.append({
            "name": name,
            "digit": digit,
            "position": position
        })

    return list(reversed(result))


# =========================================================
# ดึงวันจันทรคติไทยจริง
# =========================================================

def get_thai_lunar_date(gregorian_date):

    if not THAI_LUNAR_AVAILABLE:

        return {
            "success": False,
            "error": "ยังไม่ได้ติดตั้ง pythaidate"
        }

    try:

        # Julian Day ของวันที่
        # ใช้วันที่แบบ Gregorian
        y = gregorian_date.year
        m = gregorian_date.month
        d = gregorian_date.day

        if m <= 2:
            y2 = y - 1
            m2 = m + 12
        else:
            y2 = y
            m2 = m

        A = y2 // 100
        B = 2 - A + (A // 4)

        jd = int(
            365.25 * (y2 + 4716)
        ) + int(
            30.6001 * (m2 + 1)
        ) + d + B - 1524

        cs = CsDate.fromjulianday(jd)

        # พยายามอ่านข้อมูลจาก CsDate
        text = str(cs)

        # -------------------------------------------------
        # อ่านคำว่า ขึ้น / แรม
        # -------------------------------------------------

        if "ขึ้น" in text:
            phase = "ข้างขึ้น"
            direction = -1

        elif "แรม" in text:
            phase = "ข้างแรม"
            direction = 1

        else:
            phase = "ไม่ทราบ"
            direction = 0

        # -------------------------------------------------
        # อ่านจำนวนค่ำ
        # -------------------------------------------------

        lunar_day = None

        thai_numbers = {
            "๑": 1,
            "๒": 2,
            "๓": 3,
            "๔": 4,
            "๕": 5,
            "๖": 6,
            "๗": 7,
            "๘": 8,
            "๙": 9,
            "๑๐": 10,
            "๑๑": 11,
            "๑๒": 12,
            "๑๓": 13,
            "๑๔": 14,
            "๑๕": 15,
        }

        # ตัวเลขไทยหลังคำว่า ขึ้น/แรม
        for thai, number in sorted(
            thai_numbers.items(),
            key=lambda x: len(x[0]),
            reverse=True
        ):

            if f"{phase.replace('ข้าง', '')} {thai}" in text:
                lunar_day = number
                break

            if f"{phase.replace('ข้าง', '')}{thai}" in text:
                lunar_day = number
                break

        # fallback จาก property
        if lunar_day is None:

            for attr in ["day", "lunar_day", "tithi"]:

                if hasattr(cs, attr):

                    try:
                        value = int(getattr(cs, attr))

                        if 1 <= value <= 30:

                            lunar_day = (
                                value
                                if value <= 15
                                else value - 15
                            )

                            break

                    except Exception:
                        pass

        return {
            "success": True,
            "text": text,
            "phase": phase,
            "lunar_day": lunar_day,
            "direction": direction,
            "cs": cs,
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# =========================================================
# คำนวณหนึ่งหลัก
# =========================================================

def calculate_digit(digit, moon_info):

    # ขั้นที่ 1
    divided = digit / GOLDEN_RATIO

    # ขั้นที่ 2
    multiplied = divided * MOON_CYCLE

    # ขั้นที่ 3
    if moon_info["direction"] == -1:

        final = multiplied - moon_info["lunar_day"]

        operation = (
            f"{multiplied:.10f} "
            f"- {moon_info['lunar_day']}"
        )

    elif moon_info["direction"] == 1:

        final = multiplied + moon_info["lunar_day"]

        operation = (
            f"{multiplied:.10f} "
            f"+ {moon_info['lunar_day']}"
        )

    else:

        final = multiplied
        operation = f"{multiplied:.10f}"

    return {
        "digit": digit,
        "divided": divided,
        "multiplied": multiplied,
        "operation": operation,
        "final": final,
    }


# =========================================================
# คำนวณทุกหลัก
# =========================================================

def calculate_number(value, label, moon_info):

    results = []

    for item in split_digits(value):

        result = calculate_digit(
            item["digit"],
            moon_info
        )

        result["label"] = label
        result["place"] = item["name"]

        results.append(result)

    return results
  # =========================================================
# ตั้งค่าหน้า
# =========================================================

st.set_page_config(
    page_title="เครื่องคำนวณ 1.618",
    page_icon="🌙",
    layout="wide"
)

st.title("🌙 เครื่องคำนวณ 1.618 + 29.53")
st.caption(
    "คำนวณวัน • เดือน • ปี • นักษัตร "
    "และปรับด้วยข้างขึ้น/ข้างแรมของปฏิทินไทย"
)

st.divider()


# =========================================================
# ตรวจไลบรารี
# =========================================================

if not THAI_LUNAR_AVAILABLE:

    st.error(
        "ยังไม่มีไลบรารี pythaidate"
    )

    st.code(
        "streamlit\n"
        "pythaidate",
        language="text"
    )

    st.stop()


# =========================================================
# รับวันที่
# =========================================================

st.subheader("📅 เลือกวันที่")

selected_date = st.date_input(
    "วันที่",
    value=date.today(),
    format="DD/MM/YYYY"
)

be_year = selected_date.year + 543


# =========================================================
# วัน
# =========================================================

weekday_index = selected_date.weekday()

weekday_name, weekday_value = WEEKDAYS[
    weekday_index
]


# =========================================================
# เดือน
# =========================================================

month_value = selected_date.month
month_name = MONTHS[month_value]


# =========================================================
# นักษัตร
# =========================================================

zodiac_value, zodiac_name = zodiac_from_be(
    be_year
)


# =========================================================
# จันทรคติไทย
# =========================================================

moon_info = get_thai_lunar_date(
    selected_date
)


st.divider()

st.subheader("🌙 จันทรคติไทยจริง")

if moon_info["success"]:

    st.success(
        f"วันที่ {selected_date.strftime('%d/%m/%Y')}\n\n"
        f"จันทรคติ: {moon_info['text']}"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "ข้าง",
            moon_info["phase"]
        )

    with c2:
        st.metric(
            "จำนวนค่ำ",
            f"{moon_info['lunar_day']} ค่ำ"
        )

    with c3:

        if moon_info["direction"] == -1:
            action = "ลบ"

        elif moon_info["direction"] == 1:
            action = "บวก"

        else:
            action = "-"

        st.metric(
            "การปรับสูตร",
            action
        )

else:

    st.error(
        "ไม่สามารถอ่านปฏิทินจันทรคติไทยได้"
    )

    st.code(
        moon_info.get(
            "error",
            "ไม่ทราบสาเหตุ"
        )
    )

    st.stop()


# =========================================================
# ข้อมูลพื้นฐาน
# =========================================================

st.divider()

st.subheader("🔢 ค่าที่นำเข้าสูตร")

a, b, c, d = st.columns(4)

with a:
    st.metric(
        "วัน",
        f"{weekday_name} = {weekday_value}"
    )

with b:
    st.metric(
        "เดือน",
        f"{month_name} = {month_value}"
    )

with c:
    st.metric(
        "ปี พ.ศ.",
        be_year
    )

with d:
    st.metric(
        "นักษัตร",
        f"{zodiac_name} = {zodiac_value}"
    )


# =========================================================
# ค่าคงที่
# =========================================================

st.divider()

st.subheader("⚖️ ค่าคงที่")

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Golden Ratio",
        "1.618"
    )

with c2:
    st.metric(
        "รอบดวงจันทร์",
        "29.53"
    )


# =========================================================
# ฟังก์ชันแสดงรายละเอียด
# =========================================================

def show_detail(value, title):

    st.markdown(
        f"## {title} = `{value}`"
    )

    results = calculate_number(
        value,
        title,
        moon_info
    )

    total = 0

    for row in results:

        st.markdown(
            f"### {row['place']} = {row['digit']}"
        )

        st.code(
            f"ขั้นที่ 1\n"
            f"{row['digit']} ÷ 1.618\n"
            f"= {row['divided']:.10f}\n\n"

            f"ขั้นที่ 2\n"
            f"{row['divided']:.10f} × 29.53\n"
            f"= {row['multiplied']:.10f}\n\n"

            f"ขั้นที่ 3\n"
            f"{row['operation']}\n"
            f"= {row['final']:.10f}"
        )

        total += row["final"]

        st.success(
            f"ผล {row['place']} = "
            f"{row['final']:.10f}"
        )

    st.info(
        f"รวมผลของ {title} = "
        f"**{total:.10f}**"
    )

    return results, total


# =========================================================
# วัน
# =========================================================

st.divider()

st.header("① วัน")

day_results, day_total = show_detail(
    weekday_value,
    f"วัน{weekday_name}"
)


# =========================================================
# เดือน
# =========================================================

st.divider()

st.header("② เดือน")

month_results, month_total = show_detail(
    month_value,
    month_name
)


# =========================================================
# ปี
# =========================================================

st.divider()

st.header("③ ปี พ.ศ.")

year_results, year_total = show_detail(
    be_year,
    f"ปี พ.ศ. {be_year}"
)


# =========================================================
# นักษัตร
# =========================================================

st.divider()

st.header("④ นักษัตร")

zodiac_results, zodiac_total = show_detail(
    zodiac_value,
    f"ปี{zodiac_name}"
)


# =========================================================
# รวม
# =========================================================

st.divider()

st.header("🎯 ⑤ ผลรวมสุดท้าย")

grand_total = (
    day_total
    + month_total
    + year_total
    + zodiac_total
)

st.metric(
    "ผลรวมทั้งหมด",
    f"{grand_total:.10f}"
)


# =========================================================
# สรุปสูตร
# =========================================================

st.divider()

st.subheader("🧮 สูตรที่ใช้กับวันนี้")

if moon_info["direction"] == -1:

    st.code(
        f"วันนี้ = {moon_info['phase']} "
        f"{moon_info['lunar_day']} ค่ำ\n\n"
        f"แต่ละหลัก ÷ 1.618\n"
        f"↓\n"
        f"× 29.53\n"
        f"↓\n"
        f"− {moon_info['lunar_day']}\n"
        f"↓\n"
        f"นำผลของ วัน + เดือน + ปี + นักษัตร มารวมกัน"
    )

else:

    st.code(
        f"วันนี้ = {moon_info['phase']} "
        f"{moon_info['lunar_day']} ค่ำ\n\n"
        f"แต่ละหลัก ÷ 1.618\n"
        f"↓\n"
        f"× 29.53\n"
        f"↓\n"
        f"+ {moon_info['lunar_day']}\n"
        f"↓\n"
        f"นำผลของ วัน + เดือน + ปี + นักษัตร มารวมกัน"
    )


# =========================================================
# สรุปข้อมูล
# =========================================================

st.divider()

st.subheader("📋 สรุป")

summary = f"""
วันที่: {selected_date.strftime('%d/%m/%Y')}

วัน: {weekday_name} = {weekday_value}
เดือน: {month_name} = {month_value}
ปี พ.ศ.: {be_year}
นักษัตร: {zodiac_name} = {zodiac_value}

จันทรคติไทย:
{moon_info['text']}

ข้าง: {moon_info['phase']}
ค่ำ: {moon_info['lunar_day']} ค่ำ

Golden Ratio: 1.618
รอบดวงจันทร์: 29.53

ผลวัน: {day_total:.10f}
ผลเดือน: {month_total:.10f}
ผลปี: {year_total:.10f}
ผลนักษัตร: {zodiac_total:.10f}

ผลรวมสุดท้าย:
{grand_total:.10f}
"""

st.text_area(
    "คัดลอกผล",
    summary,
    height=300
)
  
  
  
