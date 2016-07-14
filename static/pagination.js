/**
 * Created by LongTang on 7/14/16.
 */

function autoRun() {
    pageIndex = document.URL.split('/')[3];
    if (pageIndex == "") {
        pageIndex = "1";
    }
    pageDisplay = parseInt(pageIndex);
    if (pageDisplay == 1){
        document.getElementById("backward").onclick = "javascript:return false;";
        document.getElementById("backward").innerHTML = "第一页";
    }
    if (pageDisplay == 15){
        document.getElementById("forward").onclick = "javascript:return false;";
        document.getElementById("forward").innerHTML = "最后一页";
    }
    if (pageDisplay == 1 || pageDisplay == 2){
        pageDisplay = 3
    }
    if (pageDisplay == 15 || pageDisplay == 14){
        pageDisplay = 13
    }
    document.getElementsByClassName("paginationIndex")[0].innerHTML = String(pageDisplay - 2);
    document.getElementsByClassName("paginationIndex")[1].innerHTML = String(pageDisplay - 1);
    document.getElementsByClassName("paginationIndex")[2].innerHTML = String(pageDisplay);
    document.getElementsByClassName("paginationIndex")[3].innerHTML = String(pageDisplay + 1);
    document.getElementsByClassName("paginationIndex")[4].innerHTML = String(pageDisplay + 2);

    document.getElementById("currentIndex").innerHTML = "日志\t第" + pageIndex + "页";
    document.getElementById("totalPage").innerHTML = "共" + "15" + "页";

    //if (event.keyCode == 37) {
    //    backward();
    //}
    //if (event.keyCode == 39) {
    //    forward();
    //}
}
function backward() {
    pageIndex = document.URL.split('/')[3];
    if (pageIndex == "") {
        pageIndex = "1";
    }
    window.location.href = "http://127.0.0.1:5000/" + String(parseInt(pageIndex)-1);
}
function forward(){
    pageIndex = document.URL.split('/')[3];
    if(pageIndex==""){
        pageIndex = "1";
    }
    window.location.href="http://127.0.0.1:5000/"+String(parseInt(pageIndex)+1);
}
function jumping(){
    window.location.href="http://127.0.0.1:5000/"+document.getElementById("jumping").value;
}
function jumpToOnePage(index){
    window.location.href="http://127.0.0.1:5000/"+document.getElementsByClassName("paginationIndex")[index].innerHTML;
}