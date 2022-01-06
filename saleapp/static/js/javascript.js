function addComment(roomId) {
    let content = document.getElementById('commentId')
    if(content !== null) {
        fetch('/api/comments', {
            method: 'post',
            body: JSON.stringify ({
                'room_id': roomId,
                'content': content.value
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if(data.status == 201) {
                let c = data.comment

                let area = document.getElementById('commentArea')

                area.innerHTML = `
                    <div class="row">
                        <div class="col-md-1 col-xs-4">
                            <img class="img-fluid rounded-circle" src="${c.user.avatar}" alt="avatar" />
                        </div>

                        <div class="col-md-11 col-xs-8">
                            <p>${c.content}</p>
                            <p><em>${moment(c.created_date).locale('vi').fromNow()}</em></p>
                        </div>
                    </div>
                ` + area.innerHTML //chèn cmt mới lên đầu
            } else if(data.status == 404)
                alert(data.err_msg)
    })
    }
}

