document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const response = await fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const result = await response.json();

  if (response.ok) {
    // Redireciona com base no tipo de usuário
    if (result.user_type === "client") {
      window.location.href = "/client.html";
    } else if (result.user_type === "delivery") {
      window.location.href = "/entregador.html";
    } else if (result.user_type === "enterprise") {
      window.location.href = "/enterprise.html";
    } else {
      alert("Tipo de usuário desconhecido.");
    }
  } else {
    alert(result.detail || "Erro no login");
  }
});
