// profile
function editProfile() { 
    document.getElementById('name').classList.add('hidden'); 
    document.getElementById('email').classList.add('hidden'); 
    document.getElementById('phone').classList.add('hidden'); 
    document.getElementById('name-input').classList.remove('hidden'); 
    document.getElementById('email-input').classList.remove('hidden'); 
    document.getElementById('phone-input').classList.remove('hidden'); 
    document.getElementById('name-input').value = document.getElementById('name').innerText; 
    document.getElementById('email-input').value = document.getElementById('email').innerText; 
    document.getElementById('phone-input').value = document.getElementById('phone').innerText; 
    document.getElementById('save-button').classList.remove('hidden'); 
} 
function saveProfile() { 
    document.getElementById('name').innerText = document.getElementById('name-input').value; 
    document.getElementById('email').innerText = document.getElementById('email-input').value; 
    document.getElementById('phone').innerText = document.getElementById('phone-input').value; document.getElementById('name').classList.remove('hidden'); 
    document.getElementById('email').classList.remove('hidden'); 
    document.getElementById('phone').classList.remove('hidden'); 
    document.getElementById('name-input').classList.add('hidden'); 
    document.getElementById('email-input').classList.add('hidden'); 
    document.getElementById('phone-input').classList.add('hidden'); 
    document.getElementById('save-button').classList.add('hidden'); 
}
//menu
let offset01=$("div.wrapper>category>div.part>div.cart1").offset().top - 48

let offset02=$("div.wrapper>category>div.part:nth-of-type(2)").offset().top - 48

let offset03=$("div.wrapper>category>div.part:nth-of-type(3)").offset().top - 48

console.log(offset03);


$("#li1").on({
    click:function(){
        $("html,body").animate({
            scrollTop:offset01
        },500,"linear")
    }
})


$("#li2").on({
    click:function(){
        $("html,body").animate({
            scrollTop:offset02
        },500,"linear")
    }
})

$("#li3").on({
    click:function(){
        $("html,body").animate({
            scrollTop:offset03
        },500,"linear")
    }
})
//prof

// Preview selected image 
document.getElementById('profile-image').addEventListener('change', function(event) {
         const imagePreview = document.getElementById('image-preview');     
         const imageElement = document.getElementById('image-preview-element');     
         const file = event.target.files[0];     
         if (file) {         
            const reader = new FileReader();         
            reader.onload = function(e) {             
                imageElement.src = e.target.result;             
                imagePreview.style.display = 'block';         
            };         reader.readAsDataURL(file);     
        } else {         
            imagePreview.style.display = 'none';     
        } 
    }); 
    // Remove selected image 
    document.getElementById('remove-image').addEventListener('click', function() {     
        const fileInput = document.getElementById('profile-image');     
        const imagePreview = document.getElementById('image-preview');     
        fileInput.value = '';  
        // Clear file input     
        imagePreview.style.display = 'none';     
        alert('تصویر فعلی پاک شد.'); 
    });