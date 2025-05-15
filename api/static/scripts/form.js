const tabClient = document.getElementById("tab-cliente");
const tabDelivery = document.getElementById("tab-entregador");
const tabEnterprise = document.getElementById("tab-empresa");
const formClient = document.getElementById("client-form");
const formDelivery = document.getElementById("delivery-form");
const formEnterprise = document.getElementById("form-empresa");

function switchToClient() {
  formClient.classList.remove("hidden");
  formEnterprise.classList.add("hidden");
  formDelivery.classList.add("hidden");

  tabClient.classList.add("border-blue-600", "text-blue-600");
  tabClient.classList.remove("border-transparent", "text-gray-500");
  tabDelivery.classList.remove("border-blue-600", "text-blue-600");
  tabDelivery.classList.add("border-transparent", "text-gray-500");
  tabEnterprise.classList.remove("border-blue-600", "text-blue-600");
  tabEnterprise.classList.add("border-transparent", "text-gray-500");
}

function switchToDelivery() {
  formDelivery.classList.remove("hidden");
  formEnterprise.classList.add("hidden");
  formClient.classList.add("hidden");

  tabDelivery.classList.add("border-blue-600", "text-blue-600");
  tabDelivery.classList.remove("border-transparent", "text-gray-500");
  tabClient.classList.remove("border-blue-600", "text-blue-600");
  tabClient.classList.add("border-transparent", "text-gray-500");
  tabEnterprise.classList.remove("border-blue-600", "text-blue-600");
  tabEnterprise.classList.add("border-transparent", "text-gray-500");
}

function switchToEnterprise() {
  formDelivery.classList.add("hidden");
  formClient.classList.add("hidden");
  formEnterprise.classList.remove("hidden");

  tabEnterprise.classList.remove("border-transparent", "text-gray-500");
  tabEnterprise.classList.add("border-blue-600", "text-blue-600");
  tabClient.classList.remove("border-blue-600", "text-blue-600");
  tabClient.classList.add("border-transparent", "text-gray-500");
  tabDelivery.classList.remove("border-blue-600", "text-blue-600");
  tabDelivery.classList.add("border-transparent", "text-gray-500");
}

// Verifica o parâmetro na URL ao carregar a página
window.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const tipo = urlParams.get("tipo");

  if (tipo === "entregador") {
    switchToDelivery();
  } else if (tipo === "cliente") {
    switchToClient();
  } else {
    switchToEnterprise();
  }
});

// Event listeners para os tabs
tabClient.addEventListener("click", switchToClient);
tabDelivery.addEventListener("click", switchToDelivery);
tabEnterprise.addEventListener("click", switchToEnterprise);

// Máscaras

function mascaraCPF(cpf) {
  cpf = cpf.replace(/\D/g, "");
  cpf = cpf.replace(/^(\d{3})(\d)/, "$1.$2");
  cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
  cpf = cpf.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
  return cpf;
}

function mascaraCNH(cnh) {
  cnh = cnh.replace(/\D/g, "");
  cnh = cnh.replace(/^(\d{3})(\d)/, "$1.$2");
  cnh = cnh.replace(/(\d{3})(\d)/, "$1.$2");
  cnh = cnh.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
  return cnh;
}

function mascaraCNPJ(cnpj) {
  cnpj = cnpj.replace(/\D/g, "");
  cnpj = cnpj.replace(/^(\d{2})(\d)/, "$1.$2");
  cnpj = cnpj.replace(/(\d{3})(\d)/, "$1.$2");
  cnpj = cnpj.replace(/(\d{3})(\d)/, "$1/$2");
  cnpj = cnpj.replace(/(\d{4})(\d)/, "$1-$2");
  return cnpj;
}

function mascaraTelefone(telefone) {
  telefone = telefone.replace(/\D/g, "");
  telefone = telefone.replace(/^(\d{2})(\d)/, "($1) $2");
  telefone = telefone.replace(/(\d{5})(\d{1,4})$/, "$1-$2");
  return telefone;
}

function aplicarMascara(event, tipo) {
  let value = event.target.value;

  switch (tipo) {
    case "cpf":
      event.target.value = mascaraCPF(value);
      break;
    case "cnh":
      event.target.value = mascaraCNH(value);
      break;
    case "cpnj":
      event.target.value = mascaraCNPJ(value);
      break;
    case "telefone":
      event.target.value = mascaraTelefone(value);
      break;
  }
}
