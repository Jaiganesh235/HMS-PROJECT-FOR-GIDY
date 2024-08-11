import streamlit as st
import pandas as pd
import json
from datetime import datetime


# Data storage
def load_data():
    try:
        with open('hostel_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'students': {},
            'rooms': {},
            'canteen_menu': {},
            'complaints': [],
            'inout_times': [],
            'visitors': [],
            'users': {
                'admin': 'admin123',
                'security': 'security123'
            }
        }


def save_data(data):
    with open('hostel_data.json', 'w') as f:
        json.dump(data, f)


# Authentication
def login(data):
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    user_type = st.sidebar.selectbox("User Type", ["Admin", "Student", "Security"])

    if st.sidebar.button("Login"):
        if user_type == "Admin" and username == "admin" and password == 'admin123':
            st.session_state['logged_in'] = True
            st.session_state['user_type'] = "Admin"
            return True
        elif user_type == "Security" and username == "security" and password == 'security123':
            st.session_state['logged_in'] = True
            st.session_state['user_type'] = "Security"
            return True
        elif user_type == "Student" and username in data['students']:
            # For simplicity, we're using student ID as both username and password
            if password == username:
                st.session_state['logged_in'] = True
                st.session_state['user_type'] = "Student"
                st.session_state['student_id'] = username
                return True
        st.sidebar.error("Invalid credentials")
    return False


def logout():
    st.session_state['logged_in'] = False
    st.session_state['user_type'] = None
    if 'student_id' in st.session_state:
        del st.session_state['student_id']


# Streamlit App



def student_menu(data, student_id):
    st.header("Student Dashboard")

    student_options = ["View Profile", "Check Room", "View Canteen Menu", "File Complaint", "Record In/Out Time"]
    student_choice = st.sidebar.selectbox("Select Action", student_options)

    if student_choice == "View Profile":
        view_student_profile(data, student_id)
    elif student_choice == "Check Room":
        check_student_room(data, student_id)
    elif student_choice == "View Canteen Menu":
        view_canteen_menu(data)
    elif student_choice == "File Complaint":
        file_complaint(data, student_id)
    elif student_choice == "Record In/Out Time":
        record_inout_time(data, student_id)



def manage_rooms(data):
    st.subheader("Manage Rooms")

    room_number = st.text_input("Room Number")
    capacity = st.number_input("Capacity", min_value=1, max_value=4)

    if st.button("Add/Update Room"):
        data['rooms'][room_number] = {'capacity': capacity, 'occupants': []}
        st.success(f"Room {room_number} added/updated successfully!")

    st.subheader("Current Rooms")
    room_df = pd.DataFrame.from_dict(data['rooms'], orient='index')
    st.dataframe(room_df)


def update_canteen_menu(data):
    st.subheader("Update Canteen Menu")

    day = st.selectbox("Select Day", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    breakfast = st.text_input("Breakfast")
    lunch = st.text_input("Lunch")
    dinner = st.text_input("Dinner")

    if st.button("Update Menu"):
        data['canteen_menu'][day] = {
            'breakfast': breakfast,
            'lunch': lunch,
            'dinner': dinner
        }
        st.success(f"Menu for {day} updated successfully!")


def view_complaints(data):
    st.subheader("Student Complaints")

    if data['complaints']:
        complaint_df = pd.DataFrame(data['complaints'])
        st.dataframe(complaint_df)
    else:
        st.info("No complaints filed yet.")


def security_menu(data):
    st.header("Security Dashboard")

    security_options = ["Record Visitor", "View Visitors"]
    security_choice = st.sidebar.selectbox("Select Action", security_options)

    if security_choice == "Record Visitor":
        record_visitor(data)
    elif security_choice == "View Visitors":
        view_visitors(data)


# The rest of your functions (add_student, manage_rooms, etc.) remain the same

def record_inout_time(data, student_id):
    st.subheader("Record In/Out Time")

    action = st.radio("Select Action", ["In", "Out"])
    if st.button("Record Time"):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['inout_times'].append({
            'student_id': student_id,
            'action': action,
            'timestamp': current_time
        })
        st.success(f"{action} time recorded successfully!")

def generate_reports(data):
    st.subheader("Generate Reports")

    report_type = st.selectbox("Select Report Type", ["Room Occupancy", "Student List"])

    if report_type == "Room Occupancy":
        room_occupancy = {room: len(info['occupants']) for room, info in data['rooms'].items()}
        occupancy_df = pd.DataFrame.from_dict(room_occupancy, orient='index', columns=['Occupants'])
        st.dataframe(occupancy_df)

    elif report_type == "Student List":
        student_df = pd.DataFrame.from_dict(data['students'], orient='index')
        st.dataframe(student_df)


def view_student_profile(data, student_id):
    st.subheader("Student Profile")
    student_info = data['students'][student_id]
    for key, value in student_info.items():
        st.write(f"{key.capitalize()}: {value}")



def view_canteen_menu(data):
    st.subheader("Canteen Menu")
    if data['canteen_menu']:
        for day, meals in data['canteen_menu'].items():
            st.write(f"**{day}**")
            for meal, items in meals.items():
                st.write(f"- {meal.capitalize()}: {items}")
    else:
        st.info("Canteen menu not available.")

def file_complaint(data, student_id):
    st.subheader("File a Complaint")
    complaint_text = st.text_area("Enter your complaint")
    if st.button("Submit Complaint"):
        data['complaints'].append({
            'student_id': student_id,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'complaint': complaint_text
        })
        st.success("Complaint submitted successfully!")



def view_inout_times(data):
    st.subheader("Student In/Out Times")

    if data['inout_times']:
        inout_df = pd.DataFrame(data['inout_times'])
        st.dataframe(inout_df)
    else:
        st.info("No in/out times recorded yet.")


def record_visitor(data):
    st.subheader("Record Visitor")

    visitor_name = st.text_input("Visitor Name")
    purpose = st.text_input("Purpose of Visit")
    student_id = st.text_input("Student ID to Visit")

    if st.button("Record Visitor"):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['visitors'].append({
            'visitor_name': visitor_name,
            'purpose': purpose,
            'student_id': student_id,
            'timestamp': current_time
        })
        st.success("Visitor recorded successfully!")


def view_visitors(data):
    st.subheader("Visitor Records")

    if data['visitors']:
        visitor_df = pd.DataFrame(data['visitors'])
        st.dataframe(visitor_df)
    else:
        st.info("No visitors recorded yet.")


# Add other functions like add_student, manage_rooms, etc. here



def admin_menu(data):
    st.header("Admin Dashboard")

    admin_options = ["Add Student", "Delete Student", "Manage Rooms", "Update Canteen Menu", "View Complaints",
                     "Generate Reports",
                     "View In/Out Times", "View Visitors"]
    admin_choice = st.sidebar.selectbox("Select Admin Action", admin_options)

    if admin_choice == "Add Student":
        add_student(data)
    elif admin_choice == "Delete Student":
        delete_student(data)
    elif admin_choice == "Manage Rooms":
        manage_rooms(data)
    elif admin_choice == "Update Canteen Menu":
        update_canteen_menu(data)
    elif admin_choice == "View Complaints":
        view_complaints(data)
    elif admin_choice == "Generate Reports":
        generate_reports(data)
    elif admin_choice == "View In/Out Times":
        view_inout_times(data)
    elif admin_choice == "View Visitors":
        view_visitors(data)


def add_student(data):
    st.subheader("Add New Student")

    student_id = st.text_input("Student ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=16, max_value=30)
    course = st.text_input("Course")
    room_number = st.selectbox("Assign Room", list(data['rooms'].keys()))

    if st.button("Add Student"):
        if student_id not in data['students']:
            data['students'][student_id] = {
                'name': name,
                'age': age,
                'course': course,
                'room': room_number
            }
            # Add student to room occupants
            data['rooms'][room_number]['occupants'].append(student_id)
            st.success(f"Student {name} added successfully!")
        else:
            st.error("Student ID already exists!")


def delete_student(data):
    st.subheader("Delete Student")

    student_id = st.selectbox("Select Student to Delete", list(data['students'].keys()))

    if st.button("Delete Student"):
        if student_id in data['students']:
            # Remove student from room occupants
            room_number = data['students'][student_id]['room']
            if room_number in data['rooms']:
                data['rooms'][room_number]['occupants'].remove(student_id)

            # Delete student data
            del data['students'][student_id]
            st.success(f"Student {student_id} deleted successfully!")
        else:
            st.error("Student ID not found!")


def check_student_room(data, student_id):
    st.subheader("Room Information")
    student_info = data['students'].get(student_id, {})
    room_number = student_info.get('room')

    if room_number and room_number in data['rooms']:
        room_info = data['rooms'][room_number]
        st.write(f"Room Number: {room_number}")
        st.write(f"Capacity: {room_info['capacity']}")
        st.write(f"Current Occupants: {len(room_info['occupants'])}")
    else:
        st.error("Room information not available for this student.")


# ... (keep other functions as they were)

def main():
    st.title("Hostel Management System")

    data = load_data()

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        if login(data):
            st.rerun()
    else:
        st.sidebar.button("Logout", on_click=logout)

        if st.session_state['user_type'] == "Admin":
            admin_menu(data)
        elif st.session_state['user_type'] == "Student":
            if 'student_id' in st.session_state:
                student_menu(data, st.session_state['student_id'])
            else:
                st.error("Student ID not found. Please log in again.")
                logout()
        else:
            security_menu(data)

    save_data(data)


if __name__ == "__main__":
    main()
