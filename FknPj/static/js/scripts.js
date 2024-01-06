


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
