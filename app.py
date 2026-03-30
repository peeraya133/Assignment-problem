import streamlit as st
import datetime

# ================== Linked List ==================
class HomeworkNode:
    def __init__(self, task, due, detail):
        self.task = task
        self.due = due
        self.detail = detail
        self.status = "ยังไม่เสร็จ"
        self.next = None

class HomeworkList:
    def __init__(self):
        self.head = None

    def add(self, task, due, detail):
        new = HomeworkNode(task, due, detail)
        if not self.head:
            self.head = new
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new

    def to_list(self):
        temp = self.head
        res = []
        while temp:
            res.append(temp)
            temp = temp.next
        return res


# ================== Tree ==================
class TreeNode:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.left = None
        self.right = None

def insert(root, name, data):
    if root is None:
        return TreeNode(name, data)
    if name < root.name:
        root.left = insert(root.left, name, data)
    else:
        root.right = insert(root.right, name, data)
    return root

def search(root, name):
    if root is None or root.name == name:
        return root
    if name < root.name:
        return search(root.left, name)
    return search(root.right, name)


# ================== Session ==================
if "subjects" not in st.session_state:
    st.session_state.subjects = []  # Array

if "tree" not in st.session_state:
    st.session_state.tree = None

st.title("📚 Study Planner System")

menu = st.sidebar.selectbox(
    "เมนู",
    ["เพิ่มวิชา","เพิ่มการบ้าน","แก้ไขวิชา","แก้ไขการบ้าน","ลบวิชา","ค้นหา","แสดงทั้งหมด"]
)

# ================== เพิ่มวิชา ==================
if menu == "เพิ่มวิชา":
    st.header("➕ เพิ่มวิชา")

    name = st.text_input("ชื่อวิชา")
    code = st.text_input("รหัส")
    teacher = st.text_input("อาจารย์")
    day = st.selectbox("วัน", ["จันทร์","อังคาร","พุธ","พฤหัส","ศุกร์"])
    start = st.time_input("เริ่ม", datetime.time(9,0))
    end = st.time_input("ถึง", datetime.time(10,0))

    if st.button("เพิ่ม"):
        subject = {
            "name": name,
            "code": code,
            "teacher": teacher,
            "day": day,
            "time": f"{start} - {end}",
            "hw": HomeworkList()
        }

        st.session_state.subjects.append(subject)
        st.session_state.tree = insert(st.session_state.tree, name, subject)

        st.success("เพิ่มแล้ว")


# ================== เพิ่มการบ้าน ==================
elif menu == "เพิ่มการบ้าน":
    st.header("📝 เพิ่มการบ้าน")

    names = [s["name"] for s in st.session_state.subjects]

    if names:
        sub = st.selectbox("วิชา", names)
        task = st.text_input("งาน")
        date = st.date_input("วันที่")
        time = st.time_input("เวลา")
        detail = st.text_area("รายละเอียด")

        if st.button("เพิ่ม"):
            node = search(st.session_state.tree, sub)
            if node:
                node.data["hw"].add(task, f"{date} {time}", detail)
                st.success("เพิ่มแล้ว")
    else:
        st.warning("ไม่มีวิชา")


# ================== แก้ไขวิชา ==================
elif menu == "แก้ไขวิชา":
    st.header("✏️ แก้ไขวิชา")

    names = [s["name"] for s in st.session_state.subjects]

    if names:
        old = st.selectbox("เลือก", names)
        node = search(st.session_state.tree, old)

        if node:
            sub = node.data

            new_name = st.text_input("ชื่อใหม่", sub["name"])
            code = st.text_input("รหัส", sub["code"])
            teacher = st.text_input("อาจารย์", sub["teacher"])

            if st.button("บันทึก"):
                sub["name"] = new_name
                sub["code"] = code
                sub["teacher"] = teacher
                st.success("แก้ไขแล้ว")


# ================== แก้ไขการบ้าน ==================
elif menu == "แก้ไขการบ้าน":
    st.header("✔ การบ้าน")

    names = [s["name"] for s in st.session_state.subjects]

    if names:
        sub = st.selectbox("วิชา", names)
        node = search(st.session_state.tree, sub)

        if node:
            hw = node.data["hw"].to_list()

            for i, h in enumerate(hw):
                st.write(f"{i}. {h.task} | {h.status}")

            if hw:
                idx = st.number_input("เลือก", 0, len(hw)-1)

                if st.button("ทำเสร็จ"):
                    hw[idx].status = "เสร็จแล้ว"
                    st.success("อัปเดตแล้ว")


# ================== ลบวิชา ==================
elif menu == "ลบวิชา":
    st.header("🗑 ลบ")

    names = [s["name"] for s in st.session_state.subjects]

    if names:
        name = st.selectbox("เลือก", names)

        if st.button("ลบ"):
            st.session_state.subjects = [s for s in st.session_state.subjects if s["name"] != name]
            st.success("ลบแล้ว")


# ================== ค้นหา ==================
elif menu == "ค้นหา":
    st.header("🔍 ค้นหา")

    name = st.text_input("ชื่อวิชา")

    if st.button("ค้นหา"):
        node = search(st.session_state.tree, name)

        if node:
            sub = node.data
            st.subheader(sub["name"])
            st.write(sub["day"], sub["time"])

            for h in sub["hw"].to_list():
                st.write(f"- {h.task} | {h.due} | {h.status}")
                if h.detail:
                    st.write(f"   📌 {h.detail}")
        else:
            st.error("ไม่พบ")


# ================== แสดงทั้งหมด ==================
elif menu == "แสดงทั้งหมด":
    st.header("📋 ทั้งหมด")

    for sub in st.session_state.subjects:
        st.subheader(sub["name"])
        st.write(sub["day"], sub["time"])

        for h in sub["hw"].to_list():
            st.write(f"- {h.task} | {h.due} | {h.status}")
            if h.detail:
                st.write(f"   📌 {h.detail}")
