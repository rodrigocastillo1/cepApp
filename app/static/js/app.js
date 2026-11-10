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
    const scannedValue = value.trim();
    let productId = scannedValue;
    if (!/^[A-Za-z0-9_-]+$/.test(scannedValue)) {
      try {
        const scannedUrl = new URL(scannedValue, window.location.origin);
        const productPath = scannedUrl.pathname.match(
          /^\/products\/([A-Za-z0-9_-]+)\/?$/,
        );
        if (productPath) productId = productPath[1];
      } catch {
        // Treat non-URL content as a product ID; Flask will show 404 if unknown.
      }
    }

    const passportUrl = new URL(
      `/products/${encodeURIComponent(productId)}`,
      window.location.origin,
    );
    stopScanner("Opening product passport…");
    window.location.assign(passportUrl.href);
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

  const liveCarbonChart = document.querySelector("[data-live-carbon-chart]");
  if (liveCarbonChart) {
    const status = liveCarbonChart.querySelector("#live-carbon-status");
    const bars = liveCarbonChart.querySelector("#live-carbon-bars");
    const updated = liveCarbonChart.querySelector("#live-carbon-updated");
    let refreshing = false;
    let previousTotals = null;

    const showStatus = (message, isError = false) => {
      status.textContent = message;
      status.classList.toggle("is-error", isError);
      bars.hidden = true;
    };

    const refreshCarbonChart = async () => {
      if (refreshing) return;
      refreshing = true;
      try {
        const url = new URL(liveCarbonChart.dataset.apiUrl, window.location.origin);
        const response = await fetch(url, { cache: "no-store" });
        if (!response.ok) throw new Error("Analytics data request failed.");
        const data = await response.json();

        bars.replaceChildren();
        if (data.brands.length === 0) {
          showStatus("No lifecycle events have been processed yet.");
          updated.textContent = "";
          previousTotals = new Map();
          return;
        }

        const brands = [...data.brands].sort(
          (left, right) =>
            left.total_kg_co2e - right.total_kg_co2e
            || left.brand.localeCompare(right.brand),
        );
        const largestTotal = Math.max(...brands.map((brand) => brand.total_kg_co2e));
        const currentTotals = new Map();
        brands.forEach((brand) => {
          const totalValue = Number(brand.total_kg_co2e);
          const hasChanged = previousTotals !== null
            && previousTotals.get(brand.brand) !== totalValue;
          currentTotals.set(brand.brand, totalValue);

          const row = document.createElement("div");
          row.className = "bar-row carbon-bar";

          const label = document.createElement("div");
          label.className = "bar-label";
          const brandName = document.createElement("span");
          brandName.textContent = `${brand.brand} · ${brand.event_count} events`;
          const total = document.createElement("strong");
          total.textContent = totalValue.toFixed(2);
          if (hasChanged) {
            brandName.classList.add("live-carbon-value-updated");
            total.classList.add("live-carbon-value-updated");
          }
          label.append(brandName, total);

          const track = document.createElement("div");
          track.className = "bar-track";
          track.setAttribute("role", "img");
          track.setAttribute(
            "aria-label",
            `${brand.brand}: ${Number(brand.total_kg_co2e).toFixed(2)} kg CO2 equivalent`,
          );
          const fill = document.createElement("span");
          fill.style.width = `${largestTotal > 0 ? (brand.total_kg_co2e / largestTotal) * 100 : 0}%`;
          track.append(fill);
          row.append(label, track);
          bars.append(row);
        });
        previousTotals = currentTotals;

        status.textContent = "Live totals from processed demo events · kg CO₂e";
        status.classList.remove("is-error");
        bars.hidden = false;
        const latest = brands.reduce(
          (newest, brand) => (brand.updated_at > newest ? brand.updated_at : newest),
          "",
        );
        updated.textContent = latest
          ? `Latest event: ${new Date(latest).toLocaleString()}`
          : "";
      } catch {
        showStatus("Live analytics are temporarily unavailable. Retrying shortly.", true);
        updated.textContent = "";
      } finally {
        refreshing = false;
      }
    };

    refreshCarbonChart();
    window.setInterval(refreshCarbonChart, 3000);
  }
});
