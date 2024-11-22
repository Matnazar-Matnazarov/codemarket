 // Generate random pastel color
 function getRandomPastelColor() {
    const hue = Math.floor(Math.random() * 360);
    return `hsl(${hue}, 70%, 80%)`;
}

// Generate initials from username/email
function getInitials(username) {
    return username
        .split('@')[0] // Remove email domain
        .match(/\b\w/g) // Get first letter of each word
        .slice(0, 2) // Take first two initials
        .join('')
        .toUpperCase();
}

// Initialize avatars
function initializeAvatars() {
    const avatarPlaceholder = document.getElementById('avatar-placeholder');
    if (avatarPlaceholder) {
        const username = '{{ user.email }}';
        avatarPlaceholder.style.backgroundColor = getRandomPastelColor();
        avatarPlaceholder.textContent = getInitials(username);
    }

    document.querySelectorAll('.user-avatar').forEach(avatar => {
        const username = avatar.dataset.username;
        avatar.style.backgroundColor = getRandomPastelColor();
        avatar.textContent = getInitials(username);
    });
}

// Initialize avatars on page load
initializeAvatars();

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
            // Create new comment element with enhanced animation
            const newComment = document.createElement("div");
            newComment.className = "p-6 bg-white dark:bg-gray-800/50 rounded-xl shadow-sm hover:shadow-xl transition-all duration-500 transform hover:-translate-y-1 border border-purple-100 dark:border-purple-900/50 opacity-0 translate-y-4";
            
            const avatarHtml = data.picture ? 
                `<img src="${data.picture}" alt="${data.username}" class="w-14 h-14 rounded-full shadow-md ring-2 ring-purple-300 dark:ring-purple-700 object-cover">` :
                `<div class="user-avatar w-14 h-14 rounded-full shadow-md ring-2 ring-purple-300 dark:ring-purple-700 flex items-center justify-center text-white font-semibold text-xl" style="background-color: ${getRandomPastelColor()}">${getInitials(data.username)}</div>`;

            newComment.innerHTML = `
                <div class="flex items-center mb-4">
                    <div class="relative">
                        ${avatarHtml}
                        <div class="absolute -bottom-1 -right-1 bg-purple-500 w-3 h-3 rounded-full border-2 border-white dark:border-gray-800"></div>
                    </div>
                    <div class="ml-4">
                        <h3 class="font-semibold text-gray-800 dark:text-gray-200 text-lg flex items-center">
                            ${data.username}
                        </h3>
                        <p class="text-sm text-gray-500 dark:text-gray-400 flex items-center">
                            <i class="far fa-clock mr-1"></i>
                            just now
                        </p>
                    </div>
                </div>
                <p class="text-gray-700 dark:text-gray-300 text-lg leading-relaxed">${data.comment}</p>
            `;

            // Update comments container with enhanced animation
            const emptyMessage = commentsContainer.querySelector(".py-16");
            if (emptyMessage) {
                emptyMessage.remove();
            }
            commentsContainer.insertBefore(newComment, commentsContainer.firstChild);
            requestAnimationFrame(() => {
                newComment.style.opacity = "1";
                newComment.style.transform = "translateY(0)";
            });

            // Animate comment count update
            const currentCount = parseInt(commentsCount.textContent) + 1;
            commentsCount.textContent = currentCount;
            commentCount.textContent = currentCount;
            commentsCount.classList.add("animate-bounce");
            setTimeout(() => commentsCount.classList.remove("animate-bounce"), 1000);

            // Enhanced success message
            responseMessage.innerHTML = `
                <div class="bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 p-5 rounded-xl shadow-lg transform transition-all duration-500 flex items-center space-x-3">
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
            <div class="bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 p-5 rounded-xl shadow-lg transform transition-all duration-500 flex items-center space-x-3">
                <i class="fas fa-exclamation-circle text-xl"></i>
                <span>${error.message}</span>
            </div>
        `;
    }

    // Enhanced auto-hide animation
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
