

const editBtn=document.querySelectorAll('.edit');
const posts = document.querySelectorAll('.post')
const likeBtn = document.querySelectorAll('.heart')
const user = document.querySelector('#currentuser').innerHTML

// editing
editBtn.forEach(btn => {
    btn.addEventListener('click', ()=> {
       posts.forEach(post => {
        if(btn.name === post.getAttribute('name')) {
            if(post.classList.contains('open')){
                const textarea=document.createElement('textarea')
                const save = document.createElement('button')
                save.classList.add('save');
                save.classList.add('btn');
                save.classList.add('btn-primary');
                save.innerText = 'save';
                textarea.value = post.querySelector('.msg').innerHTML
                post.querySelector('.edit').classList.add('closed')
                save.classList.add('open')
                textarea.classList.add('open')
                post.append(textarea)
                post.append(save)
                post.querySelector('.msg').replaceWith(textarea)

                save.addEventListener('click', ()=> {
                    if(textarea.value.length !== 0){
                    save.classList.add('closed')
                    save.classList.remove('open')
                    textarea.classList.add('closed')
                    post.querySelector('.edit').classList.remove('closed')
                    const msg = document.createElement('p')
                    msg.innerText = textarea.value
                    msg.classList.add('msg')
                    post.querySelector('textarea').replaceWith(msg)
                    
                    fetch(`/posts/${post.getAttribute('name')}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                          message: msg.innerText
                        }),
                        
                      }
                      
                      );
                    } else {
                        alert('Field is empty!')
                    }
                    
                      
                     
                })
            }
          

            


         
        }
       })
    })
})



// liking the post
posts.forEach(post => {  
likeBtn.forEach(like => {

    if(like.getAttribute('name') === post.getAttribute('name')){
        fetch(`post/${post.getAttribute('name')}`)
.then(response=> response.json())
.then(result => {
post.querySelector('.likes').innerHTML = parseInt(result.post.likes.length)
   if(result.status === true){
    like.classList.add('liked')
    like.innerHTML = '&#10084;';
   }
   else {
    like.classList.remove('liked')
    like.innerHTML = '&#9825;';
   }
   

   like.addEventListener('click', ()=> {
    fetch(like.classList.contains('liked') ? 
        `posts/${like.getAttribute('name')}/unlike`: 
        `posts/${like.getAttribute('name')}/like`, {
            method: 'POST',
            body: JSON.stringify({
                likes: "{{request.user}}"
            })
        })
       
    if(!like.classList.contains('liked')){
        like.classList.add('liked')
        like.innerHTML = '&#10084;';
        post.querySelector('.likes').innerHTML = parseInt(result.post.likes.length) + 1;
        
    } else {
        like.classList.remove('liked');
        like.innerHTML = '&#9825;';
        post.querySelector('.likes').innerHTML = parseInt(result.post.likes.length) - 1;
    }
    
    
    
  
})
}) 

   
        }
    })
  
})


