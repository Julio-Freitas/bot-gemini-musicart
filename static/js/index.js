const selectorEl = (s) => document.querySelector(s);
let chat = selectorEl("#chat");
let input = selectorEl("#input");
let botaoEnviar = selectorEl("#botao-enviar");
let imagemSelecionada;
let botaoAnexo = selectorEl("#mais_arquivo");
let miniaturaImagem;

function createMiniImg(img) {
  miniaturaImagem = document.createElement("img");
  miniaturaImagem.src = URL.createObjectURL(img);
  miniaturaImagem.style.maxWidth = "3rem";
  miniaturaImagem.style.maxHeight = "3rem";
  miniaturaImagem.style.margin = "0.5rem";
  miniaturaImagem.style.borderRadius = "50%";
}

async function getImage() {
  let fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.accept = "image/*";

  fileInput.onchange = async (event) => {
    if (miniaturaImagem) miniaturaImagem.remove();

    imagemSelecionada = event.target.files[0];
    createMiniImg(imagemSelecionada);

    selectorEl(".entrada__container").insertBefore(miniaturaImagem, input);

    let formData = new FormData();
    formData.append("imagem", imagemSelecionada);

    const response = await fetch("http://127.0.0.1:5000/upload_imagem", {
      method: "POST",
      body: formData,
    });

    const resposta = await response.text();
    console.log(resposta);
    console.log(imagemSelecionada);
  };
  fileInput.click();
}

async function requestChat(msg) {
  let response = "";
  try {
    response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ msg }),
    });
  } catch (error) {
    response = "Algum Error!";
  } finally {
    return response;
  }
}

async function enviarMensagem() {
  if (input.value == "" || input.value == null) return;
  let mensagem = input.value;
  input.value = "";

  if (miniaturaImagem) miniaturaImagem.remove();

  let novaBolha = criaBolhaUsuario();
  novaBolha.innerHTML = mensagem;
  chat.appendChild(novaBolha);

  let novaBolhaBot = criaBolhaBot();
  chat.appendChild(novaBolhaBot);
  vaiParaFinalDoChat();

  let loading = document.createElement("p");
  let spinner = document.createElement("span");

  spinner.classList = "spinner";
  loading.textContent = "Analisando...";

  const status = ["Analisando", "Analisando.", "Analisando..", "Analisando..."];
  let indice = 0;
  novaBolhaBot.appendChild(spinner);
  novaBolhaBot.appendChild(loading);

  // const intervalAnimation = setInterval(() => {
  //   novaBolhaBot.innerHTML = status[indice];
  //   indice = (indice + 1) % status.length;
  // }, 500);

  // Envia requisição com a mensagem para a API do ChatBot
  const resposta = await requestChat(mensagem);
  const textoDaResposta = await resposta.text();
  // clearInterval(intervalAnimation);
  novaBolhaBot.innerHTML = textoDaResposta.replace(/\n/g, "<br>");
  vaiParaFinalDoChat();
}

function criaBolhaUsuario() {
  let bolha = document.createElement("p");
  bolha.classList = "chat__bolha chat__bolha--usuario";
  return bolha;
}

function criaBolhaBot() {
  let bolha = document.createElement("p");
  bolha.classList = "chat__bolha chat__bolha--bot chat__bolha-wrapper-flex";
  return bolha;
}

function vaiParaFinalDoChat() {
  chat.scrollTop = chat.scrollHeight;
}

botaoEnviar.addEventListener("click", enviarMensagem);
input.addEventListener("keyup", function (event) {
  event.preventDefault();
  if (event.keyCode === 13) botaoEnviar.click();
});

botaoAnexo.addEventListener("click", getImage);
