var demo = new Vue({
  el: '#container',
  data: {
    searchQuery: '',
    data :[
  {
    "nickname": "Yu",
    "pid": 10,
    "name": "abc",
    "id": 0
  },
  {
    "nickname": "Xu",
    "pid": 20,
    "name": "cba",
    "id": 1
  },
  {
    "nickname": "solo",
    "pid": 30,
    "name": "kda",
    "id": 2
  }
]
  },computed:{
    columns:function(){
      return Object.keys(this.data[0])
  }
  },
  methods: {
    updateMessage: function () {
      var self = this;
      this.$http.get('/orders').then(function (res) {
        console.log(res.data);
        try {
          self.data = JSON.parse(res.data);
        } catch (e) {
          console.log(e);
          alert("出错了");
        }
      }, function (esrr) {
        console.error(err);
        alert("出错了");
      });
    },
    postMessage: function () {
      var self = this;
      self.searchQuery = document.getElementById("searchOrder").value
      this.$http.post('/orders/order?id='+self.searchQuery).then(function (res) {
        console.log(res.data);
        try {
          self.data = JSON.parse(res.data);
        } catch (e) {
          console.log(e);
          alert("出错了");
        }
      });
    }
  },
  created:function(){
    this.updateMessage();
  }
})