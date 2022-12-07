document.addEventListener('DOMContentLoaded', () => {
    document.querySelector("#heart").addEventListener('click', likeUnlike(`${id}`));
    document.querySelector(`#edit-${id}`).addEventListener('click', edit(id));
    document.querySelector(`#delete${id}`).addEventListener('click', delete_post(id));
    document.querySelector(`#theme`).addEventListener('click', theme())
});

function delete_post(id) {
    fetch(`/edit/${id}`,{
        method : "PUT",
        body: JSON.stringify({
            del : "delete"
        })
    })
    document.querySelector(`#card${id}`).style.display = 'none';
};
function theme(){
    console.log("hello")
    document.getElementById(`l`).style.backgroundColor="black"
}

function edit(id) {
    var text_area = document.querySelector(`#edit-area${id}`);
    var bttn = document.querySelector(`#edit-bttn${id}`);
    // var img_area = document.querySelector(`#edit-img${id}`);
    
    text_area.style.display= 'block';
    // img_area.style.display= 'block';
    bttn.style.display= 'block';
    // document.querySelector(`#content${id}`).innerHTML = text_area.value;
    fetch(`/edit/${id}`)
    .then(response=> response.json())
    .then(datas =>{
        console.log(datas.content_img)
        text_area.innerHTML = datas.content;
        // img_area.value = datas.content_img;
    })
    bttn.addEventListener('click', () => {
        fetch(`/edit/${id}`, {
            method : "PUT",
            body: JSON.stringify({
                del : text_area.value,
                
            })
        })
        text_area.style.display = 'none';
        // img_area.style.display = 'none'
        bttn.style.display = 'none';
        document.querySelector(`#content${id}`).innerHTML = text_area.value;
        // document.querySelector(`#img${id}`).innerHTML = img_area.value;
    })
}


function likeUnlike(id) {
    fetch(`/like/${id}`)
    // .then( lik => {
    //     console.log(lik)
    //     var like_ct = document.querySelector(`#lik-${id}`)
    //     like_ct.innerHTML = lik.likes;
    // })
    fetch(`/like/${id}`,{
        method: "PUT",
        body: JSON.stringify({
            liked : true
        }),
    })
    fetch(`/like/${id}`)
    .then(response => response.json())
    .then( lik => {
        console.log(lik.likes)
        var like_ct = document.querySelector(`#lik-${id}`)
        like_ct.innerHTML = lik.likes;        
    });
};
    // method: "POST",
    //     body: JSON.stringify({
    //         liked: true
    //     })



