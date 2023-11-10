const { JSDOM } = require('jsdom');
const fs = require('fs');
const filePath = 'templates/result.html'
const htmlContent = fs.readFileSync(filePath, 'utf-8');

describe('Text Detection Results Script', () => {
  let window;
  let document;
  let languageDropdown;
  const allLanguages = [
    "English",
    "Chinese",
    "Spanish",
    "French",
    "German",
  ];
  const detectedLanguage = "{{ detectedLanguage }}";

  beforeAll(() => {
    const { window } = new JSDOM(htmlContent);
    document = window.document;

    languageDropdown = document.getElementById("language");
  });

  it('Should populate language dropdown with options', () => {
    const options = languageDropdown.querySelectorAll('option');

    const expectedLanguages = ["English", "Chinese", "Spanish", "French", "German"];
    options.forEach((option, index) => {
      expect(option.textContent).toBe(expectedLanguages[index]);
    });
  });

  it('Should not include detected language in the dropdown', () => {
    const options = languageDropdown.querySelectorAll('option');

    options.forEach((option) => {
      expect(option.value).not.toBe(detectedLanguage);
    });
  });

});