const online_status = new WebSocket(
    'ws://'
    +window.location.host
    +"/ws/online/"
)

online_status.onopen = function(e){
    console.log('Connected to online consumer')
}


online_status.onclose= function(e){
    console.log('Disconnected to online consumer')
}