import csv

data = [
    ["name", "gender", "adhar_card_number", "dob", "identification_marks", "admission_category", "height", "weight", "mail_id", "contact_detail", "address", "father_name", "father_qualification", "father_profession", "father_designation", "father_aadhar_card", "father_mobile_number", "father_mail_id", "mother_name", "mother_qualification", "mother_profession", "mother_designation", "mother_aadhar_card", "mother_mobile_number", "mother_mail_id", "enrollment_id", "class_name", "section", "date_of_joining", "file", "document_type"],
    ["John Doe", "Male", "1234567890", "2000-01-01", "A scar on the left hand", "General", "175.5", "70.2", "john.doe@example.com", "1234567890", "123 Main Street, Cityville", "John Doe Sr.", "Bachelor's Degree", "Engineer", "Senior Engineer", "0987654321", "9876543210", "john.doe.sr@example.com", "Jane Doe", "Master's Degree", "Doctor", "Pediatrician", "9876543210", "1234567890", "jane.doe@example.com", "EN123456", "12th", "A", "2022-01-01", "path/to/your/document.pdf", "Admission Form"]
]

filename = 'C:\\Users\\immra\\Desktop\\Habrie\\habrie_assignment\\dummy_data.csv'


with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f'Data has been written to {filename}')
