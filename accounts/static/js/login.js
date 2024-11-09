document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const loginForm = document.getElementById('loginForm');
    const togglePasswordBtn = document.querySelector('button[aria-label="Toggle password visibility"]');
    const passwordInput = document.getElementById('password');
    const submitBtn = document.querySelector('button[type="submit"]');
    const googleBtn = document.querySelector('button[type="button"]');
    const inputs = document.querySelectorAll('input');

    // Add smooth focus animations for form inputs
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('scale-[1.02]', 'transition-transform', 'duration-300');
        });
        
        input.addEventListener('blur', () => {
            input.parentElement.classList.remove('scale-[1.02]');
        });
    });

    // Enhanced password visibility toggle with animations
    togglePasswordBtn.addEventListener('click', function() {
        const icon = this.querySelector('i');
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);

        // Animate icon transition
        icon.classList.add('transition-opacity', 'duration-150', 'opacity-0');
        
        setTimeout(() => {
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
            icon.classList.remove('opacity-0');
        }, 150);
    });

    // Form submission with loading and success/error states
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            username: document.getElementById('username').value,
            password: passwordInput.value,
            remember: document.getElementById('remember').checked
        };

        // Add loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <div class="flex items-center justify-center">
                <i class="fas fa-spinner fa-spin mr-2"></i>
                <span>Signing in...</span>
            </div>
        `;
        submitBtn.classList.add('opacity-75');

        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1500));
            console.log('Login attempt:', formData);
            
            // Success animation
            submitBtn.innerHTML = `
                <div class="flex items-center justify-center">
                    <i class="fas fa-check mr-2"></i>
                    <span>Success!</span>
                </div>
            `;
            submitBtn.classList.remove('from-purple-600', 'to-blue-600');
            submitBtn.classList.add('from-green-500', 'to-green-600');

        } catch (error) {
            console.error('Login failed:', error);
            submitBtn.innerHTML = `
                <div class="flex items-center justify-center">
                    <i class="fas fa-times mr-2"></i>
                    <span>Error</span>
                </div>
            `;
            submitBtn.classList.remove('from-purple-600', 'to-blue-600');
            submitBtn.classList.add('from-red-500', 'to-red-600');
        } finally {
            setTimeout(() => {
                submitBtn.innerHTML = `
                    <span>Sign In</span>
                `;
                submitBtn.disabled = false;
                submitBtn.classList.remove('opacity-75');
                submitBtn.classList.remove('from-green-500', 'to-green-600', 'from-red-500', 'to-red-600');
                submitBtn.classList.add('from-purple-600', 'to-blue-600');
            }, 2000);
        }
    });

    // Google Sign In button animation
    googleBtn.addEventListener('click', function() {
        this.classList.add('scale-95', 'transition-transform', 'duration-150');
        
        setTimeout(() => {
            this.classList.remove('scale-95');
            console.log('Google sign in initiated');
        }, 150);
    });
});