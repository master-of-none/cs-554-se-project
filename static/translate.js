const languageDropdown = document.getElementById("language");
const translateButton = document.getElementById("translateButton");
const detectedLanguage = document.getElementById("detectedLanguage").value;
const extractedText = document.getElementById("extractedText").value;
let languageCodes;

async function fetchData() {
  try {
    const response = await fetch("/static/language_codes.json");
    if (!response.ok) {
      throw new Error("Failed to fetch language codes");
    }
    languageCodes = await response.json();
    populateDropdown();
  } catch (error) {
    console.error("Error fetching language codes:", error);
  }
}

fetchData();

function populateDropdown() {
  for (const [language, code] of Object.entries(languageCodes)) {
    if (language !== detectedLanguage) {
      const option = document.createElement("option");
      option.value = code;
      option.textContent = language;
      languageDropdown.appendChild(option);
    }
  }
};

translateButton.addEventListener("click", () => {
  const selectedLanguageCode = languageDropdown.value;
  if (selectedLanguageCode) {
    fetch("/translate", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `extracted_text=${extractedText}&target_language=${selectedLanguageCode}`,
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("translatedText").innerHTML =
          data.translated_text;
      })
      .catch((error) => console.error("Error:", error));
  }
});
