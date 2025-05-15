document
  .getElementById("enterprise-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    const responseApi = await fetch("/api/register-enterprise", {
      method: "POST",
      body: formData,
    });
  });
