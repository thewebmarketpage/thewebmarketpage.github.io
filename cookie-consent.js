(function () {
    // Check if localStorage is supported
    if (typeof Storage === "undefined") {
        console.error("LocalStorage is not supported in this browser.");
        return;
    }

    // Cookie Consent Popup Styles
    const styles = `
        .cookie-consent-popup {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            max-width: 350px;
            z-index: 1000;
            display: none;
            font-family: 'Poppins', sans-serif;
        }

        .cookie-consent-popup.show {
            display: block;
        }

        .cookie-consent-popup img {
            width: 40px;
            height: 40px;
            margin-bottom: 10px;
        }

        .cookie-consent-popup h3 {
            font-size: 18px;
            font-weight: bold;
            color: #05325e;
            margin-bottom: 10px;
        }

        .cookie-consent-popup p {
            font-size: 14px;
            color: #555;
            margin-bottom: 15px;
        }

        .cookie-consent-popup a {
            color: #05325e;
            text-decoration: underline;
        }

        .cookie-consent-popup .buttons {
            display: flex;
            gap: 10px;
        }

        .cookie-consent-popup button {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s;
        }

        .cookie-consent-popup button.accept {
            background-color: #05325e;
            color: white;
        }

        .cookie-consent-popup button.decline {
            background-color: #f8f9fa;
            color: #05325e;
            border: 1px solid #05325e;
        }

        .cookie-consent-popup button.accept:hover {
            background-color: #04284e;
        }

        .cookie-consent-popup button.decline:hover {
            background-color: #e9ecef;
        }
    `;

    // Add styles to the document
    const styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = styles;
    document.head.appendChild(styleSheet);

    // Create the cookie consent popup HTML
    const popupHTML = `
        <div class="cookie-consent-popup" id="cookieConsentPopup">
            <img src="https://raw.githubusercontent.com/thewebmarketpage/thewebmarketpage.github.io/refs/heads/root/websites-explorer/websites-explorer-logo1.png" alt="Websites Explorer Logo">
            <h3>We Value Your Privacy</h3>
            <p>
                We use cookies to enhance your browsing experience, analyze site traffic, and personalize content. By clicking "Accept," you consent to our use of cookies. 
                <a href="https://giantwebmarket.com/privacy-policy.html" target="_blank">Learn more</a>.
            </p>
            <div class="buttons">
                <button class="accept" id="acceptCookies">Accept</button>
                <button class="decline" id="declineCookies">Decline</button>
            </div>
        </div>
    `;

    // Add the popup to the document
    const popupContainer = document.createElement("div");
    popupContainer.innerHTML = popupHTML;
    document.body.appendChild(popupContainer);

    // Function to show the cookie consent popup
    function showCookieConsentPopup() {
        const hasConsent = localStorage.getItem("cookieConsent");
        if (!hasConsent) {
            const popup = document.getElementById("cookieConsentPopup");
            popup.classList.add("show");
        }
    }

    // Function to handle "Accept" button click
    function acceptCookies() {
        localStorage.setItem("cookieConsent", "accepted");
        hideCookieConsentPopup();
    }

    // Function to handle "Decline" button click
    function declineCookies() {
        localStorage.setItem("cookieConsent", "declined");
        hideCookieConsentPopup();
    }

    // Function to hide the cookie consent popup
    function hideCookieConsentPopup() {
        const popup = document.getElementById("cookieConsentPopup");
        popup.classList.remove("show");
    }

    // Attach event listeners to buttons
    document.addEventListener("DOMContentLoaded", function () {
        const acceptButton = document.getElementById("acceptCookies");
        const declineButton = document.getElementById("declineCookies");

        if (acceptButton && declineButton) {
            acceptButton.addEventListener("click", acceptCookies);
            declineButton.addEventListener("click", declineCookies);
        }

        // Show the popup if no consent has been given
        showCookieConsentPopup();
    });
})();
