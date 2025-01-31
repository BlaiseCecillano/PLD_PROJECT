import os
import time
import numpy as np

def start_feature():
    print("Welcome to the Transcript Generation System")
    level = input("Select student level (U for Undergraduate, G for Graduate, B for Both): ").strip().upper()
    if level not in ['U', 'G', 'B']:
        print("Invalid selection. Please try again.")
        return start_feature()

    degree = None
    if level in ['G', 'B']:
        degree = input("Select degree (M for Master, D for Doctorate, B0 for Both): ").strip().upper()
        if degree not in ['M', 'D', 'B0']:
            print("Invalid selection. Please try again.")
            return start_feature()

    print("Loading menu...")
    time.sleep(2)
    menu_feature(level, degree)

def menu_feature(level, degree):
    menu_options = {
        1: "Student Details",
        2: "Statistics",
        3: "Transcript Based on Major Courses",
        4: "Transcript Based on Minor Courses",
        5: "Full Transcript",
        6: "Previous Transcript Requests",
        7: "Select another Student",
        8: "Terminate the System"
    }

    print("\n--- Student Transcript Generation System ---")
    print("\n=============================================")
    for key, value in menu_options.items():
        print(f"{key}. {value}")
    print("=============================================")
    
    try:
        choice = int(input("Enter your choice (1-8): ").strip())
        if choice not in menu_options:
            raise ValueError("Invalid option.")
    except ValueError as e:
        print(e)
        return menu_feature(level, degree)

    if choice == 1:
        details_feature(level, degree)
    elif choice == 2:
        statistics_feature(level, degree)
    elif choice == 3:
        major_transcript_feature(level, degree)
    elif choice == 4:
        minor_transcript_feature(level, degree)
    elif choice == 5:
        full_transcript_feature(level, degree)
    elif choice == 6:
        previous_requests_feature(level, degree)
    elif choice == 7:
        new_student_feature()
    elif choice == 8:
        terminate_feature()

def details_feature(level, degree):
    student_id = input("Enter student ID: ").strip()

    try:
        # Load the CSV file
        data = np.loadtxt(r"D:\TranscriptGenerationSystem\data\studentDetails.csv", delimiter=",", dtype=str)

        # Strip whitespace and ensure consistency for all fields
        data = np.char.strip(data)

        # Filter data by student ID
        student_data = data[data[:, 1] == student_id]

        if student_data.size == 0:
            raise ValueError("Student ID not found.")

        # Further filter data based on level and degree
        filtered_data = []
        for record in student_data:
            record_level = record[5].upper().strip()  # Ensure consistency
            record_degree = record[6].upper().strip()  # Ensure consistency

            # Check if the record matches the selected level
            if level == 'B' or record_level == level:  # 'B' means include all levels
                if level in ['G', 'B']:  # Graduate or Both levels
                    if degree == 'B0' or record_degree == degree:  # 'B0' means include all degrees
                        filtered_data.append(record)
                elif level == 'U':  # Undergraduate level
                    filtered_data.append(record)  # No degree filtering for undergraduate

        if not filtered_data:
            raise ValueError("No records found matching the selected level and degree.")

        # Save the filtered details to a file
        with open(f"D:\TranscriptGenerationSystem\data\{student_id}details.txt", "w") as file:
            lines_to_print = []
            for record in filtered_data:
                line = (
                    f"\nName: {record[2]}\n"
                    f"stdID: {record[1]}\n"
                    f"Level(s): {record[5]}\n"
                    f"Degree: {record[6]}\n"
                    f"Number of Terms: {record[9]}\n"
                    f"College(s): {record[3]}\n"
                    f"Department: {record[4]}\n"
                )
                lines_to_print.append(line)
                print(line, end="")
                file.write(line)

        print("\nDetails saved to file.")
        time.sleep(5)

        # Erase printed lines
        for _ in lines_to_print:
            print("\033[F\033[K", end="")  # Move cursor up one line and clear it

        print("\nOutput cleared. Returning to menu.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Continue with the menu
        menu_feature(level, degree)

def statistics_feature(level, degree):
    student_id = input("Enter student ID: ").strip()
    try:
        filename = f"D:\TranscriptGenerationSystem\data\{student_id}.csv"

        # Load the data, skipping the header row
        data = np.loadtxt(filename, delimiter=",", dtype=str, skiprows=1)

        # Extract relevant columns: level, scores, and course type
        levels = data[:, 0]  # Assuming 1st column contains the level (G/U)
        scores = data[:, 7].astype(float)  
        terms = data[:, 2]  # Assuming 3rd column contains term numbers
        level_names = {'G': 'Graduate Level', 'U': 'Undergraduate Level'}

        # Initialize a dictionary to store statistics by level
        statistics = {}

        for level_type in ['G', 'U']:  # Graduate and Undergraduate
            # Filter data for the current level
            level_indices = levels == level_type
            level_scores = scores[level_indices]
            level_terms = terms[level_indices]

            if level_scores.size > 0:
                # Filter rows based on term numbers for this level
                term1_scores = level_scores[level_terms == "1"]
                term2_scores = level_scores[level_terms == "2"]

                # Calculate averages for the current level
                overall_average = np.mean(level_scores)
                term1_average = np.mean(term1_scores) if term1_scores.size > 0 else 0.0
                term2_average = np.mean(term2_scores) if term2_scores.size > 0 else 0.0

                # Determine maximum and minimum scores and their corresponding terms
                max_score = np.max(level_scores)
                min_score = np.min(level_scores)

                max_term = "Term 1" if max_score in term1_scores else "Term 2"
                min_term = "Term 1" if min_score in term1_scores else "Term 2"

                # Store statistics in the dictionary
                statistics[level_type] = {
                    "Overall Average": overall_average,
                    "Term 1": term1_average,
                    "Term 2": term2_average,
                    "Max Score": max_score,
                    "Max Term": max_term,
                    "Min Score": min_score,
                    "Min Term": min_term,
                }

        # Save statistics to a file
        output_filename = f"D:\TranscriptGenerationSystem\data\{student_id}statistics.txt"
        with open(output_filename, "w") as file:
            for level_type, stats in statistics.items():
                level_name = level_names.get(level_type, level_type)  # Get the full name or use the type as fallback
                file.write("\n==========================================================")
                file.write(f"\n***************    {level_name}    ***************")
                file.write("\n==========================================================")
                file.write(f"\nOverall Average (major and minor) for all terms: {stats['Overall Average']:.2f}")
                file.write("\nAverage (major and minor) of each term:")
                file.write(f"\n      Term 1: {stats['Term 1']:.2f}")
                file.write(f"\n      Term 2: {stats['Term 2']:.2f}")
                file.write(f"\nMaximum grade(s) and in which terms(s): {stats['Max Score']:.2f} ({stats['Max Term']})")
                file.write(f"\nMinimum grade(s) and in which terms(s): {stats['Min Score']:.2f} ({stats['Min Term']})")
                file.write("\n==========================================================")
                file.write("\n")

        # Print statistics to the console
        for level_type, stats in statistics.items():
            level_name = level_names.get(level_type, level_type)  # Get the full name or use the type as fallback
            print("\n==========================================================")
            print(f"***************    {level_name}    ***************")
            print("==========================================================")
            print(f"Overall Average (major and minor) for all terms: {stats['Overall Average']:.2f}")
            print("Average (major and minor) of each term:")
            print(f"      Term 1: {stats['Term 1']:.2f}")
            print(f"      Term 2: {stats['Term 2']:.2f}")
            print(f"Maximum grade(s) and in which terms(s): {stats['Max Score']:.2f} ({stats['Max Term']})")
            print(f"Minimum grade(s) and in which terms(s): {stats['Min Score']:.2f} ({stats['Min Term']})")
            print("\n==========================================================")

        print("\nStatistics saved to file.")
        time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        menu_feature(level, degree)

def major_transcript_feature(level, degree):
    student_id = input("Enter student ID: ").strip()
    try:
        filename = f"D:\TranscriptGenerationSystem\data\{student_id}.csv"
        
        # Load data with correct dtype
        data = np.genfromtxt(
            filename,
            delimiter=",",
            dtype=[
                ('Level', 'U10'),
                ('Degree', 'U10'),
                ('Term', 'U10'),
                ('courseName', 'U50'),
                ('courseID', 'U10'),
                ('courseType', 'U10'),
                ('creditHours', 'f8'),
                ('Grade', 'f8')
            ],
            names=True,
            encoding="utf-8"
        )
        
        # Extract columns
        terms = data['Term']
        scores = data['Grade'].astype(float)
        course_name = data['courseName']
        course_id = data['courseID']
        course_type = data['courseType']
        credit_hours = data['creditHours']

        term_names = {'1': 'Term 1', '2': 'Term 2'}
        statistics = {}

        for term_type in ['1', '2']:
            term_indices = terms == term_type
            term_scores = scores[term_indices]
            coursetype_scores = course_type[term_indices]
            coursename_terms = course_name[term_indices]
            courseid_terms = course_id[term_indices]
            credithrs_terms = credit_hours[term_indices]

            if term_scores.size > 0:
                major_scores = term_scores[coursetype_scores == "Major"]
                minor_scores = term_scores[coursetype_scores == "Minor"]

                overall_term_average = np.mean(term_scores)
                major_average = np.mean(major_scores) if major_scores.size > 0 else 0.0
                minor_average = np.mean(minor_scores) if minor_scores.size > 0 else 0.0

                statistics[term_type] = {
                    "Overall Average": overall_term_average,
                    "Major": major_average,
                    "Minor": minor_average,
                }

        for term_type, stats in statistics.items():
            term_name = term_names.get(term_type, term_type)
            print("\n==========================================================")
            print(f"\n***************    Term {term_name}    ***************")
            print("\n==========================================================")
            print("\nCourse ID     Course Name                Credit Hours     Grade")
            for i in range(len(coursename_terms)):
                print(
                    f"\n{courseid_terms[i]}     {coursename_terms[i]}                {credithrs_terms[i]}     {term_scores[i]}"
                )
            print(f"\nMajor Average = {stats['Major']:.2f}                Overall Average = {stats['Overall Average']:.2f} ")
            print("\n==========================================================")

        output_filename = f"D:\TranscriptGenerationSystem\data\{student_id}_majortranscript.txt"
        with open(output_filename, "w") as file:
            for term_type, stats in statistics.items():
                term_name = term_names.get(term_type, term_type)
                file.write("\n==========================================================")
                file.write(f"\n***************    Term {term_name}    ***************")
                file.write("\n==========================================================")
                file.write("\nCourse ID     Course Name                Credit Hours     Grade")
                for i in range(len(coursename_terms)):
                    file.write(
                        f"\n{courseid_terms[i]}     {coursename_terms[i]}                {credithrs_terms[i]}     {term_scores[i]}"
                    )
                file.write(f"\nMajor Average = {stats['Major']:.2f}                Overall Average = {stats['Overall Average']:.2f} ")
                file.write("\n==========================================================")
                file.write("\n")

        print("Major transcript saved to file.")
        time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        menu_feature(level, degree)

def minor_transcript_feature(level, degree):
    student_id = input("Enter student ID: ").strip()
    try:
        filename = f"D:\TranscriptGenerationSystem\data\{student_id}.csv"
        
        # Load data with correct dtype
        data = np.genfromtxt(
            filename,
            delimiter=",",
            dtype=[
                ('Level', 'U10'),
                ('Degree', 'U10'),
                ('Term', 'U10'),
                ('courseName', 'U50'),
                ('courseID', 'U10'),
                ('courseType', 'U10'),
                ('creditHours', 'f8'),
                ('Grade', 'f8')
            ],
            names=True,
            encoding="utf-8"
        )
        
        # Extract columns
        terms = data['Term']
        scores = data['Grade'].astype(float)
        course_name = data['courseName']
        course_id = data['courseID']
        course_type = data['courseType']
        credit_hours = data['creditHours']

        term_names = {'1': 'Term 1', '2': 'Term 2'}
        statistics = {}

        for term_type in ['1', '2']:
            term_indices = terms == term_type
            term_scores = scores[term_indices]
            coursetype_scores = course_type[term_indices]
            coursename_terms = course_name[term_indices]
            courseid_terms = course_id[term_indices]
            credithrs_terms = credit_hours[term_indices]

            if term_scores.size > 0:
                # Filter MINOR courses
                minor_scores = term_scores[coursetype_scores == "Minor"]
                minor_course_names = coursename_terms[coursetype_scores == "Minor"]
                minor_course_ids = courseid_terms[coursetype_scores == "Minor"]
                minor_credithrs = credithrs_terms[coursetype_scores == "Minor"]

                # Calculate averages
                overall_term_average = np.mean(term_scores)
                minor_average = np.mean(minor_scores) if minor_scores.size > 0 else 0.0

                statistics[term_type] = {
                    "Overall Average": overall_term_average,
                    "Minor Average": minor_average,
                    "Minor Courses": list(zip(minor_course_ids, minor_course_names, minor_credithrs, minor_scores))
                }

        # Print and save minor transcript
        for term_type, stats in statistics.items():
            term_name = term_names.get(term_type, term_type)
            print("\n==========================================================")
            print(f"\n***************    Term {term_name} (Minor Courses)    ***************")
            print("\n==========================================================")
            print("\nCourse ID     Course Name                Credit Hours     Grade")
            
            # Print minor courses for this term
            for course in stats["Minor Courses"]:
                course_id, course_name, credit_hrs, grade = course
                print(f"\n{course_id}     {course_name.ljust(25)} {credit_hrs}               {grade:.2f}")
            
            print(f"\nMinor Average = {stats['Minor Average']:.2f}                Overall Average = {stats['Overall Average']:.2f} ")
            print("\n==========================================================")

        # Save to file
        output_filename = f"D:\TranscriptGenerationSystem\data\{student_id}_minortranscript.txt"
        with open(output_filename, "w") as file:
            for term_type, stats in statistics.items():
                term_name = term_names.get(term_type, term_type)
                file.write("\n==========================================================")
                file.write(f"\n***************    Term {term_name} (Minor Courses)    ***************")
                file.write("\n==========================================================")
                file.write("\nCourse ID     Course Name                Credit Hours     Grade")
                
                for course in stats["Minor Courses"]:
                    course_id, course_name, credit_hrs, grade = course
                    file.write(f"\n{course_id}     {course_name.ljust(25)} {credit_hrs}               {grade:.2f}")
                
                file.write(f"\nMinor Average = {stats['Minor Average']:.2f}                Overall Average = {stats['Overall Average']:.2f} ")
                file.write("\n==========================================================\n")

        print("\nMinor transcript saved to file.")
        time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        menu_feature(level, degree)

def full_transcript_feature(level, degree):
    student_id = input("Enter student ID: ").strip()
    # Combine major and minor transcript features.
    pass

def previous_requests_feature(level, degree):
    student_id = input("Enter student ID: ").strip()
    # Retrieve and display previous requests.
    pass

def new_student_feature():
    print("Starting new student session...")
    time.sleep(2)
    start_feature()

def terminate_feature():
    print("Terminating the program. Goodbye!")
    exit()

if __name__ == "__main__":
    start_feature()