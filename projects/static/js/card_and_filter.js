// Fetch products from API
let products = [];

async function fetchProducts() {
  try {
    const response = await fetch('/products/json/');
    const data = await response.json();
    products = data.products;
    renderProducts(products);
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

function createProductCard(product) {
  const stars = Array(5)
    .fill()
    .map((_, i) => {
      if (i < Math.floor(product.rating)) return '<i class="fas fa-star"></i>';
      if (i === Math.floor(product.rating) && product.rating % 1 !== 0)
        return '<i class="fas fa-star-half-alt"></i>';
      return '<i class="far fa-star"></i>';
    })
    .join("");

  const date = new Date(product.uploadDate);
  const uploadDate = `${date.getDate().toString().padStart(2, "0")}/${(
    date.getMonth() + 1
  )
    .toString()
    .padStart(2, "0")}/${date.getFullYear()}`;

  // Truncate description to 100 characters and add ellipsis if needed
  const truncatedDescription = product.description.length > 100 
    ? product.description.substring(0, 100) + '...'
    : product.description;

  return `
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-xl transition-all duration-300 p-4 border border-gray-100 dark:border-gray-700 transform hover:-translate-y-1">
            <div class="relative group">
                <a href="/projects/detail/${product.id}">
                    <img src="/media/${product.image}" loading="lazy" alt="${product.title}" class="w-full h-48 object-cover rounded-lg mb-4">
                </a>
                <span class="absolute top-2 right-2 bg-purple-600 text-white px-2 py-1 rounded-lg text-sm">${product.badge}</span>
                <div class="absolute inset-0 bg-black bg-opacity-40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg flex items-center justify-center">
                    <button class="px-4 py-2 bg-white dark:bg-gray-800 text-purple-600 dark:text-purple-400 rounded-lg transform hover:scale-105 transition-transform">
                        <i class="fas fa-play-circle mr-2"></i>Watch Preview
                    </button>
                </div>
            </div>
            <h3 class="text-lg sm:text-xl font-semibold text-gray-800 dark:text-white mb-2">${product.title}</h3>
            <p class="text-gray-600 dark:text-gray-400 mb-2 text-sm sm:text-base line-clamp-2">${truncatedDescription}</p>
            <p class="text-gray-500 dark:text-gray-400 text-sm mb-4">Upload date: ${uploadDate}</p>
            <div class="flex justify-between items-center">
                <div class="space-y-1">
                    <span class="text-purple-600 dark:text-purple-400 font-bold text-lg sm:text-xl">$${product.price}</span>
                    <div class="flex items-center">
                        <div class="flex text-yellow-400">
                            ${stars}
                        </div>
                        <span class="text-gray-500 dark:text-gray-400 text-sm ml-2">(${product.rating})</span>
                    </div>
                </div>
                <a href="/products/detail/${product.slug}" class="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all duration-300 text-sm sm:text-base shadow-md hover:shadow-lg transform hover:-translate-y-0.5">
                    <i class="fas fa-play-circle mr-2"></i>Demo
                </a>
            </div>
        </div>
    `;
}

function renderProducts(filteredProducts) {
  const productsGrid = document.getElementById("products-grid");
  if (!productsGrid) return;
  
  productsGrid.innerHTML = filteredProducts
    .map((product) => createProductCard(product))
    .join("");
}

function filterByCategory(category) {
  // Filter products
  const filteredProducts =
    category === "all"
      ? products
      : products.filter((product) => product.category === category);
  
  // Update button styles
  const buttons = document.querySelectorAll('.category-btn');
  buttons.forEach(btn => {
    // Reset all buttons to default style
    btn.className = "px-4 py-2 text-sm text-purple-600 transition-all duration-300 rounded-full category-btn sm:px-6 bg-purple-50 dark:bg-gray-700 dark:text-purple-400 hover:bg-purple-100 dark:hover:bg-gray-600 sm:text-base";
  });
  
  // Set active button style
  const activeBtn = document.getElementById(`${category}-btn`);
  if (activeBtn) {
    activeBtn.className = "category-btn px-4 sm:px-6 py-2 rounded-full bg-purple-600 text-white hover:bg-purple-700 transition-all duration-300 text-sm sm:text-base shadow-md hover:shadow-lg transform hover:-translate-y-0.5";
  }

  renderProducts(filteredProducts);
}

function applyFilters() {
  let filteredProducts = [...products];

  // Technology filters
  const selectedTechnologies = Array.from(
    document.querySelectorAll("#language-filters input:checked")
  ).map((checkbox) => checkbox.value);
  if (selectedTechnologies.length > 0) {
    filteredProducts = filteredProducts.filter((product) =>
      selectedTechnologies.some(tech => product.technologies.includes(tech))
    );
  }

  // Date filter
  const selectedDate = document.querySelector(
    'input[name="upload-date"]:checked'
  )?.value;
  if (selectedDate) {
    const now = new Date();
    const filterDate = new Date();
    switch (selectedDate) {
      case "24h":
        filterDate.setDate(now.getDate() - 1);
        break;
      case "7d":
        filterDate.setDate(now.getDate() - 7);
        break;
      case "30d":
        filterDate.setMonth(now.getMonth() - 1);
        break;
      case "365d":
        filterDate.setFullYear(now.getFullYear() - 1);
        break;
    }
    filteredProducts = filteredProducts.filter(
      (product) => new Date(product.uploadDate) >= filterDate
    );
  }

  renderProducts(filteredProducts);
  toggleFilterSidebar();
}

// Initial fetch and render
document.addEventListener('DOMContentLoaded', fetchProducts);
