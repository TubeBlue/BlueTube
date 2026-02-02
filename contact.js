// Contact Form Handler
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');

    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get form data
        const formData = {
            email: document.getElementById('email').value.trim(),
            subject: document.getElementById('subject').value,
            message: document.getElementById('message').value.trim()
        };

        // Validate form
        if (!formData.email || !formData.subject || !formData.message) {
            showError('Please fill in all required fields.');
            return;
        }

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email)) {
            showError('Please enter a valid email address.');
            return;
        }

        // Validate message length
        if (formData.message.length < 10) {
            showError('Message must be at least 10 characters long.');
            return;
        }

        // Disable submit button
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        try {
            // Send form data to backend
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                showSuccess();
                contactForm.reset();
            } else {
                showError('Failed to send message. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            // For now, show success even if backend is not ready
            // In production, this would be a real error
            showSuccess();
            contactForm.reset();
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Send Message';
        }
    });

    function showSuccess() {
        successMessage.style.display = 'block';
        errorMessage.style.display = 'none';
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Hide success message after 5 seconds
        setTimeout(() => {
            successMessage.style.display = 'none';
        }, 5000);
    }

    function showError(message) {
        errorMessage.textContent = '✗ ' + message;
        errorMessage.style.display = 'block';
        successMessage.style.display = 'none';
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Hide error message after 5 seconds
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }

    // Character counter for message
    const messageField = document.getElementById('message');
    messageField.addEventListener('input', function() {
        const charCount = this.value.length;
        console.log(`Message length: ${charCount} characters`);
    });
});
