document.addEventListener('DOMContentLoaded', function() {
    const cookieBanner = document.getElementById('cookie-banner');
    const cookieSettings = document.getElementById('cookie-settings');
    const acceptAllBtn = document.getElementById('accept-all');
    const rejectAllBtn = document.getElementById('reject-all');
    const customizeBtn = document.getElementById('customize');
    const savePreferencesBtn = document.getElementById('save-preferences');

    function showCookieBanner() {
        cookieBanner.classList.remove('hidden');
    }

    function hideCookieBanner() {
        cookieBanner.classList.add('hidden');
    }

    function showCookieSettings() {
        cookieSettings.classList.remove('hidden');
        cookieBanner.classList.add('hidden'); 
    }

    function hideCookieSettings() {
        cookieSettings.classList.add('hidden');
        showCookieBanner();
    }

    function setConsent(analytics, marketing, preferences) {
        fetch('/cookies/set-cookie-consent/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `analytics=${analytics}&marketing=${marketing}&preferences=${preferences}`
        }).then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  hideCookieBanner();
                  hideCookieSettings();
                  // Store the user's choice in localStorage
                  localStorage.setItem('cookieConsent', JSON.stringify({analytics, marketing, preferences}));
              }
          })
          .catch(error => {
              console.error('Error:', error);
          });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    acceptAllBtn.addEventListener('click', () => {
        setConsent(true, true, true);
    });

    rejectAllBtn.addEventListener('click', () => {
        setConsent(false, false, false);
    });

    customizeBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent any default action
        showCookieSettings();
    });

    savePreferencesBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent any default action
        const analytics = document.getElementById('analytics-consent').checked;
        const marketing = document.getElementById('marketing-consent').checked;
        const preferences = document.getElementById('preferences-consent').checked;
        setConsent(analytics, marketing, preferences);
    });

    cookieSettings.addEventListener('click', (e) => {
        if (e.target === cookieSettings) {
            hideCookieSettings();
        }
    });

    // Check if user has already made a choice
    const storedConsent = localStorage.getItem('cookieConsent');
    if (!storedConsent) {
        showCookieBanner();
    } else {
        // User has already made a choice, apply their preferences
        const { analytics, marketing, preferences } = JSON.parse(storedConsent);
        setConsent(analytics, marketing, preferences);
    }
});