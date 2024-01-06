


// ----------------------------------------------------------------------------------


// profile image input scripts
var loadFile = function (event) {
   var image = document.getElementById("output");
   image.src = URL.createObjectURL(event.target.files[0]);
 };
 

// Get the scroll position from the URL query parameter
const urlParams = new URLSearchParams(window.location.search);
const scrollPosition = urlParams.get('scroll_position') || 0;

// Scroll to the saved position after the page loads
window.onload = () => {
    window.scrollTo(0, scrollPosition);
};


// to show the section of copy, edit, delete, otc for a post

// Get all posts
const posts = document.querySelectorAll('.post');

// Loop through each post
posts.forEach(post => {
    // Add click event listener to the overflow-hidden section of each post
    const overflowHidden = post.querySelector('.overflow-hidden');
    overflowHidden.addEventListener('click', function(event) {
        // Show or hide the corresponding navbar for this post
        const navbar = post.querySelector('.navbar_2');
        if (navbar.style.display === 'block') {
            navbar.style.display = 'none'; // Hide the navbar if it's currently visible
        } else {
            navbar.style.display = 'block'; // Show the navbar if it's currently hidden
        }
    });
});


// read-more script 


  function toggleContent(button) {
    var content = button.previousElementSibling;

    if (content.style.overflow === "hidden") {
      content.style.overflow = "visible";
      content.style.maxHeight = "none";
      button.innerText = "Read Less";
    } else {
      content.style.overflow = "hidden";
      content.style.maxHeight = "195px"; // Adjust this value to match initial height
      button.innerText = "Read More";
    }
  }

  document.addEventListener("DOMContentLoaded", function() {
    var contentDivs = document.querySelectorAll(".content");
    
    contentDivs.forEach(function(contentDiv) {
      var words = contentDiv.textContent.trim().split(/\s+/).length;
      var button = contentDiv.nextElementSibling;
      
      if (words > 35) {
        contentDiv.style.overflow = "hidden";
        contentDiv.style.maxHeight = "175px"; // Adjust this value to match initial height
        button.style.display = "inline-block";
      } else {
        button.style.display = "none";
      }
    });
  });


    // JavaScript to show toast on click for each post without scrolling to top
    var scrollLinks = document.querySelectorAll('.scrollLink');

    scrollLinks.forEach(function(link) {
        link.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent the default behavior of the anchor link
            var infoToast = new bootstrap.Toast(document.getElementById('infoToast'));
            infoToast.show();
        });
    });



// -------------------------------------------------------------------------------------



// JavaScript code to handle notification click
self.addEventListener('notificationclick', function (event) {
  event.notification.close();
  const postData = event.notification.data.post_id;
  // Redirect to the post page using the post_id
  window.location.href = '/post/' + postData;
});



// JavaScript to toggle the rotation class
function toggleRotation() {
  document.body.classList.toggle("rotate");
}

// JavaScript to toggle interaction
function toggleInteraction() {
  document.body.classList.toggle("enable-interaction");
}
