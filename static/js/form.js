const guestForm = document.getElementById('guest-form');
const guestFormName = document.getElementById('guest-form-name');
const guestFormSubmit = document.getElementById('guest-form-submit');

// Form Submit
guestForm.addEventListener('submit', submitButton);

// Make name entry turn black on focus to undo `submitButton` error formatting
guestFormName.addEventListener('focus', function () {
  guestFormName.style.color = 'black';
  guestFormName.style.borderColor = '#ccc';
});

// Add `Enter` to submit form
guestFormName.addEventListener('keypress', async function (e) {
  if (e.code === 'Enter') {
    e.preventDefault();

    await submitButton();
  }
});

// Make submit button submit form
guestFormSubmit.addEventListener('click', submitButton);

// Function to make submit API call
async function submitButton() {
  if (guestFormName.value === '' || guestFormName.value.length < 3) {
    guestFormName.style.borderColor = 'red';

    return;
  }

  try {
    const res = await fetch('/api/guests', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        guest_name: guestFormName.value,
      }),
    });

    if (res.status === 201) {
      window.location.href = '/';
    }
  } catch (e) {
    return;
  }
}
