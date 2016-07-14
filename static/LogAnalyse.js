var myVue = new Vue({
  el: '#myContainer',
  data: {
    active:0,
    searchQuery: '',
    data :[''],
  },
  computed:{
    columns:function(){
//      console.log(Object.keys(this.data[0]));
      return Object.keys(this.data[0])
    }
  },
  methods: {
    postMessage: function () {
      var self = this;
      self.searchQuery = document.getElementById("searchOrder").value
      this.$http.post('/orders/order?userId='+self.searchQuery).then(function (res) {
//        console.log(res.data);
        try {
          self.data = JSON.parse(res.data);
        } catch (e) {
          console.log(e);
          alert("出错了");
        }
      });
    },
    clearMessage: function(){
      var self = this;
      document.getElementById("searchOrder").value="";
    }
  },

  created:function(){
//      this.updateMessage();
    pageIndex = document.URL.split('/')[3]
    if(pageIndex==""){
      pageIndex = "1";
    }
    console.log(pageIndex)
    var self = this;
    this.$http.post('/orders?pageIndex='+pageIndex).then(function (res) {
//        console.log(res.data);
      try {
        self.data = JSON.parse(res.data);
        console.log(self.data[2].createTime);
        self.data.sort(function(a,b){
          return b.createTime>a.createTime?1:-1;})
        //        console.log(res.data);
      } catch (e) {
        console.log(e);
        alert("出错了");
      }
    });
  },

  filters: {
    ignoreDetails: function(title){
      if(title!="orderInfo"){return title}
    },
    ignoreContent: function(content){
      if(content.length>40){return null}
      return content
    },
    getContent: function(content){
      if(content.length>40){return content}
    }
  }

})
myVue.filter('myReverse', function (value) {
  return value.split('').reverse().join('')
})
