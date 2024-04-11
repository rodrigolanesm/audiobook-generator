let currentPage = 1; // Página atual
let totalPages = 0; // Número total de páginas
let escala = 1

// URL do PDF que você deseja renderizar
var pdfUrl = '../saves/Fisica_2_-_Gravitacao_Ondas_e_Termodinamica_Halliday_10a_Edicao.pdf';

// Função para carregar e renderizar a página atual
function renderPage(pageNumber) {
  pdfjsLib.getDocument(pdfUrl).promise.then(pdf => {
    totalPages = pdf.numPages; // Atualizar número total de páginas

    // Verificar limites da página
    if (pageNumber < 1) {
      pageNumber = 1;
    } else if (pageNumber > totalPages) {
      pageNumber = totalPages;
    }
    
    currentPage = pageNumber; // Atualizar número da página atual

    // Limpar conteúdo anterior
    document.getElementById('pdfRenderer').innerHTML = '';

    // Carregar a página
    pdf.getPage(pageNumber).then(page => {
      const scale = escala;
      const viewport = page.getViewport({ scale });

      // Criar uma div para cada página
      const pageContainer = document.createElement('div');
      pageContainer.className = 'page-container';

      // Adicionar a div ao elemento onde o PDF será renderizado
      document.getElementById('pdfRenderer').appendChild(pageContainer);

      // Renderizar a página dentro da div
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      canvas.height = viewport.height;
      canvas.width = viewport.width;
      page.render({
        canvasContext: context,
        viewport: viewport
      });

      // Adicionar a canvas à div
      pageContainer.appendChild(canvas);

      // Atualizar o contador de páginas
      document.getElementById('pageCounter').textContent = `Página ${currentPage} de ${totalPages}`;
    });
  });
}

// Função para avançar para a próxima página
function nextPage() {
  renderPage(currentPage + 1);
}

// Função para voltar para a página anterior
function prevPage() {
  renderPage(currentPage - 1);
}

function plusSize(){
  escala += 0.1
  renderPage(currentPage)
}

function minusSize(){
  escala -= 0.1
  renderPage(currentPage)
}

renderPage(1)