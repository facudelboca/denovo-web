CustomEase.create("cubic", "0.83, 0, 0.17, 1");
let isAnimating = false;

function splitTextIntoSpans(selector) {
    let elements = document.querySelectorAll(selector);
    elements.forEach((element) => {  // Paréntesis corregido
        let text = element.innerText;
        let splitText = text
            .split("")
            .map((char) => `<span>${char === " " ? "&nbsp;&nbsp;" : char}</span>`) // Uso correcto de backticks
            .join("");
        element.innerHTML = splitText;  // Corregido "innerHTHL" -> "innerHTML"
    });
}

function initializeCards() {
    let cards = Array.from(document.querySelectorAll(".card"));
    gsap.to(cards, {
        y: (i) => -15 + 15 * i + "%",
        z: (i) => 15 * i,
        duration: 1,
        ease: "cubic",
        stagger: -0.1,
    });

}

document.addEventListener("DOMContentLoaded", function (){
    splitTextIntoSpans(".copy txt-carousel");
    initializeCards();

    gsap.set(".txt-carousel span", {y: -200});
    gsap.set(".slider .card:last-child .txt-carousel span", {y: 0})

    function startCarousel() {
        let slider = document.querySelector(".slider");
        let cards = Array.from(slider.querySelectorAll(".card"));
        let lastCard = cards.pop();
        let nextCard = cards[cards.length - 1];
        let intervalTime = lastCard.classList.contains("casas") ? 2000 : 4000;

        gsap.to(lastCard.querySelectorAll(".txt-carousel span"), {
            y: 200,
            duration: 0.75,
            ease: "cubic",
        });

        gsap.to(lastCard, {
            y: "+=150%",
            duration: 0.75,
            ease: "cubic",
            onComplete: () => {
                slider.prepend(lastCard);
                initializeCards();
                gsap.set(lastCard.querySelectorAll(".txt-carousel span"), { y: -200 });
                isAnimating = false;
                setTimeout(startCarousel, intervalTime);
            },
        });

        gsap.to(nextCard.querySelectorAll(".txt-carousel span"), {
            y: 0,
            duration: 1,
            ease: "cubic",
            stagger: 0.05,
        });
    }

    setTimeout(startCarousel, 3000); // Inicia con un intervalo de 3 segundos por defecto
});

