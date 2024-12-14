function updateCharCount(textarea) {
    const maxLength = 500;
    const currentLength = textarea.value.length;
    const charCount = document.getElementById('char-count');
    const warning = document.getElementById('char-limit-warning');
    
    charCount.textContent = currentLength;
    
    // Add dynamic color changes based on length
    if (currentLength >= maxLength) {
        charCount.classList.add('text-red-500', 'dark:text-red-400');
        warning.classList.remove('hidden');
        warning.classList.add('flex');
    } else if (currentLength >= maxLength * 0.8) {
        charCount.classList.add('text-yellow-500', 'dark:text-yellow-400');
        charCount.classList.remove('text-red-500', 'dark:text-red-400');
        warning.classList.add('hidden');
    } else {
        charCount.classList.remove(
            'text-yellow-500',
            'dark:text-yellow-400',
            'text-red-500',
            'dark:text-red-400'
        );
        warning.classList.add('hidden');
    }
    
    // Add subtle scale animation on count change
    charCount.style.transform = 'scale(1.2)';
    setTimeout(() => {
        charCount.style.transform = 'scale(1)';
    }, 200);
}

// Reset character count after form submission
document.getElementById('comment-form').addEventListener('submit', function() {
    setTimeout(() => {
        document.getElementById('char-count').textContent = '0';
        document.getElementById('char-limit-warning').classList.add('hidden');
    }, 100);
});

// Generate random pastel color with improved contrast
function getRandomPastelColor() {
    const hue = Math.floor(Math.random() * 360);
    const saturation = Math.floor(Math.random() * (80 - 60) + 60);
    const lightness = Math.floor(Math.random() * (85 - 75) + 75);
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}

// Generate initials from username/email with improved handling
function getInitials(username) {
    if (!username) return '??';
    
    return username
        .split('@')[0]
        .split(/[\s._-]/)
        .filter(word => word.length > 0)
        .map(word => word[0])
        .slice(0, 2)
        .join('')
        .toUpperCase();
}

// Initialize avatars with improved error handling
function initializeAvatars() {
    try {
        const avatarPlaceholder = document.getElementById('avatar-placeholder');
        if (avatarPlaceholder) {
            const username = '{{ user.email }}';
            avatarPlaceholder.style.backgroundColor = getRandomPastelColor();
            avatarPlaceholder.textContent = getInitials(username);
        }

        document.querySelectorAll('.user-avatar').forEach(avatar => {
            const username = avatar.dataset.username;
            if (username) {
                avatar.style.backgroundColor = getRandomPastelColor();
                avatar.textContent = getInitials(username);
            }
        });
    } catch (error) {
        console.error('Error initializing avatars:', error);
    }
}

// Initialize avatars on page load
document.addEventListener('DOMContentLoaded', initializeAvatars);

// Enhanced comment submission handler with improved text wrapping
document.getElementById("comment-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const form = event.target;
    const responseMessage = document.getElementById("response-message");
    const commentsContainer = document.getElementById("comments-container");
    const commentsCount = document.getElementById("comments-count");
    const commentCount = document.getElementById("comment-count");
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            }
        });

        const data = await response.json();

        if (response.ok) {
            const newComment = document.createElement("div");
            newComment.className = [
                "p-6 bg-white dark:bg-gray-800/50 rounded-xl",
                "shadow-sm hover:shadow-xl transition-all duration-500",
                "transform hover:-translate-y-1",
                "border border-purple-100 dark:border-purple-900/50",
                "opacity-0 translate-y-4",
                "overflow-hidden"
            ].join(' ');
            
            const avatarHtml = data.picture 
                ? `<img src="${data.picture}" alt="${data.username}" 
                     class="w-14 h-14 rounded-full shadow-md ring-2 
                     ring-purple-300 dark:ring-purple-700 object-cover">`
                : `<div class="user-avatar w-14 h-14 rounded-full shadow-md 
                     ring-2 ring-purple-300 dark:ring-purple-700 flex items-center 
                     justify-center text-white font-semibold text-xl" 
                     style="background-color: ${getRandomPastelColor()}">
                     ${getInitials(data.username)}</div>`;

            newComment.innerHTML = `
                <div class="flex items-center mb-4">
                    <div class="relative">
                        ${avatarHtml}
                        <div class="absolute -bottom-1 -right-1 bg-purple-500 
                             w-3 h-3 rounded-full border-2 border-white 
                             dark:border-gray-800"></div>
                    </div>
                    <div class="ml-4">
                        <h3 class="font-semibold text-gray-800 dark:text-gray-200 
                            text-lg flex items-center">
                            ${data.username}
                        </h3>
                        <p class="text-sm text-gray-500 dark:text-gray-400 
                           flex items-center">
                            <i class="far fa-clock mr-1"></i>
                            just now
                        </p>
                    </div>
                </div>
                <div class="comment-content">
                    <p class="text-gray-700 dark:text-gray-300 text-lg leading-relaxed 
                       break-words whitespace-pre-line max-h-[300px] overflow-y-auto
                       scrollbar-thin scrollbar-thumb-purple-500 scrollbar-track-transparent
                       pr-2">${data.comment}</p>
                </div>
            `;

            const emptyMessage = commentsContainer.querySelector(".py-16");
            if (emptyMessage) {
                emptyMessage.remove();
            }

            commentsContainer.insertBefore(newComment, commentsContainer.firstChild);
            requestAnimationFrame(() => {
                newComment.style.opacity = "1";
                newComment.style.transform = "translateY(0)";
            });

            const currentCount = parseInt(commentsCount.textContent) + 1;
            commentsCount.textContent = currentCount;
            commentCount.textContent = currentCount;
            commentsCount.classList.add("animate-bounce");
            setTimeout(() => commentsCount.classList.remove("animate-bounce"), 1000);

            responseMessage.innerHTML = `
                <div class="bg-green-50 dark:bg-green-900/30 text-green-600 
                     dark:text-green-400 p-5 rounded-xl shadow-lg transform 
                     transition-all duration-500 flex items-center space-x-3">
                    <i class="fas fa-check-circle text-xl"></i>
                    <span>Comment posted successfully!</span>
                </div>
            `;

            form.reset();
        } else {
            throw new Error(data.errors || "Failed to post comment");
        }
    } catch (error) {
        responseMessage.innerHTML = `
            <div class="bg-red-50 dark:bg-red-900/30 text-red-600 
                 dark:text-red-400 p-5 rounded-xl shadow-lg transform 
                 transition-all duration-500 flex items-center space-x-3">
                <i class="fas fa-exclamation-circle text-xl"></i>
                <span>${error.message}</span>
            </div>
        `;
    }

    setTimeout(() => {
        responseMessage.style.transform = "translateX(100%)";
        responseMessage.style.opacity = "0";
        setTimeout(() => {
            responseMessage.innerHTML = "";
            responseMessage.style.transform = "";
            responseMessage.style.opacity = "";
        }, 500);
    }, 3000);
});
