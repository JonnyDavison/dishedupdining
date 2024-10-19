// Check for stored consent immediately
const storedConsent = localStorage.getItem('cookieConsent');
let consentApplied = false;

if (storedConsent) {
    console.log('Stored consent found:', storedConsent);
    const consent = JSON.parse(storedConsent);
    applyConsentPreferences(consent);
    consentApplied = true;
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

document.addEventListener('DOMContentLoaded', function() {
    // Rest of your code...
});

document.addEventListener('DOMContentLoaded', function() {
    const cookieBanner = document.getElementById('cookie-banner');
    const cookieSettings = document.getElementById('cookie-settings');
    const acceptAllBtn = document.getElementById('accept-all');
    const rejectAllBtn = document.getElementById('reject-all');
    const customizeBtn = document.getElementById('customize');
    const savePreferencesBtn = document.getElementById('save-preferences');

    function showCookieBanner() {
        if (!consentApplied) {
            console.log('Showing cookie banner');
            cookieBanner.classList.remove('hidden');
        } else {
            console.log('Consent already applied, not showing banner');
        }
    }

    function hideCookieBanner() {
        console.log('Hiding cookie banner');
        cookieBanner.classList.add('hidden');
    }

    function showCookieSettings() {
        console.log('Showing cookie settings');
        cookieSettings.classList.remove('hidden');
        cookieBanner.classList.add('hidden'); 
    }

    function hideCookieSettings() {
        console.log('Hiding cookie settings');
        cookieSettings.classList.add('hidden');
    }

    function setConsent(analytics, marketing, preferences) {
        console.log('Setting consent:', { analytics, marketing, preferences });
        hideCookieBanner(); // Hide banner immediately
        fetch('/cookies/set-cookie-consent/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `analytics=${analytics}&marketing=${marketing}&preferences=${preferences}`
        }).then(response => response.json())
          .then(data => {
              console.log('Server response:', data);
              if (data.status === 'success') {
                  hideCookieSettings();
                  localStorage.setItem('cookieConsent', JSON.stringify({analytics, marketing, preferences}));
                  applyConsentPreferences({analytics, marketing, preferences});
                  consentApplied = true;
              } else {
                  console.error('Consent setting failed:', data);
                  showCookieBanner(); // Show banner again if setting consent failed
              }
          })
          .catch(error => {
              console.error('Error:', error);
              showCookieBanner(); // Show banner again if there was an error
          });
    }

    // ... (rest of your functions remain the same)

    acceptAllBtn.addEventListener('click', () => {
        setConsent(true, true, true);
    });

    rejectAllBtn.addEventListener('click', () => {
        setConsent(false, false, false);
    });

    customizeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        showCookieSettings();
    });

    savePreferencesBtn.addEventListener('click', (e) => {
        e.preventDefault();
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

    window.showCookieSettings = showCookieSettings;

    // Only show the banner if consent hasn't been applied
    if (!consentApplied) {
        showCookieBanner();
    }
});

function applyConsentPreferences(consent) {
    console.log('Applying consent preferences:', consent);
    if (consent.analytics) {
        loadGoogleAnalytics();
    }
    // Add similar checks for other non-essential scripts
    if (consent.marketing) {
        loadMarketingScripts();
    }
    // You can add more conditions here for other types of cookies
}

function loadGoogleAnalytics() {
    console.log('Loading Google Analytics');
    // ... (rest of the function remains the same)
}

function loadMarketingScripts() {
    console.log('Loading marketing scripts');
    // ... (implement this function if needed)
}