import streamlit as st
from datetime import date

st.set_page_config(
    page_title="MON101 Lunar Lab",
    page_icon="🌙",
    layout="wide"
)

PHI = 1.618

st.markdown("""
<style>
.stApp {
    background: #070912;
    color: white;
}
h1, h2, h3 {
    color: #00e5ff !important;
}
div[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #00bcd4;
    padding: 14px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌙 MON101 LUNAR LAB")
st.subheader("ทดลองสูตรวันประจำสัปดาห์ + จันทรคติ + Golden Ratio 1.618")

st.info(
    "เลือกวันที่ โปรแกรมจะพยายามหาวันข้างขึ้น/ข้างแรม "
    "จากปฏิทินจันทรคติไทยโดยอัตโนมัติ"
)

selected_date = st.date_input(
    "เลือกวัน เดือน ปี",
    value=date.today(),
    format="DD/MM/YYYY"
)

# วันจันทร์ = 1 ... วันอาทิตย์ = 7
weekday_number = selected_date.weekday() + 1

weekday_names = {
    1: "วันจันทร์",
    2: "วันอังคาร",
    3: "วันพุธ",
    4: "วันพฤหัสบดี",
    5: "วันศุกร์",
    6: "วันเสาร์",
    7: "วันอาทิตย์",
}

month_names = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม",
    "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน",
    "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]

st.markdown("## 📅 ข้อมูลวันที่")

c1, c2, c3 = st.columns(3)

c1.metric(
    "วันประจำสัปดาห์",
    weekday_names[weekday_number]
)

c2.metric(
    "เลขประจำวัน",
    weekday_number
)

c3.metric(
    "วันที่",
    f"{selected_date.day} "
    f"{month_names[selected_date.month - 1]} "
    f"{selected_date.year + 543}"
)

# อ่านวันจันทรคติไทย
lunar_phase = None
lunar_day = None
lunar_text = ""

try:
    from pythainlp.util import to_lunar_date

    lunar_text = str(
        to_lunar_date(selected_date)
    )

    import re

    match = re.search(
        r"(ขึ้น|แรม)\s*(\d+)\s*ค่ำ",
        lunar_text
    )

    if match:
        lunar_phase = match.group(1)
        lunar_day = int(match.group(2))

except Exception:
    lunar_text = ""

st.markdown("---")
st.markdown("## 🌙 ข้อมูลข้างขึ้น / ข้างแรม")

if lunar_phase and lunar_day is not None:
    st.success(
        f"วันที่เลือก: {lunar_text}"
    )

    st.write(
        f"ข้าง: **{lunar_phase}**"
    )

    st.write(
        f"เลขวันค่ำ: **{lunar_day}**"
    )

else:
    st.warning(
        "โปรแกรมอ่านวันจันทรคติอัตโนมัติไม่ได้ "
        "กรุณาติดตั้ง pythainlp หรือตรวจสอบรูปแบบข้อมูล"
    )

    manual_phase = st.radio(
        "เลือกข้างจันทรคติ",
        ["ขึ้น", "แรม"],
        horizontal=True
    )

    manual_day = st.number_input(
        "เลขวันค่ำ",
        min_value=1,
        max_value=15,
        value=5,
        step=1
    )

    lunar_phase = manual_phase
    lunar_day = int(manual_day)

st.markdown("---")
st.markdown("## 🧪 วิธีที่ 1: บวกหรือลบวันค่ำ")

st.write(
    f"วันประจำสัปดาห์ = {weekday_number}"
)

st.write(
    f"เลขวันค่ำ = {lunar_day}"
)

if lunar_phase == "ขึ้น":
    result_1 = weekday_number - lunar_day
    expression_1 = (
        f"{weekday_number} - {lunar_day}"
    )
else:
    result_1 = weekday_number + lunar_day
    expression_1 = (
        f"{weekday_number} + {lunar_day}"
    )

st.code(
    f"{expression_1} = {result_1}"
)

st.metric(
    "ผลลัพธ์วิธีที่ 1",
    f"{result_1}"
)

st.markdown("---")
st.markdown("## 🔢 วิธีที่ 2: จับตัวเลขมาต่อกัน")

result_2 = int(
    f"{weekday_number}{lunar_day}"
)

st.write(
    f"เลขวันประจำสัปดาห์ = {weekday_number}"
)

st.write(
    f"เลขวันค่ำ = {lunar_day}"
)

st.code(
    f"{weekday_number} ต่อกับ {lunar_day}"
    f" = {result_2}"
)

st.metric(
    "ผลลัพธ์วิธีที่ 2",
    f"{result_2}"
)

st.markdown("---")
st.markdown("## 🌀 ทดลองค่าคงที่ Golden Ratio 1.618")

st.caption(
    "ทดลองทั้งการหารและการคูณ "
    "โดยใช้ผลลัพธ์จากแต่ละวิธี"
)

for title, value in [
    ("วิธีที่ 1", result_1),
    ("วิธีที่ 2", result_2),
]:
    st.markdown(f"### {title}")

    a, b = st.columns(2)

    divided = value / PHI
    multiplied = value * PHI

    with a:
        st.write(
            f"{value} ÷ {PHI}"
        )
        st.metric(
            "ผลหาร",
            f"{divided:.8f}"
        )

    with b:
        st.write(
            f"{value} × {PHI}"
        )
        st.metric(
            "ผลคูณ",
            f"{multiplied:.8f}"
        )

    st.divider()

st.markdown("## 📋 สรุปผลทั้งสองวิธี")

st.dataframe(
    [
        {
            "วิธี": "วิธีที่ 1",
            "สูตร": expression_1,
            "ผลก่อนใช้ 1.618": result_1,
            "หาร 1.618": round(
                result_1 / PHI, 8
            ),
            "คูณ 1.618": round(
                result_1 * PHI, 8
            ),
        },
        {
            "วิธี": "วิธีที่ 2",
            "สูตร": (
                f"{weekday_number}"
                f" ต่อกับ {lunar_day}"
            ),
            "ผลก่อนใช้ 1.618": result_2,
            "หาร 1.618": round(
                result_2 / PHI, 8
            ),
            "คูณ 1.618": round(
                result_2 * PHI, 8
            ),
        },
    ],
    use_container_width=True,
    hide_index=True
)

st.caption(
    "MON101 LUNAR LAB — ใช้สำหรับทดลองสูตร "
    "ผลคำนวณไม่ได้รับประกันผลหวย"
    )
