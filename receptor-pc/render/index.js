
const path = require("path")

window.$ = window.jQuery = require('jquery')
window.Bootstrap = require('bootstrap')
window.Vue = require("vue/dist/vue.min.js")


Vue.component('pedido',{
   props:{
     id: Number,
     camarero: String,
     mesa: String,
     hora: String,
     urgente: Boolean,
     lineas: Array,
     callback: Object,
     obj: Object,
    },
   template: '#pedido'
})

app = new Vue({
  el: '#app',
  data:{
    pedidos: []
  },
  methods:{
     add_linea: function(datos){
        this.pedidos.push(datos)
        this.play_sound()
     },
     play_sound: function(){
       var click_sound = require("electron").remote.require("./play-sound").click_sound
       url_sound = path.join(__dirname, "../sound/beep-06.wav")
       var player  = require('play-sound')(opts={})
       player.play(url_sound, (err)=>{
           if (err) console.log(err)
           player.play(url_sound, (err)=>{
               if (err) console.log(err)
           })
       })


     },rm_linea: function (obj) {
        var index = this.pedidos.indexOf(obj)
        this.pedidos.splice(index,1)
     },
  }
 })






var socket = new WebSocket("ws://gstr.elbrasilia.com/ws/impresion/caja/");

socket.onopen = function(){
	console.log("Socket has been opened!");
}

socket.onmessage = function(msg){
  var message = msg["data"]
  message = JSON.parse(message)["message"];

  if (message["op"] == "urgente" || message["op"] == "pedido"){
      obj = {
        camarero: message["camarero"],
        mesa: message["mesa"],
        hora: message["hora"],
        urgente:  message["op"] == "urgente" ? true : false,
        lineas: message["lineas"]
      }
    	app.add_linea(obj)
    }
}
