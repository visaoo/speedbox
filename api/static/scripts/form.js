const tabCliente = document.getElementById("tab-cliente");
const tabEntregador = document.getElementById("tab-entregador");
const formCliente = document.getElementById("form-cliente");
const formEntregador = document.getElementById("form-entregador");
const tabEmpresa = document.getElementById("tab-empresa")
const formEmpresa = document.getElementById("form-empresa");


function switchToCliente() {
    formCliente.classList.remove("hidden");
    formEmpresa.classList.add("hidden");
    formEntregador.classList.add("hidden");

    tabCliente.classList.add("border-blue-600", "text-blue-600");
    tabCliente.classList.remove("border-transparent", "text-gray-500");
    tabEntregador.classList.remove("border-blue-600", "text-blue-600");
    tabEntregador.classList.add("border-transparent", "text-gray-500");
    tabEmpresa.classList.remove("border-blue-600", "text-blue-600");
    tabEmpresa.classList.add("border-transparent", "text-gray-500");
}

function switchToEntregador() {
    formEntregador.classList.remove("hidden");
    formEmpresa.classList.add("hidden");
    formCliente.classList.add("hidden");

    tabEntregador.classList.add("border-blue-600", "text-blue-600");
    tabEntregador.classList.remove("border-transparent", "text-gray-500");
    tabCliente.classList.remove("border-blue-600", "text-blue-600");
    tabCliente.classList.add("border-transparent", "text-gray-500");
    tabEmpresa.classList.remove("border-blue-600", "text-blue-600");
    tabEmpresa.classList.add("border-transparent", "text-gray-500");
}

function switchToEmpresa() {
    formEntregador.classList.add("hidden");
    formCliente.classList.add("hidden");
    formEmpresa.classList.remove("hidden");

    tabEmpresa.classList.remove("border-transparent", "text-gray-500");
    tabEmpresa.classList.add("border-blue-600", "text-blue-600");
    tabCliente.classList.remove("border-blue-600", "text-blue-600");
    tabCliente.classList.add("border-transparent", "text-gray-500");
    tabEntregador.classList.remove("border-blue-600", "text-blue-600");
    tabEntregador.classList.add("border-transparent", "text-gray-500");
}

// Verifica o parâmetro na URL ao carregar a página
window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const tipo = urlParams.get('tipo');

    if (tipo === 'entregador') {
        switchToEntregador();
    } else if (tipo === 'cliente') {
        switchToCliente();
    } else {
        switchToEmpresa();
    }
});

// Event listeners para os tabs
tabCliente.addEventListener("click", switchToCliente);
tabEntregador.addEventListener("click", switchToEntregador);
tabEmpresa.addEventListener("click", switchToEmpresa);

// Máscaras 

// Máscara para CPF 
function mascaraCPF(cpf) {
    cpf = cpf.replace(/\D/g, ''); // Remove caracteres não numéricos
    cpf = cpf.replace(/^(\d{3})(\d)/, '$1.$2'); // Adiciona ponto
    cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona ponto
    cpf = cpf.replace(/(\d{3})(\d{1,2})$/, '$1-$2'); // Adiciona hífen
    return cpf;
}

// Máscara para CNH
function mascaraCNH(cnh) {
    cnh = cnh.replace(/\D/g, ''); // Remove caracteres não numéricos
    cnh = cnh.replace(/^(\d{3})(\d)/, '$1.$2'); // Adiciona ponto
    cnh = cnh.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona ponto
    cnh = cnh.replace(/(\d{3})(\d{1,2})$/, '$1-$2'); // Adiciona hífen
    return cnh;
}

// Máscara para CNPJ
function mascaraCNPJ(cnpj) {
    cnpj = cnpj.replace(/\D/g, ''); // Remove caracteres não numéricos
    cnpj = cnpj.replace(/^(\d{2})(\d)/, '$1.$2'); // Adiciona ponto
    cnpj = cnpj.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona ponto
    cnpj = cnpj.replace(/(\d{3})(\d)/, '$1/$2'); // Adiciona barra
    cnpj = cnpj.replace(/(\d{4})(\d)/, '$1-$2'); // Adiciona hífen
    return cnpj;
}

// Máscara para Telefone
function mascaraTelefone(telefone) {
    telefone = telefone.replace(/\D/g, ''); // Remove caracteres não numéricos
    telefone = telefone.replace(/^(\d{2})(\d)/, '($1) $2'); // Adiciona parênteses e espaço
    telefone = telefone.replace(/(\d{5})(\d{1,4})$/, '$1-$2'); // Adiciona hífen
    return telefone;
}

function aplicarMascara(event, tipo) {
    let value = event.target.value;

    if (tipo === "cpf") {
        event.target.value = mascaraCPF(value);
    } else if (tipo === "cnh") {
        event.target.value = mascaraCNH(value);
    } else if (tipo === "cnpj") {
        event.target.value = mascaraCNPJ(value);
    } else if (tipo === "telefone") {
        event.target.value = mascaraTelefone(value);
    }
}