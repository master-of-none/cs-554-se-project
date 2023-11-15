  function displayFileName() {
        const fileInput = document.getElementById('file');
        const fileNameDisplay = document.getElementById('selectedFileName');
        fileNameDisplay.textContent = fileInput.files[0].name;
}
function animateHeading() {
        const heading = document.getElementById('uploadHeading');
        const text = heading.textContent;
        heading.textContent = '';

        function addLetters(index) {
          setTimeout(function() {
            heading.textContent += text[index];
            if (index < text.length - 1) {
              addLetters(index + 1);
            } else {
              setTimeout(function() {
                heading.textContent = '';
                setTimeout(function() {
                  addLetters(0);
                }, 500);
              }, 1000);
            }
          }, 100);
        }

        addLetters(0);
      }
      window.onload = animateHeading;
