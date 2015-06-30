function request(type, url, data) {
    var http = new XMLHttpRequest();
    http.open(type, url);
    http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    http.send(data);
    http.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                location.reload();
            }
        }
    };
}