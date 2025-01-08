
document.addEventListener('DOMContentLoaded', function() {
    const commonConfig = {
        multiple: true,
        search: true,
        showSelectedOptionsFirst: true,
        hideClearButton: false,
        markSearchResults: true,
        showDropboxAsPopup: true,
        popupDropboxBreakpoint: '640px',
        maxWidth: '100%',
        hiddenInputName: true,
        name: 'technology[]',
        required: true,
        dropboxWrapper: 'body',
        position: 'auto',
        showDropboxAsPopup: true,
        popupDropboxBreakpoint: '640px',
        zIndex: 9999,
        afterDropboxOpen: (vsObj) => {
            const dropbox = vsObj.dropboxWrapper.querySelector('.vscomp-dropbox');
            const toggleButton = vsObj.container.querySelector('.vscomp-toggle-button');
            
            if (dropbox && toggleButton) {
                const rect = toggleButton.getBoundingClientRect();
                dropbox.style.top = `${rect.bottom + 8}px`;
                dropbox.style.left = `${rect.left}px`;
                
                // Check if dropdown goes beyond viewport
                const dropboxRect = dropbox.getBoundingClientRect();
                const viewportWidth = window.innerWidth;
                
                if (dropboxRect.right > viewportWidth) {
                    dropbox.style.left = `${viewportWidth - dropboxRect.width - 16}px`;
                }
            }
        }
    };

    // Initialize selects with enhanced config
    const initSelect = (elementId, options, placeholder) => {
        VirtualSelect.init({
            ...commonConfig,
            ele: elementId,
            options: options,
            placeholder: placeholder,
            // Enhanced option renderer
            optionRenderer: (option) => {
                return `
                    <div class="flex items-center justify-between w-full py-1">
                        <div class="flex items-center gap-3">
                            <div class="vscomp-option-checkbox"></div>
                            <div class="flex flex-col">
                                <span class="font-medium">${option.label}</span>
                            </div>
                        </div>
                        <span class="selected-badge opacity-0 transition-opacity duration-200">
                            Selected
                        </span>
                    </div>
                `;
            },
            // After dropbox opens
            afterDropboxOpen: (vsObj) => {
                requestAnimationFrame(() => {
                    updateDropboxPosition(vsObj.container);
                });
            }
        });

        // Add scroll and resize listeners
        ['scroll', 'resize'].forEach(event => {
            window.addEventListener(event, () => {
                const wrapper = document.querySelector(elementId);
                if (wrapper?.classList.contains('show-dropdown')) {
                    requestAnimationFrame(() => updateDropboxPosition(wrapper));
                }
            }, { passive: true });
        });
    };
   
    const techSelect = document.getElementById('technologies-select');
    const techOptions = JSON.parse(techSelect.dataset.options);
    const dbSelect = document.getElementById('database-select');
    const dbOptions = JSON.parse(dbSelect.dataset.options);


    // Initialize selects
    initSelect('#technologies-select', 
       techOptions,
        'Select technologies'
    );

    initSelect('#database-select',
        dbOptions,
        'Select databases'
    );

});


const addImageField = () => {
    const newImageField = document.createElement('input');
    newImageField.type = 'file';
    newImageField.name = 'image';
    newImageField.accept = '.jpg, .png';
    newImageField.classList.add('file-input', 'file-input-bordered', 'file-input-primary', 'w-full', 'bg-gray-50', 'dark:bg-gray-700', 'images-list', 'text-sm', 'sm:text-base');
    

     // Xatolik uchun container yaratish
    const errorContainer = document.createElement('div');
    errorContainer.classList.add('mt-2', 'text-red-600', 'hidden');  // Xatolikni yashirish
    errorContainer.innerText = 'Iltimos, faqat .jpg, yoki .png formatidagi faylni tanlang!';

    
    // Fayl tanlanganidan keyin tekshiruv
    newImageField.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const fileType = file.type;
            const validTypes = ['image/jpg', 'image/png'];

            if (!validTypes.includes(fileType)) {
               // alert('Iltimos, faqat .jpg, yoki .png formatidagi faylni tanlang!');
                errorContainer.classList.remove('hidden');

                newImageField.value = '';  // Faylni tozalash
            }
            else {
                // Xatolikni yashirish
                errorContainer.classList.add('hidden');
            }
        }
    });

    const imageContainer = document.getElementById('image-container');
    const wrapper = document.createElement('div');
    wrapper.classList.add('flex', 'items-center', 'space-x-4');
    wrapper.appendChild(newImageField);
    wrapper.appendChild(errorContainer);  // Xatolikni wrapperga qo'shish

    imageContainer.appendChild(wrapper);
};

const check_images = () => {
    // Barcha inputlar uchun ishlash
    const imageFields = document.querySelectorAll('input[name="image"]');

    imageFields.forEach((newImageField) => {
        newImageField.accept = '.jpg,.jpeg,.png';  // .jpg, .jpeg, .png fayllarini qabul qilish
        newImageField.classList.add('file-input', 'file-input-bordered', 'file-input-primary', 'w-full', 'bg-gray-50', 'dark:bg-gray-700', 'images-list', 'text-sm', 'sm:text-base');

        // Xatolik uchun container yaratish
        const errorContainer = document.createElement('div');
        errorContainer.classList.add('mt-2', 'text-red-600', 'hidden');  // Xatolikni yashirish
        errorContainer.innerText = 'Iltimos, faqat .jpg, yoki .png formatidagi faylni tanlang!';

        // Fayl tanlanganidan keyin tekshiruv
        newImageField.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                const fileType = file.type;
                const validTypes = ['image/jpeg', 'image/png'];

                if (!validTypes.includes(fileType)) {
                    // Xatolikni ko'rsatish
                    errorContainer.classList.remove('hidden');
                    newImageField.value = '';  // Faylni tozalash
                } else {
                    // Xatolikni yashirish
                    errorContainer.classList.add('hidden');
                }
            }
        });

        // Yangi wrapper yaratish va errorContainerni unga qo'shish
        const wrapper = document.createElement('div');
        wrapper.classList.add('flex', 'items-center', 'space-x-4');
        wrapper.appendChild(newImageField);
        wrapper.appendChild(errorContainer);  // Xatolikni wrapperga qo'shish

        // Fayl inputining parent containeriga qo'shish
        const imageContainer = document.getElementById('image-container');
        imageContainer.appendChild(wrapper);
    });
};

// Bu funksiya ishga tushurilganida barcha input[name="image"] elementlar tekshiriladi
check_images();


const addZipFileValidation = () => {
    const zipFileInput = document.getElementById('id_zip_file'); // zip_file inputini olish

    // Fayl tanlanganidan keyin tekshiruv
    zipFileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const fileType = file.name.split('.').pop().toLowerCase(); // Fayl kengaytmasini olish
            const validTypes = ['zip', 'rar', '7z'];

            if (!validTypes.includes(fileType)) {
                // Xatolikni ko'rsatish
                alert('Iltimos, faqat .zip, .rar, yoki .7z formatidagi faylni tanlang!');
                zipFileInput.value = '';  // Faylni tozalash
            }
        }
    });
};

// Bu funksiya ishga tushurilganda zip faylni tekshirish boshlanadi
addZipFileValidation();
