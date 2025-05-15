document
  .getElementById("delivery-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    const responseApi = await fetch("/api/register-delivery", {
      method: "POST",
      body: formData,
    });
  });
