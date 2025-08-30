function addComment(doctorId) {
    fetch(`/api/doctors/${doctorId}/comments`, {
        method: 'post',
        body: JSON.stringify({
            'content': document.getElementById('content').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(c => {

        let m = document.getElementById("myComments");
        m.innerHTML = `
           <li class="list-group-item">
                <div class="row">
                    <div class="col-md-1 md-4">
                        <img class="img-fluid rounded-circle"
                             src="${c.user.avatar}"/>
                    </div>
                    <div class="col-md-11 md-8">
                        <p>${c.content}</p>
                        <p class="created-date">${moment(c.created_date).locale('vi').fromNow()}</p>
                    </div>
                </div>
            </li>
        ` + m.innerHTML;
    })
}