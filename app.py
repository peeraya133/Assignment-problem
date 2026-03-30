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
        new_node = HomeworkNode(task, due, detail)
        if not self.head:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

    def to_list(self):
        temp = self.head
        result = []
        while temp:
            result.append(temp)
            temp = temp.next
        return result


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

st.title("📚 Study Planner (Array + LinkedList + Tree)")

menu = st.sidebar.selectbox(
    "เมนู",
    ["เพิ่มวิชา", "เพิ่มการบ้าน", "ค้นหา", "แสดงทั้งหมด"]
)

# ================== เพิ่มวิชา ==================
if menu == "เพิ่มวิชา":
    st.header("➕ เพิ่มวิชา")

    name = st.text_input("ชื่อวิชา")
    code = st.text_input("รหัสวิชา")
    teacher = st.text_input("อาจารย์")
    day = st.selectbox("วัน", ["จันทร์","อังคาร","พุธ","พฤหัส","ศุกร์"])
    start = st.time_input("เวลาเริ่ม", datetime.time(9,0))
    end = st.time_input("เวลาสิ้นสุด", datetime.time(10,0))

    if st.button("เพิ่มวิชา"):
        subject = {
            "name": name,
            "code": code,
            "teacher": teacher,
            "day": day,
            "time": f"{start} - {end}",
            "hw": HomeworkList()
        }

        st.session_state.subjects.append(subject)  # Array
        st.session_state.tree = insert(st.session_state.tree, name, subject)  # Tree

        st.success("เพิ่มวิชาแล้ว")


# ================== เพิ่มการบ้าน ==================
elif menu == "เพิ่มการบ้าน":
    st.header("📝 เพิ่มการบ้าน")

    names = [s["name"] for s in st.session_state.subjects]

    if names:
        subject_name = st.selectbox("เลือกวิชา", names)
        task = st.text_input("ชื่อการบ้าน")
        date = st.date_input("วันที่")
        time = st.time_input("เวลา")
        detail = st.text_area("รายละเอียด (ไม่บังคับ)")

        if st.button("เพิ่ม"):
            node = search(st.session_state.tree, subject_name)
            if node:
                node.data["hw"].add(task, f"{date} {time}", detail)
                st.success("เพิ่มการบ้านแล้ว")
    else:
        st.warning("ยังไม่มีวิชา")


# ================== ค้นหา ==================
elif menu == "ค้นหา":
    st.header("🔍 ค้นหาวิชา")

    name = st.text_input("ชื่อวิชา")

    if st.button("ค้นหา"):
        node = search(st.session_state.tree, name)

        if node:
            sub = node.data
            st.subheader(sub["name"])
            st.write(sub["day"], sub["time"])

            st.subheader("📌 การบ้าน")
            for hw in sub["hw"].to_list():
                st.write(f"- {hw.task} | {hw.due} | {hw.status}")
                if hw.detail:
                    st.write(f"   📌 {hw.detail}")
        else:
            st.error("ไม่พบ")


# ================== แสดงทั้งหมด ==================
elif menu == "แสดงทั้งหมด":
    st.header("📋 ทั้งหมด")

    for sub in st.session_state.subjects:
        st.subheader(sub["name"])
        st.write(sub["day"], sub["time"])

        for hw in sub["hw"].to_list():
            st.write(f"- {hw.task} | {hw.due} | {hw.status}")
            if hw.detail:
                st.write(f"   📌 {hw.detail}")
