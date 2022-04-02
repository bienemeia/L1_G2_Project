

function change_status (obj, prompt_tag_id){
    if ($(`#${prompt_tag_id}`).text() == "On"){
        $(`#${prompt_tag_id}`).text("Off");
        $(obj).find("div").css("left","5px");
    } else {
        $(`#${prompt_tag_id}`).text("On");
        $(obj).find("div").css("left","25px");
    }
}

$(function () {
    $("#vplay").click(function (e) {
        $(this).append("<video src=\"/static/miemiegergerger.mp4\" autoplay></video>")
        $("video")[0].play()
        $("video").click(function (e) {
            e.stopPropagation()
            if ($("video")[0].paused){
                $("video")[0].play()
            } else {
                $("video").remove()
            }
        })

        $("video")[0].addEventListener("ended",function () {
            $(this).remove()
        })
    })
    $("#iplay").click(function (e) {
        $(this).append("<img src=\"/static/snow.jpg\" autoplay controls>")
        $("img").click(function (e) {
            e.stopPropagation()
            $(this).remove()
        })
    })

    setInterval(function () {
        var myDate = new Date();
        $("#date").text(`${myDate.getFullYear()}/${myDate.getMonth()+1}/${myDate.getDate()}`)
        $("#time").text(`${myDate.getHours()-12>0 ? myDate.getHours()-12 : myDate.getHours()}:${myDate.getMinutes()}:${myDate.getSeconds()}${myDate.getHours()-12>0 ? ' pm' : ' am'}`)
    },500)

})