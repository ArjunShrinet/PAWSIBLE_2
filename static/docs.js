var shownimage=document.querySelector("#click")
var fileshow=document.querySelector("#docshow")
var submit=document.querySelector("#submitbutton")
submit.addEventListener("click",()=>{
    var selectedfile=fileshow.files[0]
    shownimage.src=URL.createObjectURL(selectedfile)
})