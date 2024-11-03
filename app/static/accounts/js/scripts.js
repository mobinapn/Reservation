const inputs = document.querySelectorAll(".input");


function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});


const errorMessage = document.getElementById("error");
const progressBar = document.getElementById("progress-bar");
const duration = 5000; // مدت زمان نمایش پیام به میلی‌ثانیه (5 ثانیه)

// شروع پر کردن نوار پیشرفت
progressBar.style.width = "100%";

// محو کردن پیام بعد از مدت زمان مشخص
setTimeout(() => {
    errorMessage.style.opacity = 0; // محو کردن پیام
    setTimeout(() => {
        errorMessage.style.display = 'none'; // پنهان کردن پیام
    }, 300); // زمان محو شدن کامل
}, duration);