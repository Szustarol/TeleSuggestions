const server_host = "127.0.0.1"
const server_port = 8000

const insert_element = "masthead"

const response_content = `
<style>
    .nav_panel{
        background-color: #e9f0fa;
        width: 100%;
        height: 50px;
    }
    #social-share-buttons{
        margin-top: 130px;
    }
    .inner_nav_scroll{
        justify-content: center;
        margin: 0 auto;
        width: 90%;
        overflow-x: auto;
        overflow-y: hidden;
        white-space: nowrap;
        display: flex;
        flex-direction: row;
    }
    .nav_element{padding:7px 18px;display:inline-block;background-color:#e42957;color:#FFF;text-decoration:none;margin-right:1em;}
    .nav_element:hover{color:#FFF !important;opacity:0.85}
</style>
<br/>
<div id="smart_nav_panel" class="nav_panel">
    <div class="inner_nav_scroll">
        {{navigation_elements}}
    </div>
</div>
`

const render_navigation = (suggestions) => {
    div = document.createElement('div')

    response_raw = response_content
    response_navs = ""

    suggestions.forEach(element => {
        response_navs += `<a href="${element.href}"><div class="nav_element">${element.title}</div></a>`
    });

    response_full = response_raw.replace("{{navigation_elements}}", response_navs)

    div.innerHTML = response_full
    document.getElementById(insert_element).appendChild(div)
}

const uuidv4 = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

var xhr = new XMLHttpRequest()
var url = "http://"+server_host+":"+server_port

xhr.open("POST", url, true)
xhr.setRequestHeader("Content-Type", "application/json")

var access_url = window.location.href.split('?')[0]
var access_url = access_url.replace(/(^\w+:|^)\/\//, '')

if(typeof localStorage.telecom_session_uuid == "undefined")
    localStorage.telecom_session_uuid = uuidv4()

var data = JSON.stringify({
    "uri": access_url,
    "client_id": localStorage.telecom_session_uuid
})

xhr.onreadystatechange = () => {
    if(xhr.readyState == 4){
        render_navigation(JSON.parse(xhr.response).suggestions)
    }
}

xhr.send(data)