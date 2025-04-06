// Navigation Handler
document.querySelectorAll('.sidebar-nav a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        
        // Remove active classes
        document.querySelectorAll('.sidebar-nav a').forEach(a => a.classList.remove('active'));
        document.querySelectorAll('.content-section').forEach(section => section.classList.remove('active'));
        
        // Set active state
        this.classList.add('active');
        document.querySelector(targetId).classList.add('active');
    });
});

// Initialize default view
document.querySelector('.sidebar-nav a.active').click();

   // Initialize Charts
   document.addEventListener('DOMContentLoaded', function() {
    // Alumni Growth Chart
    const alumniGrowthCtx = document.getElementById('alumniGrowthChart').getContext('2d');
    new Chart(alumniGrowthCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Alumni Growth',
                data: [100, 200, 300, 400, 500, 600],
                borderColor: '#2563eb',
                fill: false,
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });

    // Event Participation Chart
    const eventParticipationCtx = document.getElementById('eventParticipationChart').getContext('2d');
    new Chart(eventParticipationCtx, {
        type: 'bar',
        data: {
            labels: ['Event 1', 'Event 2', 'Event 3', 'Event 4', 'Event 5'],
            datasets: [{
                label: 'Participants',
                data: [50, 75, 100, 120, 150],
                backgroundColor: '#f59e0b',
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
});

// Navigation Handling
document.querySelectorAll('.sidebar-nav a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        
        // Remove active classes
        document.querySelectorAll('.sidebar-nav a').forEach(a => a.classList.remove('active'));
        document.querySelectorAll('.content-section').forEach(section => section.classList.remove('active'));
        
        // Set active state
        this.classList.add('active');
        if(document.querySelector(targetId)) {
            document.querySelector(targetId).classList.add('active');
        }
    });
});

// Initialize default view
document.querySelector('.sidebar-nav a.active').click();

document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for alumni search and sort buttons
    const alumniSearchBtn = document.getElementById('alumniSearchBtn');
    const alumniSortBtn = document.getElementById('alumniSortBtn');
  
    if (alumniSearchBtn) {
      alumniSearchBtn.addEventListener('click', searchAlumni);
    }
  
    if (alumniSortBtn) {
      alumniSortBtn.addEventListener('click', sortAlumni);
    }
  
    // Function to filter alumni based on the search input
    function searchAlumni() {
      const searchValue = document.getElementById('alumniSearch').value.toLowerCase();
      const table = document.getElementById('alumniTable');
      const rows = table.getElementsByTagName('tr');
  
      // Loop through table rows (skipping header row)
      for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let matchFound = false;
        // Check each cell (except the actions cell)
        for (let j = 0; j < cells.length - 1; j++) {
          if (cells[j].innerText.toLowerCase().includes(searchValue)) {
            matchFound = true;
            break;
          }
        }
        rows[i].style.display = matchFound ? '' : 'none';
      }
    }
  
    // Function to sort alumni based on the selected criteria
    function sortAlumni() {
      const sortBy = document.getElementById('alumniSort').value;
      if (!sortBy) return; // Exit if no sort option is selected
  
      const table = document.getElementById('alumniTable');
      const tbody = table.querySelector('tbody');
      const rowsArray = Array.from(tbody.querySelectorAll('tr'));
  
      // Determine which column to sort (Name = 0, Email = 1, Graduation Year = 2)
      let colIndex;
      switch (sortBy) {
        case 'name':
          colIndex = 0;
          break;
        case 'email':
          colIndex = 1;
          break;
        case 'year':
          colIndex = 2;
          break;
        default:
          colIndex = 0;
      }
  
      // Sort the rows based on the selected column
      rowsArray.sort((rowA, rowB) => {
        const cellA = rowA.cells[colIndex].innerText.toLowerCase();
        const cellB = rowB.cells[colIndex].innerText.toLowerCase();
        if (cellA < cellB) return -1;
        if (cellA > cellB) return 1;
        return 0;
      });
  
      // Re-append the sorted rows
      tbody.innerHTML = '';
      rowsArray.forEach(row => tbody.appendChild(row));
    }
  });

  document.addEventListener('DOMContentLoaded', function() {
    // Modal Elements with unique names
    const btnOpenModalAddAlumni = document.getElementById('btnOpenModalAddAlumni');
    const modalAddAlumni = document.getElementById('modalAddAlumni');
    const btnCloseModalAddAlumni = document.getElementById('btnCloseModalAddAlumni');
  
    // Open the modal when the "Add Alumni" button is clicked
    if (btnOpenModalAddAlumni) {
      btnOpenModalAddAlumni.addEventListener('click', function() {
        modalAddAlumni.style.display = 'block';
      });
    }
  
    // Close the modal when the close button is clicked
    if (btnCloseModalAddAlumni) {
      btnCloseModalAddAlumni.addEventListener('click', function() {
        modalAddAlumni.style.display = 'none';
      });
    }
  
    // Close the modal when clicking outside of the modal content
    window.addEventListener('click', function(event) {
      if (event.target === modalAddAlumni) {
        modalAddAlumni.style.display = 'none';
      }
    });
  });
  
  //admin dash

  // Generic Modal Handler
function initializeModal(modalId, openButtonId) {
  const modal = document.getElementById(modalId);
  const openButton = document.getElementById(openButtonId);
  if (!modal || !openButton) return;

  const closeButton = modal.querySelector('.close');
  
  openButton.addEventListener('click', () => modal.style.display = 'block');
  closeButton.addEventListener('click', () => modal.style.display = 'none');
  window.addEventListener('click', (e) => e.target === modal && (modal.style.display = 'none'));
}

// Form Submission Handler
async function handleFormSubmit(formId, endpoint, successMessage) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);

      try {
          const response = await fetch(endpoint, {
              method: 'POST',
              headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
              body: formData
          });

          if (response.ok) {
              alert(successMessage);
              form.reset();
              document.getElementById(form.closest('.modal').id).style.display = 'none';
              // Add logic to refresh relevant data
          } else {
              alert('Error: ' + response.statusText);
          }
      } catch (error) {
          console.error('Error:', error);
          alert('An error occurred');
      }
  });
}

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
  // Navigation
  document.querySelectorAll('.sidebar-nav a').forEach(link => {
      link.addEventListener('click', function(e) {
          e.preventDefault();
          document.querySelectorAll('.sidebar-nav a, .content-section').forEach(el => 
              el.classList.remove('active')
          );
          this.classList.add('active');
          document.querySelector(this.getAttribute('href')).classList.add('active');
      });
  });

  // Profile Dropdown
  const profilePic = document.querySelector('.profile-pic');
  const profileDropdown = document.querySelector('.profile-dropdown');
  if (profilePic && profileDropdown) {
      profilePic.addEventListener('click', (e) => {
          e.stopPropagation();
          profileDropdown.classList.toggle('show');
      });

      document.addEventListener('click', () => profileDropdown.classList.remove('show'));
      document.addEventListener('keydown', (e) => 
          e.key === 'Escape' && profileDropdown.classList.remove('show')
      );
  }

  // Initialize Modals
  initializeModal('modalAddAlumni', 'btnOpenModalAddAlumni');
  initializeModal('modalAddEvent', 'btnOpenModalAddEvent');

  // Form Submissions
  handleFormSubmit('alumniForm', '/add_alumni/', 'Alumni added successfully!');
  handleFormSubmit('eventForm', '/add_event/', 'Event created successfully!');

  // Charts
  new Chart(document.getElementById('alumniGrowthChart').getContext('2d'), {
      type: 'line',
      data: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [{
              label: 'Alumni Growth',
              data: [100, 200, 300, 400, 500, 600],
              borderColor: '#2563eb',
              fill: false
          }]
      },
      options: { responsive: true, scales: { y: { beginAtZero: true } } }
  });

  new Chart(document.getElementById('eventParticipationChart').getContext('2d'), {
      type: 'bar',
      data: {
          labels: ['Event 1', 'Event 2', 'Event 3', 'Event 4', 'Event 5'],
          datasets: [{
              label: 'Participants',
              data: [50, 75, 100, 120, 150],
              backgroundColor: '#f59e0b'
          }]
      },
      options: { responsive: true, scales: { y: { beginAtZero: true } } }
  });
});


//logout
function confirmLogout(event) {
  event.preventDefault(); // Prevent default link behavior

  console.log("Hello");
  if (window.confirm('Are you sure you want to logout?')) {
    // Get the logout URL from the data attribute
    const logoutUrl = event.target.dataset.logoutUrl;
    window.location.href = logoutUrl; // Redirect to the logout URL
  }
}

//add event
document.addEventListener('DOMContentLoaded', function() {

  var modal = document.getElementById("modalAddEvent");
  var btn = document.getElementById("btnOpenModalAddEvent");
  var span = document.getElementsByClassName("close")[0];

  btn.onclick = function() {
      modal.style.display = "block";
  }

  span.onclick = function() {
      modal.style.display = "none";
  }


  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
  }
});

// Admin Management Functions
function showAddAdminModal() {
    const modal = document.getElementById('modalAddAdmin');
    if (modal) {
        modal.style.display = 'block';
    }
}

function showEditAdminModal(admin) {
    const modal = document.getElementById('modalEditAdmin');
    if (modal) {
        // Populate form fields with admin data
        document.getElementById('editAdminId').value = admin.id;
        document.getElementById('editAdminName').value = admin.name;
        document.getElementById('editAdminEmail').value = admin.email;
        
        modal.style.display = 'block';
    }
}

function getAdminDetails(adminId) {
    showLoader();
    
    fetch('/get_admin_details/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: `admin_id=${adminId}`
    })
    .then(response => response.json())
    .then(data => {
        hideLoader();
        if (data.success) {
            showEditAdminModal(data.admin);
        } else {
            alert(data.message || 'Error fetching admin details');
        }
    })
    .catch(error => {
        hideLoader();
        console.error('Error:', error);
        alert('An error occurred while fetching admin details');
    });
}

function confirmDeleteAdmin(adminId) {
    if (confirm('Are you sure you want to delete this admin?')) {
        showLoader();
        
        fetch('/delete_admin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCsrfToken()
            },
            body: `admin_id=${adminId}`
        })
        .then(response => response.json())
        .then(data => {
            hideLoader();
            if (data.success) {
                alert('Admin deleted successfully');
                location.reload(); // Refresh the page to update the admin list
            } else {
                alert(data.message || 'Error deleting admin');
            }
        })
        .catch(error => {
            hideLoader();
            console.error('Error:', error);
            alert('An error occurred while deleting the admin');
        });
    }
}

// Form validation for admin
function validateAdminForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    const name = form.querySelector('input[name="name"]').value.trim();
    const email = form.querySelector('input[name="email"]').value.trim();
    const password = form.querySelector('input[name="password"]').value.trim();

    if (!name) {
        alert('Please enter admin name');
        return false;
    }

    if (!email) {
        alert('Please enter admin email');
        return false;
    }

    if (!validateEmail(email)) {
        alert('Please enter a valid email address');
        return false;
    }

    if (!password && formId === 'formAddAdmin') {
        alert('Please enter admin password');
        return false;
    }

    return true;
}

// Event Listeners for Admin Management
document.addEventListener('DOMContentLoaded', function() {
    // Add Admin Modal
    const btnOpenModalAddAdmin = document.getElementById('btnOpenModalAddAdmin');
    const modalAddAdmin = document.getElementById('modalAddAdmin');
    const btnCloseModalAddAdmin = document.getElementById('btnCloseModalAddAdmin');

    if (btnOpenModalAddAdmin) {
        btnOpenModalAddAdmin.addEventListener('click', showAddAdminModal);
    }

    if (btnCloseModalAddAdmin) {
        btnCloseModalAddAdmin.addEventListener('click', () => {
            modalAddAdmin.style.display = 'none';
        });
    }

    // Add Admin Form Submission
    const formAddAdmin = document.getElementById('formAddAdmin');
    if (formAddAdmin) {
        formAddAdmin.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateAdminForm('formAddAdmin')) {
                const formData = new FormData(this);
                showLoader();

                fetch('/add_admin/', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    hideLoader();
                    if (data.success) {
                        alert('Admin added successfully');
                        modalAddAdmin.style.display = 'none';
                        location.reload();
                    } else {
                        alert(data.message || 'Error adding admin');
                    }
                })
                .catch(error => {
                    hideLoader();
                    console.error('Error:', error);
                    alert('An error occurred while adding the admin');
                });
            }
        });
    }

    // Edit Admin Form Submission
    const formEditAdmin = document.getElementById('formEditAdmin');
    if (formEditAdmin) {
        formEditAdmin.addEventListener('submit', function(e) {
            e.preventDefault();
            if (validateAdminForm('formEditAdmin')) {
                const formData = new FormData(this);
                showLoader();

                fetch('/edit_admin/', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    hideLoader();
                    if (data.success) {
                        alert('Admin updated successfully');
                        document.getElementById('modalEditAdmin').style.display = 'none';
                        location.reload();
                    } else {
                        alert(data.message || 'Error updating admin');
                    }
                })
                .catch(error => {
                    hideLoader();
                    console.error('Error:', error);
                    alert('An error occurred while updating the admin');
                });
            }
        });
    }

    // Close modals when clicking outside
    window.addEventListener('click', function(event) {
        if (event.target === modalAddAdmin) {
            modalAddAdmin.style.display = 'none';
        }
        const modalEditAdmin = document.getElementById('modalEditAdmin');
        if (event.target === modalEditAdmin) {
            modalEditAdmin.style.display = 'none';
        }
    });
});

// Utility Functions
function getCsrfToken() {
    const csrfCookie = document.cookie.split(';')
        .find(cookie => cookie.trim().startsWith('csrftoken='));
    return csrfCookie ? csrfCookie.split('=')[1] : '';
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showLoader() {
    const loader = document.getElementById('loader-overlay');
    if (loader) {
        loader.style.display = 'flex';
    }
}

function hideLoader() {
    const loader = document.getElementById('loader-overlay');
    if (loader) {
        loader.style.display = 'none';
    }
}

  
// Function to confirm delete alumni
function confirmDeleteAlumni(alumniEmail) {
    if (confirm('Are you sure you want to delete this alumni? This action cannot be undone.')) {
      // Optional: show loading
      showLoadingState('alumni');
  
      const formData = new FormData();
      formData.append('alumni_email', alumniEmail);
  
      fetch('{% url "delete_alumni" %}', {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
      })
      .then(response => response.json())
      .then(data => {
        // Show Django response as an alert
        alert(data.message);
  
        // If successful, reload the page
        if (data.success) {
          window.location.reload();
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while deleting the alumni.');
      })
      .finally(() => {
        hideLoadingState('alumni');
      });
    }
  }
  
  // Show loader when page is loading
  window.addEventListener('load', function () {
    const loader = document.getElementById('pageLoader');
    if (loader) {
      loader.style.display = 'none';
    }
  });