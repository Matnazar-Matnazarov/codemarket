$(document).ready(function () {
    // Initialize Select2
    $('.select2').select2({
        placeholder: "Select technologies",
        allowClear: true,
        theme: "classic",
        width: '100%',
        closeOnSelect: false,
        tags: true,
        selectionCssClass: 'text-sm',
        dropdownCssClass: 'text-sm',
        tokenSeparators: [',', ' '],
        createTag: function (params) {
            return {
                id: params.term,
                text: params.term,
                newTag: true
            };
        },
        templateResult: function (data) {
            var $result = $("<span></span>");
            $result.text(data.text);
            if (data.newTag) {
                $result.append(" <em class='text-blue-500'>(new)</em>");
            }
            return $result;
        }
    });

    // Custom Tailwind Styling for Select2
    const select2BaseClass = 'bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg p-2 shadow-sm transition focus:ring-2 focus:ring-blue-500 focus:border-blue-500';
    const choiceClass = 'bg-blue-500 text-white rounded-lg px-2 py-1 mr-1 mb-1 flex items-center space-x-1';
    const removeClass = 'text-white hover:text-gray-200 transition';
    const searchFieldClass = 'bg-transparent focus:outline-none placeholder-gray-400 text-sm';

    $('.select2-container .select2-selection--multiple').addClass(select2BaseClass);
    $('.select2-container .select2-selection--multiple .select2-selection__choice').addClass(choiceClass);
    $('.select2-container .select2-selection--multiple .select2-selection__choice__remove').addClass(removeClass);
    $('.select2-container .select2-search--inline .select2-search__field').addClass(searchFieldClass);
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
