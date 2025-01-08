let products=[];async function fetchProducts(){try{const response=await fetch('/products/json/');const data=await response.json();products=data.products;renderProducts(products);}catch(error){console.error('Error fetching products:',error);}}
function createProductCard(product){const stars=Array(5).fill().map((_,i)=>{if(i<Math.floor(product.rating))return'<i class="fas fa-star"></i>';if(i===Math.floor(product.rating)&&product.rating%1!==0)
return'<i class="fas fa-star-half-alt"></i>';return'<i class="far fa-star"></i>';}).join("");const date=new Date(product.uploadDate);const uploadDate=`${date.getDate().toString().padStart(2, "0")}/${(
    date.getMonth() + 1
  )
    .toString()
    .padStart(2, "0")}/${date.getFullYear()}`;const truncatedDescription=product.description.length>100?product.description.substring(0,100)+'...':product.description;return`
    <div class="group bg-white dark:bg-gray-800/95 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 p-5 border border-gray-100/10 dark:border-gray-700/50 transform hover:-translate-y-2">
        <div class="relative overflow-hidden rounded-xl">
            <a href="/projects/detail/${product.slug}">
                <img src="/media/${product.image}" loading="lazy" alt="${product.title}" 
                     class="w-full h-52 object-cover transform transition-transform duration-700 group-hover:scale-110">
            </a>
            <div class="absolute top-3 right-3 flex gap-2">
                <span class="bg-purple-600/90 backdrop-blur-sm text-white px-3 py-1.5 rounded-lg text-sm font-medium">
                    ${product.badge}
                </span>
                <span class="bg-gradient-to-r from-amber-500 to-orange-600 text-white px-3 py-1.5 rounded-lg text-sm font-medium flex items-center gap-1.5">
                    ${product.price}
                    <i class="fas fa-coins text-amber-300"></i>
                </span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-all duration-500 flex items-center justify-center">
                <button class="px-6 py-3 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm text-purple-600 dark:text-purple-400 rounded-xl transform hover:scale-105 transition-all duration-300 font-medium flex items-center gap-2 shadow-lg">
                    <i class="fas fa-play-circle text-lg"></i>
                    Watch Preview
                </button>
            </div>
        </div>
        
        <div class="mt-4 space-y-3">
            <h3 class="text-xl font-bold text-gray-800 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors duration-300">
                ${product.title}
            </h3>
            
            <p class="text-gray-600 dark:text-gray-400 text-sm line-clamp-2">
                ${truncatedDescription}
            </p>
            
            <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <div class="flex text-amber-400">
                        ${stars}
                    </div>
                    <span class="text-gray-500 dark:text-gray-400 text-sm">(${product.rating})</span>
                </div>
                <p class="text-gray-500 dark:text-gray-400 text-sm">
                    ${uploadDate}
                </p>
            </div>
            
            <div class="pt-4 flex justify-between items-center border-t border-gray-100 dark:border-gray-700/50">
                <div class="flex items-center gap-1.5">
                    <span class="text-2xl font-bold bg-gradient-to-r from-amber-500 to-orange-600 bg-clip-text text-transparent">
                        ${product.price}
                    </span>
                    <i class="fas fa-coins text-xl text-amber-500"></i>
                </div>
                
                <a href="/products/detail/${product.slug}" 
                   class="px-5 py-2.5 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-xl 
                          hover:from-purple-700 hover:to-blue-700 transition-all duration-300 
                          font-medium shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 
                          flex items-center gap-2">
                    <i class="fas fa-play-circle"></i>
                    Demo
                </a>
            </div>
        </div>
    </div>
  `;}
function renderProducts(filteredProducts){const productsGrid=document.getElementById("products-grid");if(!productsGrid)return;productsGrid.innerHTML=filteredProducts.map((product)=>createProductCard(product)).join("");}
function filterByCategory(category){const filteredProducts=category==="all"?products:products.filter((product)=>product.category===category);const buttons=document.querySelectorAll('.category-btn');buttons.forEach(btn=>{btn.className="px-4 py-2 text-sm text-purple-600 transition-all duration-300 rounded-full category-btn sm:px-6 bg-purple-50 dark:bg-gray-700 dark:text-purple-400 hover:bg-purple-100 dark:hover:bg-gray-600 sm:text-base";});const activeBtn=document.getElementById(`${category}-btn`);if(activeBtn){activeBtn.className="category-btn px-4 sm:px-6 py-2 rounded-full bg-purple-600 text-white hover:bg-purple-700 transition-all duration-300 text-sm sm:text-base shadow-md hover:shadow-lg transform hover:-translate-y-0.5";}
renderProducts(filteredProducts);}
function applyFilters(){let filteredProducts=[...products];const selectedTechnologies=Array.from(document.querySelectorAll("#language-filters input:checked")).map((checkbox)=>checkbox.value);if(selectedTechnologies.length>0){filteredProducts=filteredProducts.filter((product)=>selectedTechnologies.some(tech=>product.technologies.includes(tech)));}
const selectedDate=document.querySelector('input[name="upload-date"]:checked')?.value;if(selectedDate){const now=new Date();const filterDate=new Date();switch(selectedDate){case"24h":filterDate.setDate(now.getDate()-1);break;case"7d":filterDate.setDate(now.getDate()-7);break;case"30d":filterDate.setMonth(now.getMonth()-1);break;case"365d":filterDate.setFullYear(now.getFullYear()-1);break;}
filteredProducts=filteredProducts.filter((product)=>new Date(product.uploadDate)>=filterDate);}
renderProducts(filteredProducts);toggleFilterSidebar();}
document.addEventListener('DOMContentLoaded',fetchProducts);;