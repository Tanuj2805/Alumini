// add alumni
document.getElementById('alumniForm').addEventListener('submit', function (e) {
    let valid = true;

    // Clear previous errors
    document.querySelectorAll('.error-message').forEach(el => el.innerText = '');

    // Validate Name
    const nameField = document.getElementById('inputAlumniName');
    const namePattern = /^[A-Za-z\s'-]+$/;
    if (!namePattern.test(nameField.value)) {
        document.getElementById('alumniNameError').innerText = "Name can only contain letters, spaces, hyphens, and apostrophes.";
        valid = false;
    }

    // Validate DOB
    const dobField = document.getElementById('inputDOB');
    if (!dobField.value) {
        document.getElementById('dobError').innerText = "Date of birth is required.";
        valid = false;
    }

    // Validate Email
    const emailField = document.getElementById('inputAlumniEmail');
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(emailField.value)) {
        document.getElementById('emailError').innerText = "Enter a valid email address.";
        valid = false;
    }

    // Validate Phone
    const phoneField = document.getElementById('inputAlumniPhone');
    const phonePattern = /^[0-9]{10,15}$/;
    if (!phonePattern.test(phoneField.value)) {
        document.getElementById('phoneError').innerText = "Phone number must be 10 to 15 digits.";
        valid = false;
    }

    // Validate Address
    const addressField = document.getElementById('inputAddress');
    if (!addressField.value.trim()) {
        document.getElementById('addressError').innerText = "Address is required.";
        valid = false;
    }

    // Validate Department
    const departmentField = document.getElementById('inputDepartment');
    if (!departmentField.value) {
        document.getElementById('departmentError').innerText = "Please select a department.";
        valid = false;
    }

    // Validate Graduation Year
    const gradYearField = document.getElementById('inputGraduationYear');
    const gradYear = parseInt(gradYearField.value);
    const currentYear = new Date().getFullYear();
    if (!gradYear || gradYear < 1950 || gradYear > 2100) {
        document.getElementById('graduationYearError').innerText = "Enter a valid graduation year (1950 - 2100).";
        valid = false;
    }

    if (!valid) e.preventDefault();
});
