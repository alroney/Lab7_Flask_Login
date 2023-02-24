//Declared for easier usage.
const usernameElement = document.getElementById("account-user");
const linkElement = document.getElementById("log-link");

function setUsernameText(name, uElement, lElement, logoutLink, loginLink) {
    if(name != "" || name != null) {
        uElement.innerHTML = "Welcome, "+ name;

        lElement.setAttribute("href", logoutLink);//Set the link
        lElement.innerHTML = "Logout";
        
    }

    if (name == "" || name == null) {
        uElement.innerHTML = "Not logged in";

        lElement.setAttribute("href", loginLink);//Set the link
        lElement.innerHTML = "Login";
        
    }
}

setUsernameText(username, usernameElement, linkElement, logoutLink, loginLink);
//username, logoutLink and loginLink are declared in the HTML files where it can grab the Python data.