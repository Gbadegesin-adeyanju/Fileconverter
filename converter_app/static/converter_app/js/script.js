const fileLabel = document.querySelector(".file-upload"); 
const fileNameDisplay = document.getElementById("fileName");
const fileInput = document.getElementById("file-upload");
const fileInputs = document.querySelectorAll(".file-input");
const imgTxt = document.querySelector(".img-txt");
const audioTxt = document.querySelector(".audio-txt");
const convert = document.querySelectorAll("#convertNow");
const imgTxtBtn = document.querySelector('.img-txt-btn');
const audioTxtBtn = document.querySelector('.audio-txt-btn');
const imgTxtCon = document.querySelector('.img-txt-container');
const audioTxtCon = document.querySelector('.audio-txt-container');
const imgSpinner = document.querySelector('#img-spinner');
const audioSpinner = document.querySelector('#audio-spinner');

fileInputs.forEach(input => {
    input.addEventListener('change', function() {
        const label = document.querySelector(`label[for="${this.id}"]`);
        let selectedFile = this.files[0].name;
        if(selectedFile.length > 12) {
            const dotIndex = selectedFile.lastIndexOf('.'); 
            const extension = dotIndex !== -1 ? selectedFile.slice(dotIndex) : ''; 
            selectedFile = selectedFile.slice(0, 10) + "..." + extension;
        }
        const fileName = this.files[0] ? selectedFile : 'No file chosen';
        if (label) {
            label.textContent = fileName; 
        }
    });
});

const subscribe = document.querySelector(".footer-btn");

subscribe.addEventListener('click', function(event) {
    event.preventDefault();
    const form = this.closest("form");
    if (form) {
        console.log(form);
        submitemail(form);
        subscribe.textContent = "Subscribed!";
        subscribe.style.backgroundColor = "green";
    } else {
        console.error("Form not found!");
    }
});

function submitemail(form) {
    let formData = new FormData(form);
    console.log(formData);

    fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(response => {
        if (response.ok) {
            console.log("Email submitted successfully!");
        } else {
            console.error("Failed to submit email.");
        }
    })
    .catch(error => console.error("Error:", error));
}

convert.forEach(button => {
    button.addEventListener("click", function (event) {
        event.preventDefault();
        console.log("Convert button clicked");
        const form = this.closest("form");
        submitForm(form);
    });
});

function submitForm(form) {
    let formData = new FormData(form);

    if (form.id === "img-form") {
        imgSpinner.style.display = "flex"; 
        imgTxt.style.display = "flex";
    } else if (form.id === "audio-form") {
        audioSpinner.style.display = "flex"; 
        audioTxt.style.display = "flex"; 
    }

    fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(response => response.text())
    .then(html => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");

        if (form.id === "img-form") {
            let imgContent = doc.querySelector(".img-txt-container").innerHTML;
            document.querySelector(".img-txt-container").innerHTML = imgContent;
            imgTxt.style.display = "flex"; 
            imgSpinner.style.display = "none"; 
        } else if (form.id === "audio-form") {
            let audioContent = doc.querySelector(".audio-txt-container").innerHTML;
            document.querySelector(".audio-txt-container").innerHTML = audioContent;
            audioTxt.style.display = "flex"; 
            audioSpinner.style.display = "none"; 
        }
    })
    .catch(error => error.text())
    .catch(html => {
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        // console.error("Error:", error);
        if (form.id === "img-form") {
            let imgContent = doc.querySelector(".img-error-container").innerHTML;
            document.querySelector(".img-error-container").innerHTML = imgContent;
            imgTxt.style.display = "none";
            imgSpinner.style.display = "none";
        } else if (form.id === "pdf-form") {
            audioSpinner.style.display = "none";
        } else if (form.id === "audio-form") {
            audioSpinner.style.display = "none";
        }
    });
}

document.querySelector('.img-txt-container').addEventListener('click', function(event) {
    if (event.target.classList.contains('close-btn')) {
        console.log("Close button clicked (img-txt)");
        imgTxt.style.display = "none";
    }
    if (event.target.classList.contains('copy-button')) {
        console.log("Copy button clicked (img-txt)");
        const container = event.target.parentElement;
        const pElement = container.querySelector('p');
        if (pElement) {
            navigator.clipboard.writeText(pElement.textContent)
                .then(() => {
                    const originalText = event.target.textContent;
                    event.target.textContent = 'Copied!';
                    setTimeout(() => {
                        event.target.textContent = originalText;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                });
        } else {
            console.warn("No text content found to copy in img-txt.");
            event.target.textContent = 'No Text to Copy';
            setTimeout(() => {
                event.target.textContent = 'Copy Text';
            }, 2000);
        }
    }
});

// Event delegation for audio-txt-container
document.querySelector('.audio-txt-container').addEventListener('click', function(event) {
    if (event.target.classList.contains('close-btn2')) {
        console.log("Close button clicked (audio-txt)");
        audioTxt.style.display = "none";
    }
    if (event.target.classList.contains('copy-button')) {
        console.log("Copy button clicked (audio-txt)");
        const container = event.target.parentElement;
        const pElement = container.querySelector('p');
        if (pElement) {
            navigator.clipboard.writeText(pElement.textContent)
                .then(() => {
                    const originalText = event.target.textContent;
                    event.target.textContent = 'Copied!';
                    setTimeout(() => {
                        event.target.textContent = originalText;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy text: ', err);
                });
        } else {
            console.warn("No text content found to copy in audio-txt.");
            event.target.textContent = 'No Text to Copy';
            setTimeout(() => {
                event.target.textContent = 'Copy Text';
            }, 2000);
        }
    }
});

imgTxt.addEventListener("click", function(event) {
    if (event.target === imgTxt) {
        imgTxt.style.display = "none";
    }
});

audioTxt.addEventListener("click", function(event) {
    if (event.target === audioTxt) {
        audioTxt.style.display = "none";
    }
});