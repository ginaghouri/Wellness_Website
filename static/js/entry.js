
function editUpdating() {
    // enable editing.
    document.getElementById('entry').readOnly = false;

    // show save button.
    const save = document.getElementById('save-update');
    save.style.display = 'block';

    // hide update button.
    const update = document.querySelector('button[onclick="editUpdating()"]');
    update.style.display = 'none';

    // hide delete button.
    const del = document.getElementById('delete');
    del.style.display = 'none';
};
