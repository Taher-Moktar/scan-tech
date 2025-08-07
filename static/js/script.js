const video = document.getElementById("camera");
const canvas = document.getElementById("snapshot");
const context = canvas.getContext("2d");
const imageDataInput = document.getElementById("imageData");
const form = document.getElementById("captureForm");
const resultDiv = document.getElementById("resultat");
const detectedImage = document.getElementById("detectedImage");

// Démarrer la caméra
navigator.mediaDevices.getUserMedia({ video: true })
  .then((stream) => {
    video.srcObject = stream;
  })
  .catch((err) => {
    console.error("Erreur caméra:", err);
  });

function takePhoto() {
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = canvas.toDataURL("image/jpeg");
  imageDataInput.value = imageData;
}

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(form);

  resultDiv.innerHTML = "Chargement en cours...";
  detectedImage.src = "";

  try {
    const response = await fetch("/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (result.error) {
      resultDiv.innerHTML = `<span style="color:red;">Erreur: ${result.error}</span>`;
    } else {
      resultDiv.innerHTML = result.documentation;
      detectedImage.src = result.image_path;
    }
  } catch (error) {
    resultDiv.innerHTML = `<span style="color:red;">Erreur: ${error}</span>`;
  }
});
