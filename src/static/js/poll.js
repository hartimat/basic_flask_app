/* Name: Matthew Hartigan
Assignment: CS336 Assignment #9
Page Name: poll.js
Created: 4/30/2019
Description: The poll.js page for Assignment #9.*/


// Helper fuction that returns array element whose key matches the input
// parameter 'value'
function getByValue(array, value) {
  console.log("getByValue");
  console.log("Array is: ");
  console.log(array);

  for (let i = 0; i < array.length; i++) {
    if (array[i].key == value) {
      console.log("Found a match");
      return array[i];
    }
    else {
      console.log("No match found");
    }
  }
}


// Function that takes current cookie string as input, returns an array
// of objects that each hold key value pairs
function parseCookie(currentCookie) {
  console.log("parseCookie");
  var name = "";
  var value = "";
  var parsedArray = [];
  var splitCookie = currentCookie.split("; ");

  //Turn input cookie into an array of objects that hold key value pairs
  for (let j = 0; j < splitCookie.length; j++) {
    var nameValue = splitCookie[j].split("=");
    parsedArray.push({key: nameValue[0], value: nameValue[1]});
    console.log("name = " + nameValue[0] + " and value = " + nameValue[1]);
  }

  return parsedArray;
}


// Function that takes an input array of key value pairs, extracts the values
// and uses them as keys which get initialized to zero and appended onto the
// document cookie string.  Returns document cookie
function makeCookies(cookieArray) {
  console.log("makeCookies");
  var name = "";

  for (let i = 0; i < cookieArray.length; i++) {
    name = cookieArray[i].getAttribute('value');
    console.log("Writing a cookie named: " + name);
    document.cookie = name + "=0;";
  }

  return document.cookie;
}


// Function that saves an input array of key value pairs to the document
// cookie.  Returns the document cookie.
function saveCookies(cookieArray) {
  console.log("saveCookies");

  var name = "";
  var value = "";

  for (let i = 0; i < cookieArray.length; i++) {
    name = cookieArray[i].key;
    value = cookieArray[i].value;
    document.cookie = name + "=" + value;
  }

  return document.cookie;
}


// Function that takes the current cookie, calls a function to parse its
// contents, calls a function to sort the parsed contents, and finally
// saves the parsed, sorted values as the textContent of the input
// array of poll totals from the html page
function setCookies(totalsArray, currentCookie) {
  console.log("setCookies");

  var parsedArray = parseCookie(currentCookie);
  console.log(parsedArray);

  var sortedArray = [];

  sortedArray.push(getByValue(parsedArray, "Mountain Biking"));
  sortedArray.push(getByValue(parsedArray, "Road Biking"));
  sortedArray.push(getByValue(parsedArray, "Leisure Biking"));

  console.log("Newly sorted array");
  console.log(sortedArray);

  for (let i = 0; i < totalsArray.length; i++) {
    totalsArray[i].textContent = 'Total votes: ' + sortedArray[i].value;
  }
}


// Function that checks to see if a cookie already exists.  If not, it calls a
// function to make (i.e. intialize) a cookie.  It then calls a function to
// add the cookie values to the html page
function getCookies() {
  console.log("getCookie");

  //See what's in the oven
  var currentCookie = document.cookie;
  var cookieArray = document.getElementsByClassName("nominee");
  var totalsArray = document.getElementsByClassName("totals");

  //If you don't find any cookies, bake some
  if (! currentCookie) {
    currentCookie = makeCookies(cookieArray);
  }

  //Add the current cookie values to the page
  setCookies(totalsArray, currentCookie);
}


// Function that is initially called on form submission to update the tally for
// each nominee on the page.
function updateCookies() {
  console.log('updateCookies');
  var vote = document.querySelector('input[name="nominee"]:checked').value;

  // Get current cookie and parse it
  let currentCookie = document.cookie;
  let parsedArray = parseCookie(currentCookie);

  // Upate cookie vote totals based on user input
  for (let i = 0; i < parsedArray.length; i++) {
    if (parsedArray[i].key == vote) {
      let newTotal = (Number(parsedArray[i].value) + 1);
      parsedArray[i].value = "" + newTotal;
    }
  }

  // Save updated cookie
  let newCookie = saveCookies(parsedArray);
  let totalsArray = document.getElementsByClassName("totals");

  setCookies(totalsArray, newCookie);

  // Notify user of update
  alert('Thanks for selecting: ' + vote);
}


// MAIN
// Initialize cookies on page load
document.addEventListener('onload', getCookies(), false);
