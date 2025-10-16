document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submit-btn');
    const symptomsInput = document.getElementById('symptoms');
    const loader = document.getElementById('loader');
    const responseOutput = document.getElementById('response-output');
    const apiEndpoint = '/check_symptoms'; // Use a relative path

    // Event Listeners
    submitBtn.addEventListener('click', handleSymptomCheck);

    // Allow submission with Enter key (but not Shift+Enter for a new line)
    symptomsInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSymptomCheck();
        }
    });

    /**
     * Handles the form submission, validation, and API call.
     */
    async function handleSymptomCheck() {
        const symptoms = symptomsInput.value.trim();

        if (!symptoms) {
            showError("Please describe your symptoms before analyzing.");
            return;
        }

        // --- Update UI to show loading state ---
        responseOutput.innerHTML = '';
        responseOutput.classList.remove('visible');
        loader.classList.remove('hidden');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Analyzing...';

        try {
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symptoms }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'An unknown network error occurred.');
            }

            const data = await response.json();
            const formattedResponse = parseAndFormatResponse(data.result);
            responseOutput.innerHTML = formattedResponse;

        } catch (error) {
            console.error("API call failed:", error);
            showError(
                `Could not get a response. Please check if the backend server is running and try again.
                <br><small>${error.message}</small>`
            );
        } finally {
            loader.classList.add('hidden');
            responseOutput.classList.add('visible');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Analyze Symptoms';
        }
    }


    function showError(message) {
        responseOutput.innerHTML = `<div class="error-message">${message}</div>`;
        responseOutput.classList.add('visible');
    }


    function parseAndFormatResponse(text) {
        if (!text) return '';

        let html = '';
        let inList = false;

        // Split the entire response into individual lines
        const lines = text.split('\n');

        for (let line of lines) {
            // Sanitize and apply inline formatting like **bold**
            line = line
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

            const trimmedLine = line.trim();

            // Skip empty lines
            if (trimmedLine === '') {
                if (inList) {
                    html += '</ul>'; // End any open list
                    inList = false;
                }
                continue;
            }

            if (
                trimmedLine.startsWith('<strong>') &&
                trimmedLine.endsWith('</strong>') &&
                trimmedLine.includes(':')
            ) {
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                const content = trimmedLine.substring(8, trimmedLine.length - 9);
                html += `<h3 class="result-heading">${content}</h3>`;
            }

            else if (trimmedLine.startsWith('*')) {
                if (!inList) {
                    html += '<ul>';
                    inList = true;
                }
                const content = trimmedLine.substring(1).trim();
                html += `<li>${content}</li>`;
            }

            else if (trimmedLine.includes('IMPORTANT DISCLAIMER:')) {
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                html += '<hr>'
                html += `<div class="disclaimer-box">${trimmedLine}</div>`;
            }

            else {
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                html += `<p>${trimmedLine}</p>`;
            }
        }

        if (inList) {
            html += '</ul>';
        }

        return html;
    }
});
