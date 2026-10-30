document.addEventListener("DOMContentLoaded", () => {
  const video = document.querySelector("#camera-video");
  const startButton = document.querySelector("#start-camera");
  const stopButton = document.querySelector("#stop-camera");
  const status = document.querySelector("#scanner-status");
  const placeholder = document.querySelector("#camera-placeholder");
  const questionInput = document.querySelector("#coach-question");
  let stream = null;
  let scanFrame = null;
  let checkingFrame = false;
  let detector = null;

  const stopScanner = (message) => {
    if (scanFrame !== null) {
      cancelAnimationFrame(scanFrame);
      scanFrame = null;
    }
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      stream = null;
    }
    if (video) {
      video.pause();
      video.srcObject = null;
      video.hidden = true;
    }
    if (placeholder) placeholder.hidden = false;
    if (startButton) startButton.disabled = false;
    if (stopButton) stopButton.disabled = true;
    if (status && message) status.textContent = message;
  };

  if (startButton && video && status) {
    const scan = async () => {
      if (!stream || !detector || checkingFrame) return;
      checkingFrame = true;
      try {
        const codes = await detector.detect(video);
        const value = codes[0]?.rawValue;
        if (value) {
          const scannedUrl = new URL(value, window.location.origin);
          const productPath = /^\/products\/[A-Za-z0-9_-]+\/?$/.test(scannedUrl.pathname);
          if (scannedUrl.origin !== window.location.origin || !productPath) {
            stopScanner("That QR code is not a product passport link for this application.");
            return;
          }
          stopScanner("Product found. Opening its passport…");
          window.location.assign(scannedUrl.href);
          return;
        }
      } catch {
        stopScanner("The QR code could not be read. Try again or search by product ID.");
        return;
      } finally {
        checkingFrame = false;
      }
      if (stream) scanFrame = requestAnimationFrame(scan);
    };

    startButton.addEventListener("click", async () => {
      if (!window.isSecureContext) {
        status.textContent = "Camera access requires HTTPS or localhost. You can still search by product ID.";
        return;
      }
      if (!navigator.mediaDevices?.getUserMedia) {
        status.textContent = "This browser does not provide camera access. Search by product ID instead.";
        return;
      }
      if (!("BarcodeDetector" in window)) {
        status.textContent = "QR scanning is not supported by this browser. Search by product ID or open a QR link directly.";
        return;
      }

      startButton.disabled = true;
      status.textContent = "Requesting camera permission…";
      try {
        detector = new window.BarcodeDetector({ formats: ["qr_code"] });
        stream = await navigator.mediaDevices.getUserMedia({
          audio: false,
          video: { facingMode: { ideal: "environment" } },
        });
        video.srcObject = stream;
        await video.play();
        video.hidden = false;
        placeholder.hidden = true;
        stopButton.disabled = false;
        status.textContent = "Camera is active. Point it at a product passport QR code.";
        scanFrame = requestAnimationFrame(scan);
      } catch (error) {
        const denied = error?.name === "NotAllowedError" || error?.name === "PermissionDeniedError";
        stopScanner(
          denied
            ? "Camera permission was denied. Allow access in browser settings or search by product ID."
            : "The camera could not be started. Check browser permissions or search by product ID.",
        );
      }
    });

    stopButton.addEventListener("click", () => {
      stopScanner("Camera stopped. Search by product ID or start scanning again.");
    });
    window.addEventListener("pagehide", () => stopScanner());
  }

  document.querySelectorAll("[data-question]").forEach((button) => {
    button.addEventListener("click", () => {
      if (questionInput) {
        questionInput.value = button.dataset.question || "";
        questionInput.focus();
      }
    });
  });
});
