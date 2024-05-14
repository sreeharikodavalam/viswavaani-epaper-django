// Fullscreen loaders
function showFullLoader() {
  $(".loading").fadeIn();
}

function hideFullLoader() {
  $(".loading").fadeOut();
}

$(document).ready(function () {
  hideFullLoader();
});

// CSRF
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
// sourcery skip: use-braces
  if (parts.length === 2) return parts.pop().split(";").shift();
}

// Axios
function postFormData(
  url,
  formData,
  callback,
  showLoader = true,
  showToast = false
) {
  if (showLoader) {
    showFullLoader();
  }
  const csrftoken = getCookie("csrftoken");

  axios
    .post(url, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "X-CSRFToken": csrftoken,
      },
    })
    .then((response) =>
      handleResponse(response, callback, showLoader, showToast)
    )
    .catch((error) => handleAxiosError(error, callback, showLoader, showToast));
}
function jsonToFormData(json) {
  return Object.keys(json)
    .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(json[key]))
    .join('&');
}
function postJsonDataAsFormData(
  url,
  jsonData,
  callback,
  showLoader = true,
  showToast = false
) {
  if (showLoader) {
    showFullLoader();
  }
  const csrftoken = getCookie("csrftoken");
  const formDataString = jsonToFormData(jsonData);

  axios
    .post(url, formDataString, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        "X-CSRFToken": csrftoken,
      },
    })
    .then((response) =>
      handleResponse(response, callback, showLoader, showToast)
    )
    .catch((error) => handleAxiosError(error, callback, showLoader, showToast));
}

function postJsonData(
  url,
  jsonData,
  callback,
  showLoader = true,
  showToast = false
) {
  if (showLoader) {
    showFullLoader();
  }
  const csrftoken = getCookie("csrftoken");

  axios
    .post(url, jsonData, {
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": csrftoken,
      },
    })
    .then((response) =>
      handleResponse(response, callback, showLoader, showToast)
    )
    .catch((error) => handleAxiosError(error, callback, showLoader, showToast));
}

function handleResponse(response, callback, showLoader, showToast = false) {
  if (showLoader) {
    hideFullLoader(); // Hide loader if shown
  }
  if (response.status >= 200 && response.status < 300) {
    console.log(response.data);
    callback(response.status, response.data);
    if (showToast === true) {
      if (response.data.result === true) {
        $.niceToast.success(
          "<strong>Success</strong>: " + response.data.message
        );
      } else {
        $.niceToast.error("<strong>Error</strong>: " + response.data.message);
      }
    }
  } else {
    const error = new Error(response.statusText);
    error.response = response.data;
    throw error; // Force throw
  }
}

function handleAxiosError(error, callback, showLoader, showToast = false) {
  console.error("Axios error:", error);
  if (showLoader) {
    hideFullLoader(); // Hide loader if shown
  }
  callback(0, { result: false, message: "Failed to connect to the server." });
  if (showToast === true) {
    $.niceToast.error(
      "<strong>Error</strong>: Failed to connect to the server."
    );
  }
}

function serializeFormData(form) {
  const formData = {};
  $(form)
    .serializeArray()
    .forEach((item) => {
      formData[item.name] = item.value;
    });
  return formData;
}


//Alerts
// Function to show success alert
function showSuccessAlert(title, message) {
  Swal.fire({
    icon: 'success',
    title: title,
    text: message,
    confirmButtonColor: '#3085d6',
    confirmButtonText: 'OK'
  });
}

// Function to show error alert
function showErrorAlert(title, message) {
  Swal.fire({
    icon: 'error',
    title: title,
    text: message,
    confirmButtonColor: '#d33',
    confirmButtonText: 'OK'
  });
}

// Function to show warning alert
function showWarningAlert(title, message) {
  Swal.fire({
    icon: 'warning',
    title: title,
    text: message,
    confirmButtonColor: '#ffc107',
    confirmButtonText: 'OK'
  });
}

// Function to show confirmation alert
function showConfirmationAlert(title, message, callback) {
  Swal.fire({
    icon: 'question',
    title: title,
    text: message,
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Yes',
    cancelButtonText: 'No'
  }).then((result) => {
    if (result.isConfirmed) {
      callback();
    }
  });
}
