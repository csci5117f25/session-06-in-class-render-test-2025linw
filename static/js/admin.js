const guestListDelete = document.getElementById('guest-list');

// Add delete function to delete button
guestListDelete.querySelectorAll('button').forEach(butt => {
  const id = butt.id.split('-')[1];

  console.log(id);

  butt.addEventListener('click', () => {
    deleteGuest(id);
  })
})


async function deleteGuest(id) {
  console.log(id);

  try {
    const res = await fetch(`/api/guests/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    switch (res.status) {
      case 204:
        window.location.href = '/';

        break;
      case 500:
        window.location.href = '/';

        break;
      default:
        break;
    }
  } catch (e) {
    return;
  }
}
