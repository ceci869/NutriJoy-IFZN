function rolarCarrossel(containerID, direcao) {
    const container = document.getElementById(containerID);
    const quantRolagem = 336;
    container.scrollBy({
        left: direcao * quantRolagem
    });
}