function revealOnScroll() {
    const sections = document.querySelectorAll('section');
    sections.forEach((section, index) => {
        const sectionTop = section.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        if (sectionTop < windowHeight * 0.75) {
            setTimeout(() => {
                section.classList.add('opacity-100', 'translate-y-0');
                section.classList.remove('opacity-0', 'translate-y-10');
            }, index * 200);
        }
    });
}

document.querySelectorAll('section').forEach(section => {
    section.classList.add('transform', 'transition-all', 'duration-1000', 'opacity-0', 'translate-y-10');
});

window.addEventListener('scroll', revealOnScroll);
window.addEventListener('load', () => {
    setTimeout(revealOnScroll, 500);
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
