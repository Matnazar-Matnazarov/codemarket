const images = [];
const thumbnailContainer = document.getElementById('thumbnailContainer');
if (thumbnailContainer) {
    const thumbnails = thumbnailContainer.querySelectorAll('[data-image-url]');
    thumbnails.forEach(thumbnail => {
        images.push(thumbnail.dataset.imageUrl);
    });
}
  let currentImageIndex = 0;
  let autoplayInterval;
console.log(images);
  function updateMainImage(index) {
    currentImageIndex = index;
    document.getElementById('mainImage').src = images[index];
    document.getElementById('modalImage').src = images[index];
  }

  function openModal(index) {
    currentImageIndex = index;
    document.getElementById('modalImage').src = images[index];
    document.getElementById('imageModal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    stopAutoplay();
  }

  function closeModal() {
    document.getElementById('imageModal').classList.add('hidden');
    document.body.style.overflow = 'auto';
    startAutoplay();
  }

  function changeImage(direction) {
    currentImageIndex = (currentImageIndex + direction + images.length) % images.length;
    document.getElementById('modalImage').src = images[currentImageIndex];
  }

  function startAutoplay() {
    autoplayInterval = setInterval(() => {
      currentImageIndex = (currentImageIndex + 1) % images.length;
      updateMainImage(currentImageIndex);
    }, 3000);
  }

  function stopAutoplay() {
    clearInterval(autoplayInterval);
  }

  // Close modal when clicking outside the image
  document.getElementById('imageModal').addEventListener('click', function(e) {
    if (e.target === this) {
      closeModal();
    }
  });

  // Keyboard navigation
  document.addEventListener('keydown', function(e) {
    if (document.getElementById('imageModal').classList.contains('hidden')) return;
    
    if (e.key === 'Escape') closeModal();
    if (e.key === 'ArrowLeft') changeImage(-1);
    if (e.key === 'ArrowRight') changeImage(1);
  });

  // Start autoplay on page load
  startAutoplay();

  // Pause autoplay when hovering over thumbnails
  document.getElementById('thumbnailContainer').addEventListener('mouseenter', stopAutoplay);
  document.getElementById('thumbnailContainer').addEventListener('mouseleave', startAutoplay);
