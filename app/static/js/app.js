document.addEventListener("DOMContentLoaded", () => {
  const video = document.querySelector("#camera-video");
  const startButton = document.querySelector("#start-camera");
  const stopButton = document.querySelector("#stop-camera");
  const status = document.querySelector("#scanner-status");
  const placeholder = document.querySelector("#camera-placeholder");
  const questionInput = document.querySelector("#coach-question");
  let stream = null;
  let zxingControls = null;
  let cameraTrack = null;
  let scannerActive = false;
  let scanFrame = null;
  let checkingFrame = false;
  let detector = null;
  let zxingScriptPromise = null;

  const onCameraTrackEnded = () => {
    if (scannerActive) {
      stopScanner("The camera connection ended. Try starting the camera again or search by product ID.");
    }
  };

  const watchCameraTrack = (track) => {
    cameraTrack = track;
    cameraTrack.addEventListener("ended", onCameraTrackEnded, { once: true });
  };

  const loadZxing = () => {
    if (window.ZXingBrowser) return Promise.resolve(window.ZXingBrowser);
    if (zxingScriptPromise) return zxingScriptPromise;

    zxingScriptPromise = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "https://unpkg.com/@zxing/browser@0.2.1/umd/zxing-browser.min.js";
      script.integrity = "sha384-HRtzk9lZgkbSgvUyQrnfC/GxiXZgwaNyD7hC9wcXlsBpDhkS80ISl73juef2FRuf";
      script.crossOrigin = "anonymous";
      script.onload = () => {
        if (window.ZXingBrowser) resolve(window.ZXingBrowser);
        else reject(new Error("QR scanning library did not initialize."));
      };
      script.onerror = () => reject(new Error("QR scanning library could not be loaded."));
      document.head.appendChild(script);
    });
    return zxingScriptPromise;
  };

  const openScannedPassport = (value) => {
    let scannedUrl;
    try {
      scannedUrl = new URL(value, window.location.origin);
    } catch {
      stopScanner("That QR code does not contain a valid link. Try again or search by product ID.");
      return;
    }

    const productPath = /^\/products\/[A-Za-z0-9_-]+\/?$/.test(scannedUrl.pathname);
    if (scannedUrl.origin !== window.location.origin || !productPath) {
      stopScanner("That QR code is not a product passport link for this application.");
      return;
    }
    stopScanner("Product found. Opening its passport…");
    window.location.assign(scannedUrl.href);
  };

  const stopScanner = (message) => {
    scannerActive = false;
    if (scanFrame !== null) {
      cancelAnimationFrame(scanFrame);
      scanFrame = null;
    }
    if (zxingControls) {
      zxingControls.stop();
      zxingControls = null;
    }
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      stream = null;
    }
    if (cameraTrack) {
      cameraTrack.removeEventListener("ended", onCameraTrackEnded);
      cameraTrack = null;
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
      if (!scannerActive || !stream || !detector || checkingFrame) return;
      checkingFrame = true;
      try {
        const codes = await detector.detect(video);
        const value = codes[0]?.rawValue;
        if (value) {
          openScannedPassport(value);
          return;
        }
      } catch {
        stopScanner("The QR code could not be read. Try again or search by product ID.");
        return;
      } finally {
        checkingFrame = false;
      }
      if (scannerActive && stream) scanFrame = requestAnimationFrame(scan);
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

      startButton.disabled = true;
      status.textContent = "Requesting camera permission…";
      try {
        if (typeof window.BarcodeDetector === "function") {
          try {
            detector = new window.BarcodeDetector({ formats: ["qr_code"] });
          } catch {
            detector = null;
          }
        }

        if (detector) {
          stream = await navigator.mediaDevices.getUserMedia({
            audio: false,
            video: { facingMode: { ideal: "environment" } },
          });
          const [track] = stream.getVideoTracks();
          if (track) watchCameraTrack(track);
          video.srcObject = stream;
          await video.play();
          scannerActive = true;
          status.textContent = "Camera is active. Point it at a product passport QR code.";
          scanFrame = requestAnimationFrame(scan);
        } else {
          status.textContent = "Loading QR scanner…";
          const zxing = await loadZxing();
          const reader = new zxing.BrowserQRCodeReader();
          scannerActive = true;
          video.hidden = false;
          placeholder.hidden = true;
          const controls = await reader.decodeFromConstraints(
            {
              audio: false,
              video: { facingMode: { ideal: "environment" } },
            },
            video,
            (result) => {
              if (result && scannerActive) {
                openScannedPassport(result.getText());
              }
            },
          );
          if (!scannerActive) {
            controls.stop();
            return;
          }
          zxingControls = controls;
          const [track] = video.srcObject?.getVideoTracks() || [];
          if (track) watchCameraTrack(track);
          scannerActive = true;
          status.textContent = "Camera is active. Point it at a product passport QR code.";
        }

        video.hidden = false;
        placeholder.hidden = true;
        stopButton.disabled = false;
      } catch (error) {
        const denied = error?.name === "NotAllowedError" || error?.name === "PermissionDeniedError";
        stopScanner(
          denied
            ? "Camera permission was denied. Allow access in browser settings or search by product ID."
            : error?.message?.includes("QR scanning library")
              ? "The QR scanner could not be loaded. Check your internet connection, then try again or search by product ID."
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
