// heic_to_jpg_script.js
// HEIC Converter + FAQ accordion

document.addEventListener("DOMContentLoaded", () => {

  /* =========================
     ELEMENTS
  ========================= */
  const selectBtn = document.getElementById("selectBtn");
  const clearBtn = document.getElementById("clearBtn");
  const fileInput = document.getElementById("fileInput");
  const dropZone = document.getElementById("dropZone");
  const fileCount = document.getElementById("fileCount");

  const convertBtn = document.getElementById("convertBtn");
  const downloadZipBtn = document.getElementById("downloadZipBtn");
  const zipNote = document.getElementById("zipNote");

  const progressBox = document.getElementById("progressBox");
  const progressFill = document.getElementById("progressFill");
  const progressPct = document.getElementById("progressPct");
  const spinner = document.getElementById("spinner");

  const resultsSection = document.getElementById("resultsSection");
  const resultsGrid = document.getElementById("results");

  const scrollToToolBtn = document.getElementById("scrollToToolBtn");
  const toolWrap = document.querySelector(".tool-wrap");

  /* =========================
     STATE
  ========================= */
  let convertedFiles = [];

  /* =========================
     SCROLL TO TOOL
  ========================= */
  if (scrollToToolBtn && toolWrap) {
    scrollToToolBtn.addEventListener("click", () => {
      toolWrap.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  /* =========================
     FILE PICKING
  ========================= */
  if (selectBtn && fileInput) {
    selectBtn.addEventListener("click", () => fileInput.click());
  }

  if (clearBtn && fileInput) {
    clearBtn.addEventListener("click", () => {
      fileInput.value = "";
      convertedFiles = [];
      if (resultsGrid) resultsGrid.innerHTML = "";
      if (fileCount) fileCount.textContent = "0 file(s) selected";

      downloadZipBtn?.classList.add("hide");
      zipNote?.classList.add("hide");
      progressBox?.classList.add("hide");
      spinner?.classList.add("hide");
      if (progressFill) progressFill.style.width = "0%";
      if (progressPct) progressPct.textContent = "0%";
      resultsSection?.classList.add("hide");
    });
  }

  fileInput?.addEventListener("change", () => {
    if (fileCount) {
      fileCount.textContent = fileInput.files.length + " file(s) selected";
    }
  });

  /* =========================
     DRAG & DROP
  ========================= */
  if (dropZone && fileInput) {
    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        fileInput.click();
      }
    });

    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.classList.add("hover");
    });

    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("hover");
    });

    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("hover");

      const dt = e.dataTransfer;
      if (!dt || !dt.files.length) return;

      const transfer = new DataTransfer();
      [...dt.files].forEach((f) => transfer.items.add(f));
      fileInput.files = transfer.files;

      if (fileCount) {
        fileCount.textContent = fileInput.files.length + " file(s) selected";
      }
    });
  }

  /* =========================
     CONVERT
  ========================= */
  convertBtn?.addEventListener("click", async () => {
    if (!fileInput || !fileInput.files.length) {
      alert("Please add HEIC images first.");
      return;
    }

    convertedFiles = [];
    if (resultsGrid) resultsGrid.innerHTML = "";
    resultsSection?.classList.add("hide");
    downloadZipBtn?.classList.add("hide");
    zipNote?.classList.add("hide");

    progressBox?.classList.remove("hide");
    spinner?.classList.remove("hide");
    if (progressFill) progressFill.style.width = "0%";
    if (progressPct) progressPct.textContent = "0%";

    convertBtn.disabled = true;

    const files = Array.from(fileInput.files);
    let done = 0;

    for (const file of files) {
      try {
        const out = await processFile(file);
        convertedFiles.push(out);
        renderResult(out);
      } catch (err) {
        console.error(err);
      }

      done++;
      const percent = Math.round((done / files.length) * 100);
      if (progressFill) progressFill.style.width = percent + "%";
      if (progressPct) progressPct.textContent = percent + "%";
    }

    spinner?.classList.add("hide");
    resultsSection?.classList.remove("hide");
    convertBtn.disabled = false;

    if (convertedFiles.length > 1) {
      downloadZipBtn?.classList.remove("hide");
      zipNote?.classList.remove("hide");
    }
  });

  /* =========================
     ZIP DOWNLOAD
  ========================= */
  downloadZipBtn?.addEventListener("click", async () => {
    if (!convertedFiles.length || typeof JSZip === "undefined") return;

    downloadZipBtn.disabled = true;

    try {
      const zip = new JSZip();
      convertedFiles.forEach((f) => zip.file(f.name, f.blob));

      const blob = await zip.generateAsync({ type: "blob" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "heic-converted-images.zip";
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      alert("ZIP download failed.");
    } finally {
      downloadZipBtn.disabled = false;
    }
  });

  /* =========================
     CORE CONVERSION
  ========================= */
  async function processFile(file) {
    let sourceBlob = file;

    if (
      file.name.toLowerCase().endsWith(".heic") ||
      file.name.toLowerCase().endsWith(".heif")
    ) {
      if (typeof heic2any === "undefined") {
        throw new Error("HEIC library not loaded");
      }
      sourceBlob = await heic2any({
        blob: file,
        toType: "image/jpeg",
        quality: 1
      });
      if (Array.isArray(sourceBlob)) sourceBlob = sourceBlob[0];
    }

    const img = await loadImage(URL.createObjectURL(sourceBlob));

    const preset = document.getElementById("preset").value;
    const map = { small: 800, medium: 1200, large: 2400 };
    let { width, height } = img;

    if (preset !== "original") {
      const max = map[preset];
      if (width > max || height > max) {
        if (width >= height) {
          height = Math.round((height * max) / width);
          width = max;
        } else {
          width = Math.round((width * max) / height);
          height = max;
        }
      }
    }

    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    canvas.getContext("2d").drawImage(img, 0, 0, width, height);

    const mime = document.getElementById("format").value;
    const quality = parseFloat(document.getElementById("quality").value);

    const outBlob = await new Promise((r) => canvas.toBlob(r, mime, quality));
    const ext = mime === "image/jpeg" ? "jpg" : mime.split("/")[1];
    const base = file.name.replace(/\.[^/.]+$/, "");
    const name = `${base}_${width}x${height}.${ext}`;

    return {
      name,
      blob: outBlob,
      url: URL.createObjectURL(outBlob),
      width,
      height,
      size: outBlob.size
    };
  }

  function loadImage(src) {
    return new Promise((res, rej) => {
      const img = new Image();
      img.onload = () => res(img);
      img.onerror = () => rej(new Error("Image load failed"));
      img.src = src;
    });
  }

  /* =========================
     RENDER RESULT
  ========================= */
  function renderResult(item) {
    if (!resultsGrid) return;

    const card = document.createElement("div");
    card.className = "result-card";
    card.setAttribute("role", "listitem");
    card.innerHTML = `
      <img src="${item.url}" alt="${escapeHtml(item.name)}">
      <div class="result-name">${escapeHtml(item.name)}</div>
      <div class="result-meta">${item.width}×${item.height} — ${(item.size / 1024).toFixed(1)} KB</div>
      <a class="btn btn-download" href="${item.url}" download="${escapeHtml(item.name)}">Download</a>
    `;
    resultsGrid.appendChild(card);
  }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"]/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])
    );
  }

  /* =========================
     FAQ ACCORDION
  ========================= */
  const faq = document.querySelector(".faq-accordion .faq-list");
  if (faq) {
    faq.addEventListener("click", (e) => {
      const btn = e.target.closest(".faq-q");
      if (!btn) return;
      toggleFAQ(btn);
    });

    faq.addEventListener("keydown", (e) => {
      const btn = e.target.closest(".faq-q");
      if (!btn) return;

      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        const buttons = Array.from(faq.querySelectorAll(".faq-q"));
        const idx = buttons.indexOf(btn);
        const next =
          e.key === "ArrowDown"
            ? buttons[idx + 1] || buttons[0]
            : buttons[idx - 1] || buttons[buttons.length - 1];
        next.focus();
      }
    });
  }

  function toggleFAQ(btn) {
    const region = document.getElementById(btn.getAttribute("aria-controls"));
    const expanded = btn.getAttribute("aria-expanded") === "true";

    faq.querySelectorAll('.faq-q[aria-expanded="true"]').forEach((b) => {
      if (b !== btn) closeFAQ(b);
    });

    if (expanded) closeFAQ(btn);
    else openFAQ(btn, region);
  }

  function openFAQ(btn, region) {
    btn.setAttribute("aria-expanded", "true");
    btn.closest(".faq-item")?.classList.add("open");
    if (region) region.hidden = false;
  }

  function closeFAQ(btn) {
    const id = btn.getAttribute("aria-controls");
    const region = document.getElementById(id);
    btn.setAttribute("aria-expanded", "false");
    btn.closest(".faq-item")?.classList.remove("open");
    if (region) region.hidden = true;
  }

});
