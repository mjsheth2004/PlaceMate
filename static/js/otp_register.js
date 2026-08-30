/**
 * PlaceMate Email OTP Verification Client Handler
 * Manages Send OTP, 60s Resend Cooldown Timer, OTP Validation, and Form Submission Gates.
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const emailInput = document.getElementById('email');
    const sendOtpBtn = document.getElementById('btnSendOtp');
    const otpSection = document.getElementById('otpSection');
    const otpInput = document.getElementById('otpCodeInput');
    const verifyOtpBtn = document.getElementById('btnVerifyOtp');
    const otpMsg = document.getElementById('otpMessage');
    const emailVerifiedBadge = document.getElementById('emailVerifiedBadge');
    const resendTimerText = document.getElementById('resendTimerText');
    const submitBtn = document.querySelector('.btn-submit');

    if (!emailInput || !sendOtpBtn || !otpSection) return;

    let isEmailVerified = false;
    let timerInterval = null;
    let verifiedEmailAddress = '';

    // Ensure OTP box is hidden on load
    otpSection.style.display = 'none';

    // Get CSRF Token
    function getCsrfToken() {
        const tokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return tokenInput ? tokenInput.value : '';
    }

    // Email format validation
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function showMsg(text, type = 'error') {
        if (!otpMsg) return;
        otpMsg.textContent = text;
        otpMsg.className = 'otp-feedback-msg ' + type;
        otpMsg.style.display = 'block';
    }

    function startCooldown(seconds = 60) {
        sendOtpBtn.disabled = true;
        let remaining = seconds;
        
        if (resendTimerText) {
            resendTimerText.textContent = `(Resend in ${remaining}s)`;
        }

        if (timerInterval) clearInterval(timerInterval);

        timerInterval = setInterval(() => {
            remaining -= 1;
            if (remaining > 0) {
                if (resendTimerText) resendTimerText.textContent = `(Resend in ${remaining}s)`;
            } else {
                clearInterval(timerInterval);
                sendOtpBtn.disabled = false;
                sendOtpBtn.textContent = 'Resend OTP';
                if (resendTimerText) resendTimerText.textContent = '';
            }
        }, 1000);
    }

    // Reset if user modifies email
    emailInput.addEventListener('input', () => {
        if (isEmailVerified && emailInput.value.trim().toLowerCase() !== verifiedEmailAddress) {
            isEmailVerified = false;
            verifiedEmailAddress = '';
            if (emailVerifiedBadge) emailVerifiedBadge.style.display = 'none';
            sendOtpBtn.style.display = 'inline-flex';
            sendOtpBtn.disabled = false;
            sendOtpBtn.textContent = 'Send OTP';
            otpSection.style.display = 'none';
        }
    });

    // 1. Send OTP Action
    sendOtpBtn.addEventListener('click', async () => {
        const email = emailInput.value.trim();
        if (!email) {
            alert('Please enter your email address first.');
            emailInput.focus();
            return;
        }

        if (!isValidEmail(email)) {
            alert('Please enter a valid email address.');
            emailInput.focus();
            return;
        }

        sendOtpBtn.disabled = true;
        const originalText = sendOtpBtn.textContent;
        sendOtpBtn.textContent = 'Sending...';

        try {
            const formData = new FormData();
            formData.append('email', email);

            const response = await fetch('/send-otp/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                },
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                otpSection.style.display = 'block';
                showMsg(data.message, 'info');
                if (otpInput) {
                    otpInput.value = '';
                    otpInput.focus();
                }
                startCooldown(60);
            } else {
                sendOtpBtn.disabled = false;
                sendOtpBtn.textContent = originalText;
                showMsg(data.message, 'error');
                alert(data.message);
            }
        } catch (err) {
            console.error('Error sending OTP:', err);
            sendOtpBtn.disabled = false;
            sendOtpBtn.textContent = originalText;
            showMsg('Network error. Please check your connection and try again.', 'error');
        }
    });

    // 2. Verify OTP Action
    verifyOtpBtn.addEventListener('click', async () => {
        const email = emailInput.value.trim();
        const otp = otpInput ? otpInput.value.trim() : '';

        if (!otp || otp.length < 6) {
            showMsg('Please enter the complete 6-digit verification code.', 'error');
            if (otpInput) otpInput.focus();
            return;
        }

        verifyOtpBtn.disabled = true;
        verifyOtpBtn.textContent = 'Verifying...';

        try {
            const formData = new FormData();
            formData.append('email', email);
            formData.append('otp', otp);

            const response = await fetch('/verify-otp/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                },
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                isEmailVerified = true;
                verifiedEmailAddress = email.toLowerCase();
                showMsg('✓ Email verified successfully!', 'info');
                
                // Lock email field
                emailInput.readOnly = true;
                emailInput.style.backgroundColor = 'var(--color-surface-muted, rgba(42, 157, 143, 0.08))';
                
                // Hide send button and OTP box
                sendOtpBtn.style.display = 'none';
                otpSection.style.display = 'none';
                if (emailVerifiedBadge) {
                    emailVerifiedBadge.style.display = 'inline-flex';
                    emailVerifiedBadge.classList.add('active');
                }

                if (timerInterval) clearInterval(timerInterval);
            } else {
                verifyOtpBtn.disabled = false;
                verifyOtpBtn.textContent = 'Verify OTP';
                showMsg(data.message, 'error');
            }
        } catch (err) {
            console.error('Error verifying OTP:', err);
            verifyOtpBtn.disabled = false;
            verifyOtpBtn.textContent = 'Verify OTP';
            showMsg('Verification failed. Please try again.', 'error');
        }
    });

    // Allow Enter key inside OTP input to trigger verify
    if (otpInput) {
        otpInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                verifyOtpBtn.click();
            }
        });
    }

    // 3. Prevent form submission if email is not verified
    if (form) {
        form.addEventListener('submit', (e) => {
            if (!isEmailVerified) {
                e.preventDefault();
                alert('Please verify your email address with the OTP before submitting.');
                if (otpSection.style.display === 'block') {
                    if (otpInput) otpInput.focus();
                } else {
                    sendOtpBtn.click();
                }
            }
        });
    }
});
