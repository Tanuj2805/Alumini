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