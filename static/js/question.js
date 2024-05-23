function getCookie(name){
    let cookieValue = null;
    if(document.cookie && document.cookie !== ''){
        const cookies = document.cookie.split(';')
        for (let i =0; i < cookies.length;i++){
            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length+1)===(name+'=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                break;
            }
        }
    }
    return cookieValue;
}


const init = ()=>{
    const questions = document.querySelectorAll('.question-card')
    for (const question of questions){
        const likeButton = question.querySelector('.question-like-button')
        const dislikeButton = question.querySelector('.question-dislike-button')
        const counter = question.querySelector('.question-like-counter')
        const questionId = question.dataset.question_id

        likeButton.addEventListener('click', ()=>{
            const request = new Request(`/like_async/${questionId}`, {
                method:'post',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    "action":"like"
                })
            })
            fetch(request)
                .then((response)=>response.json())
                .then((data)=>counter.innerHTML=data.likes_count)
        })

        dislikeButton.addEventListener('click', ()=>{
            const request = new Request(`/like_async/${questionId}`, {
                method:'post',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({
                    "action":"dislike"
                })
            })
            fetch(request)
                .then((response)=>response.json())
                .then((data)=>counter.innerHTML=data.likes_count)
        })
    }
}

init()