from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Basic checklists
dusting_checklist = ["Floor", "Bathroom", "Under the Bed", "Wooden Racks"]
arrangement_checklist = ["Bedsheets", "Pillows", "Blankets"]

big_room_checklist = [
    ("Big Towels", 5),
    ("Hand Towels", 5),
    ("Foot Towel", 1),
    ("Bathroom Glasses", 4),
    ("Pillows", 5),
    ("Blankets", 5),
    ("Bed Sheets", 3),
]

small_room_checklist = [
    ("Big Towels", 2),
    ("Hand Towels", 2),
    ("Foot Towel", 1),
    ("Bathroom Glasses", 2),
    ("Pillows", 2),
    ("Blankets", 2),
    ("Bed Sheet", 1),
]


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/room_details", methods=["POST"])
def room_details():
    name = request.form["cleaner_name"]
    max_room_number = int(request.form["max_room_number"])
    return render_template(
        "checklist.html",
        cleaner_name=name,
        max_room_number=max_room_number,
        dusting_checklist=dusting_checklist,
        arrangement_checklist=arrangement_checklist,
        big_room_checklist=big_room_checklist,
        small_room_checklist=small_room_checklist,
    )


@app.route("/process_room_checklist", methods=["POST"])
def process_room_checklist():
    cleaner_name = request.form["cleaner_name"]
    max_room_number = int(request.form["max_room_number"])

    unchecked_tasks_per_room = {}
    additional_notes_per_room = {}

    for i in range(1, max_room_number + 1):
        room_number = request.form.get(f"room_number_{i}")
        room_size = request.form.get(f"room_size_{i}")
        additional_notes = request.form.get(f"additional_notes_{i}", "").strip()

        unchecked_tasks = []

        # Process dusting and arrangement tasks for unchecked items
        for task_type, checklist in [
            ("dusting", dusting_checklist),
            ("arrangement", arrangement_checklist),
        ]:
            for task in checklist:
                task_checkbox = request.form.get(f"{task_type}_{i}_{task}")
                if task_checkbox is None:  # Not checked
                    unchecked_tasks.append(f"{task_type.capitalize()} - {task}")

        # Process room-specific items based on room size
        room_checklist = (
            big_room_checklist if room_size == "big" else small_room_checklist
        )
        for task, required_quantity in room_checklist:
            entered_quantity = int(request.form.get(f"quantity_{i}_{task}", 0))
            if entered_quantity < required_quantity:  # Quantity shortfall
                missing_quantity = required_quantity - entered_quantity
                unchecked_tasks.append(f"{task}: Need {missing_quantity} more")

        # Track unchecked tasks and notes only if they exist for the room
        if unchecked_tasks or additional_notes:
            unchecked_tasks_per_room[room_number] = unchecked_tasks
            additional_notes_per_room[room_number] = additional_notes

    return render_template(
        "summary.html",
        cleaner_name=cleaner_name,
        unchecked_tasks_per_room=unchecked_tasks_per_room,
        additional_notes_per_room=additional_notes_per_room,
        has_issues=bool(unchecked_tasks_per_room or additional_notes_per_room),
    )


if __name__ == "__main__":
    app.run(debug=True)
