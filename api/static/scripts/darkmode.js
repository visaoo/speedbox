const toggleDarkmode = document.querySelector("#darkmode");
const sunIcon = document.querySelector("#sunIcon");
const moonIcon = document.querySelector("#moonIcon");
const root = document.querySelector(":root");

function applyLightMode() {
  moonIcon.classList.remove("hidden");
  sunIcon.classList.add("hidden");

  root.style.setProperty("--bg-color", " #FFFFFF");
  root.style.setProperty("--secundary-bg", " #EBEEF1");
  root.style.setProperty("--primary-color", " #2563EB");
  root.style.setProperty("--font-color", " #000000");
  root.style.setProperty("--secundary-font-color", " #FFFFFF");
  root.style.setProperty("--third-font-color", " #a09a9a");
  root.style.setProperty("--border-color", " #A09A9A8A");

  localStorage.setItem("theme", "light");
}

function applyDarkMode() {
  moonIcon.classList.add("hidden");
  sunIcon.classList.remove("hidden");

  root.style.setProperty("--bg-color", " #1A1A1D");
  root.style.setProperty("--secundary-bg", " #3B1C32");
  root.style.setProperty("--primary-color", " #6A1E55");
  root.style.setProperty("--font-color", " #6A1E55");
  root.style.setProperty("--secundary-font-color", " #1A1A1D");
  root.style.setProperty("--third-font-color", " #FFFFFF");
  root.style.setProperty("--border-color", " #6A1E55");

  localStorage.setItem("theme", "dark");
}

window.onload = () => {
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "light") {
    applyLightMode();
  } else {
    applyDarkMode();
  }
};

toggleDarkmode.onclick = () => {
  const isDarkmode = moonIcon.classList.contains("hidden");

  if (isDarkmode) {
    applyLightMode();
  } else {
    applyDarkMode();
  }
};
