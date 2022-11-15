// 좋아요 비동기 처리
const likeBtn = document.querySelector('#likeBtn')
likeBtn.addEventListener('click', function (event) {
    axios({
        method: 'GET',
        url: `/snacks/likes/${event.target.dataset.snackId}/`
    })
        .then(response => {
            if (response.data.existed_user === true) {
                event.target.innerText = '찜하기 취소'
            }
            else {
                event.target.innerText = '찜하기'
            }
            const likeCount = document.querySelector('#like-count')
            likeCount.innerText = response.data.likeCount
        })
})
