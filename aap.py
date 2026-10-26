import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# 1. ตั้งค่าหน้าเว็บ (Page Configuration)
# ==========================================
st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ส่วนของ Sidebar (เมนูด้านข้าง)
# ==========================================
st.sidebar.title("🎛️ แผงควบคุมระบบ")
st.sidebar.markdown("---")

# เมนูหลัก
menu = st.sidebar.radio(
    "เลือกเมนูการใช้งาน:",
    ["🏠 หน้าแรก (Overview)", "📈 วิเคราะห์ข้อมูล (Analytics)", "📁 อัปโหลดข้อมูล (Upload)", "ℹ️ เกี่ยวกับระบบ"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 ทิป: คุณสามารถปรับแต่งแถบนี้เพื่อเพิ่มตัวกรองข้อมูลเพิ่มเติมได้ตามต้องการ")

# ==========================================
# 3. ฟังก์ชันสร้างข้อมูลตัวอย่าง (Dummy Data)
# ==========================================
@st.cache_data
def load_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=100, freq="D")
    data = pd.DataFrame({
        'Date': dates,
        'Region': np.choice(['กรุงเทพฯ', 'เชียงใหม่', 'ภูเก็ต', 'ขอนแก่น'], size=100),
        'Product': np.choice(['สินค้า A', 'สินค้า B', 'สินค้า C'], size=100),
        'Sales': np.random.randint(1000, 50000, size=100),
        'Profit': np.random.randint(100, 10000, size=100),
        'Customers': np.random.randint(10, 200, size=100)
    })
    return data

df = load_sample_data()

# ==========================================
# 4. เนื้อหาตามเมนูที่เลือก
# ==========================================

if menu == "🏠 หน้าแรก (Overview)":
    st.title("📊 ภาพรวมระบบธุรกิจ (Dashboard Overview)")
    st.write("ยินดีต้อนรับเข้าสู่ระบบรายงานผลการดำเนินงานแบบเรียลไทม์")
    
    # แสดง Metric สรุปผลด้านบน
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_customers = df['Customers'].sum()
    avg_sales = df['Sales'].mean()
    
    col1.metric("ยอดขายรวม (Sales)", f"{total_sales:,.0f} บาท", "↑ 12%")
    col2.metric("กำไรสุทธิ (Profit)", f"{total_profit:,.0f} บาท", "↑ 8%")
    col3.metric("จำนวนลูกค้า", f"{total_customers:,} คน", "↑ 5%")
    col4.metric("ยอดขายเฉลี่ย/วัน", f"{avg_sales:,.2f} บาท", "↓ 2%")
    
    st.markdown("---")
    
    # แสดงกราฟเบื้องต้น
    st.subheader("📈 แนวโน้มยอดขายรายวัน")
    daily_sales = df.groupby('Date')['Sales'].sum()
    st.line_chart(daily_sales)

elif menu == "📈 วิเคราะห์ข้อมูล (Analytics)":
    st.title("📈 ส่วนวิเคราะห์ข้อมูลเชิงลึก")
    st.write("เลือกดูข้อมูลแยกตามหมวดหมู่ที่คุณสนใจ")
    
    # ตัวกรองข้อมูลในหน้าวิเคราะห์
    selected_region = st.selectbox("เลือกภูมิภาค:", ["ทั้งหมด"] + list(df['Region'].unique()))
    
    if selected_region != "ทั้งหมด":
        filtered_df = df[df['Region'] == selected_region]
    else:
        filtered_df = df
        
    st.markdown(f"### ผลการวิเคราะห์ (ภูมิภาค: {selected_region})")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### ยอดขายแยกตามประเภทสินค้า")
        product_sales = filtered_df.groupby('Product')['Sales'].sum()
        st.bar_chart(product_sales)
        
    with col2:
        st.write("#### กำไรแยกตามประเภทสินค้า")
        product_profit = filtered_df.groupby('Product')['Profit'].sum()
        st.bar_chart(product_profit)
        
    st.markdown("---")
    st.subheader("📋 ตารางข้อมูลดิบที่ผ่านการกรอง")
    st.dataframe(filtered_df, use_container_width=True)

elif menu == "📁 อัปโหลดข้อมูล (Upload)":
    st.title("📁 อัปโหลดไฟล์ข้อมูลของคุณเอง")
    st.write("คุณสามารถอัปโหลดไฟล์ CSV เพื่อนำมาแสดงผลบน Dashboard นี้ได้ทันที")
    
    uploaded_file = st.file_uploader("เลือกไฟล์ CSV", type=["csv"])
    
    if uploaded_file is not None:
        user_df = pd.read_csv(uploaded_file)
        st.success("อัปโหลดไฟล์สำเร็จ!")
        st.write("### ตัวอย่างข้อมูลของคุณ:")
        st.dataframe(user_df.head(), use_container_width=True)
    else:
        st.info("💡 หรือจะทดลองดาวน์โหลดไฟล์ตัวอย่างด้านล่างไปลองใช้งานดูก่อนก็ได้ครับ")
        
        # ปุ่มดาวน์โหลดไฟล์ตัวอย่าง
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 ดาวน์โหลดไฟล์ข้อมูลตัวอย่าง (CSV)",
            data=csv_data,
            file_name="sample_sales_data.csv",
            mime="text/csv",
        )

elif menu == "ℹ️ เกี่ยวกับระบบ":
    st.title("ℹ️ เกี่ยวกับแอปพลิเคชัน")
    st.write("""
    * **พัฒนาด้วย:** Python และ Streamlit
    * **วัตถุประสงค์:** เป็นต้นแบบสำหรับสร้างเว็บแอปพลิเคชันแสดงผลข้อมูล (Data Dashboard)
    * **ผู้พัฒนา:** คุณเอง 🚀
    """)
    st.warning("⚠️ โค้ดชุดนี้ถูกออกแบบมาเพื่อให้สามารถนำไปปรับต่อยอดกับฐานข้อมูลจริงหรือระบบ API ภายนอกได้ง่าย")

# ==========================================
# 5. ส่วนท้ายหน้า (Footer)
# ==========================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Copyright © 2026 | Built with Streamlit ❤️</div>",
    unsafe_allow_html=True
)
