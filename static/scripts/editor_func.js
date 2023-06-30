function showPrev(dialog,frame, id) {
    frame.src = `/api/preview?id=${id}`;
    dialog.showModal();
}

function byePrev(dialog) {
    dialog.close();
}