// 좋아요 비동기 처리
const likeBtn = document.querySelector('#likeBtn')
likeBtn.addEventListener('click', function (event) {
    axios({
        method: 'GET',
        url: `/snacks/likes/${event.target.dataset.snackId}/`
    })
        .then(response => {
            if (response.data.existed_user === true) {
                event.target.classList.add('bi-bookmark-heart-fill')
                event.target.classList.remove('bi-bookmark-heart')
            }
            else {
                event.target.classList.add('bi-bookmark-heart')
                event.target.classList.remove('bi-bookmark-heart-fill')

            }
            const likeCount = document.querySelector('#like-count')
            likeCount.innerText = response.data.likeCount
        })
})
