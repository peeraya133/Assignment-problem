import streamlit as st

# ================== เก็บข้อมูล ==================
if "subjects" not in st.session_state:
    st.session_state.subjects = {}

if "homeworks" not in st.session_state:
    st.session_state.homeworks = {}

st.set_page_config(page_title="Study Planner", layout="centered")
st.title("📚 Study Planner System")

# ================== เมนู ==================
menu = st.sidebar.selectbox(
    "เลือกเมนู",
    ["เพิ่มวิชา", "เพิ่มการบ้าน", "แก้ไขการบ้าน", "ลบวิชา", "ค้นหาวิชา", "แสดงทั้งหมด"]
)

# ================== เพิ่มวิชา ==================
if menu == "เพิ่มวิชา":
    st.header("➕ เพิ่มวิชา")

    code = st.text_input("รหัสวิชา")
    name = st.text_input("ชื่อวิชา")
    teacher = st.text_input("อาจารย์")
    day = st.text_input("วันเรียน")
    time = st.text_input("เวลา")

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
            st.warning("กรุณากรอกชื่อวิชา")

# ================== เพิ่มการบ้าน ==================
elif menu == "เพิ่มการบ้าน":
    st.header("📝 เพิ่มการบ้าน")

    if st.session_state.subjects:
        subject = st.selectbox("เลือกวิชา", list(st.session_state.subjects.keys()))
        task = st.text_input("ชื่อการบ้าน")
        due = st.text_input("กำหนดส่ง")

        if st.button("เพิ่ม"):
            if task:
                st.session_state.homeworks[subject].append({
                    "task": task,
                    "due": due,
                    "status": "ยังไม่เสร็จ"
                })
                st.success("เพิ่มการบ้านเรียบร้อย")
            else:
                st.warning("กรอกชื่อการบ้าน")
    else:
        st.warning("ยังไม่มีวิชา")

# ================== แก้ไขการบ้าน ==================
elif menu == "แก้ไขการบ้าน":
    st.header("✏️ แก้ไขสถานะการบ้าน")

    if st.session_state.subjects:
        subject = st.selectbox("เลือกวิชา", list(st.session_state.subjects.keys()))
        hw_list = st.session_state.homeworks[subject]

        if hw_list:
            for i, hw in enumerate(hw_list):
                col1, col2 = st.columns([3,1])
                col1.write(f"{hw['task']} | {hw['due']}")

                if col2.button("✔ เสร็จ", key=i):
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
            st.success("ลบวิชาเรียบร้อย")
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
        else:
            st.error("ไม่พบวิชา")

# ================== แสดงทั้งหมด ==================
elif menu == "แสดงทั้งหมด":
    st.header("📋 ข้อมูลทั้งหมด")

    for name, sub in st.session_state.subjects.items():
        st.subheader(f"📘 {name}")
        st.write("วัน:", sub["day"], "| เวลา:", sub["time"])

        for hw in st.session_state.homeworks[name]:
            st.write(f"- {hw['task']} ({hw['status']})")