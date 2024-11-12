// Common utility functions
export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export function getCSRFToken() {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
  return csrfToken;
}

// API utilities
const defaultOptions = {
  headers: {
    "X-CSRFToken": getCSRFToken(),
    Accept: "application/json",
    "Content-Type": "application/json",
  },
  credentials: "same-origin",
};

export async function getAPI(url) {
  const options = {
    ...defaultOptions,
    method: "GET",
  };

  try {
    const response = await fetch(url, options);
    if (response.redirected) {
      window.location.href = response.url;
      return;
    }
    console.log(response.ok);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("GET API Error:", error);
    throw error;
  }
}

export async function postAPI(url, data) {
  const options = {
    ...defaultOptions,
    method: "POST",
    body: JSON.stringify(data),
  };

  try {
    const response = await fetch(url, options);
    if (response.redirected) {
      window.location.href = response.url;
      return;
    }
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("POST API Error:", error);
    throw error;
  }
}

export async function deleteAPI(url) {
  const options = {
    method: "DELETE",
    headers: {
      "X-CSRFToken": getCSRFToken(),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  };

  try {
    const response = await fetch(url, options);
    if (response.redirected) {
      window.location.href = response.url;
      return;
    }
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return await response.json();
  } catch (error) {
    console.error("DELETE API Error:", error);
    throw error;
  }
}

// Form handling utilities
export function setupAPIForm(form) {
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    try {
      const formData = new FormData(this);
      const data = Object.fromEntries(formData);
      const response = await postAPI(this.action, data);

      if (response.redirect) {
        window.location.href = response.redirect;
      }
    } catch (error) {
      console.error("Form submission error:", error);
    }
  });
}
