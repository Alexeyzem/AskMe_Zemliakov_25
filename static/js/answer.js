const init2 = ()=>{
    const answers = document.querySelectorAll('.answer-card');
    for (const answer of answers) {
        const likeButton = answer.querySelector('.answer-like-button');
        const dislikeButton = answer.querySelector('.answer-dislike-button');
        const counter = answer.querySelector('.answer-like-counter');
        const answerId = answer.dataset.answer_id;
        const checkingButton = answer.querySelector('.checkingAnswer');
        likeButton.addEventListener('click', () => {
            const request = new Request(`/answer_like_async/${answerId}`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    "action": "like"
                })
            })
            fetch(request)
                .then((response) => response.json())
                .then((data) => counter.innerHTML = data.likes_count)
        });

        dislikeButton.addEventListener('click', () => {
            const request = new Request(`/answer_like_async/${answerId}`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    "action": "dislike"
                })
            })
            fetch(request)
                .then((response) => response.json())
                .then((data) => counter.innerHTML = data.likes_count)
        });

        checkingButton.addEventListener('click', () => {
            const request = new Request(`/answer_correct_async/${answerId}`, {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            fetch(request)
                .then((response) => response.json())
        });
    }
};


init2()