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





// firebase scripts for cloud messaging

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";

const firebaseConfig = {
  apiKey: "AIzaSyDkyNO4aWT4qVCVJwkcb354_Rtc-TdFybk",
  authDomain: "fknpj-9c7bb.firebaseapp.com",
  projectId: "fknpj-9c7bb",
  storageBucket: "fknpj-9c7bb.appspot.com",
  messagingSenderId: "624374608791",
  appId: "1:624374608791:web:143bdac26d9762dcbb0ad2",
  measurementId: "G-93ZXLVMBCF"
};


const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);


// First, we need to link the service worker.
navigator.serviceWorker
.register('./serviceworker.js') 
.then(function(register) {
messaging.useServiceWorker(register);

// Request permission from the user to receive notifications
messaging.requestPermission()
.then(function() {
  console.log("The user has accepted to receive notifications.");
  return messaging.getToken();
})
.then(function(token){
  console.log(token);

//we will send the token to django to save it in the database
fetch('save-token/', {
  method: 'post',
  headers: {
    'Content-Type': 'application/json',    
    'Accept': 'application/json'
  },
  body: JSON.stringify({
    'token': token
  })
})
  
.then(function(response) {
  if (response.ok) {
      console.log("Token has been saved");
  } else {
      console.log("Failed to save token. Status: " + response.status);
  }
})

.catch(function(e){
  console.log("token could not be saved") 
  })

})
.catch(function(e) {
  console.log("The user has not accepted.");
});
});
