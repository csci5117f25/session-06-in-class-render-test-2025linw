const guestForm = document.getElementById('guest_form');
const guestNameInput = document.getElementById('guest_name');
const guestFormSubmit = document.getElementById('guest_submit');

guestForm.addEventListener('submit', submitButton);
guestNameInput.addEventListener('focus', function() {
  guestNameInput.style.color = 'black';
  guestNameInput.style.borderColor = '#ccc';
});
guestNameInput.addEventListener('keypress', async function(e) {
  if (e.code === 'Enter') {
    e.preventDefault();

    await submitButton();
  }
});
guestFormSubmit.addEventListener('click', submitButton);

async function submitButton() {
  if (guestNameInput.value === '' || guestNameInput.value.length < 3) {
    guestNameInput.style.borderColor = 'red';

    return;
  }

  try {
    const res = await fetch('/api/guests', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        guest_name: guestNameInput.value,
      }),
    });

      if (res.status === 201) {
        window.location.href = '/';
      }
  } catch (e) {
    return;
  }
}
