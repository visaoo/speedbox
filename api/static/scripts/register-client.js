document
  .getElementById("client-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    const responseApi = await fetch("/api/register-client", {
      method: "POST",
      body: formData,
    });
  });
