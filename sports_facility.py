from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class SportsFacility:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.slots = {i: True for i in range(1, capacity + 1)}

    def book_slot(self, slot_number, roll_number):
        if slot_number not in self.slots:
            return "Invalid slot number."
        elif not self.slots[slot_number]:
            return "Slot is already booked."
        else:
            self.slots[slot_number] = False
            return f"Slot {slot_number} booked successfully for Roll Number {roll_number}."

    def check_availability(self):
        available_slots = [slot for slot, availability in self.slots.items() if availability]
        if available_slots:
            return f"Available slots for {self.name}: {available_slots}"
        else:
            return f"No available slots for {self.name}."

    def display_availability(self):
        return self.slots

class SportsFacilityManager:
    def __init__(self):
        self.facilities = []

    def add_facility(self, facility):
        self.facilities.append(facility)

    def book_slot(self, facility_name, slot_number, roll_number):
        for facility in self.facilities:
            if facility.name == facility_name:
                return facility.book_slot(slot_number, roll_number)
        return "Facility not found."

    def check_availability(self, facility_name):
        for facility in self.facilities:
            if facility.name == facility_name:
                return facility.check_availability()
        return "Facility not found."

    def display_availability(self, facility_name):
        for facility in self.facilities:
            if facility.name == facility_name:
                return facility.display_availability()
        return "Facility not found."

# Create instances of facilities
gym = SportsFacility("Gym", 10)
squash_court = SportsFacility("Squash Court", 5)
badminton_court = SportsFacility("Badminton Court", 8)

# Create manager and add facilities
manager = SportsFacilityManager()
manager.add_facility(gym)
manager.add_facility(squash_court)
manager.add_facility(badminton_court)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    facility_name = request.form['facility']
    slot_number = int(request.form['slot'])
    roll_number = request.form['roll_number']
    message = manager.book_slot(facility_name, slot_number, roll_number)
    return message

@app.route('/availability', methods=['GET'])
def availability():
    facility_name = request.args.get('facility')
    return manager.check_availability(facility_name)

@app.route('/display_availability', methods=['GET'])
def display_availability():
    facility_name = request.args.get('facility')
    return manager.display_availability(facility_name)

if __name__ == "__main__":
    app.run(debug=True)
