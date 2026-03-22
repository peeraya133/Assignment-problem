import streamlit as st

# ====== เก็บข้อมูล ======
if "subjects" not in st.session_state:
    st.session_state.subjects = {}

if "homeworks" not in st.session_state:
    st.session_state.homeworks = {}

st.set_page_config(page_title="Study Planner", layout="centered")
st.title("📚 Study Planner System")

# ====== เมนู ======
menu = st.sidebar.selectbox(
    "เมนู",
    ["เพิ่มวิชา", "เพิ่มการบ้าน", "แก้ไขวิชา", "แก้ไขการบ้าน", "ลบวิชา", "ค้นหาวิชา", "แสดงทั้งหมด"]
)

# ================== เพิ่มวิชา ==================
if menu == "เพิ่มวิชา":
    st.header("➕ เพิ่มวิชา")

    code = st.text_input("รหัสวิชา")
    name = st.text_input("ชื่อวิชา")
    teacher = st.text_input("อาจารย์")
    # เลือกวัน
    day = st.selectbox("วันเรียน", ["จันทร์", "อังคาร", "พุธ", "พฤหัส", "ศุกร์", "เสาร์", "อาทิตย์"])
        
    # เลือกเวลาเริ่ม - สิ้นสุด
    start_time = st.time_input("เวลาเริ่ม")
    end_time = st.time_input("เวลาสิ้นสุด")
        
    # รวมเวลาเป็นช่วง
    time = f"{start_time} - {end_time}"

    if st.button("บันทึก"):
        if name:
            st.session_state.subjects[name] = {
                "code": code,
                "teacher": teacher,
                "day": day,
                "time": time
            }
            st.session_state.homeworks[name] = []
            st.success("เพิ่มวิชาเรียบร้อย")
        else:
            st.warning("กรอกชื่อวิชา")

# ================== เพิ่มการบ้าน ==================
elif menu == "เพิ่มการบ้าน":
    st.header("📝 เพิ่มการบ้าน")

    if st.session_state.subjects:
        subject = st.selectbox("เลือกวิชา", list(st.session_state.subjects.keys()))
        task = st.text_input("ชื่อการบ้าน")

        # 📅 เลือกวันที่
        due_date = st.date_input("กำหนดส่ง (วันที่)")
        
        # ⏰ เลือกเวลา
        due_time = st.time_input("กำหนดส่ง (เวลา)")
        
        # 📝 รายละเอียด (ไม่กรอกก็ได้)
        detail = st.text_area("รายละเอียด (ไม่จำเป็น)", "")
        
        # รวมวันที่ + เวลา
        due = f"{due_date} {due_time}"

        if st.button("เพิ่ม"):
            if task:
                st.session_state.homeworks[subject].append({
                    "task": task,
                    "due": due,
                    "detail": detail,
                    "status": "ยังไม่เสร็จ"
                })
                st.success("เพิ่มการบ้านเรียบร้อย")
            else:
                st.warning("กรอกชื่อการบ้าน")
    else:
        st.warning("ยังไม่มีวิชา")

# ================== แก้ไขวิชา ==================
elif menu == "แก้ไขวิชา":
    st.header("✏️ แก้ไขวิชา")

    if st.session_state.subjects:
        subject = st.selectbox("เลือกวิชา", list(st.session_state.subjects.keys()))
        data = st.session_state.subjects[subject]

        new_name = st.text_input("ชื่อวิชาใหม่", value=subject)
        code = st.text_input("รหัสวิชา", value=data["code"])
        teacher = st.text_input("อาจารย์", value=data["teacher"])
        # เลือกวัน
        day = st.selectbox("วันเรียน", ["จันทร์", "อังคาร", "พุธ", "พฤหัส", "ศุกร์", "เสาร์", "อาทิตย์"])
        
        # เลือกเวลาเริ่ม - สิ้นสุด
        start_time = st.time_input("เวลาเริ่ม")
        end_time = st.time_input("เวลาสิ้นสุด")
        
        # รวมเวลาเป็นช่วง
        time = f"{start_time} - {end_time}"

        if st.button("บันทึกการแก้ไข"):
            # ถ้าเปลี่ยนชื่อวิชา ต้องย้าย key
            if new_name != subject:
                st.session_state.subjects[new_name] = st.session_state.subjects.pop(subject)
                st.session_state.homeworks[new_name] = st.session_state.homeworks.pop(subject)
                subject = new_name

            st.session_state.subjects[subject] = {
                "code": code,
                "teacher": teacher,
                "day": day,
                "time": time
            }

            st.success("แก้ไขเรียบร้อย")
    else:
        st.warning("ยังไม่มีวิชา")

# ================== แก้ไขการบ้าน ==================
elif menu == "แก้ไขการบ้าน":
    st.header("✔ อัปเดตการบ้าน")

    if st.session_state.subjects:
        subject = st.selectbox("เลือกวิชา", list(st.session_state.subjects.keys()))
        hw_list = st.session_state.homeworks[subject]

        if hw_list:
            for i, hw in enumerate(hw_list):
                col1, col2 = st.columns([3,1])
                col1.write(f"{hw['task']} | {hw['due']} | {hw['status']}")

                if col2.button("เสร็จ", key=i):
                    hw["status"] = "เสร็จแล้ว"
                    st.success("อัปเดตแล้ว")
        else:
            st.info("ยังไม่มีการบ้าน")
    else:
        st.warning("ยังไม่มีวิชา")

# ================== ลบวิชา ==================
elif menu == "ลบวิชา":
    st.header("🗑 ลบวิชา")

    if st.session_state.subjects:
        subject = st.selectbox("เลือกวิชา", list(st.session_state.subjects.keys()))

        if st.button("ลบ"):
            del st.session_state.subjects[subject]
            del st.session_state.homeworks[subject]
            st.success("ลบเรียบร้อย")
    else:
        st.warning("ไม่มีข้อมูล")

# ================== ค้นหาวิชา ==================
elif menu == "ค้นหาวิชา":
    st.header("🔍 ค้นหาวิชา")

    name = st.text_input("ชื่อวิชา")

    if st.button("ค้นหา"):
        if name in st.session_state.subjects:
            sub = st.session_state.subjects[name]

            st.subheader(f"📘 {name}")
            st.write("รหัส:", sub["code"])
            st.write("อาจารย์:", sub["teacher"])
            st.write("วัน:", sub["day"])
            st.write("เวลา:", sub["time"])

            st.subheader("📌 การบ้าน")
            for hw in st.session_state.homeworks[name]:
                st.write(f"- {hw['task']} | {hw['due']} | {hw['status']}")
                
                if hw["detail"]:
                    st.write(f"   📌 {hw['detail']}")
        else:
            st.error("ไม่พบวิชา")

# ================== แสดงทั้งหมด ==================
elif menu == "แสดงทั้งหมด":
    st.header("📋 ข้อมูลทั้งหมด")

    for name, sub in st.session_state.subjects.items():
        st.subheader(f"📘 {name}")
        st.write("วัน:", sub["day"], "| เวลา:", sub["time"])

        for hw in st.session_state.homeworks[name]:
            st.write(f"- {hw['task']} | {hw['due']} | {hw['status']}")
            
            if hw["detail"]:
                st.write(f"   📌 {hw['detail']}")
