import re  # To use regular expressions for pattern matching

class StudentTranscriptSystem:
    def __init__(self):
        # Initialize students dictionary with student ID as key
        self.students = {}
        self.current_student_id = None
        self.load_data()  # Load previously saved data when the program starts

    def add_course_details(self, student_name, student_id):
        if student_id not in self.students:
            self.students[student_id] = {"name": student_name, "major_courses": [], "minor_courses": [], "transcript_requests": []}
        print("Enter the details for courses for {}:".format(student_name))
        while True:
            course_type = input("Is this a major or minor course? (major/minor) or type 'done' to finish: ").lower()
            if course_type == 'done':
                break
            elif course_type not in ['major', 'minor']:
                print("Invalid input. Please type 'major' or 'minor'.")
                continue
            course_name = input("Enter course name for {} course: ".format(course_type))
            grade = input("Enter grade for {}: ".format(course_name))
            self.students[student_id]["{}_courses".format(course_type)].append((course_name, grade))

    def display_statistics(self, student_id):
        if student_id in self.students and (self.students[student_id]["major_courses"] or self.students[student_id]["minor_courses"]):
            total_courses = len(self.students[student_id]["major_courses"]) + len(self.students[student_id]["minor_courses"])
            print("{} has {} courses.".format(self.students[student_id]["name"], total_courses))
        else:
            print("No course details available for {}.".format(self.students[student_id]["name"]))

    def generate_transcript(self, student_id, course_type="major"):
        if student_id in self.students and (self.students[student_id]["major_courses"] or self.students[student_id]["minor_courses"]):
            transcript = "{}'s {} Transcript:\n".format(self.students[student_id]["name"], course_type.capitalize())
            if course_type == "major":
                for course, grade in self.students[student_id]["major_courses"]:
                    transcript += "{}: {}\n".format(course, grade)
            elif course_type == "minor":
                for course, grade in self.students[student_id]["minor_courses"]:
                    transcript += "{}: {}\n".format(course, grade)
            elif course_type == "full":
                for course, grade in self.students[student_id]["major_courses"]:
                    transcript += "Major - {}: {}\n".format(course, grade)
                for course, grade in self.students[student_id]["minor_courses"]:
                    transcript += "Minor - {}: {}\n".format(course, grade)
            print(transcript)
            self.students[student_id]["transcript_requests"].append(course_type)
        else:
            print("No course details available for {}.".format(self.students[student_id]["name"]))

    def show_previous_requests(self, student_id):
        if student_id in self.students and self.students[student_id]["transcript_requests"]:
            print("{} has requested the following transcripts:".format(self.students[student_id]["name"]))
            for request in self.students[student_id]["transcript_requests"]:
                print("- {} transcript".format(request))
        else:
            print("No previous transcript requests found for {}.".format(self.students[student_id]["name"]))

    def get_student_id(self):
        """Prompt user to enter a valid student ID based on the format 0000-00000-MN-0"""
        
        # Define the regex pattern for the ID format: alphanumeric characters ending with 'MN-0'
        student_id_pattern = re.compile(r'^[a-zA-Z0-9]+-?[a-zA-Z0-9]+-MN-0$')

        while True:
            std_id = input("Enter the student ID (format: 0000-00000-MN-0, alphanumeric with MN-0 at the end): ")

            # Check if the ID matches the pattern
            if student_id_pattern.match(std_id):
                # Check if ID exists in the previously loaded data
                if std_id in self.students:
                    print("Data loaded successfully.")  # Moved this message to display after valid ID
                    print("Welcome back, {}!".format(self.students[std_id]["name"]))
                    self.current_student_id = std_id  # Store the current student ID
                    return std_id
                else:
                    print("Student ID not found in the system. Please enter your name to register.")
                    student_name = input("Enter your name: ")
                    self.add_course_details(student_name, std_id)
                    self.current_student_id = std_id  # Store the current student ID
                    return std_id
            else:
                print("Invalid format. Please ensure the student ID matches the format: 0000-00000-MN-0, alphanumeric with MN-0 at the end.")

    def save_data(self):
        """Save the student data to a .txt file based on student ID"""
        if self.current_student_id:
            # Format the filename with the student's ID (e.g., std000000000mn0.txt)
            filename = "std{}.txt".format(self.current_student_id.replace('-', '').lower())
            with open(filename, "w") as file:
                for student_id, details in self.students.items():
                    file.write("Student ID: {}\n".format(student_id))
                    file.write("Name: {}\n".format(details["name"]))
                    file.write("Major Courses:\n")
                    for course, grade in details["major_courses"]:
                        file.write("{}: {}\n".format(course, grade))
                    file.write("Minor Courses:\n")
                    for course, grade in details["minor_courses"]:
                        file.write("{}: {}\n".format(course, grade))
                    file.write("Transcript Requests:\n")
                    for request in details["transcript_requests"]:
                        file.write("{} transcript\n".format(request))
                    file.write("\n")
            print("Data saved to {} successfully!".format(filename))

    def load_data(self):
        """Load student data from a saved .txt file"""
        import os

        # Look for files in the current directory that match the pattern 'std<student_id>.txt'
        files = [f for f in os.listdir() if f.endswith('.txt') and f.startswith('std')]
        
        for file in files:
            with open(file, 'r') as f:
                student_id = None
                student_name = None
                major_courses = []
                minor_courses = []
                transcript_requests = []
                
                for line in f:
                    line = line.strip()
                    if line.startswith("Student ID:"):
                        student_id = line.split(":")[1].strip()
                    elif line.startswith("Name:"):
                        student_name = line.split(":")[1].strip()
                    elif line.startswith("Major Courses:"):
                        major_courses = self._parse_courses(f)
                    elif line.startswith("Minor Courses:"):
                        minor_courses = self._parse_courses(f)
                    elif line.startswith("Transcript Requests:"):
                        transcript_requests = self._parse_requests(f)
                
                if student_id:
                    self.students[student_id] = {
                        "name": student_name,
                        "major_courses": major_courses,
                        "minor_courses": minor_courses,
                        "transcript_requests": transcript_requests
                    }

    def _parse_courses(self, file):
        courses = []
        while True:
            line = file.readline().strip()
            if not line or line.startswith("Minor Courses:") or line.startswith("Transcript Requests:"):
                break
            course, grade = line.split(":")
            courses.append((course.strip(), grade.strip()))
        return courses

    def _parse_requests(self, file):
        requests = []
        while True:
            line = file.readline().strip()
            if not line:
                break
            requests.append(line.split()[0])
        return requests

def main():
    system = StudentTranscriptSystem()

    while True:
        print("Welcome to the Student Transcript System")
        std_id = system.get_student_id()  # Get a valid student ID

        while True:  # This loop keeps the user inside the menu until they choose to exit
            print("\nMenu:")
            print("1. Add course details")
            print("2. Display statistics")
            print("3. Generate transcript based on major courses")
            print("4. Generate transcript based on minor courses")
            print("5. Generate full transcript")
            print("6. Show previous transcript requests")
            print("7. Select another student")
            print("8. Save data and Terminate the system")

            choice = input("Enter your choice (1-8): ")

            if choice == '1':
                system.add_course_details(system.students[std_id]["name"], std_id)
        
            elif choice == '2':
                system.display_statistics(std_id)
            elif choice == '3':
                system.generate_transcript(std_id, course_type="major")
            elif choice == '4':
                system.generate_transcript(std_id, course_type="minor")
            elif choice == '5':
                system.generate_transcript(std_id, course_type="full")
            elif choice == '6':
                system.show_previous_requests(std_id)
            elif choice == '7':
                break  # Break out of the menu to re-enter the student ID
            elif choice == '8':
                system.save_data()
                print("Terminating the system. Goodbye!")
                return  # Exit the program
            else:
                print("Invalid choice. Please try again.")
