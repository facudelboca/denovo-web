document.addEventListener("DOMContentLoaded", () => {
    let myCurrentIndex = 0;
    const mySlides = document.querySelectorAll(".my-carousel-slide");
    const myTotalSlides = mySlides.length;
    const myTrack = document.querySelector(".my-carousel-track");
    const btnPrev = document.querySelector(".my-carousel-btn.prev");
    const btnNext = document.querySelector(".my-carousel-btn.next");

    function myShowSlide(index) {
        const offset = -index * 100;
        myTrack.style.transform = `translateX(${offset}%)`;
    }

    btnNext.addEventListener("click", () => {
        myCurrentIndex = (myCurrentIndex + 1) % myTotalSlides;
        myShowSlide(myCurrentIndex);
    });

    btnPrev.addEventListener("click", () => {
        myCurrentIndex = (myCurrentIndex - 1 + myTotalSlides) % myTotalSlides;
        myShowSlide(myCurrentIndex);
    });

    // autoplay
    setInterval(() => {
        myCurrentIndex = (myCurrentIndex + 1) % myTotalSlides;
        myShowSlide(myCurrentIndex);
    }, 3000);
});
