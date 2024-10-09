// static/js/cookies.js

document.addEventListener('DOMContentLoaded', function () {
    const acceptButton = document.getElementById('accept-cookies');
    const declineButton = document.getElementById('decline-cookies');
    const banner = document.getElementById('cookie-consent-banner');
    const manageCookiesLink = document.getElementById('manage-cookies');

    if (acceptButton) {
        acceptButton.addEventListener('click', function () {
            setCookiePreferences({ essential: true, analytics: true });
            banner.style.display = 'none';
        });
    }

    if (declineButton) {
        declineButton.addEventListener('click', function () {
            setCookiePreferences({ essential: true, analytics: false });
            banner.style.display = 'none';
        });
    }

    if (manageCookiesLink) {
        manageCookiesLink.addEventListener('click', function (e) {
            e.preventDefault();
            // Show the cookie banner again
            banner.style.display = 'block';
        });
    }

    function setCookiePreferences(preferences) {
        fetch('/set_cookie_preferences', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                // Include CSRF token if you have CSRF protection enabled
                // 'X-CSRFToken': getCookie('csrf_token')
            },
            body: JSON.stringify({ preferences: preferences })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Preferences saved:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Function to get a cookie value by name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                // Does this cookie string begin with the name we want?
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
