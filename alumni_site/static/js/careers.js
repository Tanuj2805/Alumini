// Career Management Functions
document.addEventListener('DOMContentLoaded', function() {
  // Handle add job button click
  const addJobBtn = document.getElementById('btnOpenModalAddJob');
  if (addJobBtn) {
    addJobBtn.addEventListener('click', function() {
      showAddJobModal();
    });
  }

  // Handle edit job button click
  document.querySelectorAll('.jobs-table .btn-action.edit').forEach(button => {
    button.addEventListener('click', function() {
      const jobId = this.closest('tr').getAttribute('data-job-id');
      getJobDetails(jobId);
    });
  });

  // Handle delete job button click
  document.querySelectorAll('.jobs-table .btn-action.delete').forEach(button => {
    button.addEventListener('click', function() {
      const jobId = this.closest('tr').getAttribute('data-job-id');
      confirmDeleteJob(jobId);
    });
  });
});

// Function to show add job modal
function showAddJobModal() {
  // Create modal HTML
  const modalHtml = `
    <div class="modal" id="modalAddJob">
      <div class="modal-content">
        <span class="close">&times;</span>
        <h2>Post New Job</h2>
        <form id="addJobForm" method="POST" action="/add_job/">
          <input type="hidden" name="csrfmiddlewaretoken" value="${getCsrfToken()}">
          
          <div class="form-group">
            <label for="inputPosition">Position:</label>
            <input type="text" id="inputPosition" name="position" required>
            <small id="positionError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="inputCompany">Company:</label>
            <input type="text" id="inputCompany" name="company" required>
            <small id="companyError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="inputLocation">Location:</label>
            <input type="text" id="inputLocation" name="location" required>
            <small id="locationError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="inputJobType">Job Type:</label>
            <select id="inputJobType" name="job_type" required>
              <option value="">Select job type</option>
              <option value="full_time">Full Time</option>
              <option value="part_time">Part Time</option>
              <option value="contract">Contract</option>
              <option value="internship">Internship</option>
            </select>
            <small id="jobTypeError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="inputDescription">Job Description:</label>
            <textarea id="inputDescription" name="description" required></textarea>
            <small id="descriptionError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="inputRequirements">Requirements:</label>
            <textarea id="inputRequirements" name="requirements" required></textarea>
            <small id="requirementsError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="inputSalary">Salary Range:</label>
            <input type="text" id="inputSalary" name="salary" placeholder="e.g. $50,000 - $70,000">
            <small id="salaryError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="inputApplicationDeadline">Application Deadline:</label>
            <input type="date" id="inputApplicationDeadline" name="application_deadline" required>
            <small id="applicationDeadlineError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="inputContactEmail">Contact Email:</label>
            <input type="email" id="inputContactEmail" name="contact_email" required>
            <small id="contactEmailError" class="error-message"></small>
          </div>

          <button type="submit" class="btn-primary">Post Job</button>
        </form>
      </div>
    </div>
  `;
  
  // Add modal to the DOM
  document.body.insertAdjacentHTML('beforeend', modalHtml);
  
  // Show the modal
  document.getElementById('modalAddJob').style.display = 'block';
  
  // Add event listeners
  const modal = document.getElementById('modalAddJob');
  const closeBtn = modal.querySelector('.close');
  const form = modal.querySelector('#addJobForm');
  
  // Close modal when clicking on the close button
  closeBtn.addEventListener('click', function() {
    modal.remove();
  });
  
  // Close modal when clicking outside of it
  window.addEventListener('click', function(event) {
    if (event.target === modal) {
      modal.remove();
    }
  });
  
  // Handle form submission
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Validate form
    if (!validateJobForm()) {
      return;
    }
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Posting...';
    submitBtn.disabled = true;
    
    // Submit the form
    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: {
        'X-CSRFToken': getCsrfToken()
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Job posted successfully!');
        modal.remove();
        // Refresh the page to show updated data
        window.location.reload();
      } else {
        alert('Error: ' + data.message);
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while posting the job.');
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    });
  });
}

// Function to validate job form
function validateJobForm() {
  let isValid = true;
  const position = document.getElementById('inputPosition').value;
  const company = document.getElementById('inputCompany').value;
  const location = document.getElementById('inputLocation').value;
  const jobType = document.getElementById('inputJobType').value;
  const description = document.getElementById('inputDescription').value;
  const requirements = document.getElementById('inputRequirements').value;
  const applicationDeadline = document.getElementById('inputApplicationDeadline').value;
  const contactEmail = document.getElementById('inputContactEmail').value;

  // Clear previous error messages
  document.querySelectorAll('#modalAddJob .error-message').forEach(el => el.textContent = '');

  if (!position) {
      document.getElementById('positionError').textContent = 'Position is required.';
      isValid = false;
  }

  if (!company) {
      document.getElementById('companyError').textContent = 'Company is required.';
      isValid = false;
  }

  if (!location) {
      document.getElementById('locationError').textContent = 'Location is required.';
      isValid = false;
  }

  if (!jobType) {
      document.getElementById('jobTypeError').textContent = 'Job type is required.';
      isValid = false;
  }

  if (!description) {
      document.getElementById('descriptionError').textContent = 'Job description is required.';
      isValid = false;
  }

  if (!requirements) {
      document.getElementById('requirementsError').textContent = 'Requirements are required.';
      isValid = false;
  }

  if (!applicationDeadline) {
      document.getElementById('applicationDeadlineError').textContent = 'Application deadline is required.';
      isValid = false;
  }

  if (!contactEmail || !/\S+@\S+\.\S+/.test(contactEmail)) {
      document.getElementById('contactEmailError').textContent = 'Valid contact email is required.';
      isValid = false;
  }

  return isValid;
}

// Function to get job details
function getJobDetails(jobId) {
  // Show loading state
  showLoadingState('careers');
  
  // Create form data
  const formData = new FormData();
  formData.append('job_id', jobId);
  
  // Send request to get job details
  fetch('/get_job_details/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCsrfToken()
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Show edit modal
      showEditJobModal(data.job);
    } else {
      alert('Error: ' + data.message);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred while fetching job details.');
  })
  .finally(() => {
    // Hide loading state
    hideLoadingState('careers');
  });
}

// Function to show edit job modal
function showEditJobModal(job) {
  // Create modal HTML
  const modalHtml = `
    <div class="modal" id="modalEditJob">
      <div class="modal-content">
        <span class="close">&times;</span>
        <h2>Edit Job</h2>
        <form id="editJobForm" method="POST" action="/edit_job/">
          <input type="hidden" name="csrfmiddlewaretoken" value="${getCsrfToken()}">
          <input type="hidden" name="job_id" value="${job.job_id}">
          
          <div class="form-group">
            <label for="editPosition">Position:</label>
            <input type="text" id="editPosition" name="position" value="${job.position}" required>
            <small id="editPositionError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="editCompany">Company:</label>
            <input type="text" id="editCompany" name="company" value="${job.company}" required>
            <small id="editCompanyError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="editLocation">Location:</label>
            <input type="text" id="editLocation" name="location" value="${job.location}" required>
            <small id="editLocationError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="editJobType">Job Type:</label>
            <select id="editJobType" name="job_type" required>
              <option value="">Select job type</option>
              <option value="full_time" ${job.job_type === 'full_time' ? 'selected' : ''}>Full Time</option>
              <option value="part_time" ${job.job_type === 'part_time' ? 'selected' : ''}>Part Time</option>
              <option value="contract" ${job.job_type === 'contract' ? 'selected' : ''}>Contract</option>
              <option value="internship" ${job.job_type === 'internship' ? 'selected' : ''}>Internship</option>
            </select>
            <small id="editJobTypeError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="editDescription">Job Description:</label>
            <textarea id="editDescription" name="description" required>${job.description}</textarea>
            <small id="editDescriptionError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="editRequirements">Requirements:</label>
            <textarea id="editRequirements" name="requirements" required>${job.requirements}</textarea>
            <small id="editRequirementsError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="editSalary">Salary Range:</label>
            <input type="text" id="editSalary" name="salary" value="${job.salary || ''}" placeholder="e.g. $50,000 - $70,000">
            <small id="editSalaryError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="editApplicationDeadline">Application Deadline:</label>
            <input type="date" id="editApplicationDeadline" name="application_deadline" value="${job.application_deadline}" required>
            <small id="editApplicationDeadlineError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="editContactEmail">Contact Email:</label>
            <input type="email" id="editContactEmail" name="contact_email" value="${job.contact_email}" required>
            <small id="editContactEmailError" class="error-message"></small>
          </div>

          <div class="form-group">
            <label for="editStatus">Status:</label>
            <select id="editStatus" name="status" required>
              <option value="active" ${job.status === 'active' ? 'selected' : ''}>Active</option>
              <option value="closed" ${job.status === 'closed' ? 'selected' : ''}>Closed</option>
              <option value="draft" ${job.status === 'draft' ? 'selected' : ''}>Draft</option>
            </select>
            <small id="editStatusError" class="error-message"></small>
          </div>

          <button type="submit" class="btn-primary">Update Job</button>
        </form>
      </div>
    </div>
  `;
  
  // Add modal to the DOM
  document.body.insertAdjacentHTML('beforeend', modalHtml);
  
  // Show the modal
  document.getElementById('modalEditJob').style.display = 'block';
  
  // Add event listeners
  const modal = document.getElementById('modalEditJob');
  const closeBtn = modal.querySelector('.close');
  const form = modal.querySelector('#editJobForm');
  
  // Close modal when clicking on the close button
  closeBtn.addEventListener('click', function() {
    modal.remove();
  });
  
  // Close modal when clicking outside of it
  window.addEventListener('click', function(event) {
    if (event.target === modal) {
      modal.remove();
    }
  });
  
  // Handle form submission
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Validate form
    if (!validateEditJobForm()) {
      return;
    }
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Updating...';
    submitBtn.disabled = true;
    
    // Submit the form
    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: {
        'X-CSRFToken': getCsrfToken()
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Job updated successfully!');
        modal.remove();
        // Refresh the page to show updated data
        window.location.reload();
      } else {
        alert('Error: ' + data.message);
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while updating the job.');
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    });
  });
}

// Function to validate edit job form
function validateEditJobForm() {
  let isValid = true;
  const position = document.getElementById('editPosition').value;
  const company = document.getElementById('editCompany').value;
  const location = document.getElementById('editLocation').value;
  const jobType = document.getElementById('editJobType').value;
  const description = document.getElementById('editDescription').value;
  const requirements = document.getElementById('editRequirements').value;
  const applicationDeadline = document.getElementById('editApplicationDeadline').value;
  const contactEmail = document.getElementById('editContactEmail').value;
  const status = document.getElementById('editStatus').value;

  // Clear previous error messages
  document.querySelectorAll('#modalEditJob .error-message').forEach(el => el.textContent = '');

  if (!position) {
      document.getElementById('editPositionError').textContent = 'Position is required.';
      isValid = false;
  }

  if (!company) {
      document.getElementById('editCompanyError').textContent = 'Company is required.';
      isValid = false;
  }

  if (!location) {
      document.getElementById('editLocationError').textContent = 'Location is required.';
      isValid = false;
  }

  if (!jobType) {
      document.getElementById('editJobTypeError').textContent = 'Job type is required.';
      isValid = false;
  }

  if (!description) {
      document.getElementById('editDescriptionError').textContent = 'Job description is required.';
      isValid = false;
  }

  if (!requirements) {
      document.getElementById('editRequirementsError').textContent = 'Requirements are required.';
      isValid = false;
  }

  if (!applicationDeadline) {
      document.getElementById('editApplicationDeadlineError').textContent = 'Application deadline is required.';
      isValid = false;
  }

  if (!contactEmail || !/\S+@\S+\.\S+/.test(contactEmail)) {
      document.getElementById('editContactEmailError').textContent = 'Valid contact email is required.';
      isValid = false;
  }

  if (!status) {
      document.getElementById('editStatusError').textContent = 'Status is required.';
      isValid = false;
  }

  return isValid;
}

// Function to confirm delete job
function confirmDeleteJob(jobId) {
  if (confirm('Are you sure you want to delete this job posting? This action cannot be undone.')) {
    // Show loading state
    showLoadingState('careers');
    
    // Create form data
    const formData = new FormData();
    formData.append('job_id', jobId);
    
    // Send request to delete job
    fetch('/delete_job/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCsrfToken()
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Job deleted successfully!');
        // Refresh the page to show updated data
        window.location.reload();
      } else {
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while deleting the job.');
    })
    .finally(() => {
      // Hide loading state
      hideLoadingState('careers');
    });
  }
}

// Helper function to get CSRF token
function getCsrfToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Helper function to show loading state
function showLoadingState(sectionId) {
  const section = document.getElementById(sectionId);
  if (section) {
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';
    loadingOverlay.innerHTML = `
      <div class="loading-spinner"></div>
      <p>Loading...</p>
    `;
    section.appendChild(loadingOverlay);
  }
}

// Helper function to hide loading state
function hideLoadingState(sectionId) {
  const section = document.getElementById(sectionId);
  if (section) {
    const loadingOverlay = section.querySelector('.loading-overlay');
    if (loadingOverlay) {
      loadingOverlay.remove();
    }
  }
} 