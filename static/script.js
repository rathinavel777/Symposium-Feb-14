document.addEventListener('DOMContentLoaded', () => {
    
    // Accommodation Logic
    const accomodationRadios = document.querySelectorAll('input[name="accommodation"]');
    const accomodationNote = document.getElementById('accommodation-note');

    accomodationRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
            if (e.target.value === 'Yes') {
                accomodationNote.style.display = 'block';
                accomodationNote.classList.add('animate-fade');
            } else {
                accomodationNote.style.display = 'none';
            }
        });
    });

    // Checkbox styling toggle
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(cb => {
        cb.addEventListener('change', (e) => {
            if (e.target.checked) {
                e.target.parentElement.classList.add('selected');
            } else {
                e.target.parentElement.classList.remove('selected');
            }
        });
    });

    // Form Submission
    const form = document.getElementById('reg-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Registering...';

            // Collect data
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Handle checkboxes manually as FormData doesn't group same-name keys well in basic JSON conversion
            const events = [];
            form.querySelectorAll('input[name="events"]:checked').forEach(cb => {
                events.push(cb.value);
            });
            data.events = events;

            try {
                const response = await fetch('/api/register', {
                    headers: { 'Content-Type': 'application/json' },
                    method: 'POST',
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();

                if (result.success) {
                    window.location.href = '/success';
                } else {
                    alert('Registration Failed: ' + result.message);
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Register Now';
                }
            } catch (error) {
                alert('An error occurred. Please try again.');
                console.error(error);
                submitBtn.disabled = false;
                submitBtn.textContent = 'Register Now';
            }
        });
    }
});
