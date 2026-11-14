function rolarCarrossel(containerID, direcao) {
    const container = document.getElementById(containerID);

    if (!container) {
        console.error(`Carrossel "${containerID}" não encontrado.`);
        return;
    }

    const quantRolagem = 336;

    container.scrollBy({
        left: direcao * quantRolagem,
        behavior: 'smooth'
    });
}