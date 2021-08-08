/* Name: Matthew Hartigan
Assignment: CS336 Assignment #9
Page Name: registration.js
Created: 4/30/2019
Description: The registration.js page for Assignment #9.*/

///////////////////////////////////////////////////////////////////
// ASSIGNMENT 5A //

// Function to close popup window
function closeWindow() {
//   window.close();
}


// Function to generate error popup for invalid input
function displayErrors(errors, browserHeight, browserWidth) {

  let popupHeight = 400;
  let popupWidth = 500;
  let left = (browserWidth / 2) - (popupWidth / 2);
  let top = (browserHeight / 2) - (popupHeight / 2);
  let windowFeatures = 'height = 400, width = 500, menubar = no, minimizable = no, ' +
    'toolbar = no, location = no, status = yes, fullscreen = no, resizable = no, titlebar = no, top=' + top + ',left=' + left;

  //Create popup window
  var popup = window.open("invalid.html", "", windowFeatures);

  // Update status message
  popup.status = "Status: Displaying invalid input message to user.";

  //Workaround for issue with page load timing
  popup.document.write('<body style="background-color:lightblue" id="invalid-body" class="invalid">');
  popup.document.write('<h3 id="headline">Invalid Input from User...</h3>');

  for (let j = 0; j < errors.length; j++) {
    popup.document.write('<p>' + errors[j] + '</p><br><br>');
  }
}


// Function for validation of workshop selections
function validateWorkshopSelections() {
  var session_1_elements = document.getElementsByName("session_1");
  var session_2_elements = document.getElementsByName("session_2");
  var session_3_elements = document.getElementsByName("session_3");
  var errors = [];
  var status = true;

  // Validate input
  // Case 1: Session 1b covers Sessions 1 & 2
  if (session_1_elements[1].checked) {
    for (let i = 0; i < session_2_elements.length; i++) {
      if (session_2_elements[i].checked) {
        errors.push("Invalid input.  Session 1b covers Sessions 1 & 2. " +
          "Therefore, no additional Session 2 workshop can be selected.");
        status = false;
      }
    }
    if (session_3_elements[1].checked) {
      errors.push("Invalid input.  Session 1b covers Sessions 1 & 2. " +
        "Session 3b can only be selected if Session 2c is selected. " +
        "Since no additional Session 2 workshop can be selected, the Session 3b selection is also invalid.");
      status = false;
    }
  }

  // Case 2: Session 2c requires Session 3b
  if ((!session_1_elements[1].checked) && (session_2_elements[2].checked)) {
    if (!session_3_elements[1].checked) {
      errors.push("Invalid input.  Session 3b must be selected if Session 2c is selected.");
      status = false;
    }
  }

  // Case 3: Session 3b requires Session 2c
  if ((!session_1_elements[1].checked) && (session_3_elements[1].checked)) {
    if (!session_2_elements[2].checked) {
      errors.push("Invalid input.  Session 2c must be selected if Session 3b is selected.");
      status = false;
    }
  }

  // Alert reader of errors if applicable
  if (errors) {
    displayErrors(errors, window.innerHeight, window.innerWidth);
    return status;
  }
}
//////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////
// ASSIGNMENT 5B //


// Function that takes an input array of cookie values and places them back into
// the corresponding html page based on the names of each form value
function autofillCookie(cookieArray) {
  console.log("autofillCookie");

  let nameArray = [];
  let valueArray = [];
  let nameSearch = "";

  for (let j = 0; j < cookieArray.length; j++) {
    let splitCookie = cookieArray[j].split(":");
    nameArray.push(splitCookie[0]);
    valueArray.push(splitCookie[1]);
  }

  console.log(nameArray);
  console.log(valueArray);

  // Insert cookie values into the input fields
  for (let i = 0; i < nameArray.length; i++) {
   if (nameArray[i]) {
     nameSearch = 'input[name="' + nameArray[i] + '"]';

     let replacement = document.querySelector(nameSearch);
     replacement.value = valueArray[i];
   }
  }
}


// Function that searches the page's cookies for one that matches the input
// cookie name.  Returns an array of that cookie's values if a match is found.
function readCookie(conferenceID) {
  console.log("readCookie");
  console.log("Full document.cookie: " + document.cookie);

  var allCookies = document.cookie.split(";");
  let name = "";

  console.log("All document cookies separated: " + allCookies);

  for (let i = 0; i < allCookies.length; i++) {
    var individualCookie = allCookies[i].split("=");
    console.log(individualCookie);
    if(conferenceID == individualCookie[0].trim()) {
      var individualCookieValues = individualCookie[1].split("|");
      console.log("Individual cookie values after split: ");
      console.log(individualCookieValues);
      autofillCookie(individualCookieValues);
    }
  }


  // for (let i = 0; i < splitCookie.length; i++) {
  //   name = splitCookie[i].split("|");
  //   console.log(name);
  //
  //   if (name[0].trim() == cookieName) {
  //     console.log("The cookie: " + name[0] + " was matched!");
  //     autofillCookie(splitCookie[i]);
  //   }
  //   else {
  //     console.log("No match");
  //   }
  // }
}


// Function that is called when event listener for an input conference ID is triggered
function getCookie() {
  console.log("getCookie");

  // Get the input conference ID number
  let conferenceID = document.querySelector('input[name=conference_id]');

  // Check to see if it matches an existing cookie
  if (conferenceID) {
    readCookie(conferenceID.value);
  }
}


// Function that is called on form submission.  Checks to see if the
// conference ID exists.  If one does not, it calls a function to create
// a new cookie
function updateCookies(formInput) {
  console.log("updateCookies");
  let name = "";
  let value = "";
  let cookieString = "";
  let cookieName = ";";


  for (let i = 1; i < formInput.length; i++) {
    name = formInput[i].name;
    value = formInput[i].value;
    cookieString = cookieString + name + ":" + value + "|";
  }

  console.log("cookieString is: " + cookieString);

  if (! formInput[0].value) {
    cookieName = "123456";
  }
  else {
    cookieName = formInput[0].value.trim();
  }

  document.cookie = cookieName + "=" + cookieString;
}



