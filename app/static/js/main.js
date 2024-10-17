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